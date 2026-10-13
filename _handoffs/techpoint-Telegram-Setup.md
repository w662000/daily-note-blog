---
layout: default
title: 技术点 · Telegram Setup
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Telegram Setup

> 来源：261010_Telegram Setup_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- The **Messaging → Telegram** page in the [dashboard](../features/web-dashboard.md) and the [desktop app](../desktop.md) has a **Create with QR** button. Scan the code (or open the link) in Telegram; Hermes creates the bot for you, detects your Telegram user ID, writes `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS` into your profile's `.env`, and restarts the gateway. If you prefer to create the bot yourself, follow the manual steps below.
- Every Telegram bot requires an API token issued by [@BotFather](https://t.me/BotFather), Telegram's official bot management tool.
- 5. BotFather replies with your **API token**. It looks like this:
- ```
123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```
- Keep your bot token secret. Anyone with this token can control your bot. If it leaks, revoke it immediately via `/revoke` in BotFather.
- ```
help - Show help information
new - Start a new conversation
sethome - Set this chat as the home channel
```
- *user-account* feature, not something the Bot API exposes for bots. The closest
- ```
gateway:
  platforms:
    telegram:
      extra:
        status_indicator: true
        # Optional custom strings (defaults: "Online" / "Offline"):
        status_online: "🟢 Online"
        status_offline: "🔴 Offline"
```
- messages sent while the gateway is offline sit in Telegram's Bot API queue,
- ```
platforms:
  telegram:
    extra:
      drop_pending_on_cold_boot: false
```
- ```
platforms:
  telegram:
    extra:
      command_menu:
        max_commands: 60
        priority_mode: prepend  # prepend | append | replace
        priority:
          - my_plugin_command
          - songsee          # skill commands work here too
```
- The `/` menu is capped, but Telegram's **inline mode** is not. Once enabled, type `@yourbotname` followed by a search term in any chat to get a live, searchable picker over **every** Hermes command and installed skill — results are computed per keystroke and paginated, so nothing is ever trimmed:

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
