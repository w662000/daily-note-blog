---
layout: default
title: 交接文档 · memos-local-plugin — runtime data
date: 2026-10-13 23:30:00 +0800
---

# memos-local-plugin — runtime data

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\Local_hermes\memos-plugin\templates\README.user.md

This directory holds **your** memory data and configuration. The plugin's
source code lives somewhere else (typically under `~/.<agent>/plugins/…/`) and
can be uninstalled or upgraded freely without touching anything here.

## What's in here

```
config.yaml      # all configuration (including API keys); chmod 600
data/            # SQLite database, vector blobs
skills/          # crystallized skill packages (one per directory)
logs/            # rotating logs (memos.log, error.log, audit.log, llm.jsonl, perf.jsonl, events.jsonl)
daemon/          # bridge pid/port files (auto-managed)
```

## Editing your config

Open `config.yaml` in any editor. The viewer's *Settings* page can also write
back to this file; it preserves comments and field order.

API keys go directly inside `config.yaml`. The file is created with `chmod 600`
so only your user can read it.

## Resetting

- **Lose everything**: delete this whole directory. The next time you start
  your agent, it will be recreated empty.
- **Lose only memory, keep config**: delete `data/` and `skills/`.
- **Lose only logs**: delete the contents of `logs/`. Audit logs are gzipped,
  not deleted, so keeping them around forever is the default.

## Multiple agents on the same machine

Each agent has its own home directory (e.g. `~/.openclaw/memos-plugin/` and
`~/.hermes/memos-plugin/`). They never share data unless you explicitly
configure team sharing in `config.yaml`'s `hub:` section.

## Need help?

- User docs:   open the viewer's *Help* link.
- Bug reports: include `logs/error.log` and the relevant slice of
                `logs/events.jsonl`.
