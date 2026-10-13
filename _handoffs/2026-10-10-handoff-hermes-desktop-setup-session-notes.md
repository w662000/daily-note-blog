---
layout: default
title: 交接文档 · Hermes Desktop Setup - Session Notes
date: 2026-10-13 23:30:00 +0800
---

# Hermes Desktop Setup - Session Notes

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\hermes-desktop-setup\references\session-notes.md

## Date
2026-08-05

## Problem
Hermes Desktop failed to launch with multiple errors:
1. Node.js not found in PATH
2. TypeScript compiler missing
3. npm lock file out of sync
4. Missing mermaid dependency
5. Electron build failures

## Environment
- **OS:** Windows 10 (x86_64)
- **Node.js:** v24.18.0 (from .meituan-catpaw)
- **npm:** 11.17.0
- **Hermes Agent:** v0.20.0
- **Desktop App:** v0.17.0

## Resolution
1. Set PATH to Node.js
2. Install TypeScript globally
3. Clean node_modules and reinstall
4. Install mermaid and electron
5. Build successfully
6. Run in dev mode on two terminals

## Key Insight
Always use `--legacy-peer-deps` flag when installing dependencies to avoid peer dependency conflicts.
