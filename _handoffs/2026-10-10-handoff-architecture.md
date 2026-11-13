---
layout: default
title: 交接文档 · Architecture
date: 2026-10-13 23:30:00 +0800
---

# Architecture

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\software-development\code-wiki\templates\architecture.md

{% raw %}{{{% endraw %}TWO_TO_THREE_PARAGRAPHS_SHAPE_OF_SYSTEM}}

## Components

- **{% raw %}{{{% endraw %}COMPONENT_1}}** — {% raw %}{{{% endraw %}ONE_TO_TWO_SENTENCES}} See [`modules/{% raw %}{{{% endraw %}MODULE}}.md`](modules/{% raw %}{{{% endraw %}MODULE}}.md).
- **{% raw %}{{{% endraw %}COMPONENT_2}}** — {% raw %}{{{% endraw %}ONE_TO_TWO_SENTENCES}}

## System Diagram

```mermaid
flowchart TD
    User([User]) --> Entry[Entry Point]
    Entry --> Core[Core Engine]
    Core --> StorageA[(Database)]
    Core --> ExternalAPI{% raw %}{{{% endraw %}External API}}
```

## Data Flow

1. **{% raw %}{{{% endraw %}STEP_1}}** — [`{% raw %}{{{% endraw %}FILE}}`]({% raw %}{{{% endraw %}LINK}})
2. **{% raw %}{{{% endraw %}STEP_2}}** — [`{% raw %}{{{% endraw %}FILE}}`]({% raw %}{{{% endraw %}LINK}})
3. **{% raw %}{{{% endraw %}STEP_3}}** — [`{% raw %}{{{% endraw %}FILE}}`]({% raw %}{{{% endraw %}LINK}})

## Key Design Decisions

- {% raw %}{{{% endraw %}DECISION_1}}
- {% raw %}{{{% endraw %}DECISION_2}}
- {% raw %}{{{% endraw %}DECISION_3}}
