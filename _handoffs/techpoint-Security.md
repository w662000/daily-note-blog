---
layout: default
title: 技术点 · Security
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Security

> 来源：261010_Security_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
approvals:
  mode: smart                     # smart | manual | off
  timeout: 300                    # seconds to wait for user response (default: 300)
  cron_mode: deny                 # deny | approve — what cron jobs do when they hit a dangerous command
  single_query_mode: deny         # deny | approve — what single-query (-q) sessions do on a dangerous command
  unattended_mode: deny           # deny | approve — what webhook/API sessions do on a dangerous command
  mcp_reload_confirm: true        # /reload-mcp asks before invalidating the MCP tool cache
  destructive_slash_confirm: true # /clear, /new, /reset, /undo prompt before discarding state
```
- The full set of keys:
- | Key | Default | What it controls |
- | `unattended_mode` | `deny` | How sessions on unattended programmatic platforms (webhook, msgraph_webhook, api_server) behave when they trigger a dangerous-command prompt. These surfaces have no human who can answer `/approve`, so instead of blocking for the full approval timeout, `deny` blocks the command instantly (the agent must find another path) and `approve` auto-approves everything in unattended context. Mirrors `cron_mode`. |
- | `mcp_reload_confirm` | `true` | When true, `/reload-mcp` asks before rebuilding the MCP tool set. Rebuilding invalidates the provider prompt cache (tool schemas live in the system prompt), so the next message re-sends full input tokens. Users who click **Always Approve** flip this key to `false`. |
- | `destructive_slash_confirm` | `true` | When true, destructive session slash commands (`/clear`, `/new`, `/reset`, `/undo`) prompt before discarding conversation state. Three-option dialog (Approve Once / Always Approve / Cancel) routed through native yes/no buttons on Telegram, Discord, and Slack; text fallback elsewhere. Users who click **Always Approve** flip this key to `false`. The TUI also honors this setting for its `/clear`, `/new`, and `/reset` modal; `HERMES_TUI_NO_CONFIRM=1` force-skips that modal regardless of the configured value. |
- ```
> /yolo
  ⚡ YOLO mode ON — all commands auto-approved. Use with caution.

> /yolo
  ⚠ YOLO mode OFF — dangerous commands will require approval.
```
- with `RunAtLoad=false` and no `KeepAlive` key; rejection does **not** establish that
- ```
approvals:
  deny:
    - "git push --force*"
    - "*curl*|*sh*"
    - "dd if=* of=/dev/*"
```
- Like the rest of the approval config, changes take effect immediately (the config cache is mtime-keyed) — no session restart needed.
- ```
approvals:
  timeout: 300  # seconds (default: 300)
```
- ```
  ⚠️  DANGEROUS COMMAND: recursive delete
      rm -rf ~/old-project

      [o]nce  |  [s]ession  |  [a]lways  |  [d]eny

      Choice [o/s/a/D]:
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
