---
layout: default
title: 技术点 · Windows (Native) Guide
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Windows (Native) Guide

> 来源：261010_Windows (Native) Guide_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```
- ```
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1))) -NoVenv -SkipSetup -Branch main
```
- 7. **Auto-installs messaging SDKs** keyed off `.env` — if `TELEGRAM_BOT_TOKEN` / `DISCORD_BOT_TOKEN` / `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` / `WHATSAPP_ENABLED` are present, runs `python -m ensurepip --upgrade` and targeted `pip install` calls so each platform's SDK is actually importable.
- On Windows, per-tool API key setup (Firecrawl, FAL, Browser Use, OpenAI TTS) is the highest-friction part of getting a useful agent. A [Nous Portal](./features/tool-gateway.md) subscription covers the model **and** all of those tools through one OAuth login. After the installer finishes, run `hermes setup --portal` to wire everything up.
- ```
# In $PROFILE
$env:EDITOR = "code --wait"
```
- Windows Terminal passes `Ctrl+Enter` through as a dedicated key sequence. Hermes binds it to "insert newline" so you can compose multi-line prompts in the CLI without falling back to `Esc`-then-`Enter`. Works in Windows Terminal, VS Code integrated terminal, and any modern Windows console host that honors VT escape sequences.
- ```
hermes gateway install
```
- ```
hermes gateway status      # Merged view: schtasks + Startup folder + running PID
hermes gateway start       # Starts the gateway in the background (asks about login auto-start only on a TTY when nothing is installed)
hermes gateway stop        # Writes the planned-stop marker, waits for the gateway to drain (≤ agent.restart_drain_timeout, capped at 30 s), then force-kills only if it is still alive
hermes gateway restart     # Same drain-first stop, then a fresh start
hermes gateway uninstall   # Removes schtasks entry, Startup shortcut, pid file
```
- ```
Get-Command hermes        # should print C:\Users\<you>\AppData\Local\hermes\bin\hermes.exe
hermes --version
```
- Hermes honors both `$env:X` (process-scope) and User environment variables (permanent, set in System Properties → Environment Variables). Setting API keys in `%LOCALAPPDATA%\hermes\.env` (your `HERMES_HOME`) is the normal path — same as Linux:
- ```
OPENROUTER_API_KEY=sk-or-...
TELEGRAM_BOT_TOKEN=...
```
- ```
hermes uninstall
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
