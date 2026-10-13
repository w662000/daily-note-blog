---
layout: default
title: 技术点 · Feishu / Lark Setup
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Feishu / Lark Setup

> 来源：261010_Feishu _ Lark Setup_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
group_sessions_per_user: true
```
- ```
hermes gateway setup
```
- ```
FEISHU_CONNECTION_MODE=websocket
```
- ```
FEISHU_CONNECTION_MODE=webhook
```
- ```
/feishu/webhook
```
- ```
FEISHU_WEBHOOK_HOST=127.0.0.1   # default: 127.0.0.1
FEISHU_WEBHOOK_PORT=8765         # default: 8765
FEISHU_WEBHOOK_PATH=/feishu/webhook  # default: /feishu/webhook
```
- When Feishu sends a URL verification challenge (`type: url_verification`), the webhook responds automatically so you can complete the subscription setup in the Feishu developer console. The challenge response is gated on `FEISHU_VERIFICATION_TOKEN` when set — challenge requests with a missing or mismatched token are rejected so an unauthenticated remote cannot prove endpoint control by echoing attacker-controlled challenge data.
- ```
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=secret_xxx
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket

# Optional but strongly recommended
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
FEISHU_HOME_CHANNEL=oc_xxx
```
- ```
hermes gateway
```
- ```
FEISHU_HOME_CHANNEL=oc_xxx
```
- ```
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
```
- When running in webhook mode, set an encryption key to enable signature verification of inbound webhook payloads:

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
