---
layout: default
title: 技术点 · Discord Setup
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Discord Setup

> 来源：261010_Discord Setup_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
group_sessions_per_user: true
```
- ```
group_sessions_per_user: false
```
- users share context growth and token costs
- Hermes tracks running agents by session key.
- ```
discord:
  websocket_liveness_interval_seconds: 15
  websocket_liveness_failure_threshold: 2
  websocket_heartbeat_ack_max_age_seconds: 60
  websocket_max_latency_seconds: 30
  websocket_event_max_silence_seconds: 14400
```
- The bot token is the credential Hermes Agent uses to log in as your bot. Still on the **Bot** page:
- 1. Under the **Token** section, click **Reset Token**.
- 3. Discord will display your new token. **Copy it immediately.**
- :::warning[Token shown only once]
- The token is only displayed once. If you lose it, you'll need to reset it and generate a new one. Never share your token publicly or commit it to Git — anyone with this token has full control of your bot.
- Store the token somewhere safe (a password manager, for example). You'll need it in Step 8.
- ```
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=274878286912
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
