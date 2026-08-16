---
layout: default
title: 技术点 · 模型平台对比清单（按实际调用 Key / 端点归类）
date: 2026-07-31 23:30:00 +0800
---

# 技术点 · 模型平台对比清单（按实际调用 Key / 端点归类）

> 来源：260731_模型平台对比_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260731_模型平台对比_handoff.md（编码探测：utf-8）
- > 文档用途：汇总 WorkBuddy 当前 `models.json` 中**实际接入**的全部模型，按**你用来调用的 Key 和端点**归类，便于额度管理与并发控制。
- **归类原则**：以 `models.json` 中每个模型实际使用的 **API Key 和 endpoint** 为准，而不是模型原始提供方。
- 例：GLM-5.2 原始提供方是智谱，但你用 SenseNova Key 调用 → 归入商汤日日新。
- 例：Cohere North-Mini-Code 原始提供方是 Cohere，但你用 OpenRouter Key 调用 → 归入 OpenRouter。
- **额度 / 并发数**：取各平台公开免费额度或限速；未公开者标注「按 Key 限额」。
- | 平台名称 | 模型 | 类型 | 上下文 | 额度（免费层） | 并发数（RPM） |
- | 阶跃星辰 (StepFun) | Step-Image-Edit-2 | 文生图 | - | 同上 | 按 Key 限额 |
- | 商汤日日新 (SenseNova) | 6.7-Flash-Lite | 文本推理 | - | 按 Key 限额 | 约 10-60 RPM |
- | 智谱 AI (Zhipu/GLM) | GLM-4.5-Air | 文本推理 | - | 智谱 API 赠送额度 | 按 Key 限额 |
- | Agnes (Agnes-AI) | Image-2.1-Flash | 文生图 | - | 永久免费 | 按 Key 限额 |
- | Agnes (Agnes-AI) | Video-V2.0 | 视频生成 | - | 永久免费 | 按 Key 限额 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
