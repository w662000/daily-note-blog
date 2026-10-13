---
layout: default
title: 技术点 · Session Lifecycle
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Session Lifecycle

> 来源：261010_Session Lifecycle_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "SessionSource, SessionEntry, SessionStore, session-key rules and multi-user isolation in the gateway"
- key generation (`build_session_key`), and the main store (`SessionStore`).
- | `chat_id` | `str` | *(required)* | Platform-level chat/group/channel identifier. Routed through the adapter's `chat_id_key` transform. |
- | `chat_type` | `str` | `"dm"` | One of `"dm"`, `"group"`, `"channel"`, `"thread"`. Controls session key generation and isolation. |
- | `message_id` | `Optional[str]` | `None` | ID of the triggering message. Used for pin/reply/react operations and Discord ID injection (the injected `[Triggering message id: …]` note rides the API-bound message only; the persisted user row keeps the authored text). |
- `{sessions_dir}/sessions.json`. Each entry maps a `session_key` to its current `session_id`.
- | `session_key` | `str` | *(required)* | Deterministic key identifying the conversation lane (see §4). |
- | `input_tokens` | `int` | `0` | Cumulative LLM input (prompt) tokens consumed. |
- | `output_tokens` | `int` | `0` | Cumulative LLM output (completion) tokens consumed. |
- | `cache_read_tokens` | `int` | `0` | Cumulative prompt cache read tokens. |
- | `cache_write_tokens` | `int` | `0` | Cumulative prompt cache write tokens. |
- | `total_tokens` | `int` | `0` | Total token count across all turns. |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
