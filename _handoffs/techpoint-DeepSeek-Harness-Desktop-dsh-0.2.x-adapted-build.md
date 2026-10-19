---
layout: default
title: 技术点 · DeepSeek Harness Desktop (dsh 0.2.x adapted build)
date: 2026-10-18 23:30:00 +0800
---

# 技术点 · DeepSeek Harness Desktop (dsh 0.2.x adapted build)

> 来源：261018_DeepSeek Harness Desktop (dsh 0.2.x adapted build)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **Shares `~/.dsh` with the CLI**: API keys, model settings, session history and installed plugins all carry over; both entry points can be mixed freely
- First-run wizard for the API key (skipped automatically if already configured); one-click service restart on crash; NSIS installer in Chinese
- ```
Use AgentTeams to review this project from performance, security, and product
perspectives. Return one consolidated report.
```
- 1. **Token authentication gate on the web UI**: bare URLs return 401; the full `?token=` address printed at startup is required
- | Token auth adaptation | ❌ fixed URL, white screen on 0.2.x | ✅ `main.js` URL regex captures the full `?token=` address (unit-verified against both 0.1.x and 0.2.x output) |
- 4. **Already using the dsh CLI? Just use it** — the desktop app reads the same `~/.dsh`; your API keys, plugins and sessions are all there, nothing to reconfigure
- **Auth mechanism**: dsh 0.2.x generates a random token on every launch (handled automatically and invisibly by this app). The token is for local loopback access only, combined with Host/Origin checks defending against DNS rebinding and cross-site requests — a security feature, not a bug
- **Uninstall keeps your data**: sessions, settings and API keys live in `%USERPROFILE%\.dsh`; uninstalling the app doesn't touch them
- ```
scripts\assemble-runtime.cmd
```
- ```
npm ci
npm run dist        # output: dist/DeepSeek-Harness-Setup-<version>.exe
```
- `dist/win-unpacked/DeepSeekHarness.exe` runs without installation (note: when testing from the built-in terminal of Electron-based IDEs like WorkBuddy, clear the `ELECTRON_RUN_AS_NODE` variable first, otherwise electron runs as plain Node). Check `%APPDATA%\deepseek-harness-desktop\logs\server.log` for `resolved URL: http://127.0.0.1:<port>/?token=...` — that's the token pipeline working end to end.
- ```
├── main.js                # Electron main process (0.2.x token URL parsing patch + --no-open)
├── preload.js             # Secure renderer bridge
├── build/                 # Icons and NSIS installer assets
├── scripts/
│   ├── assemble-runtime.cmd   # Assemble server/runtime from your global dsh + node.exe (required before build)
│   └── ...                # Icon generation / e2e / wizard verification scripts (from upstream)
└── server/runtime/        # Runtime (not committed; assembled pre-build): node.exe + node_modules/@deepseek-ai/dsh
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
