---
layout: default
title: 技术点 · Relay ↔ Connector Contract (v1, EXPERIMENTAL)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Relay ↔ Connector Contract (v1, EXPERIMENTAL)

> 来源：261010_Relay ↔ Connector Contract (v1, EXPERIMENTAL)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- gateway already dialed. The gateway keys the session via `build_session_key()`
- `src/core/relayBus.ts`) keyed by tenant. Every connector instance subscribes and
- `{"type":"interrupt_inbound", "session_key", "chat_id"}` (§5)
- §6 — so the gateway re-processes a sanitized, token-free body and acts on it via
- the token-less `follow_up` path). See §3.1.
- > `inbound_receiver`), HMAC-signed with a per-tenant delivery key. That required
- > per-tenant delivery key is retained at provision for forward-compat but is no
- every key the gateway accepts on the wire. `platform`, `chat_id`, `chat_type`,
- | `chat_id` | string | yes | Primary conversation id (channel/chat). Session-key discriminator. |
- | `user_id` | string\|null | yes | Message author id. Session-key discriminator. |
- | `thread_id` | string\|null | yes | Thread/forum-topic id when in a thread. Session-key discriminator. |
- | `scope_id` | string | no | Platform-neutral **scope** discriminator: Discord guild / Slack workspace / Matrix server. **REQUIRED for Discord/Slack scope isolation.** Session-key discriminator. (Canonical name as of the D-Q2.5 wire migration.) |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
