---
layout: default
title: 技术点 · Slack Setup
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Slack Setup

> 来源：261010_Slack Setup_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Classic Slack apps (using RTM API) were **fully deprecated in March 2025**. Hermes uses the modern
- | **Auth tokens needed** | Bot Token (`xoxb-`) + App-Level Token (`xapp-`) |
- ```
   hermes slack manifest --agent-view --write
```
- ```
   hermes slack manifest --agent-view \
     --long-description-file AGENTS.md --write
```
- 2. Go to [https://api.slack.com/apps](https://api.slack.com/apps) →
- 1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
- Navigate to **Features → OAuth & Permissions** in the sidebar. Scroll to **Scopes → Bot Token Scopes** and add the following:
- 3. You'll be prompted to create an **App-Level Token**:
- 4. **Copy the token** — it starts with `xapp-`. This is your `SLACK_APP_TOKEN`
- You can always find or regenerate app-level tokens under **Settings → Basic Information → App-Level Tokens**.
- 4. After authorization, you'll see a **Bot User OAuth Token** starting with `xoxb-`
- 5. **Copy this token** — this is your `SLACK_BOT_TOKEN`

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
