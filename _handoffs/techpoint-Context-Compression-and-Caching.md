---
layout: default
title: 技术点 · Context Compression and Caching
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Context Compression and Caching

> 来源：261010_Context Compression and Caching_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- `bedrock_confirmed_v1` map binds each confirmed key to its exact value in the
- same atomic write. Generic writes clear that key's provenance. Older writers
- profiles) is 500,000 tokens, per the
- This is Bedrock-specific, not the direct xAI API window. Existing compression
- yields 375,000 at this window, which the default `threshold_tokens` cap (256,000) then lowers.
- ```
context:
  engine: "compressor"    # default — built-in lossy summarization
  engine: "lcm"           # example — plugin providing lossless context
```
- Tracking token usage from API responses
- ```
                     ┌──────────────────────────┐
  Incoming message   │   Gateway Session Hygiene │  Fires at 85% of context
  ─────────────────► │   (pre-agent, rough est.) │  Safety net for large sessions
                     └─────────────┬────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │   Agent ContextCompressor │  Fires at 50% of context (default)
                     │   (in-loop, real tokens)  │  Normal context management
                     └──────────────────────────┘
```
- runs before the agent processes a message. It prevents API failures when sessions
- **Token source**: Prefers actual API-reported tokens from last turn, then the
- character-based estimate (`estimate_messages_tokens_rough`)
- API-reported token counts.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
