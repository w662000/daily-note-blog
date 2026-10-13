---
layout: default
title: 交接文档 · Hermes Studio vs WebUI vs Agent
date: 2026-10-13 23:30:00 +0800
---

# Hermes Studio vs WebUI vs Agent

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\hermes-studio-vs-webui\SKILL.md

---
name: hermes-studio-vs-webui
description: >
  Probe, compare, and operate local Hermes surfaces correctly:
  Hermes Agent CLI, Hermes WebUI (:8787), and Hermes Studio (:8650).
  Covers live verification steps, frontend-vs-API fact checking,
  authentication behavior, and how to call Studio endpoints after login.
version: 1.0.0
author: Hermes Agent
tags: [hermes, studio, webui, api, local-debug]
---

# Hermes Studio vs WebUI vs Agent

## When to use this skill

Use this when you need to:
- Verify which Hermes surface is running locally and on which port.
- Compare capabilities across Studio, WebUI, and the Agent CLI.
- Call Studio or WebUI APIs without guessing endpoints or auth flow.
- Debug "is this module missing?" by checking the SPA frontend, not just the API catalog.
- Recover gracefully when Studio Kanban is blocked by `spawn hermes ENOENT` on Windows.

## Three-layer reality

Hermes is one platform with three layers, not three unrelated products.

| Layer | Surface | Typical local port | Role |
|-------|---------|-------------------|------|
| Execution | Hermes Agent | CLI | Core AI engine, tools, skills, memory |
| Conversation UI | Hermes WebUI | :8787 | Browser chat surface, session list, themes, workspace panel |
| Orchestration | Hermes Studio | :8650 | Full SPA: Kanban, Jobs, Devices, Group Chat, Coding Agents, MCP, Profiles, etc. |

WebUI is **not** a superset of Studio. Studio is the richer surface; WebUI is the lightweight conversation surface. They may share some backend modules, but Studio-only modules such as Kanban, Coding Agents, Devices, Group Chat, Jobs, Write Gate, and MCP management are not exposed by WebUI.

## Live probing recipe

### 1) Liveness

```bash
curl -s -o /dev/null -w "HTTP %{http_code} | Size: %{size_download}" http://127.0.0.1:8650/ --max-time 5
curl -s -o /dev/null -w "HTTP %{http_code} | Size: %{size_download}" http://localhost:8787/ --max-time 5
```

### 2) API catalog

- Use `hermes_studio_api_openapi_get` without filters to list all Studio modules and operation counts.
- Use `hermes_studio_api_openapi_get(tag="Kanban")` or `path="/api/hermes/kanban"` to inspect one module.

### 3) Frontend check

Studio has a real SPA frontend. To verify:
- Fetch the root HTML from `http://127.0.0.1:8650/`; look for `<title>Hermes Studio</title>` and `<base href=...>`.
- Fetch the JS bundle at `/assets/js/index-*.js`.
- Extract router paths from the bundle:
  - Look for route strings like `path: "/hermes/kanban"`, `"/hermes/jobs"`, `"/hermes/devices"`, `"/hermes/group-chat"`, `"/hermes/coding-agents"`, `"/hermes/mcp"`, `"/hermes/settings"`, etc.
- Look for dedicated view bundles: `KanbanView-*.js`, `LoginView-*.js`, `auth-*.js`, `DesktopPetView-*.js`, etc.

### 4) Call authenticated endpoints

Studio login endpoint (confirmed working):

```bash
curl -s http://127.0.0.1:8650/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  --data '{"username":"admin","password":"<PASSWORD>"}'
```

The response includes a bearer token and `userId`. Use that token for subsequent Studio API calls.

### 5) Distinguish auth gating from missing features

- `{"error":"Unauthorized"}` with HTTP 401 means the route exists and auth is required.
- `{"error":"not found"}` means the route is not exposed by this surface.
- A `500` with `spawn hermes ENOENT` means a backend child-process dependency is missing; it is not proof that the frontend is absent.

## Common pitfalls

- Do not conclude "Studio has no frontend / no Kanban UI" just because one API call returns 401 or 500. The frontend bundles and router routes are the authoritative source for UI presence.
- Do not treat WebUI and Studio as the same surface. Some backend modules are shared, but Studio-only modules do not appear in WebUI.
- On Windows, the Studio Node process may not inherit the same `PATH` as your shell. If Kanban/Jobs fail with `spawn hermes ENOENT`, set `HERMES_BIN` to the exact Hermes CLI path and restart the Studio service so the new process env sees it.
- On this setup, Studio’s Studio-MCP processes are launched from `C:\Users\Administrator\.hermes\config.yaml` under `mcp_servers.*.env`. Updating `HERMES_BIN` there via `hermes config set mcp_servers.hermes-studio-api.env.HERMES_BIN <path>` is the supported way; direct edits to `config.yaml` may be refused.
- The failing backend path is: Studio HTTP API → Node MCP server → Python agent bridge → `spawn("hermes")`. So both the MCP server env and the underlying `hermes` binary resolution matter.
- Do not blindly restart entire services. When restarting Studio on Windows, stop only the Studio process (`dist/server/index.js` on the Studio port) and relaunch it, rather than tearing down unrelated services.
- On Windows, shell PATH and the user-level registry PATH can differ. If `shutil.which('hermes')` works in your terminal but Studio still returns `spawn hermes ENOENT`, the likely cause is that the Studio Node/Python bridge processes were launched from the registry environment and did not inherit the shell PATH. Fix by adding `D:\hermes-agent\venv\Scripts` to `HKCU\Environment\Path` or by setting `HERMES_BIN`, then restart the Studio process.
- The real backend chain for Kanban is: Studio HTTP API → Node MCP server → Python agent-bridge bridge process → `spawn("hermes")`. Updating only the MCP server env is therefore necessary but not always sufficient; the bridge process env must also see the Hermes binary.
- If `spawn hermes ENOENT` persists after PATH/HERMES_BIN fixes, treat it as a blocker and fall back to a local `kanban.md` rather than endless restarts. The skill’s reference file includes a minimal local-kanban template.

## Quick comparison by capability

| Capability | WebUI :8787 | Studio :8650 |
|------------|-------------|--------------|
| Chat / session history | Yes | Yes |
| Theme / skin system | Yes, 20+ skins | Yes, separate Studio theme system |
| PWA install | Yes | Yes |
| Kanban board | No | Yes |
| Jobs / cron tasks | No | Yes |
| Coding agents | No | Yes |
| LAN Devices | No | Yes |
| Group chat | No | Yes |
| Write gate | No | Yes |
| MCP management | No | Yes |
| Profiles / skills / models / files / memory | Partial / limited | Yes, fuller management UI |

## Maintained facts

- Studio version: v0.6.39
- WebUI version: same runtime line as Studio; Hermes Agent v0.20.0 installed under `D:\\hermes-agent`
- Kanban route confirmed present in Studio frontend bundle: `/hermes/kanban`
- Studio login route confirmed present in frontend bundle: login view plus `Authorization: Bearer` injection in API client code
- Studio API requires auth by default; WebUI local auth may be disabled
- Local kanban template: `templates/daily-kanban.md` in this skill
