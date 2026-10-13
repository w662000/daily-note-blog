---
layout: default
title: 交接文档 · Hermes Desktop Connection Troubleshooting
date: 2026-10-13 23:30:00 +0800
---

# Hermes Desktop Connection Troubleshooting

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\hermes-desktop-setup\references\api-connection-troubleshooting.md

**Session Date:** 2026-08-05  
**Problem:** Desktop shows 404 when connecting to http://localhost:8642/  
**Status:** ✅ Resolved

## Root Cause Analysis

### Why 404 on Root Path?
API Server only provides OpenAI-compatible API endpoints, not a web interface:
- ✅ `GET /v1/health` → 200 OK
- ❌ `GET /` → 404 Not Found (expected)

### API Server Configuration
From `~/.hermes/.env`:
```env
API_SERVER_ENABLED=true
API_SERVER_KEY=2429037064705e32237b76fd2e25ffa91236ef57ee582a827589b566049d2ba3
API_SERVER_HOST=127.0.0.1
API_SERVER_PORT=8642
```

## Successful Connection Test

### 1. Health Check (No Auth)
```bash
curl http://localhost:8642/v1/health
# Response: {"status": "ok", "platform": "hermes-agent", "version": "0.20.0"}
```

### 2. Models List (With Auth)
```bash
curl http://localhost:8642/v1/models \
  -H "Authorization: Bearer 2429037064705e32237b76fd2e25ffa91236ef57ee582a827589b566049d2ba3"
# Response: [{"id": "hermes-agent", "object": "model", "created": 1785936280, ...}]
```

### 3. Chat Completion (With Auth)
```bash
curl http://localhost:8642/v1/chat/completions -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 2429037064705e32237b76fd2e25ffa91236ef57ee582a827589b566049d2ba3" \
  -d '{"model":"glm-4.5-air","messages":[{"role":"user","content":"test"}]}'
# Response: {"id": "chatcmpl-...", "choices": [...], "usage": {...}}
```

## Desktop Connection Issues

### Issue: No API Key Input Field Visible
**Symptom:** Desktop shows "Connect to existing Hermes" but no API Key field

**Possible Solutions:**
1. Wait 2-3 minutes for full UI load
2. Click "Browser Sign-in" option instead
3. Check for "Use API Key" link or "Advanced options"
4. Close and restart Desktop: `hermes desktop`

### Alternative: Web Dashboard
```bash
hermes dashboard
# Access at: http://localhost:9119
```

### Alternative: CLI/TUI
```bash
hermes --cli    # Classic terminal
hermes --tui    # Modern terminal UI
```

## System Verification Checklist

- [ ] API Server running: `hermes gateway status`
- [ ] Port 8642 listening: `netstat -an | grep 8642`
- [ ] Health check passes: `curl http://localhost:8642/v1/health`
- [ ] API Key correct: `cat ~/.hermes/.env | grep API_SERVER_KEY`
- [ ] Models accessible: `curl .../v1/models -H "Authorization: Bearer KEY"`

## Related Resources
- [Hermes API Server Docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/api-server)
- [Hermes Desktop Docs](https://hermes-agent.nousresearch.com/docs/user-guide/desktop)
- [Gateway Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
