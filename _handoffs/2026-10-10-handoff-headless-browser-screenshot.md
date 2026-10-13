---
layout: default
title: 交接文档 · Headless Browser Screenshot
date: 2026-10-13 23:30:00 +0800
---

# Headless Browser Screenshot

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\media\headless-browser-screenshot\SKILL.md

---
name: headless-browser-screenshot
description: Take screenshots of URLs via Playwright headless browser.
---

# Headless Browser Screenshot

Capture full-page or viewport screenshots of any URL using Playwright's headless Chromium from the terminal.

## Trigger

User asks to "screenshot a URL", "capture a webpage", "take a browser screenshot", "open X and screenshot", etc.

## One-shot flow

```bash
# 1. Ensure Chromium is installed (first time only; ~190MB)
npx playwright install chromium

# 2. Capture full-page screenshot
npx playwright screenshot --full-page <URL> /path/to/output.png

# 3. Confirm file exists
ls -la /path/to/output.png
```

## Options

- `--full-page` — capture the entire scrollable page (default recommendation)
- `--viewport-size=1280,720` — override viewport dimensions
- `--wait-for-timeout=3000` — extra wait after load (useful for SPA/JS-heavy pages)
- `--user-agent="..."` — spoof UA string if the site behaves differently for headless
- Omit `--full-page` for viewport-only capture

## Pitfalls

- **First install required**: Playwright ships without the browser binary. `npx playwright screenshot` on a fresh env will fail with "Executable doesn't exist" — run `npx playwright install chromium` first (downloads Chrome + FFmpeg + headless-shell). Only run once per machine.
- **Save path**: on Windows, use forward-slash POSIX paths like `D:/workspace/foo.png` (via git-bash) or the terminal's current working directory. Do NOT use backslashes in MSYS paths.
- **Use cwd or absolute paths**: set `workdir` when calling from `terminal`, or pass an absolute save path. Relative paths resolve against the tool's cwd, which may differ from the user's workspace.
- **Large pages can time out**: raise `timeout` on `terminal` to 60s+ for JS-heavy sites; default 30s may cut off.
- **Hermes MCP browser tool exists too**: if `hermes-studio-browser` MCP server is enabled, prefer the native `browser` toolset for interactive screenshots. Playwright CLI is the fallback.
- **SVG-only pages**: `vision_analyze` cannot read raw SVG URLs. Rasterize via Playwright to PNG first.

## Reference

See `references/playwright-quickref.md` for the full CLI flag reference.
