---
layout: default
title: 技术点 · Hermes Web Dashboard
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Hermes Web Dashboard

> 来源：261010_Hermes Web Dashboard_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "Browser-based administration panel for managing configuration, API keys, MCP servers, messaging pairing, webhooks, the gateway, memory, credentials, sessions, logs, analytics, cron jobs, and skills"
- The web dashboard is a browser-based UI for managing your Hermes Agent installation. Instead of editing YAML files or running CLI commands, you can configure settings, manage API keys, and monitor sessions from a clean web interface.
- ```
hermes dashboard
```
- ```
# Custom port
hermes dashboard --port 8080

# Bind to all interfaces (use with caution on shared networks)
hermes dashboard --host 0.0.0.0

# Start without opening browser
hermes dashboard --no-open
```
- profile the management pages read and write — Config, API Keys, Skills,
- ```
worker dashboard
# → already running: opens the browser at ?profile=worker
# → not running:     starts the machine dashboard with "worker" preselected
```
- The default `hermes-agent` install does not ship the HTTP stack or PTY helper — those are optional extras. The **web dashboard** needs FastAPI and Uvicorn (`web` extra). The **Chat** tab also needs `ptyprocess` to spawn the embedded TUI behind a pseudo-terminal (`pty` extra on POSIX). Install both with:
- ```
cd ~/.hermes/hermes-agent && uv pip install -e ".[web,pty]"
```
- The `web` extra pulls in FastAPI/Uvicorn; `pty` pulls in `ptyprocess` (POSIX) or `pywinpty` (native Windows — note that the embedded TUI itself still requires WSL). `cd ~/.hermes/hermes-agent && uv pip install -e ".[all]"` includes both extras and is the easiest path if you also want messaging/voice/etc.
- **Recent sessions** — list of the 20 most recent sessions with model, message count, token usage, and a preview of the conversation
- `/api/pty` opens a WebSocket authenticated with the dashboard's session token
- Keystrokes travel to the PTY; ANSI output streams back to the browser

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
