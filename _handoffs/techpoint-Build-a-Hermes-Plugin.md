---
layout: default
title: 技术点 · Build a Hermes Plugin
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Build a Hermes Plugin

> 来源：261010_Build a Hermes Plugin_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Hermes has several distinct pluggable interfaces — some use Python `register_*` APIs, others are config-driven or drop-in directories. Use this map first:
- | A **secret-manager backend** (vault / password manager / OS keystore) | [Secret Source Plugins](../secret-source-plugin.md) |
- | An **STT backend** (custom whisper / ASR CLI) | [Voice Message Transcription](../../user-guide/features/tts.md#voice-message-transcription-stt) — set `HERMES_LOCAL_STT_COMMAND` to an argv-tokenized template |
- ```
my-portable-plugin/
├── plugin.json
├── skills/
│   └── summarize/
│       ├── SKILL.md
│       └── references/
└── mcp.json
```
- ```
hermes plugins install owner/repository --no-enable
hermes plugins list
hermes plugins enable <plugin-name>
```
- one executable token with a separate argument list, never through a shell.
- from the discovered plugin key so sanitized names cannot collide. A portable
- records it as Published. Hermes keys behavior on the canonical v1.0.0 schema
- not by one global plugin API number. Hermes does not expose a
- `PLUGIN_API_VERSION`, require a manifest-wide `api:` match, or attach an API
- keyword-only. Existing return fields are not removed or silently retyped.
- **Hook payloads are keyword payloads.** New hook data is added as keyword

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
