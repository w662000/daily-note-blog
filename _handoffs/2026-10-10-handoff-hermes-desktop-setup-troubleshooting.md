---
layout: default
title: 交接文档 · Hermes Desktop Setup & Troubleshooting
date: 2026-10-13 23:30:00 +0800
---

# Hermes Desktop Setup & Troubleshooting

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\hermes-desktop-setup\SKILL.md

---
name: hermes-desktop-setup
description: "Fix Hermes Desktop install issues on Windows."
version: 1.0.0
platforms: [windows]
metadata:
  hermes:
    tags: [hermes, desktop, installation, troubleshooting, windows]
---

# Hermes Desktop Setup & Troubleshooting

## Overview
Hermes Desktop is the official native Electron app from Nous Research. This skill covers systematic troubleshooting when the desktop app fails to install or launch.

## Common Issues & Solutions

### Issue 1: TypeScript compiler missing
**Symptom:** `tsc: command not found` during build
**Fix:**
```bash
npm install -g typescript
```

### Issue 2: npm lock file mismatch
**Symptom:** `npm ci` fails with "package.json and package-lock.json are out of sync"
**Fix:**
```bash
cd /path/to/apps/desktop
rm -f package-lock.json
npm install --legacy-peer-deps
```

### Issue 3: Missing mermaid dependency
**Symptom:** `Rolldown failed to resolve import "mermaid"`
**Fix:**
```bash
npm install mermaid --legacy-peer-deps
```

### Issue 4: Electron not installed
**Symptom:** Electron module not found
**Fix:**
```bash
npm install electron --save-dev --legacy-peer-deps
```

### Issue 5: Node.js/npm not on PATH
**Symptom:** `bash: npm: command not found`
**Fix:**
```bash
export PATH="/c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0:$PATH"
```

## Systematic Fix Procedure

1. **Check environment:**
   ```bash
   node --version
   npm --version
   hermes --version
   ```

2. **Install TypeScript:**
   ```bash
   npm install -g typescript
   ```

3. **Clean and reinstall dependencies:**
   ```bash
   cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop
   rm -rf node_modules
   npm install --legacy-peer-deps
   ```

4. **Install missing dependencies:**
   ```bash
   npm install mermaid electron --save-dev --legacy-peer-deps
   ```

5. **Build the app:**
   ```bash
   npm run build
   ```

6. **Run in development mode:**
   ```bash
   # Terminal 1: Start Vite dev server
   npm run dev:renderer
   
   # Terminal 2: Start Electron
   npm run dev:electron
   ```

## Ports & Debugging
- **Vite dev server:** http://127.0.0.1:5174
- **Electron CDP debug:** ws://127.0.0.1:9222
- **Renderer debug:** http://127.0.0.1:9222

## Verification
After successful setup:
- Build completes without errors
- `dist/` directory contains built files
- Electron app launches
- DevTools available on port 9222
- API Server connection working (run `scripts/diagnose-connection.sh`)

## Development Mode
For debugging, run in development mode:
```bash
# Terminal 1: Start Vite dev server
export PATH="/c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0:$PATH"
cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop
npm run dev:renderer

# Terminal 2: Start Electron
export PATH="/c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0:$PATH"
cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop
npm run dev:electron
```

## API Server Connection

### Finding API Key
API key is stored in `~/.hermes/.env`:
```bash
cat ~/.hermes/.env | grep API_SERVER_KEY
```

### Testing Connection
```bash
# Health check (no auth needed)
curl http://localhost:8642/v1/health

# Models endpoint (needs auth)
curl http://localhost:8642/v1/models -H "Authorization: Bearer YOUR_API_KEY"

# Chat endpoint (needs auth)
curl http://localhost:8642/v1/chat/completions -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"model":"glm-4.5-air","messages":[{"role":"user","content":"test"}]}'
```

### Desktop Connection Steps
1. Click "Connect to existing Hermes" card
2. Select "API Key" authentication method
3. Enter:
   - Server URL: `http://localhost:8642`
   - API Key: (from .env file)
4. Click "Connect" or "Test Connection"

**Note:** If API Key input box doesn't appear, try "Browser Sign-in" option instead.

## Related Skills
- `hermes-agent` - General Hermes configuration
- `computer-use` - Desktop automation
