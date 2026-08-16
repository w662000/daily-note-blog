---
layout: default
title: 交接文档 · 活清单各供应方「编程最适用」TOP3 + 多轮测速 + 测限流 总表
date: 2026-08-16 23:30:00 +0800
---

> 来源：2026-08-16-10-57-55\各供应方编程TOP3_测速_限流_总表_20260816.md
> 由用户显式指定放入 handoff 收件箱，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# 活清单各供应方「编程最适用」TOP3 + 多轮测速 + 测限流 总表

> 生成：2026-08-16。数据源：①编程能力 `model-speed-radar/model_scores_merged.json`(74模型)；②多轮测速 `model-speed-radar/data/history.jsonl`(**102轮**, 轮2–102)；③测限流 `C:/Users/Administrator/.cache/rate-limit-radar/data/history.jsonl`(**12轮×每轮15测=180次/模型**, 08-05→08-15)。

## 评定方法（先讲清楚，避免被误导）

- **编程排名按「基准难度分层」而非单一数字**：Tier1(最难/最可比代码生成)=LiveCodeBench、SWE-bench V；Tier2(真实SWE/agentic)=FrontierSWE、SWE-Bench PRO、Terminal-Bench；Tier3(旧基准/异量纲)=HumanEval、Codeforces ELO、Tau-bench、AA Coding；Tier4(仅内部真跑)=Q3/Q4。同层才比数字，跨层 Tier 高者永远排前（即「有 LiveCodeBench 的」必排在「只有 HumanEval 的」前面，不管 HumanEval 数字多大）。
- **绝不把 HumanEval(老·函数填空) 与 LiveCodeBench(近期竞赛·难) 当同一数轴比**——这是上一轮踩过的坑，已修。
- **可信度**：编程分来自 Google 模型卡/Artificial Analysis/madebyagents/benched.ai/IBM 等（活清单逐条标 src）；Q3/Q4 为项目真跑代码跑基准用例；测速/限流为真实轮次记录。凡活清单缺字段的，表中标「—」不推断。

## 总览（每个供应方 TOP3）

| 供应方 | # | 模型 | 编程代表分(基准·层) | 综合/可信 | 测速TTFT中位·均值·成功率 | 测速等级 | 限流被限次数(轮) | 限流成功率 | 限流avg_ms |
|---|---|---|---|---|---|---|---|---|---|
| GLM API | 1 | `glm-4.7` | 84.9(LiveCodeBench·T1) | 80/高 | 3659·3676·16% | A:1/B:9/C:85/S:1 | 1(1轮) | 50% | 6251 |
| GLM API | 2 | `glm-5` | 77.8(SWE-bench V·T1) | 87/高 | 3518·3477·9% | B:9/C:87 | 0(0轮) | 55% | 4207 |
| GLM API | 3 | `glm-4.5-air` | 68.4(LiveCodeBench·T1) | 62/高 | 755·1054·82% | A:4/B:3/C:20/S:69 | 0(0轮) | 91% | 893 |
| Cloudflare | 1 | `@cf/google/gemma-4-26b-a4b-it` | 77.1(LiveCodeBench·T1) | 80/高 | 1289·1834·93% | A:31/B:16/C:12/S:38 | 0(0轮) | 96% | 2230 |
| Cloudflare | 2 | `@cf/qwen/qwen3-30b-a3b-fp8` | 70.7(LiveCodeBench·T1) | 63/高 | 1158·1480·97% | A:33/B:11/C:4/S:49 | 0(0轮) | 97% | 1954 |
| Cloudflare | 3 | `@cf/qwen/qwq-32b` | 63.1(LiveCodeBench·T1) | 62/高 | 1450·1852·91% | A:42/B:8/C:15/S:32 | 0(0轮) | 98% | 2252 |
| StepFun | 1 | `step-3.5-flash` | 86.4(LiveCodeBench·T1) | 78/高 | 604·640·100% | A:2/S:92 | 4(4轮) | 98% | 907 |
| StepFun | 2 | `step-3.7-flash` | 63.7(LiveCodeBench·T1) | 76/高 | 671·775·97% | A:5/C:4/S:86 | 0(0轮) | 90% | 690 |
| StepFun | 3 | `step-router-v1` | 90.0(Q3真跑·T4) | 80/低 | 1106·1693·98% | A:24/B:2/C:11/S:57 | 6(6轮) | 96% | 662 |
| OpenRouter | 1 | `nvidia/nemotron-3-ultra-550b-a55b:free` | 89.0(LiveCodeBench·T1) | 78/高 | 1872·3841·35% | A:10/B:9/C:74/S:8 | 180(12轮) | 0% | — |
| OpenRouter | 2 | `cohere/north-mini-code:free` | 80.2(SWE-bench V·T1) | 54/中 | 1980·2278·37% | A:18/B:7/C:68/S:8 | 180(12轮) | 0% | — |
| OpenRouter | 3 | `google/gemma-4-31b-it:free` | 80.0(LiveCodeBench·T1) | 73/高 | 2057·2057·2% | A:2/C:95 | 148(11轮) | 0% | — |
| NVIDIA NIM | 1 | `openai/gpt-oss-120b` | 87.8(LiveCodeBench·T1) | 63/高 | 814·1310·92% | A:21/B:8/C:10/S:62 | 0(0轮) | 88% | 1002 |
| NVIDIA NIM | 2 | `google/gemma-4-31b-it` | 80.0(LiveCodeBench·T1) | 78/高 | 3219·4481·50% | A:15/B:13/C:71/S:2 | 0(0轮) | 79% | 5575 |
| NVIDIA NIM | 3 | `thinkingmachines/inkling` | 77.6(SWE-bench V·T1) | 82/中 | 1754·3293·60% | A:24/B:8/C:52/S:17 | 25(9轮) | 84% | 2073 |
| Agnes-AI | 1 | `agnes-2.5-pro` | 82.7(SWE-bench V·T1) | 80/中 | 768·1139·94% | A:3/B:4/C:10/S:79 | 0(0轮) | 96% | 725 |
| Agnes-AI | 2 | `agnes-2.5-flash` | 75.8(SWE-bench V·T1) | 70/中 | 516·1147·83% | A:4/B:4/C:23/S:70 | 0(0轮) | 100% | 799 |
| Agnes-AI | 3 | `agnes-2.0-flash` | 72.4(SWE-bench V·T1) | 63/中 | 492·992·85% | A:5/B:1/C:19/S:71 | 0(0轮) | 99% | 882 |
| HF | 1 | `moonshotai/Kimi-K2-Instruct` | 65.8(SWE-bench V·T1) | 78/高 | 1743·1909·54% | A:43/B:6/C:46/S:4 | 0(0轮) | 50% | 4044 |
| HF | 2 | `Qwen/Qwen3-VL-30B-A3B-Instruct` | 42.6(LiveCodeBench·T1) | 72/中 | 1635·2183·35% | A:21/B:4/C:68/S:6 | 0(0轮) | 39% | 2415 |
| HF | 3 | `Qwen/Qwen3-4B-Instruct-2507` | 35.1(LiveCodeBench·T1) | 60/中 | 1332·1546·61% | A:35/B:6/C:39/S:19 | 0(0轮) | 32% | 1668 |
| SenseNova | 1 | `deepseek-v4-flash` | 91.6(LiveCodeBench·T1) | 89/高 | 1848·1920·93% | A:83/B:7/C:8/S:3 | 43(12轮) | 76% | 1508 |
| SenseNova | 2 | `glm-5.2` | 62.1(SWE-bench V·T1) | 91/高 | 2004·2167·71% | A:59/B:8/C:33/S:2 | 79(12轮) | 49% | 1475 |
| SenseNova | 3 | `sensenova-6.7-flash-lite` | —(无代码生成基准·T9) | 72/中 | 1272·2386·95% | A:28/B:7/C:23/S:43 | 0(0轮) | 0% | — |
| Gemini | 1 | `gemini-3.1-flash-lite` | 72.0(LiveCodeBench·T1) | 76/高 | 1687·2083·31% | A:22/B:3/C:73/S:3 | 0(0轮) | 34% | 1955 |
| Gemini | 2 | `gemini-3.6-flash` | 58.7(SWE-bench V·T1) | 86/高 | 2001·2588·30% | A:23/B:5/C:73 | 53(9轮) | 1% | 1538 |
| Gemini | 3 | `gemini-flash-latest` | 95.3(Tau-bench·T3) | 86/高 | 2312·3026·16% | A:10/B:4/C:87 | 84(10轮) | 0% | — |
| Groq | 1 | `llama-3.1-8b-instant` | 11.6(LiveCodeBench·T1) | 32/高 | 1398·1851·24% | A:8/B:5/C:77/S:9 | 0(0轮) | 38% | 2092 |

## 各供应方明细（含全部编程基准 + 最近测速/限流状态）

### 供应方 [GLM API]（活清单共 13 个模型）
**#1 `glm-4.7`** — [GLM API] GLM-4.7
- 编程：代表分 **84.9**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=84.9 SWE-bench V=73.8 Tau-bench=87.4；Q3真跑=0 Q4真跑=30；综合=80 可信=高 类型=文本
- 多轮测速(96轮)：成功率15.6% ｜ TTFT 中位3659/均值3676/最大6576ms ｜ 总耗时均值9924ms ｜ 等级{'C': 85, 'B': 9, 'S': 1, 'A': 1} ｜ 失败类型{'no_quota': 13, 'cooldown': 21, 'slow_cooldown': 46, 'rate_limit': 1}
- 测限流(11轮×15测=165次)：被限流 **1 次**（涉及 1 轮）｜ 其他错误 82 次 ｜ 成功率 49.7% ｜ avg_ms 6251 ｜ 末轮等级 A

**#2 `glm-5`** — [GLM API] GLM-5
- 编程：代表分 **77.8**（SWE-bench V·Tier1）；全部基准：SWE-bench V=77.8 Terminal-Bench=56.2 Tau-bench=89.7；Q3真跑=93 Q4真跑=95；综合=87 可信=高 类型=文本
- 多轮测速(96轮)：成功率9.4% ｜ TTFT 中位3518/均值3477/最大3671ms ｜ 总耗时均值12025ms ｜ 等级{'C': 87, 'B': 9} ｜ 失败类型{'no_quota': 13, 'cooldown': 19, 'slow_cooldown': 55}
- 测限流(11轮×15测=165次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 75 次 ｜ 成功率 54.5% ｜ avg_ms 4207 ｜ 末轮等级 A

**#3 `glm-4.5-air`** — [GLM API] GLM-4.5-Air (赠送)
- 编程：代表分 **68.4**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=68.4；Q3真跑=92 Q4真跑=48；综合=62 可信=高 类型=文本
- 多轮测速(96轮)：成功率82.3% ｜ TTFT 中位755/均值1054/最大7453ms ｜ 总耗时均值2024ms ｜ 等级{'C': 20, 'S': 69, 'B': 3, 'A': 4} ｜ 失败类型{'no_quota': 8, 'cooldown': 7, 'timeout': 2}
- 测限流(11轮×15测=165次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 15 次 ｜ 成功率 90.9% ｜ avg_ms 893 ｜ 末轮等级 A


### 供应方 [Cloudflare]（活清单共 12 个模型）
**#1 `@cf/google/gemma-4-26b-a4b-it`** — [Cloudflare] gemma-4-26b-a4b-it
- 编程：代表分 **77.1**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=77.1 Codeforces ELO=1718.0 Tau-bench=68.2；Q3真跑=66 Q4真跑=92；综合=80 可信=高 类型=多模态
- 多轮测速(97轮)：成功率92.8% ｜ TTFT 中位1289/均值1834/最大8586ms ｜ 总耗时均值2513ms ｜ 等级{'A': 31, 'S': 38, 'C': 12, 'B': 16} ｜ 失败类型{'network': 3, 'http_5xx': 2, 'cooldown': 2}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 8 次 ｜ 成功率 95.6% ｜ avg_ms 2230 ｜ 末轮等级 A

**#2 `@cf/qwen/qwen3-30b-a3b-fp8`** — [Cloudflare] qwen3-30b-a3b-fp8
- 编程：代表分 **70.7**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=70.7；Q3真跑=88 Q4真跑=22；综合=63 可信=高 类型=文本
- 多轮测速(97轮)：成功率96.9% ｜ TTFT 中位1158/均值1480/最大6583ms ｜ 总耗时均值2199ms ｜ 等级{'S': 49, 'B': 11, 'A': 33, 'C': 4} ｜ 失败类型{'network': 3}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 5 次 ｜ 成功率 97.2% ｜ avg_ms 1954 ｜ 末轮等级 S

**#3 `@cf/qwen/qwq-32b`** — [Cloudflare] qwq-32b
- 编程：代表分 **63.1**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=63.1；Q3真跑=None Q4真跑=None；综合=62 可信=高 类型=推理
- 多轮测速(97轮)：成功率90.7% ｜ TTFT 中位1450/均值1852/最大8664ms ｜ 总耗时均值3470ms ｜ 等级{'A': 42, 'S': 32, 'B': 8, 'C': 15} ｜ 失败类型{'network': 6, 'empty': 1, 'stream': 2}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 3 次 ｜ 成功率 98.3% ｜ avg_ms 2252 ｜ 末轮等级 S


### 供应方 [StepFun]（活清单共 12 个模型）
**#1 `step-3.5-flash`** — [StepFun] step-3.5-flash
- 编程：代表分 **86.4**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=86.4 SWE-bench V=74.4 Terminal-Bench=51.0 AA Coding=31.6 Tau-bench=88.2；Q3真跑=68 Q4真跑=93；综合=78 可信=高 类型=文本
- 多轮测速(94轮)：成功率100.0% ｜ TTFT 中位604/均值640/最大2332ms ｜ 总耗时均值1127ms ｜ 等级{'S': 92, 'A': 2}
- 测限流(11轮×15测=165次)：被限流 **4 次**（涉及 4 轮）｜ 其他错误 0 次 ｜ 成功率 97.6% ｜ avg_ms 907 ｜ 末轮等级 B

**#2 `step-3.7-flash`** — [StepFun] Step-3.7-Flash (step_plan 订阅)
- 编程：代表分 **63.7**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=63.7 Terminal-Bench=35.6 AA Coding=39.6 Tau-bench=98.5；Q3真跑=90 Q4真跑=92；综合=76 可信=高 类型=多模态
- 多轮测速(95轮)：成功率96.8% ｜ TTFT 中位671/均值775/最大4722ms ｜ 总耗时均值1276ms ｜ 等级{'S': 86, 'A': 5, 'C': 4} ｜ 失败类型{'http_4xx': 3}
- 测限流(11轮×15测=165次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 16 次 ｜ 成功率 90.3% ｜ avg_ms 690 ｜ 末轮等级 A

**#3 `step-router-v1`** — [StepFun] step-router-v1
- 编程：代表分 **90.0**（Q3真跑·Tier4）；全部基准：无第三方基准；Q3真跑=90 Q4真跑=88；综合=80 可信=低 类型=文本
- 多轮测速(94轮)：成功率97.9% ｜ TTFT 中位1106/均值1693/最大9885ms ｜ 总耗时均值1694ms ｜ 等级{'S': 57, 'A': 24, 'C': 11, 'B': 2} ｜ 失败类型{'timeout': 2}
- 测限流(11轮×15测=165次)：被限流 **6 次**（涉及 6 轮）｜ 其他错误 0 次 ｜ 成功率 96.3% ｜ avg_ms 662 ｜ 末轮等级 B


### 供应方 [OpenRouter]（活清单共 11 个模型）
**#1 `nvidia/nemotron-3-ultra-550b-a55b:free`** — [OpenRouter] Nemotron Ultra 550B (免费)
- 编程：代表分 **89.0**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=89.0 SWE-bench V=71.9；Q3真跑=None Q4真跑=None；综合=78 可信=高 类型=推理
- 多轮测速(101轮)：成功率34.7% ｜ TTFT 中位1872/均值3841/最大20721ms ｜ 总耗时均值5648ms ｜ 等级{'B': 9, 'C': 74, 'A': 10, 'S': 8} ｜ 失败类型{'rate_limit': 26, 'cooldown': 33, 'network': 5, 'model_gone': 1, 'timeout': 1}
- 测限流(12轮×15测=180次)：被限流 **180 次**（涉及 12 轮）｜ 其他错误 0 次 ｜ 成功率 0.0% ｜ avg_ms — ｜ 末轮等级 C

**#2 `cohere/north-mini-code:free`** — [OpenRouter] North Mini Code (免费)
- 编程：代表分 **80.2**（SWE-bench V·Tier1）；全部基准：SWE-bench V=80.2；Q3真跑=None Q4真跑=None；综合=54 可信=中 类型=文本
- 多轮测速(101轮)：成功率36.6% ｜ TTFT 中位1980/均值2278/最大6345ms ｜ 总耗时均值5443ms ｜ 等级{'C': 68, 'A': 18, 'B': 7, 'S': 8} ｜ 失败类型{'rate_limit': 26, 'cooldown': 33, 'network': 5}
- 测限流(12轮×15测=180次)：被限流 **180 次**（涉及 12 轮）｜ 其他错误 0 次 ｜ 成功率 0.0% ｜ avg_ms — ｜ 末轮等级 C

**#3 `google/gemma-4-31b-it:free`** — [OpenRouter] Gemma 4 31B (免费)
- 编程：代表分 **80.0**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=80.0 Codeforces ELO=2150.0；Q3真跑=None Q4真跑=None；综合=73 可信=高 类型=多模态
- 多轮测速(97轮)：成功率2.1% ｜ TTFT 中位2057/均值2057/最大2331ms ｜ 总耗时均值2058ms ｜ 等级{'C': 95, 'A': 2} ｜ 失败类型{'rate_limit': 41, 'cooldown': 51, 'network': 3}
- 测限流(11轮×15测=165次)：被限流 **148 次**（涉及 11 轮）｜ 其他错误 17 次 ｜ 成功率 0.0% ｜ avg_ms — ｜ 末轮等级 C


### 供应方 [NVIDIA NIM]（活清单共 7 个模型）
**#1 `openai/gpt-oss-120b`** — [NVIDIA NIM] GPT-OSS 120B ⚡(推理)
- 编程：代表分 **87.8**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=87.8 SWE-bench V=26.0；Q3真跑=None Q4真跑=None；综合=63 可信=高 类型=文本|推理
- 多轮测速(101轮)：成功率92.1% ｜ TTFT 中位814/均值1310/最大11005ms ｜ 总耗时均值1600ms ｜ 等级{'A': 21, 'S': 62, 'C': 10, 'B': 8} ｜ 失败类型{'network': 4, 'timeout': 4}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 21 次 ｜ 成功率 88.3% ｜ avg_ms 1002 ｜ 末轮等级 A

**#2 `google/gemma-4-31b-it`** — [NVIDIA NIM] Gemma-4-31B ⚡(NVIDIA直连)
- 编程：代表分 **80.0**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=80.0 Codeforces ELO=2150.0；Q3真跑=None Q4真跑=None；综合=78 可信=高 类型=文本|多模态|推理
- 多轮测速(101轮)：成功率49.5% ｜ TTFT 中位3219/均值4481/最大32152ms ｜ 总耗时均值4481ms ｜ 等级{'B': 13, 'C': 71, 'A': 15, 'S': 2} ｜ 失败类型{'network': 6, 'timeout': 17, 'slow_cooldown': 26, 'empty': 2}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 38 次 ｜ 成功率 78.9% ｜ avg_ms 5575 ｜ 末轮等级 A

**#3 `thinkingmachines/inkling`** — [NVIDIA NIM] Inkling ⚡(NVIDIA直连)
- 编程：代表分 **77.6**（SWE-bench V·Tier1）；全部基准：SWE-bench V=77.6 Terminal-Bench=63.8；Q3真跑=None Q4真跑=None；综合=82 可信=中 类型=文本|推理|多模态|语音
- 多轮测速(101轮)：成功率60.4% ｜ TTFT 中位1754/均值3293/最大46647ms ｜ 总耗时均值4491ms ｜ 等级{'C': 52, 'B': 8, 'S': 17, 'A': 24} ｜ 失败类型{'timeout': 12, 'network': 7, 'model_gone': 2, 'empty': 6, 'slow_cooldown': 13}
- 测限流(12轮×15测=180次)：被限流 **25 次**（涉及 9 轮）｜ 其他错误 4 次 ｜ 成功率 83.9% ｜ avg_ms 2073 ｜ 末轮等级 B


### 供应方 [Agnes-AI]（活清单共 6 个模型）
**#1 `agnes-2.5-pro`** — [Agnes-AI] agnes-2.5-pro
- 编程：代表分 **82.7**（SWE-bench V·Tier1）；全部基准：SWE-bench V=82.7 SWE-Bench PRO=61.8 Terminal-Bench=77.3；Q3真跑=92 Q4真跑=92；综合=80 可信=中 类型=文本|推理
- 多轮测速(96轮)：成功率93.8% ｜ TTFT 中位768/均值1139/最大6993ms ｜ 总耗时均值1905ms ｜ 等级{'S': 79, 'A': 3, 'B': 4, 'C': 10} ｜ 失败类型{'http_5xx': 1, 'cooldown': 2, 'http_4xx': 3}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 7 次 ｜ 成功率 96.1% ｜ avg_ms 725 ｜ 末轮等级 A

**#2 `agnes-2.5-flash`** — [Agnes-AI] agnes-2.5-flash
- 编程：代表分 **75.8**（SWE-bench V·Tier1）；全部基准：SWE-bench V=75.8 SWE-Bench PRO=50.4 Terminal-Bench=62.3；Q3真跑=92 Q4真跑=92；综合=70 可信=中 类型=文本
- 多轮测速(101轮)：成功率83.2% ｜ TTFT 中位516/均值1147/最大9211ms ｜ 总耗时均值1364ms ｜ 等级{'S': 70, 'B': 4, 'C': 23, 'A': 4} ｜ 失败类型{'timeout': 9, 'slow_cooldown': 7, 'model_gone': 1}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 0 次 ｜ 成功率 100.0% ｜ avg_ms 799 ｜ 末轮等级 S

**#3 `agnes-2.0-flash`** — [Agnes-AI] agnes-2.0-flash
- 编程：代表分 **72.4**（SWE-bench V·Tier1）；全部基准：SWE-bench V=72.4 SWE-Bench PRO=49.6 Terminal-Bench=52.6；Q3真跑=92 Q4真跑=90；综合=63 可信=中 类型=文本|多模态
- 多轮测速(96轮)：成功率85.4% ｜ TTFT 中位492/均值992/最大9035ms ｜ 总耗时均值1333ms ｜ 等级{'A': 5, 'S': 71, 'B': 1, 'C': 19} ｜ 失败类型{'http_5xx': 1, 'cooldown': 2, 'timeout': 11}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 1 次 ｜ 成功率 99.4% ｜ avg_ms 882 ｜ 末轮等级 S


### 供应方 [HF]（活清单共 6 个模型）
**#1 `moonshotai/Kimi-K2-Instruct`** — [HF] Kimi-K2-Instruct
- 编程：代表分 **65.8**（SWE-bench V·Tier1）；全部基准：SWE-bench V=65.8；Q3真跑=None Q4真跑=None；综合=78 可信=高 类型=文本|推理
- 多轮测速(99轮)：成功率53.5% ｜ TTFT 中位1743/均值1909/最大3888ms ｜ 总耗时均值2415ms ｜ 等级{'A': 43, 'B': 6, 'C': 46, 'S': 4} ｜ 失败类型{'network': 18, 'slow_cooldown': 19, 'http_4xx': 4, 'timeout': 5}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 90 次 ｜ 成功率 50.0% ｜ avg_ms 4044 ｜ 末轮等级 A

**#2 `Qwen/Qwen3-VL-30B-A3B-Instruct`** — [HF] Qwen3-VL-30B-A3B
- 编程：代表分 **42.6**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=42.6；Q3真跑=None Q4真跑=None；综合=72 可信=中 类型=多模态|推理|GUI
- 多轮测速(99轮)：成功率35.4% ｜ TTFT 中位1635/均值2183/最大8748ms ｜ 总耗时均值2285ms ｜ 等级{'A': 21, 'S': 6, 'C': 68, 'B': 4} ｜ 失败类型{'network': 18, 'timeout': 1, 'slow_cooldown': 19, 'http_4xx': 26}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 109 次 ｜ 成功率 39.4% ｜ avg_ms 2415 ｜ 末轮等级 A

**#3 `Qwen/Qwen3-4B-Instruct-2507`** — [HF] Qwen3-4B-Instruct
- 编程：代表分 **35.1**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=35.1；Q3真跑=None Q4真跑=None；综合=60 可信=中 类型=文本
- 多轮测速(99轮)：成功率60.6% ｜ TTFT 中位1332/均值1546/最大3835ms ｜ 总耗时均值1640ms ｜ 等级{'A': 35, 'S': 19, 'B': 6, 'C': 39} ｜ 失败类型{'network': 18, 'slow_cooldown': 19, 'http_4xx': 2}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 122 次 ｜ 成功率 32.2% ｜ avg_ms 1668 ｜ 末轮等级 A


### 供应方 [SenseNova]（活清单共 3 个模型）
**#1 `deepseek-v4-flash`** — [SenseNova] SenseNova DeepSeek V4 Flash
- 编程：代表分 **91.6**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=91.6 SWE-bench V=79.0 Codeforces ELO=3052.0；Q3真跑=None Q4真跑=None；综合=89 可信=高 类型=文本
- 多轮测速(101轮)：成功率93.1% ｜ TTFT 中位1848/均值1920/最大5148ms ｜ 总耗时均值2001ms ｜ 等级{'A': 83, 'B': 7, 'C': 8, 'S': 3} ｜ 失败类型{'rate_limit': 2, 'cooldown': 4, 'empty': 1}
- 测限流(12轮×15测=180次)：被限流 **43 次**（涉及 12 轮）｜ 其他错误 0 次 ｜ 成功率 76.1% ｜ avg_ms 1508 ｜ 末轮等级 C

**#2 `glm-5.2`** — [SenseNova] SenseNova GLM-5.2
- 编程：代表分 **62.1**（SWE-bench V·Tier1）；全部基准：SWE-bench V=62.1 SWE-Bench PRO=62.1 Terminal-Bench=81.0；Q3真跑=95 Q4真跑=93；综合=91 可信=高 类型=文本
- 多轮测速(102轮)：成功率70.6% ｜ TTFT 中位2004/均值2167/最大4580ms ｜ 总耗时均值2447ms ｜ 等级{'C': 33, 'A': 59, 'S': 2, 'B': 8} ｜ 失败类型{'no_quota': 2, 'rate_limit': 11, 'cooldown': 14, 'timeout': 3}
- 测限流(12轮×15测=180次)：被限流 **79 次**（涉及 12 轮）｜ 其他错误 12 次 ｜ 成功率 49.5% ｜ avg_ms 1475 ｜ 末轮等级 C

**#3 `sensenova-6.7-flash-lite`** — [SenseNova] sensenova-6.7-flash-lite
- 编程：代表分 **—**（无代码生成基准·Tier9）；全部基准：无第三方基准；Q3真跑=None Q4真跑=None；综合=72 可信=中 类型=多模态
- 多轮测速(101轮)：成功率95.0% ｜ TTFT 中位1272/均值2386/最大13775ms ｜ 总耗时均值2406ms ｜ 等级{'S': 43, 'B': 7, 'C': 23, 'A': 28} ｜ 失败类型{'timeout': 5}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 180 次 ｜ 成功率 0.0% ｜ avg_ms — ｜ 末轮等级 A


### 供应方 [Gemini]（活清单共 3 个模型）
**#1 `gemini-3.1-flash-lite`** — [Gemini] Gemini 3.1 Flash Lite
- 编程：代表分 **72.0**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=72.0；Q3真跑=None Q4真跑=None；综合=76 可信=高 类型=文本|多模态|推理
- 多轮测速(101轮)：成功率30.7% ｜ TTFT 中位1687/均值2083/最大5782ms ｜ 总耗时均值2083ms ｜ 等级{'A': 22, 'S': 3, 'C': 73, 'B': 3} ｜ 失败类型{'network': 16, 'slow_cooldown': 35, 'http_4xx': 19}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 119 次 ｜ 成功率 33.9% ｜ avg_ms 1955 ｜ 末轮等级 A

**#2 `gemini-3.6-flash`** — [Gemini] Gemini 3.6 Flash
- 编程：代表分 **58.7**（SWE-bench V·Tier1）；全部基准：SWE-bench V=58.7 SWE-Bench PRO=58.7 Terminal-Bench=78.0；Q3真跑=None Q4真跑=None；综合=86 可信=高 类型=文本|多模态|推理|GUI
- 多轮测速(101轮)：成功率29.7% ｜ TTFT 中位2001/均值2588/最大11563ms ｜ 总耗时均值2588ms ｜ 等级{'B': 5, 'A': 23, 'C': 73} ｜ 失败类型{'network': 16, 'slow_cooldown': 35, 'timeout': 1, 'http_4xx': 17, 'rate_limit': 1, 'cooldown': 1}
- 测限流(12轮×15测=180次)：被限流 **53 次**（涉及 9 轮）｜ 其他错误 125 次 ｜ 成功率 1.1% ｜ avg_ms 1538 ｜ 末轮等级 A

**#3 `gemini-flash-latest`** — [Gemini] Gemini Flash (最新)
- 编程：代表分 **95.3**（Tau-bench·Tier3）；全部基准：Tau-bench=95.3；Q3真跑=None Q4真跑=None；综合=86 可信=高 类型=文本|多模态|推理|GUI
- 多轮测速(101轮)：成功率15.8% ｜ TTFT 中位2312/均值3026/最大12163ms ｜ 总耗时均值3026ms ｜ 等级{'A': 10, 'C': 87, 'B': 4} ｜ 失败类型{'rate_limit': 2, 'cooldown': 3, 'network': 16, 'slow_cooldown': 45, 'timeout': 1, 'http_4xx': 17, 'empty': 1}
- 测限流(12轮×15测=180次)：被限流 **84 次**（涉及 10 轮）｜ 其他错误 96 次 ｜ 成功率 0.0% ｜ avg_ms — ｜ 末轮等级 B


### 供应方 [Groq]（活清单共 1 个模型）
**#1 `llama-3.1-8b-instant`** — [Groq] Llama-3.1-8B-Instant
- 编程：代表分 **11.6**（LiveCodeBench·Tier1）；全部基准：LiveCodeBench=11.6 Terminal-Bench=0.8 AA Coding=5.4；Q3真跑=None Q4真跑=None；综合=32 可信=高 类型=文本
- 多轮测速(99轮)：成功率24.2% ｜ TTFT 中位1398/均值1851/最大4937ms ｜ 总耗时均值1923ms ｜ 等级{'S': 9, 'C': 77, 'A': 8, 'B': 5} ｜ 失败类型{'http_4xx': 73, 'network': 2}
- 测限流(12轮×15测=180次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 112 次 ｜ 成功率 37.8% ｜ avg_ms 2092 ｜ 末轮等级 A


## 诚实备注（数据缺口与坑）

1. **GLM API 的 TOP3 有真实第三方基准（此前我误判为「全系缺」，已更正）**：`glm-4.7` 有 LiveCodeBench v6=84.9% + SWE-bench V=73.8%（z.ai 官方）、`glm-5` 有 SWE-bench V=77.8%（NYU rits）、`glm-4.5-air` 有 LiveCodeBench=68.4%（easy-benchmarks）。真正缺代码生成基准的是免费/视觉系小模型（glm-4.7-flash、glm-z1-flash、glm-4.x-vision 系列），它们不进 TOP3，不影响结论。
2. **Gemini 的 gemini-flash-latest 靠 Tau-bench 95.3 拉分**：Tau-bench 测的是 agentic 工具调用，非纯代码生成，已降入 Tier3，故排在 LCB 72 的 gemini-3.1-flash-lite 之后。若要的是「写代码」而非「调工具」，flash-latest 不一定是首选。
3. **Cloudflare 的 granite-4.0-h-micro 只有 HumanEval 81**（旧基准·易），无 LiveCodeBench，已正确排在 gemma/qwen3 之后；别被 HumanEval 数字骗去当编程主力。
4. **OpenRouter / HF / Agnes-AI 是路由/转售层**（非原厂）：它们复用了 NVIDIA/Cohere/Google/Qwen/Kimi 等原厂权重，编程能力本质来自上游模型；列为供应方是忠实于活清单标签，但评「原厂编程最强」应看 NVIDIA NIM / Cloudflare / GLM API / StepFun / SenseNova / Gemini 这些。
5. **限流结果 12 轮 ×15 测为温和探测**（轮间 5s，符合你定的「不触发平台限流」红线），被限次数低≠永远不限——高峰期密集调用仍可能触发，gemma-4-26b 在测速里就出现过 cooldown。
6. **`glm-5.2` 在活清单里被标了两次**：`[SenseNova] SenseNova GLM-5.2` 与 `[NVIDIA NIM] GLM-5.2 ⚡(Z.ai旗舰)`，是同一个 Z.ai 模型。故它既出现在 SenseNova 组的 TOP2（SWE-bench Pro 62.1%），也出现在 NVIDIA NIM 组的 TOP3（FrontierSWE 74.4%，官方/AA 双源）。评「原厂编程」时它就是同一模型，跨组去重看即可。

---
原始脚本：`_build_final_table.py`；中间文件：`_provider_top3.json`。