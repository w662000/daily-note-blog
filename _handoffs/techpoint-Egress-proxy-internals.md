---
layout: default
title: 技术点 · Egress proxy internals
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Egress proxy internals

> 来源：261010_Egress proxy internals_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
agent/proxy_sources/iron_proxy.py     Core: binary install, CA gen, config build,
                                       subprocess lifecycle, mappings I/O, PID/nonce
                                       defense.  Pure-function surface where possible.

hermes_cli/proxy_cli.py               Wizard + slash command handlers.
                                       `hermes egress {install,setup,start,stop,
                                       status,disable,config}`.  Wires the
                                       core module into argparse.

hermes_cli/subcommands/egress.py:_dispatch_egress
                                       Top-level subparser dispatcher.
                                       dest='egress_command' (intentionally
                                       disjoint from the inbound OAuth
                                       `hermes proxy` subparser, which uses
                                       dest='proxy_command').

hermes_cli/config.py: proxy schema    The `proxy:` block in DEFAULT_CONFIG.
                                       Adding a knob means: add it here, add a
                                       wizard prompt or `setdefault` in
                                       proxy_cli.cmd_setup, and document it
                                       in the user-guide page.

tools/environments/docker.py
  _egress_proxy_args_for_docker()     Builds the volume_args / env_overrides /
                                       host_args triple that the Docker backend
                                       injects when `proxy.enabled: true`.

  DockerEnvironment.__init__          Docker-side merge logic: collision
                                       detection against critical egress vars,
                                       NODE_OPTIONS append-merge via the
                                       _HERMES_EGRESS_NODE_OPTIONS_APPEND
                                       sentinel, enforce_on_docker precedence.

tests/agent/test_iron_proxy.py              Hermetic tests (~70).  Binary install
                                       path, config build, mappings I/O,
                                       subprocess lifecycle, docker arg builder,
                                       deny CIDR defaults, bind policy, CA
                                       TOCTOU, ensure_audit_log behaviour, etc.

tests/hermes_cli/test_iron_proxy_cli.py          CLI handler unit tests (~20).  Argparse
                                       wiring, fail-loud paths, BWS refresh
                                       wire-up, dest='egress_command'
                                       regression guard.

tests/agent/test_iron_proxy_e2e.py          Live E2E (gated on HERMES_RUN_E2E=1).
                                       Real iron-proxy binary, real curl,
                                       end-to-end token swap verified.
```
- ```
hermes egress install
  -> agent.proxy_sources.iron_proxy.install_iron_proxy(force=...)
       Downloads pinned tarball + checksums.txt from GitHub Releases.
       SHA-256 verification before extraction.
       tarfile.extract(..., filter="data") on Python 3.12+ (PEP 706);
         falls back to plain extract on older Python with member-name
         sanitisation via _pick_tar_member.
       Stage into ~/.hermes/bin/.iron-proxy_XXXX, chmod 755, os.replace
         to ~/.hermes/bin/iron-proxy (atomic).
       _VERSION_CACHE.pop(target) so a forced reinstall re-probes
         --version on next call.

hermes egress setup [--from-bitwarden | --no-bitwarden] [--rotate-tokens]
  -> proxy_cli.cmd_setup
       Step 1. find_iron_proxy(install_if_missing=False) -> install if absent.
       Step 2. ensure_ca_cert()
                 Run openssl genrsa + req via subprocess.
                 Write CA key via os.open(O_WRONLY|O_CREAT|O_TRUNC|O_NOFOLLOW, 0o600)
                   + os.replace.  Never exists on disk under default umask.
                 Write CA cert with 0o644 (public).
       Step 3. discover_provider_mappings() or pull names from BWS via
                 fetch_bitwarden_secrets() when --from-bitwarden.
                 merge_mappings(existing=load_mappings(), discovered,
                                rotate=args.rotate_tokens) preserves prior
                 tokens unless --rotate-tokens is passed.
                 discover_uncovered_providers() and surface warnings.
       Step 4. ensure_audit_log(audit_log_path)   # raises on OSError
               build_proxy_config(...) with defaults applied at the call site
                 (deny CIDRs default, bind policy from _default_http_listen).
               write_proxy_config(cfg)            # atomic via .tmp + os.replace, 0o600
               write_mappings(mappings)           # atomic, 0o600
       Step 5. proxy_cfg["enabled"] = True; credential_source preservation logic
               (do NOT silently downgrade bitwarden -> env on re-run);
               save_config(cfg).

hermes egress start
  -> proxy_cli.cmd_start
       Pre-checks (refuse-start path):
         - credential_source=bitwarden? -> pre-validate access_token_env + project_id
       -> iron_proxy.start_proxy(
            refresh_secrets_from_bitwarden=...,
            bitwarden_config=...,
          )
            existing=_read_pid(); if alive, idempotent return.
            _build_proxy_subprocess_env(...):  ALLOWLIST + mapped real_env_names,
              strip HTTPS_PROXY/etc. to avoid recursion, optional BWS refresh
              (raises on missing values unless allow_env_fallback=true).
            Plant nonce: _proxy_nonce = sha256(urandom(16)); env[NONCE_ENV] = ...
            Open log_path via O_NOFOLLOW + 0o600 + st_uid check.
            Popen with stdin=DEVNULL, stdout=log_fd, stderr=STDOUT,
              start_new_session=True (POSIX).
            Close parent's log_fd in finally.
            _write_pidfile_safely(pidfile, proc.pid)
              O_EXCL + O_NOFOLLOW + uid check + persisted nonce sidecar.
              FileExistsError -> discriminate live vs stale, retry once if stale.
            Install SIGINT/SIGTERM handlers (main-thread only).
            Poll loop (do-while shape):
              while True:
                if proc.poll() is not None: tail log + unlink pidfile + raise
                if _port_listening(probe_host, tunnel_port): break  # probe_host = configured bind host
                if time.time() >= deadline: break  (do-while: checked AFTER first probe)
                time.sleep(0.1)
            If not listening at exit: _kill_and_wait(proc) + unlink pidfile + raise.

hermes egress stop
  -> iron_proxy.stop_proxy
       _read_pid + _pid_alive guard.
       starttime_before = _pid_proc_starttime(pid)   # Linux only; None elsewhere
       os.kill(pid, SIGTERM)
       Wait up to 5s for graceful exit.
       After grace: re-check starttime + _pid_alive.
         If recycled (starttime drift OR _pid_alive False), DO NOT SIGKILL.
         Otherwise os.kill(pid, _KILL_SIGNAL).
       _cleanup_state_files: unlink pidfile + nonce sibling.
```
- | `ca.key` | `0o600` | `test_ca_key_created_with_0o600` |
- Missing access token env var -> `cmd_start` refuses.
- Regression: `test_cmd_start_refuses_when_bitwarden_token_missing` (CLI layer); strict-mode assertions in `_build_proxy_subprocess_env` (daemon layer).
- When `enforce_on_docker: true`, `docker_env` overrides on any of the egress-controlling vars (HTTPS_PROXY, SSL_CERT_FILE, NODE_EXTRA_CA_CERTS, etc.) OR any mapped `real_env_name` (OPENROUTER_API_KEY, etc.) raises `RuntimeError` BEFORE the container starts.
- `merge_mappings(existing, discovered, rotate=False)` MUST return prior tokens for providers that overlap.  Re-running `hermes egress setup` cannot silently 401 running sandboxes.  `--rotate-tokens` is the explicit opt-in.
- Regression: `test_merge_mappings_preserves_existing_tokens`, `test_merge_mappings_rotate_mints_fresh_tokens`.
- `_BEARER_PROVIDERS` in `iron_proxy.py` maps env var name -> tuple of upstream hosts.  Adding an entry makes it discoverable by `discover_provider_mappings()`; the wizard mints a token for it automatically when the env var is present.
- ```
_BEARER_PROVIDERS: Dict[str, Tuple[str, ...]] = {
    ...,
    "MY_PROVIDER_API_KEY": ("api.myprovider.com",),
}
```
- If the provider authenticates with a static NON-Authorization header (like Anthropic's `x-api-key`, Azure's `api-key`, or Gemini's `x-goog-api-key`), add it to `_HEADER_AUTH_PROVIDERS` — iron-proxy's `secrets.replace.match_headers` targets arbitrary header names, so these are first-class swapped providers:
- ```
_HEADER_AUTH_PROVIDERS: Dict[str, Dict[str, Tuple[str, ...]]] = {
    ...,
    "MY_PROVIDER_API_KEY": {
        "hosts": ("api.myprovider.com",),
        "match_headers": ("x-my-auth-header", "Authorization"),
        "aliases": (),
    },
}
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
