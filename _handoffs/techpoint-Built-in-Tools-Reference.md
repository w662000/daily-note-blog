---
layout: default
title: 技术点 · Built-in Tools Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Built-in Tools Reference

> 来源：261010_Built-in Tools Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | `browser_console` | Get browser console output and JavaScript errors from the current page. Returns console.log/warn/error/info messages and uncaught JS exceptions. Use this to detect silent JavaScript errors, failed API calls, and application warnings. Requi… | — |
- | `browser_press` | Press a keyboard key. Useful for submitting forms (Enter), navigating (Tab), or keyboard shortcuts. Requires browser_navigate to be called first. | — |
- | `manage_connections` | Managed actions: `status`, `connect`, `reconnect` (repairs only what is not connected; `force: true` restarts a working one). MCP actions, for `mcp: true` targets only: `install` a catalog entry, `enable` a disabled configured server, `authorize` (OAuth). In the desktop app, the terminal UI and the classic CLI every action shows a card and blocks until each target is connected, skipped, or the 300-second deadline passes; the result lists targets as `connected`, `skipped` or `not_connected` and carries no link. An MCP `install` collects the entry's setup values in the card, runs the entry's OAuth from the card when it has one (the user opens the link; nothing opens by itself), and saves configuration, tokens and values together when the server accepts the token. A connected MCP target carries `tools` (the registered names) and `tools_listing`, and those tools are callable through `tool_describe`/`tool_call` in the same turn. A target with `discovery_error` is authorized but its tools could not be listed; call `install` or `authorize` for it again to retry discovery without new consent. On surfaces with no card (messaging, scripted dispatch) managed targets return a `connect_url` per app for the user to open, and an MCP target runs at once: `authorize` and an OAuth `install` return the authorization URL, other installs and `enable` report the outcome, and a missing credential comes back as `failed` naming the variable to set. Cannot disconnect or revoke an account. | — |
- token). Other sessions do not see it.
- | `feishu_doc_read` | Read the full text content of a Feishu/Lark document (Docx, Doc, or Sheet) given its file_type and token. | Feishu app credentials |
- | `computer_use` | Background desktop control via cua-driver — screenshots (SOM / vision / AX), click / drag / scroll / type / key / wait, list_apps, focus_app. Does NOT steal the user's cursor or keyboard focus. Works with any tool-capable model. macOS, Windows, and Linux. | `cua-driver` on `$PATH` (install via `hermes tools`). |
- | `image_generate` | Generate images from text prompts (text-to-image) or edit/transform an existing image (image-to-image) via the user-configured backend (FAL.ai, OpenAI, OpenAI Codex auth, xAI, Krea). Pass `image_url` to edit an image and `reference_image_urls` for style references; omit both for text-to-image. The model is user-configured and not selectable by the agent. Returns a single image URL or local path. | FAL_KEY / OPENAI_API_KEY / Codex OAuth / xAI OAuth / KREA_API_KEY |
- | `drive_preview` | Interact with the page open in the in-app browser: `elements` inventories what's clickable and typable (each with a ref that names it, like `btn-sign-in` or `inp-email`, plus role, label, and value), then `click`, `hover`, `type`, `scroll`, and `press` act on a ref, and `back`/`forward`/`reload` drive the pane's history. The pointer and keyboard are real input, so hover menus open. A ref lasts until the page navigates, including across a re-render that rebuilds the element, so after the first inventory every action answers with just a delta — what was added, removed, changed, or rebound — instead of the whole page again. | — |
- The `gui_tour` tool discovers its own targets — call `action='targets'` and it returns every addressable element on screen with a selector, a label, and a `stable` flag. Stable selectors key off identity (`data-tour`, `id`, `data-testid`, `aria-label`) and survive a re-render; positional `nth-child` paths don't, so stable ones sort first and should be preferred.
- ```
<div data-tour="composer">…</div>
```
- | `field-<schemaKey>` | one settings row, by its config key — `field-model`, `field-provider`, … |
- ```
import { startTour, showTourStep, stopTour } from '@/lib/tour'

startTour([
  { selector: '[data-tour="composer"]', title: 'Composer', text: 'Type here.' },
  { selector: '[data-tour="files"]', title: 'Files', text: 'Browse your project.' }
])
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
