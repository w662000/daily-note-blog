---
layout: default
title: 技术点 · Hermes Agent Configuration
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Hermes Agent Configuration

> 来源：261010_Hermes Agent Configuration_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "Configure Hermes Agent — config.yaml, providers, models, API keys, and more"
- Run `hermes setup --portal` — one OAuth gets you a model provider and all four Tool Gateway tools without hand-editing YAML. Portal subscribers also get 10% off token-billed providers. See [Nous Portal](../integrations/nous-portal.md).
- ```
~/.hermes/
├── config.yaml     # Settings (model, terminal, TTS, compression, etc.)
├── .env            # API keys and secrets
├── auth.json       # OAuth provider credentials (Nous Portal, etc.)
├── SOUL.md         # Primary agent identity (slot #1 in system prompt)
├── memories/       # Persistent memory (MEMORY.md, USER.md)
├── skills/         # Agent-created skills (managed via skill_manage tool)
├── cron/           # Scheduled jobs
├── sessions/       # Gateway sessions
└── logs/           # Logs (errors.log, gateway.log — secrets auto-redacted)
```
- ```
hermes config              # View current configuration
hermes config edit         # Open config.yaml in your editor
hermes config get KEY      # Print a resolved value
hermes config set KEY VAL  # Set a specific value
hermes config unset KEY    # Remove a user-set value
hermes config check        # Check for missing options (after updates)
hermes config migrate      # Interactively add missing options

# Examples:
hermes config get model
hermes config set model anthropic/claude-opus-4
hermes config set terminal.backend docker
hermes config unset terminal.backend
hermes config set OPENROUTER_API_KEY sk-or-...  # Saves to .env
```
- The `hermes config set` command automatically routes values to the right file — every `UPPER_SNAKE` name (`OPENROUTER_API_KEY`, `DISCORD_HOME_CHANNEL`, `TELEGRAM_GROUP_ALLOWED_USERS`, `HERMES_TIMEZONE`, …) is an environment variable and is saved to `.env`, never to `config.yaml`; dotted settings go to `config.yaml`. Any other `UPPER_SNAKE` name is saved to `.env` as-is (it is exported to the process environment for plugins and skills); names on the env writer's denylist (`HERMES_YOLO_MODE`, `PATH`, …) are refused. A known key written under the wrong prefix (`gateway.discord.foo`, where `discord.foo` is itself a known key) is refused with a did-you-mean before anything is written; pass `--force` to write it anyway. Any other unknown path under a known section (a typo such as `agent.max_turnz`, or a runtime-read key with no seeded default) is written together with a did-you-mean notice, since the schema alone cannot tell the two apart. `hermes config get` on such a path prints the value from your file together with a stderr notice that Hermes may not read it, so a leftover key cannot silently pass for a live setting.
- 3. **`~/.hermes/.env`** — fallback for env vars; **required** for secrets (API keys, tokens, passwords)
- Secrets (API keys, bot tokens, passwords) go in `.env`. Everything else (model, terminal backend, compression settings, memory limits, toolsets) goes in `config.yaml`. When both are set, `config.yaml` wins for non-secret settings.
- ```
runtime:
  nofile_soft_limit: 4096
```
- ```
database:
  # Journal mode for state.db: wal (default) or delete.
  # Use delete on filesystems where WAL is unsafe (network mounts). On
  # virtiofs/9p bind mounts (Docker Desktop, Podman on macOS, OrbStack)
  # Hermes detects the mount and creates fresh databases in delete mode
  # automatically. Note: an existing on-disk WAL database is never
  # live-downgraded — Hermes keeps WAL and logs an error telling you the
  # configured delete did not apply (or that the WAL database sits on a
  # cross-VM mount). To convert an existing database, stop
  # every process using it and run
  # `hermes sessions set-journal-mode delete` (see Sessions).
  journal_mode: wal

  # Durability level for every state.db connection: OFF, NORMAL, FULL,
  # EXTRA (or 0-3). Unset leaves SQLite's compile-time default, which
  # differs between interpreter builds. On macOS this is a floor, not a
  # pin: values below FULL are refused to protect against Darwin fsync
  # reordering; EXTRA is honored.
  # synchronous: FULL

  # Optional WAL sizing pragmas (integers). Unset = SQLite defaults.
  # wal_autocheckpoint: 1000     # pages between automatic checkpoints
  # journal_size_limit: 67108864 # cap the WAL/journal size in bytes
```
- ```
auxiliary:
  vision:
    api_key: ${GOOGLE_API_KEY}
    base_url: ${CUSTOM_VISION_URL}

delegation:
  api_key: ${DELEGATION_KEY}
```
- Under a [multiplexed multi-profile gateway](./multi-profile-gateways.md), references in a profile's `config.yaml` resolve against **that profile's** `.env` (its secret scope), not the shared process environment — a `${MATRIX_ACCESS_TOKEN}` in profile B stays unresolved (kept verbatim, warning logged) unless B defines the variable itself. This holds wherever B's config is loaded inside the multiplexer: routed gateway turns, B's adapter startup, and B's cron jobs. Single-profile runs are unchanged. See [What is isolated per profile](./multi-profile-gateways.md#what-is-isolated-per-profile) for the full list.
- You can set `providers.<id>.request_timeout_seconds` for a provider-wide request timeout, plus `providers.<id>.models.<model>.timeout_seconds` for a model-specific override. Applies to the primary turn client on every transport (OpenAI-wire, native Anthropic, Anthropic-compatible), the fallback chain, rebuilds after credential rotation, and (for OpenAI-wire) the per-request timeout kwarg — so the configured value wins over the legacy `HERMES_API_TIMEOUT` env var.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
