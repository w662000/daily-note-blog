---
layout: default
title: 技术点 · Discord 设置
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Discord 设置

> 来源：261010_Discord 设置_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Hermes Agent 以机器人形式与 Discord 集成，让你可以通过私信或服务器频道与 AI 助手对话。机器人接收你的消息，通过 Hermes Agent 管道（包括工具调用、记忆和推理）进行处理，并实时响应。它支持文本、语音消息、文件附件和斜杠命令。
- 在开始设置之前，先介绍大多数人最想了解的内容：Hermes 进入服务器后的行为方式。
- | **服务器频道** | 默认情况下，Hermes 仅在被 `@提及` 时响应。如果你在频道中发帖但未提及它，Hermes 会忽略该消息。 |
- | **线程（Thread）** | Hermes 在同一线程中回复。提及规则仍然适用，除非该线程或其父频道被配置为自由响应。线程的会话历史与父频道相互隔离。 |
- | **提及其他用户的消息** | 当 `DISCORD_IGNORE_NO_MENTION` 为 `true`（默认值）时，如果消息 @提及了其他用户但**未**提及机器人，Hermes 保持沉默。这可防止机器人介入针对其他人的对话。如果你希望机器人响应所有消息而不管提及了谁，请设置为 `false`。此设置仅适用于服务器频道，不适用于私信。 |
- 5. 正常的 Hermes agent 执行，包括工具、记忆和斜杠命令
- 这一点很重要，因为在繁忙服务器中的行为取决于 Discord 路由和 Hermes 会话策略两者。
- 每个服务器线程有独立的会话命名空间
- ```
group_sessions_per_user: true
```
- ```
group_sessions_per_user: false
```
- 用户共享上下文增长和 token（令牌）成本
- ```
discord:
  websocket_liveness_interval_seconds: 15
  websocket_liveness_failure_threshold: 2
  websocket_heartbeat_ack_max_age_seconds: 60
  websocket_max_latency_seconds: 30
  websocket_event_max_silence_seconds: 14400
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
