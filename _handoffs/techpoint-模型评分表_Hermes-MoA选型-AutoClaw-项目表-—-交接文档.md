---
layout: default
title: 技术点 · 模型评分表_Hermes-MoA选型（AutoClaw 项目表）— 交接文档
date: 2026-08-12 23:30:00 +0800
---

# 技术点 · 模型评分表_Hermes-MoA选型（AutoClaw 项目表）— 交接文档

> 来源：260812_autoclaw-模型评分表_Hermes-MoA选型_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260812_autoclaw-模型评分表_Hermes-MoA选型_handoff.md（编码探测：utf-8）
- | 2 | GLM-5.2-Coding (ZAI) | 智谱 ZAI | 文本/推理 | — | — | — | — | — | **90** | S | 中 | GLM-5.2 编码特化,1M 上下文 |
- | 4 | GLM-5.1 (赠送) | 智谱 GLM API | 文本 | — | 40 | — | 1321.4 | 72.5 | **89** | S | 高 | 智谱赠送旗舰 |
- | 8 | GLM-5 Turbo (赠送) | 智谱 GLM API | 文本 | — | — | — | — | — | **88** | S | 中 | 实测能力分 92.0 全场第一 |
- | 10 | GLM-5 | 智谱 GLM API | 文本 | — | 50 | — | 86.26 | 68.8 | **87** | S | 高 |  |
- | 14 | GLM-5V-Turbo (赠送) | 智谱 GLM API | 多模态 | — | — | — | — | — | **84** | A | 低 | 实测编程 94.0 |
- | 17 | step-router-v1 | 阶跃 StepFun | 文本 | — | — | — | — | — | **80** | A | 低 | 路由模型,实测被低估 |
- | 18 | GLM-4.7 | 智谱 GLM API | 文本 | 1443 | 42.1 | — | — | 58.09 | **80** | A | 高 |  |
- | 23 | GLM-4.6V | 智谱 GLM API | 多模态 | — | — | — | — | 37.2 | **78** | A | 高 |  |
- | 39 | GLM-4.6V-Flash (免费视觉) | 智谱 GLM API | 多模态 | — | — | — | — | — | **68** | B | 中 | 免费视觉,有 rate_limit |
- | 41 | GLM-4.7-Flash (赠送) | 智谱 GLM API | 文本 | — | — | — | — | — | **66** | B | 低 | 实测两题采集失败,实际应更高 |
- | 45 | GPT-OSS-120B (NIM) | NVIDIA NIM | 推理 | 1353 | 33 | — | — | — | **63** | B | 高 | 编码 60.2/数学 68.9 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
