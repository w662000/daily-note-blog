---
layout: default
title: 技术点 · Building a Memory Provider Plugin
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Building a Memory Provider Plugin

> 来源：261010_Building a Memory Provider Plugin_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
plugins/memory/my-provider/
├── __init__.py      # MemoryProvider implementation + register() entry point
├── plugin.yaml      # Metadata (name, description, hooks)
└── README.md        # Setup instructions, config reference, tools
```
- ```
[project.entry-points."hermes_agent.memory_providers"]
my-provider = "my_provider:register"
```
- ```
from agent.memory_provider import MemoryProvider

class MyMemoryProvider(MemoryProvider):
    @property
    def name(self) -> str:
        return "my-provider"

    def is_available(self) -> bool:
        """Check if this provider can activate. NO network calls."""
        return bool(os.environ.get("MY_API_KEY"))

    def initialize(self, session_id: str, **kwargs) -> None:
        """Called once at agent startup.

        kwargs always includes:
          hermes_home (str): Active HERMES_HOME path. Use for storage.
        """
        self._api_key = os.environ.get("MY_API_KEY", "")
        self._session_id = session_id

    # ... implement remaining methods
```
- | Keyword | Meaning |
- | `gateway_session_key` | Stable messaging-chat identity for per-chat session isolation. |
- | `prefetch(query, *, session_id="")` | Before each API call | Return recalled context |
- case the host offers an opt-in checkpoint contract (API v2):
- ```
from agent.memory_provider import MemoryProvider

class MyArchivingProvider(MemoryProvider):
    # Opt in: every successful on_pre_compress() return means the durable
    # checkpoint is committed. Raise on any failure — do not return partial
    # success. Version 1 (the inherited default) is the implicit historical
    # contract: best-effort semantics, raw message list.
    pre_compress_checkpoint_api_version = 2

    def on_pre_compress(self, messages, *, require_checkpoint=False):
        # require_checkpoint mirrors the operator's checkpoint_required
        # setting: True means a raise here blocks the lossy rewrite.
        ids = self._archive(messages)   # must be durable before returning
        return f"checkpoint: {ids}"     # forwarded into the summary prompt
```
- ```
compression:
  checkpoint_required: true   # default: false
```
- an active provider advertising the API completed its checkpoint: the
- None of the providers bundled with Hermes advertise checkpoint API v2 — the
- and each refusal names `compression.checkpoint_required` as the key to disable.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
