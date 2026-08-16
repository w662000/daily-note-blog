---
layout: default
title: 技术点 · 5 模型测速：流式(stream) vs 推理(reasoning) 双对比报告
date: 2026-08-04 23:30:00 +0800
---

# 技术点 · 5 模型测速：流式(stream) vs 推理(reasoning) 双对比报告

> 来源：260804_5 模型测速：流式(stream) vs 推理(reasoning) 双对比报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260804_5 模型测速：流式(stream) vs 推理(reasoning) 双对比报告_handoff.md（编码探测：utf-8）
- | # | 模型 id | 厂商 | 配置 supportsReasoning |
- | 1 | `step-3.7-flash` | StepFun | 否（参数可能被服务端忽略） |
- | 2 | `glm-4.5-air` | GLM API | 否（参数可能被服务端忽略） |
- | 3 | `agnes-2.5-flash` | Agnes-AI | 否（参数可能被服务端忽略） |
- **不支持推理的 3 个模型（step-3.7-flash、glm-4.5-air、agnes-2.5-flash）**：`supportsReasoning=False`，服务端忽略 `reasoning_effort` 参数。对比② 的 tot 变化来自生成量随机性，**不能归因于推理**。
- **顺序偏差**：请求按 N0→S0→S1→N1 紧挨跑，S1 紧接 S0，可能命中服务端缓存，导致部分 S1 的 TTFT 异常偏低（如 `glm-4.5-air` S1=0.642s vs S0=6.601s；`deepseek-v4-flash` S1=1.266s vs S0=1.805s）。这会让「对比② 流式 S0→S1」的 TTFT 改善被高估——**读对比② 时优先看 tot（总耗时），TTFT 仅作参考**。
- **单次采样**：每组仅 1 次请求（遵守限流红线），未做多次平均；网络抖动会让 ±20% 内的差异不显著，仅看大趋势。
- *原始数据：`bench_5models_result.json` ｜ 测速脚本：`bench_5models.py` ｜ 本表由 `bench_report.py` 自动生成。*

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
