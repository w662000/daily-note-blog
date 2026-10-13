---
layout: default
title: 技术点 · Egress credential-injection proxy (iron-proxy)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Egress credential-injection proxy (iron-proxy)

> 来源：261010_Egress credential-injection proxy (iron-proxy)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- When Hermes runs your agent inside a Docker terminal sandbox, that sandbox normally holds your real upstream API keys (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, etc.). A prompt-injected agent in that sandbox can `cat ~/.config/openrouter/auth.json` or `printenv | grep -i key` and exfiltrate them.
- The egress proxy fixes this: the sandbox holds opaque **proxy tokens**, never the real keys. All outbound traffic from the sandbox routes through a local [iron-proxy](https://github.com/ironsh/iron-proxy) daemon (Apache-2.0, Go) on the host, which terminates TLS and swaps the proxy token for the real credential before forwarding the request upstream. Compromise the sandbox and the attacker walks away with tokens that only work behind the **configured trusted proxy boundary** — the CA private key and the proxy endpoint integrity are part of that boundary. If traffic can be redirected to attacker-controlled proxy infrastructure (e.g. a stolen CA private key or a hijacked proxy endpoint), the token guarantee no longer holds.
- A `mappings.json` recording which proxy token corresponds to which real env var
- The sandbox gets `HTTPS_PROXY=http://host.docker.internal:9090`, `HTTP_PROXY=http://host.docker.internal:9091`, and standard provider env vars such as `OPENROUTER_API_KEY` set to opaque proxy tokens. Matching `HERMES_PROXY_TOKEN_<ENV_NAME>` aliases are also exported for diagnostics. Existing provider SDKs read the usual env names, send the proxy token in `Authorization`, and iron-proxy's `secrets` transform substitutes the real value sourced from the host-side daemon environment.
- It does **not** rewrite credentials for in-process LLM calls the host process makes. Those continue to use your `.env` keys directly. The threat model is the *sandbox*, not the host.
- ```
# 1. Install the iron-proxy binary (pinned version, SHA-256 verified)
hermes egress install

# 2. Run the wizard: generates CA, mints proxy tokens for every provider key
#    in your env, writes proxy.yaml.
hermes egress setup

# 3. Start the proxy daemon
hermes egress start

# 4. Check status
hermes egress status
```
- `hermes egress setup` discovers provider keys from your environment. If your keys live only in `~/.hermes/.env` (not exported into your shell), setup reads that file automatically — you don't have to `export` them first.
- When you re-run `setup` later (new allowlist host, rotated tokens, switched credential source), it stops the running daemon because its config is held in memory, then **offers to restart it for you** so the change takes effect immediately. On a tty it asks; pass `--restart` to always restart or `--no-restart` to leave it down. To apply changes any other time, `hermes egress restart` is the one-command stop-then-start.
- Exports the proxy token under the standard provider env name (for example `OPENROUTER_API_KEY`) plus one `HERMES_PROXY_TOKEN_<ENV_NAME>` diagnostic alias per minted mapping
- ```
proxy:
  # Master switch. When false the feature is a complete no-op — no
  # binaries downloaded, no docker mounts added, no subprocess started.
  enabled: false

  # Tunnel listener port. Sandboxes hit http://host.docker.internal:<port>.
  tunnel_port: 9090

  # Auto-download the pinned iron-proxy binary on first use.
  auto_install: true

  # Where iron-proxy looks up the real upstream secrets at egress time.
  #   env       — process env (default). Whatever is in your ~/.hermes/.env
  #               at proxy-start time is the source of truth.
  #   bitwarden — refetch from Bitwarden Secrets Manager on each proxy
  #               restart. Rotation in the BW web app propagates without
  #               touching .env. Requires `secrets.bitwarden.enabled: true`.
  credential_source: env

  # When true (default), the Docker backend refuses to start a sandbox if
  # the proxy is enabled but not running. Set to false to fall back to the
  # legacy "real credentials inside the sandbox" posture when the proxy
  # is unavailable.
  enforce_on_docker: true

  # When `credential_source: bitwarden` but the BWS access token /
  # project_id is missing OR the bws fetch returns no values for mapped
  # providers, the daemon raises by default (matches the spirit of "I
  # asked for rotation — don't silently use stale env values").  Set
  # to true to opt back into the legacy host-env fallback — useful for
  # migrations where you want to start switching to BW mode but haven't
  # wired every secret yet.
  allow_env_fallback: false

  # SSRF deny list applied to outbound traffic.  Omit / leave null to
  # use the safe default: loopback (v4 + v6), link-local (incl. cloud
  # metadata IPs at 169.254.169.254), RFC1918, IPv6 ULA, IPv4-mapped-v6,
  # CGNAT, and the RFC2544 benchmark range.  Set to an explicit `[]`
  # to opt out entirely (only sensible in hermetic tests).
  upstream_deny_cidrs: null

  # Extra allowed upstream hosts beyond the bundled defaults.
  # Wildcards (`*.foo.com`) are supported. The defaults cover OpenRouter,
  # OpenAI, Anthropic, Google, xAI, Mistral, Groq, Together, DeepSeek,
  # and Nous Research.
  extra_allowed_hosts: []
```
- ```
openrouter.ai           *.openrouter.ai
api.openai.com          api.anthropic.com
generativelanguage.googleapis.com
api.x.ai                api.mistral.ai
api.groq.com            api.together.xyz
api.deepseek.com        inference.nousresearch.com
```
- If your agent needs an upstream that isn't on the list — a self-hosted inference endpoint, an extra cloud LLM, an MCP server — add it to `proxy.extra_allowed_hosts`. Wildcards are matched against the full hostname (`*.example.com` matches `api.example.com` and `staging.example.com` but not `example.com` itself).

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
