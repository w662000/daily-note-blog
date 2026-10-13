---
layout: default
title: 技术点 · MCP OAuth on a Remote Hermes Gateway
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · MCP OAuth on a Remote Hermes Gateway

> 来源：261010_MCP OAuth on a Remote Hermes Gateway_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- This skill does the OAuth dance by hand and writes the resulting tokens into the
- exact files Hermes' token storage expects, so a subsequent `/reload-mcp` finds
- cached tokens and skips the browser flow entirely.
- 1. The user wants to add a remote HTTP MCP server that requires OAuth (not a static Bearer token).
- 3. The server supports OAuth 2.1 with PKCE and RFC 7591 Dynamic Client Registration (most modern MCP servers do — Better Stack, Linear, Cloudflare, Datadog, etc.). If it doesn't support DCR (GitHub is the notable exception), this skill does not apply — use a pre-registered OAuth App or a Personal Access Token instead.
- **Servers that accept a static Bearer token (API key)** — always prefer `headers.Authorization: "Bearer <token>"` when the user is willing. Simpler, no refresh dance.
- **GitHub Copilot MCP** (`api.githubcopilot.com/mcp/`) — GitHub does not expose DCR. Use a PAT or a pre-registered OAuth App (see pitfall 12).
- empty or missing tokens directory (`$HERMES_HOME/mcp-tokens/`), and a reload that
- Before any manual token surgery, check whether the built-in flow's fallbacks
- endpoints like `/api/mcp/servers`, `/api/mcp/status`, and `/connectors` (all
- 1. **Dashboard, in the user's browser** — the intended front door. Add servers, run OAuth, reload, all authenticated as the user. No copy-paste-callback dance, no hand-writing token files.
- 2. **Manual token surgery (the rest of this skill)** — the FALLBACK for when there's no browser session to the dashboard (pure-chat/headless context).

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
