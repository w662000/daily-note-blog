---
layout: default
title: 技术点 · Extending the Dashboard
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Extending the Dashboard

> 来源：261010_Extending the Dashboard_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "Build themes and plugins for the Hermes web dashboard — palettes, typography, layouts, custom tabs, shell slots, page-scoped slots, and backend API routes"
- 3. **Backend plugins** — a Python file inside that plugin directory that exposes a FastAPI `router`; routes are mounted under `/api/plugins/<name>/` and called from the plugin's UI.
- This page covers the **web dashboard** (`hermes dashboard`) plugin system — `window.__HERMES_PLUGIN_SDK__`, a `manifest.json`, and a pre-built JS bundle. The **native desktop app** (`hermes desktop`) has its own, unrelated SDK — `@hermes/plugin-sdk`, a single ESM file, no build step — documented at [Desktop Plugin SDK](../../developer-guide/desktop-plugin-sdk.md). Only the backend `plugin_api.py` namespace (`/api/plugins/<name>`) is shared between them.
- [Backend API routes](#backend-api-routes)
- [API reference](#api-reference)
- Themes are YAML files stored in `~/.hermes/dashboard-themes/`. The file name doesn't matter (the theme's `name:` field is what the system uses), but convention is `<name>.yaml`. Every field is optional — missing keys fall back to the built-in `default` theme, so a theme can be as small as one color.
- ```
mkdir -p ~/.hermes/dashboard-themes
```
- ```
# ~/.hermes/dashboard-themes/neon.yaml
name: neon
label: Neon
description: Pure magenta on black

palette:
  background: "#000000"
  midground: "#ff00ff"
```
- The palette is a triplet of color layers plus a warm-glow vignette color and a noise-grain multiplier. The dashboard's design-system cascade derives every shadcn-compatible token (card, popover, muted, border, primary, destructive, ring, etc.) from this triplet via CSS `color-mix()`. Overriding three colors cascades into the whole UI.
- | Key | Description |
- ```
palette:
  background:
    hex: "#05091a"
    alpha: 1.0
  midground: "#d8f0ff"          # bare hex, alpha = 1.0
  foreground:
    hex: "#ffffff"
    alpha: 0                    # invisible top layer
  warmGlow: "rgba(255, 199, 55, 0.24)"
  noiseOpacity: 0.7
```
- | Key | Type | Description |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
