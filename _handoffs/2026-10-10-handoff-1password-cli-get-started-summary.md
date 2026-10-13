---
layout: default
title: 交接文档 · 1Password CLI get-started (summary)
date: 2026-10-13 23:30:00 +0800
---

# 1Password CLI get-started (summary)

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\security\1password\references\get-started.md

Official docs: https://developer.1password.com/docs/cli/get-started/

## Core flow

1. Install `op` CLI.
2. Enable desktop app integration in 1Password app.
3. Unlock app.
4. Run `op signin` and approve prompt.
5. Verify with `op whoami`.

## Multiple accounts

- Use `op signin --account <subdomain.1password.com>`
- Or set `OP_ACCOUNT`

## Non-interactive / automation

- Use service accounts and `OP_SERVICE_ACCOUNT_TOKEN`
- Prefer `op run` and `op inject` for runtime secret handling
