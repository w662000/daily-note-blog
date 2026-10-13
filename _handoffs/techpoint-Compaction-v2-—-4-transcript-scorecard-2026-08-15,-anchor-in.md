---
layout: default
title: 技术点 · Compaction v2 — 4-transcript scorecard (2026-08-15, anchor-index build)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Compaction v2 — 4-transcript scorecard (2026-08-15, anchor-index build)

> 来源：261010_Compaction v2 — 4-transcript scorecard (2026-08-15, anchor-i_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Four real 500K-token lineage transcripts from state.db (sweep campaign, GUI
- FEWER TOKENS (49K vs 162K). It wins on 3 of 4 transcripts and loses only
- policy quality. Current's average is 45.8% for 162K tokens — lean+recovery
- 1.1M-token lineage truncated at 500K, dense multi-PR state. Recovery
- (+22.5pts at 0.30x tokens).
- | policy | recall | tokens before | tokens after | compress s |
- 12. **What was the GraphQL API rate limit remaining for the user when the 'API rate limit already exceeded' error first occurred?**
- 13. **Which PR was identified as the salvage of HexLab98's #85283 to fix hung inline API calls?**
- gold: `.env is for secrets only (API keys, tokens, passwords). All behavioral settings... go in config.yaml.`
- 1. **Which PR number added the public subagent lifecycle API?**
- 3. **How many contract and security tests were included with the subagent lifecycle API PR?**
- 5. **Which PR implements gateway-safe plugin injection by extending `ctx.inject_message()` with a keyword-only `session_key`?**

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
