---
layout: default
title: 交接文档 · 活清单 cf 系列模型「编程能力」TOP3 分析
date: 2026-08-16 23:30:00 +0800
---

# 活清单 cf 系列模型「编程能力」TOP3 分析

- **日期**：2026-08-16
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-16-10-57-55\cf系列编程能力_TOP3_20260816.md

> 数据来源：活清单 `model-speed-radar/model_scores_merged.json`（共 74 个模型，其中 `@cf/` 前缀 12 个，均为 Cloudflare Workers AI 托管）。
> 分析口径：以 **LiveCodeBench**（近期代码竞赛基准，最难、区分度最好、最贴近真实编程）为主排序依据；HumanEval 仅作旁证（老基准易被刷到 90+）；辅以项目内部「真实运行验证」的编程实测题 Q3/Q4。
> 可信度：基准分来源为 Google 官方模型卡 / Artificial Analysis / madebyagents / benched.ai / IBM 官方等（活清单已逐条标注 src，T1 级）；Q3/Q4 为项目内部真测（提取代码跑基准用例，T1 级）。

## 一、结论（先给）

活清单 cf 系列共 12 个模型。**按最权威编程基准 LiveCodeBench 严格排序，编程能力 TOP3：**

| 排名 | 模型 id | LiveCodeBench | 综合分 | 一句话定位 |
| ---: | --- | ---: | ---: | --- |
| 🥇 1 | `@cf/google/gemma-4-26b-a4b-it` | **77.1** | 80 | cf 编程天花板，竞赛+实战双高 |
| 🥈 2 | `@cf/qwen/qwen3-30b-a3b-fp8` | **70.7** | 63 | 小参数高性价比，Q3 实战跑通 |
| 🥉 3 | `@cf/qwen/qwq-32b` | **63.1** | 62 | 推理型，竞赛分稳 |

> 第 3 名存在争议：并列候选 `@cf/nvidia/nemotron-3-120b-a12b`（LCB 60.0，但 **AA Coding Index 37.7 全场最高**、综合分 73 也更高），详见第三节。

## 二、12 个 cf 模型完整编程指标（活清单内全量）

| 模型 | 类型 | 综合 | HumanEval | LiveCodeBench | AA Coding Index | 其他编程硬指标 | Q3实测 | Q4实测 |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| @cf/google/gemma-4-26b-a4b-it | 多模态 | 80 | — | **77.1** | — | Codeforces ELO 1718；τ2-bench 68.2；BigBench EH 64.8 | 66 | 92 |
| @cf/qwen/qwen3-30b-a3b-fp8 | 文本 | 63 | — | **70.7** | — | — | 88(运行通过) | 22(没看出bug) |
| @cf/qwen/qwq-32b | 推理 | 62 | — | **63.1** | — | IFEval 83.9 | — | — |
| @cf/nvidia/nemotron-3-120b-a12b | 推理 | 73 | — | 60.0 | **37.7(最高)** | Terminal-Bench 28.8；τ2 67.8 | — | — |
| @cf/meta/llama-4-scout-17b-16e-instruct | 多模态 | 59 | — | 32.8 | — | τ-bench 62.3 | — | — |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | 文本 | 58 | 88.4 | 28.8 | — | IFEval 92.1 | — | — |
| @cf/deepseek-ai/deepseek-r1-distill-qwen-32b | 推理 | 60 | **94.8** | 27.0 | — | — | — | — |
| @cf/mistralai/mistral-small-3.1-24b-instruct | 多模态 | 54 | — | 21.2 | 26.3 | — | — | — |
| @cf/ibm-granite/granite-4.0-h-micro | 文本 | 38 | 81.0 | — | — | IFEval 84.32 | — | — |
| @cf/zai-org/glm-4.7-flash | 推理 | 72 | — | —(缺) | — | Terminal-Bench 22.0；SciCode 33.7；τ2 98.8；IFBench 60.8 | — | — |
| @cf/openai/gpt-oss-120b | 推理 | 74 | — | —(缺) | — | （活清单未采到任何编程基准，仅 LMArena 1365 + AA 24） | — | — |
| @cf/moondream/moondream3.1-9B-A2B | 视觉 | 68 | — | —(缺) | — | CountBench 90.35(计数，非编程) | — | — |

## 三、为什么是这 3 个（大白话解释）

1. **gemma-4-26b-a4b-it**：LiveCodeBench 77.1 是 12 个 cf 里最高的，且有 Codeforces ELO 1718（竞赛级）、τ2-bench 68.2；内部实测 Q4（列表删除 bug 修复）真实跑通拿 92 分，是"基准分高 + 实战能跑"双保险，毫无争议第一。
2. **qwen3-30b-a3b-fp8**：LiveCodeBench 70.7 第二；内部实测 Q3（线程安全 LRU 缓存）真实运行通过拿 88。唯一短板是 Q4 翻车（22，始终没识别出"遍历中改列表漏删"的 bug）——说明它**不稳定但不弱**，硬指标仍稳居第二。
3. **qwq-32b**：LiveCodeBench 63.1 第三，是纯推理模型，竞赛分扎实。

**第 3 名争议点**：`@cf/nvidia/nemotron-3-120b-a12b` 的 LiveCodeBench（60.0）略低于 qwq（63.1），但它是 120B 大模型、综合分 73 更高、且 **AA Coding Index 37.7 是 12 个 cf 里最高**（专门衡量代码能力的指标）。如果你更看重"代码专项 index + 大模型综合"，可以把 nemotron 顶替 qwq 当第 3。两者 LiveCodeBench 差距仅 3 分，基本同一梯队。

## 四、两个必须避开的"坑"（诚实提醒）

- **HumanEval 虚高陷阱**：`deepseek-r1-distill-qwen-32b` HumanEval 94.8、`llama-3.3-70b` 88.4 看着很猛，但它们的 LiveCodeBench 只有 27.0 / 28.8。HumanEval 是老基准（给定函数签名补完），这两模型擅长"填空"但不擅长"从零解竞赛题"，**别被 HE 高分骗去当编程主力**。
- **数据缺失不能瞎排**：`glm-4.7-flash`（综合 72）、`gpt-oss-120b`（综合 74）在活清单里**没有任何 HumanEval/LiveCodeBench/Codeforces 字段**，只有综合分。尤其 gpt-oss-120b 真实世界编程很强（AA 称其为"开源第一梯队 + 速度第一 270 tok/s"），但活清单没采到数据，本文**不凭印象给它排名**，仅如实标注"活清单内无法比较编程名次"。

## 五、最终建议

- 要 cf 上**最能打代码**的：直接上 **gemma-4-26b-a4b-it**。
- 要**省钱/小模型高性价比**：**qwen3-30b-a3b-fp8**（但注意它偶尔会犯低级 bug，关键代码要 review）。
- 第 3 顺位在 **qwq-32b（竞赛分稳）** 与 **nemotron-3-120b（代码专项 index 最高、综合更强）** 间二选一，看你要"小模型"还是"大模型全能"。
