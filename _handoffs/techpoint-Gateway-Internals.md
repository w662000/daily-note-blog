---
layout: default
title: 技术点 · Gateway Internals
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Gateway Internals

> 来源：261010_Gateway Internals_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | `gateway/session.py` | `SessionStore` — conversation persistence and session key construction |
- | `gateway/status.py` | Token lock management for profile-scoped gateway instances |
- | `gateway/platforms/` | Shared `base.py` plus legacy/direct adapters (Signal, API server, webhooks, …) |
- ```
┌─────────────────────────────────────────────────┐
│                  GatewayRunner                  │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Telegram │  │ Discord  │  │  Slack   │       │
│  │ Adapter  │  │ Adapter  │  │ Adapter  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │
│       └─────────────┼─────────────┘             │
│                     ▼                           │
│              _handle_message()                  │
│                     │                           │
│         ┌───────────┼───────────┐               │
│         ▼           ▼           ▼               │
│  Slash command   AIAgent    Queue/BG            │
│    dispatch      creation   sessions            │
│                     │                           │
│                     ▼                           │
│                 SessionStore                    │
│              (SQLite persistence)               │
└───────┴─────────────┴─────────────┴─────────────┘
```
- Resolve session key via `_session_key_for_source()` (format: `agent:{namespace}:{platform}:{chat_type}:{chat_id}`; the namespace is `main` for the default profile, `<profile>` under multiplexing — see [Multiplexed profiles](#multiplexed-profiles))
- Session keys encode the full routing context:
- ```
agent:{namespace}:{platform}:{chat_type}:{chat_id}
```
- (`gateway/session.py::_session_key_namespace`; a profile literally named `main` is marked `main~`).
- Thread-aware platforms (Telegram forum topics, Discord threads, Slack threads) may include thread IDs in the chat_id portion. **Never construct session keys manually** — always use `build_session_key()` from `gateway/session.py`.
- ```
Admin: /pair
Gateway: "Pairing code: ABC123. Share with the user."
New user: ABC123
Gateway: "Paired! You're now authorized."
```
- While `_quick_key in self._running_agents`, `_dispatch_busy_slash_command()` in `gateway/run_busy.py` routes each recognized command by its `CommandDef.busy_policy` / `busy_handler`: a mid-run variant (`_busy_<key>_command`) if one exists, otherwise the normal handler when `busy_policy` allows it, otherwise a reject message ("⏳ Agent is running — `/model` can't run mid-turn…").
- | `~/.hermes/.env` | API keys, bot tokens, platform credentials |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
