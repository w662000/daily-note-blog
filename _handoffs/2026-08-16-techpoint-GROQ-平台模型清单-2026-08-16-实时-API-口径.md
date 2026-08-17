---
layout: default
title: 技术点 · GROQ 平台模型清单（2026-08-16 实时 API 口径）
date: 2026-08-16 23:30:00 +0800
---

# 技术点 · GROQ 平台模型清单（2026-08-16 实时 API 口径）

> 来源：260816_GROQ 平台模型清单（2026-08-16 实时 API 口径）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 来源：GROQ 实时 API `GET https://api.groq.com/openai/v1/models`（用 models.json 中 [Groq] 模型自带 apiKey 调用，HTTP 200）
- 可信度：最高（官方实时 API，非文档页）
- 教训：文档页（console.groq.com/docs/models）≠ 实时 API 列表。本次实测：
- 文档页有 `minimaxai/minimax-m2.7`，但实时 API 已无返回（疑似下架/改名）
- 实时 API 有 `allam-2-7b`，文档页未列出（文档滞后）
- 1. allam-2-7b                          ← API 独有，文档页无
- 已接雷达（models.json 中 4 个，均自带 apiKey + url=https://api.groq.com/openai/v1）：
- （文档页有但 API 已无：minimaxai/minimax-m2.7，无需接入）

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
