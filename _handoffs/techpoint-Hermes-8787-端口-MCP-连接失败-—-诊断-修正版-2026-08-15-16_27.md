---
layout: default
title: 技术点 · Hermes 8787 端口 MCP 连接失败 — 诊断（修正版 2026-08-15 16_27）
date: 2026-08-15 23:30:00 +0800
---

# 技术点 · Hermes 8787 端口 MCP 连接失败 — 诊断（修正版 2026-08-15 16_27）

> 来源：260815_Hermes 8787 端口 MCP 连接失败 — 诊断（修正版 2026-08-15 16_27）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\260815_Hermes 8787 端口 MCP 连接失败 — 诊断（修正版 2026-08-15 16_27）_handoff.md（编码探测：utf-8）
- > 修正说明：早先一版把"8787 壳 Python venv 缺 requests/httpx"当头号根因，经本轮实测**已证伪**（见「已排除的误判」）。本文为修正后的结论。
- 8787 webui 上"无法连接 MCP 服务器"的**真实症状**：Hermes 的 5 个 MCP server
- （`hermes-studio-api` / `browser` / `devices` / `use` + `playwright`）在当前
- `status="configured"`、`tool_count=0`**——即**配置都在、但一个都没被拉起/连接**。
- agent 调用"打开网站并截图"（依赖 `hermes-studio-browser` toolset）时注册表里
- 1. 8787 进程存活：PID 14920 = `D:\hermes-agent\venv\Scripts\pythonw.exe D:\hermes-webui\server.py`，监听 `127.0.0.1:8787` ✅
- 2. 8650（Node 壳）、8642（gateway/agent）、8787 三个端口**全部在监听** ✅
- 3. MCP server 依赖的二进制全存在：
- 4. **当前没有任何 MCP 子进程在跑**（tasklist 无 hermes-studio/playwright/mcp）。
- 6. 8787 的 `/api/mcp/servers` 直接读 hermes-agent 注册表（`tools.mcp_tool.get_mcp_status()`），
- 两者共用 `C:\Users\Administrator\.hermes\config.yaml`，其中 `mcp_servers` 全部硬编码指向

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
- 当前 MCP 状态：`curl -s http://127.0.0.1:8787/api/mcp/servers`
- 在跑进程：`tasklist | findstr /I "hermes-studio playwright mcp"`
- MCP 子进程 stderr（启动日志）：`C:\Users\Administrator\.hermes\logs\mcp-stderr.log`
- 8787 运行日志：`C:\Users\Administrator\.hermes-web-ui\logs\webui8787-*.err.log` / `*.log`

## 五、后续风险
（见源 handoff 后续风险字段）
