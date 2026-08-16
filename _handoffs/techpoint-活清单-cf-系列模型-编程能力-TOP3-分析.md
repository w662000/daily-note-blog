---
layout: default
title: 技术点 · 活清单 cf 系列模型「编程能力」TOP3 分析
date: 2026-08-16 23:30:00 +0800
---

# 技术点 · 活清单 cf 系列模型「编程能力」TOP3 分析

> 来源：260816_活清单 cf 系列模型「编程能力」TOP3 分析_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 1. **gemma-4-26b-a4b-it**：LiveCodeBench 77.1 是 12 个 cf 里最高的，且有 Codeforces ELO 1718（竞赛级）、τ2-bench 68.2；内部实测 Q4（列表删除 bug 修复）真实跑通拿 92 分，是"基准分高 + 实战能跑"双保险，毫无争议第一。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
- **HumanEval 虚高陷阱**：`deepseek-r1-distill-qwen-32b` HumanEval 94.8、`llama-3.3-70b` 88.4 看着很猛，但它们的 LiveCodeBench 只有 27.0 / 28.8。HumanEval 是老基准（给定函数签名补完），这两模型擅长"填空"但不擅长"从零解竞赛题"，**别被 HE 高分骗去当编程主力**。
- **数据缺失不能瞎排**：`glm-4.7-flash`（综合 72）、`gpt-oss-120b`（综合 74）在活清单里**没有任何 HumanEval/LiveCodeBench/Codeforces 字段**，只有综合分。尤其 gpt-oss-120b 真实世界编程很强（AA 称其为"开源第一梯队 + 速度第一 270 tok/s"），但活清单没采到数据，本文**不凭印象给它排名**，仅如实标注"活清单内无法比较编程名次"。
