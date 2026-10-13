---
layout: default
title: 技术点 · Micro-compaction
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Micro-compaction

> 来源：261010_Micro-compaction_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- message. In tool-heavy work that's where the bulk of the tokens live — a
- floor. If you routinely paste 10–20K-token prompts, that weight stays in context
- **The tail** — a token-budgeted window of the most recent messages, so
- than the material justifies. When the running summary crosses a token threshold
- ```
compression:
  micro_compact: true             # default: false
  micro_compact_every_n_turns: 1  # cadence — how often a pass runs
  micro_compact_defrag_threshold_tokens: 2000
```
- `micro_compact_defrag_threshold_tokens` is when the rolling summary gets
- input tokens are billed at a fraction of uncached ones. That discount survives
- itself behind `compression.proactive_prune_min_reclaim_tokens` (4096 by
- ```
auxiliary:
  compression:
    provider: openai-api
    model: <your choice>
    base_url: <endpoint>
```
- (a few thousand tokens) but the call happens **every turn**, at the end of the
- mechanical work. A thinking model will spend reasoning tokens on it and be
- | large MoE reasoning model, remote GPU | noticeably slower still — thinking tokens on a summarisation task |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
