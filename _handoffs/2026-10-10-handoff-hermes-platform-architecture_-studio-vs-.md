---
layout: default
title: 交接文档 · Hermes Platform Architecture_ Studio vs WebUI vs Agent
date: 2026-10-13 23:30:00 +0800
---

# Hermes Platform Architecture: Studio vs WebUI vs Agent

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\user-operational-guidelines\references\hermes-platform-architecture.md

Based on live probe of http://127.0.0.1:8650/ (Studio) and http://localhost:8787/ (WebUI) on 2026-08-09.

## Three-Layer Architecture

Hermes is not three separate products — it's one platform with three layers:

| Layer | Component | Address | Role |
|-------|-----------|---------|------|
| Orchestration | Hermes Studio | http://127.0.0.1:8650/ | Task boards, multi-agent dispatch, device control, coding agent management |
| Conversation/UI | Hermes WebUI | http://localhost:8787/ | Browser-based chat interface, session management, config UI |
| Execution | Hermes Agent | CLI / terminal | Core AI engine with tools, skills, memory |

## Hermes Studio (v0.6.39) — Orchestration Layer

API: 40 modules, 321 operations (via `hermes_studio_api_openapi_get` MCP tool).

### Studio-unique modules (not in WebUI as standalone features):

1. **Kanban** (27 ops) — Multi-agent task board:
   - Boards, columns, cards, parent-child task linking
   - Dispatch tasks to agents with `skills`, `goalMode`, `maxRetries`, `maxRuntime`
   - Block/unblock, assign/reassign, reclaim, diagnostics (warning/error/critical)
   - Bulk updates, task stats, attachments, comments, logs

2. **Coding Agents** (10 ops) — External coding agent orchestration:
   - Install/configure/launch Codex, Claude Code
   - Native launch + prepare launch with provider/model/apiKey/baseUrl
   - Run management: start, stop, send input, config file read/write

3. **Devices** (25 ops) — LAN peer device control:
   - Scan/discover/pair/approve/reject/block devices
   - Peer connections: remote terminal (create/write/read/resize/close)
   - Remote command exec, file upload/download
   - Forms a distributed agent network across machines

4. **Group Chat** (24 ops) — Multi-participant chat rooms

5. **Jobs** (11 ops) — Scheduled/background task management (cron-style)

6. **Write Gate** (4 ops) — Review and approve Agent write operations (security layer)

### Shared modules (Studio + WebUI both expose):
- Sessions (44 ops), Models (13), Providers (9), Skills (11), Profiles (14)
- Files (10), Memory (2), TTS (13), STT (11), Theme (5), MCP (7)
- Auth (16), Config (8), Update (7), Plugins (3), Logs (2)

### How to discover Studio API:
```
# Via MCP tool (preferred — auth handled automatically):
hermes_studio_api_openapi_get                    # list all 40 modules
hermes_studio_api_openapi_get(tag="Kanban")      # drill into one module
hermes_studio_api_openapi_get(path="/api/hermes/kanban")  # by path

# Then call endpoints:
hermes_studio_api_request(method="GET", path="/api/hermes/kanban")
```

## Hermes WebUI (:8787) — Conversation Layer

- Returns full SPA HTML directly (no auth gate on root page)
- 20+ skin themes: codex, terracotta, catppuccin, neon, zeus, hepburn, nous, geist-contrast, slate, poseidon, sisyphus, charizard, sienna, graphite, github, mono, verdigris, etc.
- Font size control, workspace panel toggle
- PWA support (manifest.json, apple-touch-icon, mobile-web-app-capable)
- Subpath mount support for reverse proxy deployment
- `hermes-webui-workspace-panel` localStorage toggle

## Key Insight

When user asks "compare Studio vs WebUI", the answer is NOT about which is "smarter" — they serve different layers:
- **Studio** = project management + multi-agent orchestration + device network
- **WebUI** = the chat window you talk to the agent through
- **Agent** = the AI brain that actually does the work

Studio's Kanban can dispatch tasks that get executed by Agent instances. WebUI is one of the surfaces those Agent instances can be reached through. They are complementary, not competing.

## Probing Technique (reusable)

When asked to evaluate/compare any local Hermes service:
1. `curl -s -o /dev/null -w "HTTP %{http_code}" http://127.0.0.1:PORT/` — liveness check
2. `hermes_studio_api_openapi_get` — get full API catalog (no auth needed via MCP)
3. `hermes_studio_api_openapi_get(tag="ModuleName")` — drill into specific modules
4. `curl -s http://PORT/ | head -c 3000` — inspect HTML for UI features
5. `hermes_studio_api_request(method="GET", path="/api/...")` — call authenticated endpoints

---

*Created: 2026-08-09 based on live probe of Studio v0.6.39 and WebUI on the same host.*
