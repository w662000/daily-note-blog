---
layout: default
title: 交接文档 · Optional Skills
date: 2026-10-13 23:30:00 +0800
---

# Optional Skills

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\DESCRIPTION.md

Official skills maintained by Nous Research that are **not activated by default**.

These skills ship with the hermes-agent repository but are not copied to
`~/.hermes/skills/` during setup. They are discoverable via the Skills Hub:

```bash
hermes skills browse               # browse all skills, official shown first
hermes skills browse --source official  # browse only official optional skills
hermes skills search <query>       # finds optional skills labeled "official"
hermes skills install <identifier> # copies to ~/.hermes/skills/ and activates
```

## Why optional?

Some skills are useful but not broadly needed by every user:

- **Niche integrations** — specific paid services, specialized tools
- **Experimental features** — promising but not yet proven
- **Heavyweight dependencies** — require significant setup (API keys, installs)

By keeping them optional, we keep the default skill set lean while still
providing curated, tested, official skills for users who want them.
