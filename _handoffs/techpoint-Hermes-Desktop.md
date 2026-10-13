---
layout: default
title: 技术点 · Hermes Desktop
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Hermes Desktop

> 来源：261010_Hermes Desktop_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- The Hermes desktop app is a native app built around the **same** agent you get from the CLI and the gateway — same config, same API keys, same sessions, same skills, same memory. It is not a separate product or a lightweight clone; it uses the same Hermes Agent core and settings, and drives it through a modern & thoughtfully designed UI. If you have used `hermes` in a terminal, everything you set up there is already here, and anything you do here shows up there.
- ```
hermes desktop
```
- That uses your current config, keys, sessions, and skills.
- **Hide vs. Close for stateful panes** — a zone holding a Browser (or HTML preview) or the Terminal pane offers **Hide** instead of Minimize. Hiding collapses the zone to its restore rail but keeps the pane's body mounted: a live page keeps its unsaved form input, timers, scroll position, and the agent's `drive_preview` automation target; a terminal keeps its running shell and scrollback; and **Restore** shows the same content without a reload. The hidden body is inert — it never takes keyboard shortcuts or steals composer focus. **Close** (the tab's ×) is what actually releases the page or shell.
- **Comment mode in the in-app browser** — click **Annotate** in the preview browser bar, then click any element (or drag a box) on the live page and type a note; each saved comment stays as a numbered pin on the page. Saving a pin never sends a turn — when you're done, **Add N comments** attaches a cropped screenshot per pin and a short prompt naming each comment to the composer, and you still hit send yourself. Each element comment carries its CSS selector, its markup, and the computed styles that matter for layout, so the agent can find the element in your source instead of guessing from the picture. Password and hidden field values, and any attribute that looks like a key or token, are redacted on the page before the markup leaves it. Larger batches arrive grouped by which part of the page each comment sits in, so twenty-odd comments become a handful of pieces of work rather than one task each — and because the groups are separate DOM subtrees they usually touch separate files, which is what makes handing them to parallel workers safe. Pin numbers hold steady if you delete one, and switching chats clears the stack.
- **Composer history and queue editing** — press the up/down arrow keys in an empty composer to recall and reuse previous prompts, and edit messages you've queued up before they're sent. Pressing Stop (or Esc) while turns are queued pauses the queue and expands it above the composer; resume it from there, or send, edit, and delete individual entries.
- **Context-usage meter** — a live "% full" meter of the session's context window. Click it to open the **Context Usage** popover with a token breakdown by category (system prompt, tool definitions, skills, memory, rules, MCP, subagent definitions, and the conversation itself) so you can see exactly what's eating the window before compression kicks in.
- **Cache hit rate and tokens per second** — off by default; turn them on from the right-click menu. Cache hit rate is the share of this session's prompt tokens served from the provider's prompt cache (cached tokens cost less, so higher is cheaper — you can watch a session get cheaper as it warms up). Tokens per second is output throughput averaged over the last 10 model calls. Both update live during a turn.
- **Customizable items** — right-click the status bar (**Show in status bar**) to choose what appears: the context meter, cache hit rate, tokens per second, workspace, model, approvals, turn/session timers, terminal, Command Center, backend version, and more — or hide the bar entirely (**Cmd/Ctrl+Shift+S** toggles it). The workspace item's menu offers **Open containing folder** only when the focused session runs on this computer; a session on a remote gateway keeps its folder on that machine, so use **Reveal in filetree** instead. When the OS file manager cannot find a path, the app says so instead of doing nothing.
- Chatting against a Hermes instance on another machine instead of the bundled local backend? See [Connecting to a remote backend](#connecting-to-a-remote-backend) below — and for the full picture of how the remote-hosted dashboard connection works (the auth gate, the `/api/ws` chat socket, and WebSocket close-code triage), see [Web Dashboard → Connecting Hermes Desktop to a remote backend](./features/web-dashboard.md#connecting-hermes-desktop-to-a-remote-backend).
- ```
desktop:
  repo_scan_enabled: true
  repo_scan_roots: []
  repo_scan_exclude_paths: []
```
- **The composer picker is sticky UI state and never touches your default.** It's remembered locally (per device) and **follows** across new chats and restarts instead of snapping back to the default — pick a model once and the next `Cmd/Ctrl+N` opens on it. With a live chat, switching models scopes the change to that **current chat**; either way the selection rides along when the session is created/switched and is **never** written to the profile default — with one exception: on a fresh profile that has no `model.default`/`model.provider` configured yet, the first pick is persisted so the app has a real default instead of falling through to a stray API-key env var on restart. Persistence follows the same rule as `/model` (`model.persist_switch_by_default`); use **Settings → Model** to change the default deliberately. (Switching [profiles](#sessions--profiles) reseeds to that profile's own default.)

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
