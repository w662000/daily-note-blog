---
layout: default
title: 技术点 · gateway/ — messaging gateway, adapters, delivery
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · gateway/ — messaging gateway, adapters, delivery

> 来源：261010_gateway_ — messaging gateway, adapters, delivery_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- `DEFAULT_CONFIG` — a key the CLI sees but the gateway doesn't means you're on the wrong loader
- adapter** (`platforms/base.py`) queues it in `_pending_messages` when `session_key in
- at-least-once admission, not proof that a model turn or final outbound reply completed. API-server
- actual delivery errors keep their bounded retry policy. Recognized raw API routes resolve after
- an expiring access token that nothing refreshes.
- gateway (`gateway run`) SURVIVES the app: the serve backend's `/api/gateway/*` endpoints spawn it
- ingress path calls the canonicalize seam before it derives a key: the adapter side
- album routing, `_handle_message_while_active`, every `_source_session_key`) and the runner side
- handlers, the adapter auth-check callback, `run_inbound.py::_hm_admit_event`). No key derivation
- with one WARNING at the first seam it reaches, never keyed into `agent:main`. `_transport_owner`,
- `_authorization_home_for_source`, `_resolve_profile_home_for_source`, `_session_key_profile` and
- `_resolve_profile_for_key` read the identity when present and fall back to their old chain only

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
