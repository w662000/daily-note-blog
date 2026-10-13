---
layout: default
title: 交接文档 · Architecture
date: 2026-10-13 23:30:00 +0800
---

# Architecture

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\software-development\code-wiki\templates\architecture.md

{{TWO_TO_THREE_PARAGRAPHS_SHAPE_OF_SYSTEM}}

## Components

- **{{COMPONENT_1}}** — {{ONE_TO_TWO_SENTENCES}} See [`modules/{{MODULE}}.md`](modules/{{MODULE}}.md).
- **{{COMPONENT_2}}** — {{ONE_TO_TWO_SENTENCES}}

## System Diagram

```mermaid
flowchart TD
    User([User]) --> Entry[Entry Point]
    Entry --> Core[Core Engine]
    Core --> StorageA[(Database)]
    Core --> ExternalAPI{{External API}}
```

## Data Flow

1. **{{STEP_1}}** — [`{{FILE}}`]({{LINK}})
2. **{{STEP_2}}** — [`{{FILE}}`]({{LINK}})
3. **{{STEP_3}}** — [`{{FILE}}`]({{LINK}})

## Key Design Decisions

- {{DECISION_1}}
- {{DECISION_2}}
- {{DECISION_3}}
