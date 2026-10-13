---
layout: default
title: 交接文档 · Navigation _ Markdown campaign probe
date: 2026-10-13 23:30:00 +0800
---

# Navigation / Markdown campaign probe

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\evals\desktop_bug_campaign\navigation-markdown-README.md

See [markdown-README.md](markdown-README.md) for the maintained Markdown-only probe and commands. It mounts production Desktop Markdown components and CSS in isolated Chromium, inspects hard/soft breaks and highlighted code, and clicks the actual code-card Copy control before reading the browser clipboard. This is component-level live renderer evidence, not native Electron, navigation, backend transport, or macOS verification. No backend or model request is made.

The earlier combined notification fixture is retained in git history at `07a4da338bc`; async-report source changes belong to a separate lane.
