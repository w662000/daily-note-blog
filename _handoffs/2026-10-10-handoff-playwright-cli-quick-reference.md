---
layout: default
title: 交接文档 · Playwright CLI Quick Reference
date: 2026-10-13 23:30:00 +0800
---

# Playwright CLI Quick Reference

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\media\headless-browser-screenshot\references\playwright-quickref.md

## Install browsers (one-time)

```bash
npx playwright install chromium        # full Chromium (~190MB)
npx playwright install chromium-headless-shell  # lighter (~115MB)
npx playwright install                  # all three browsers (Chromium, Firefox, WebKit)
```

## Screenshot commands

```bash
# Full page
npx playwright screenshot --full-page URL PATH

# Viewport only (default 1280x720)
npx playwright screenshot URL PATH

# Custom viewport + wait
npx playwright screenshot --viewport-size=1920,1080 --wait-for-timeout=2000 URL PATH

# Specific element
npx playwright screenshot --selector="#content" URL PATH

# PDF export (bonus)
npx playwright pdf URL /path/to/out.pdf
```

## Key flags

| Flag | Default | Notes |
|------|---------|-------|
| `--full-page` | false | Capture entire scrollable page |
| `--viewport-size` | 1280,720 | Comma-separated W,H |
| `--wait-for-timeout` | 0 | Extra ms after load state |
| `--user-agent` | Playwright UA | Useful for UA-sensitive sites |
| `--device` | none | E.g. `iphone-12` |
| `--color-scheme` | light | `light` / `dark` |
| `--storage-state` | none | JSON file with cookies/localStorage for logged-in sites |
| `--timeout` | 30000 | Max navigation time (ms) |

## Notes

- Output formats supported: PNG (default), JPEG, WEBP — determined by file extension.
- Headless Chromium uses the **playwright** user-agent; sites that block headless UA may require `--user-agent` override.
- `storage-state` lets you persist login cookies between runs — export via `npx playwright storage-state --path state.json URL`.
