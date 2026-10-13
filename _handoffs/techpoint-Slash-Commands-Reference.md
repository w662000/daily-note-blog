---
layout: default
title: 技术点 · Slash Commands Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Slash Commands Reference

> 来源：261010_Slash Commands Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | `/snapshot [create\|restore <id>\|prune]` (alias: `/snap`) | Create or restore state snapshots of Hermes config/state. `create [label]` saves a snapshot, `restore <id>` reverts to it, `prune [N]` removes old snapshots, or list all with no args. Database restores write through SQLite's backup API so live processes (gateway, dashboard) see the restored data safely; if that path fails while another process still holds the database open, the restore refuses instead of risking corruption — stop the holder and retry. |
- | `/egress [status]` | Show Docker egress proxy status — enabled/configured/running state, credential source, token mappings, uncovered providers, and next remediation step. Works in CLI, TUI, Desktop chat, and messaging gateway. |
- | `/status` | Show session info — model, provider, profile, session ID, working directory, title, created/updated timestamps, token totals, agent-running state — followed by a local **Session recap** block (recent user/assistant turn counts, tool result count, top tools used, last few files touched, the latest user prompt, and the latest assistant reply). The recap is computed locally from the in-memory conversation; no LLM call, no prompt-cache impact. |
- | `/context [all]` (alias: `/ctx`) | Visual context-window breakdown. On the CLI/TUI: a 5×20 glyph block grid (each cell ≈ 1% of the model window) plus an estimated per-category table — system prompt, tool definitions, rules, skills index, MCP, subagents, memory, conversation — versus free space. On messaging platforms: a usage gauge with auto-compression threshold/headroom, compression stats, cumulative throughput, and the same category table in plain text. On the CLI, messaging platforms, and TUI/Desktop sessions on a compute host, the output ends with a per-file **Context files** listing (.hermes.md, AGENTS.md chain, CLAUDE.md, .cursorrules + .cursor/rules/*.mdc, SOUL.md) showing each file's token estimate and whether it was loaded, truncated over `context_file_max_chars`, shadowed by a higher-priority context type, blocked by the injection scan, empty/unreadable, or suppressed by the install-tree guard — the answer to "why is my CLAUDE.md ignored?". `/context all` appends per-skill and per-toolset cost listings (index cost vs SKILL.md load cost; schema tokens per toolset). Read-only and computed locally — no LLM call, no prompt-cache impact. |
- | `/model [model-name]` | Show or change the current model. Supports: `/model claude-sonnet-4`, `/model provider:model` (switch providers), `/model custom:model` (custom endpoint), `/model custom:name:model` (named custom provider), `/model custom` (auto-detect from endpoint), OpenRouter account presets (`/model @preset/<slug>` or `/model <model>@preset/<slug>` — presets are account-scoped, so they skip the public model-listing check), and user-defined aliases (`/model fav`, `/model grok` — see [Custom model aliases](#custom-model-aliases)). Flags: `--global` persists the change to config.yaml; `--session` forces session-only; `--once` applies to the next turn only; `--refresh` re-fetches the provider's model list; `--provider <name>` switches backend (session-only unless `--global`); `--reasoning <level>` sets the reasoning effort (`none`, `minimal` … `ultra`) in the same step and with the same scope as the pick. A plain `/model <name>` is session-only unless `model.persist_switch_by_default: true` is set — except when no `model.default`/`model.provider` is configured yet, in which case the first pick persists so the profile gets a real default. The same rule governs the desktop composer picker. **Interactive picker:** running `/model` with no arguments opens the provider→model picker; on the model list you can **type to fuzzy-filter** the models (e.g. type `grok` to narrow to matching models), Backspace to trim the filter, Esc to clear it (or close the picker). Selection always resolves to one concrete model — the filter only narrows the list, it never guesses. After the model, a third step offers the reasoning effort for that model (or **Keep current effort**); it is skipped when the catalog says the route has no reasoning control. **Note:** `/model` can only switch between already-configured providers. To add a new provider, exit the session and run `hermes model` from your terminal. **Cost note:** switching models mid-conversation resets the prompt cache — the cache key includes the model, so your next turn re-reads the entire conversation at full input price instead of the ~75%-discounted cached rate. Expected and unavoidable, but worth knowing on long sessions. |
- | `/voice [on\|off\|tts\|status]` | Toggle CLI voice mode and spoken playback. Recording uses `voice.record_key` (default: `Ctrl+B`). |
- | `/reload` | Reload `.env` variables into the running session (picks up new API keys without restarting) |
- | `/usage` | Show token usage, cost breakdown, session duration, and — when available from the active provider — an **Account limits** section with remaining quota / credits / plan usage pulled live from the provider's API. |
- ```
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
  deploy:
    type: exec
    command: scripts/deploy.sh
  inbox:
    type: alias
    target: /gmail unread
```
- ```
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  grok:
    model: grok-4
    provider: x-ai
  ollama-qwen:
    model: qwen3-coder:30b
    provider: custom
    base_url: http://localhost:11434/v1
  theta:
    model: theta-1
    provider: custom
    base_url: https://theta.example.com/v1
    key_env: THETA_API_KEY        # or: api_key: "${THETA_API_KEY}"
```
- `api_key` (a literal, or a `"${VAR}"` reference) or `key_env` (an environment
- variable name); `api_key` wins if both are set. With neither set, the key is

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
