---
layout: default
title: 交接文档 · autoclaw-模型评分表_Hermes-MoA选型
date: 2026-08-17 23:30:00 +0800
---

# 模型评分表_Hermes-MoA选型（AutoClaw 项目表）— 交接文档

- **日期**：2026-08-12
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260812_autoclaw-模型评分表_Hermes-MoA选型_handoff.md（编码探测：utf-8）


> **数据日期**：平台分数 2026-08-02（上次评分表口径）｜模型清单 2026-08-08（openclaw.json 快照）
> **评分来源**：LMArena（ELO）｜Artificial Analysis（Intelligence Index）｜OpenCompass 司南（综合均分）｜SuperCLUE（中文总分）｜LiveBench（防污染任务分）
> **综合指数**（0–100）：5 平台异质量纲归一化估值，含预估成分；置信度 高/中/低 标注可靠性。

## 一、MoA 阵容推荐

### 主力（Aggregator·聚合最终答案）

| 角色 | 模型 | 综合分 | 理由 |
|---|---|---|---|
| **主力 1** | SenseNova GLM-5.2 | **91** | 全场最高分；实测 91.8 被低估；推理/编程双强，聚合质量最稳 |
| **主力 2（备）** | DeepSeek-V4-Pro（官方） | **90** | 独立架构，OpenCompass 65.1 / AA 52，与 GLM 系形成互补 |
| **主力 3（备）** | GLM-5.1（赠送） | **89** | 免费赠送，成本为 0 |

### 助手（Proposer·并行出初稿，5–6 个，跨厂商多样性）

| 角色 | 模型 | 综合分 | 分工建议 |
|---|---|---|---|
| 助手 1 | GLM-5 Turbo（赠送） | **88** | 主力同系补充视角，实测能力 92 分第一 |
| 助手 2 | DeepSeek-V4-Flash | **89** | DeepSeek 系，数学/代码强 |
| 助手 3 | Gemini 3.6 Flash | **86** | Google 系，LMArena 1477，长文本好（注意近期 network 不稳） |
| 助手 4 | Nemotron-3-Ultra-550B（NIM） | **84** | NVIDIA 系超大杯，推理深度好 |
| 助手 5 | Kimi-K2（HF） | **78** | 开源系，LiveBench 76.4，与闭源差异大（注意 network 不稳） |
| 助手 6（备） | agnes-2.5-pro / Step-3.7-Flash | 80 / 76 | Agnes 实测 89.4；StepFun 速度快 |

> **MoA 要点**：助手选「能力在线 + 厂商/架构尽量不同」的模型，答案多样性越高，聚合效果越好；主力必须是最强且指令遵循好的模型。**不建议**把生成类（语音/图像/视频）和 60 分以下的小模型放进 MoA。

## 二、文本 / 推理 / 多模态评分总表（按综合指数降序）

| # | 模型 | 厂商 | 类型 | LMArena | AA | OpenCompass | SuperCLUE | LiveBench | 综合 | 级 | 置信 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SenseNova GLM-5.2 | 商汤 SenseNova | 文本/推理 | — | 51 | — | 1357.7 | 89.8 | **91** | S | 高 | 全场最高分;实测 91.8 被低估 |
| 2 | GLM-5.2-Coding (ZAI) | 智谱 ZAI | 文本/推理 | — | — | — | — | — | **90** | S | 中 | GLM-5.2 编码特化,1M 上下文 |
| 3 | DeepSeek-V4-Pro (官方) | DeepSeek | 文本/推理 | — | 52 | — | — | — | **90** | S | 中 | AA 52/OpenCompass 65.1,官方渠道 |
| 4 | GLM-5.1 (赠送) | 智谱 GLM API | 文本 | — | 40 | — | 1321.4 | 72.5 | **89** | S | 高 | 智谱赠送旗舰 |
| 5 | SenseNova DeepSeek V4 Flash | 商汤 SenseNova | 文本/推理 | — | — | — | 68.82 | 70.1 | **89** | S | 高 | DeepSeek V4 Flash 托管 |
| 6 | DeepSeek-V4-Flash (官方) | DeepSeek | 文本/推理 | — | — | — | — | 70.1 | **89** | S | 高 | 官方渠道 |
| 7 | GLM-5-Turbo (ZAI) | 智谱 ZAI | 文本/推理 | — | — | — | — | — | **88** | S | 中 | ≈GLM-5 Turbo,官方加速通道 |
| 8 | GLM-5 Turbo (赠送) | 智谱 GLM API | 文本 | — | — | — | — | — | **88** | S | 中 | 实测能力分 92.0 全场第一 |
| 9 | GLM-5.2 (NIM·Z.ai旗舰) | NVIDIA NIM | 文本/推理 | 1475 | 51 | — | — | 76.24 | **88** | S | 高 | 编程专项 64.13 全场第一;近期 network 不稳 |
| 10 | GLM-5 | 智谱 GLM API | 文本 | — | 50 | — | 86.26 | 68.8 | **87** | S | 高 |  |
| 11 | Gemini 3.6 Flash | Google Gemini | 推理/多模态 | 1477 | 50 | — | — | — | **86** | A | 高 | LMArena Top15;近期 network 不稳 |
| 12 | Gemini Flash (最新) | Google Gemini | 推理/多模态 | 1477 | 50.2 | — | 71.51 | 75.02 | **86** | A | 高 | 动态别名;近期 network 不稳 |
| 13 | GLM-5V-Turbo (ZAI) | 智谱 ZAI | 多模态 | — | — | — | — | — | **84** | A | 低 | 视觉旗舰 |
| 14 | GLM-5V-Turbo (赠送) | 智谱 GLM API | 多模态 | — | — | — | — | — | **84** | A | 低 | 实测编程 94.0 |
| 15 | Nemotron-3-Ultra-550B (NIM) | NVIDIA NIM | 推理 | — | 48 | — | — | — | **84** | A | 高 | 550B 超大杯 |
| 16 | Inkling (NIM) | NVIDIA NIM | 推理/多模态 | — | — | — | — | 78.3 | **82** | A | 中 | Thinking Machines Lab |
| 17 | step-router-v1 | 阶跃 StepFun | 文本 | — | — | — | — | — | **80** | A | 低 | 路由模型,实测被低估 |
| 18 | GLM-4.7 | 智谱 GLM API | 文本 | 1443 | 42.1 | — | — | 58.09 | **80** | A | 高 |  |
| 19 | gemma-4-26b (Cloudflare) | Cloudflare | 多模态 | 1441 | 25.7 | — | — | — | **80** | A | 高 | 实测 84.8 被低估 |
| 20 | agnes-2.5-pro | Agnes-AI | 文本/推理 | — | — | — | — | — | **80** | A | 中 | 实测 89.4 |
| 21 | step-3.5-flash | 阶跃 StepFun | 文本 | — | 37.8 | — | 48.97 | — | **78** | A | 高 |  |
| 22 | step-3.5-flash-2603 | 阶跃 StepFun | 文本 | — | — | — | — | — | **78** | A | 中 | 新版本,架构设计实测强 |
| 23 | GLM-4.6V | 智谱 GLM API | 多模态 | — | — | — | — | 37.2 | **78** | A | 高 |  |
| 24 | Gemma-4-31B (NIM) | NVIDIA NIM | 文本/多模态 | 1452 | 39 | — | — | — | **78** | A | 高 | NVIDIA 直连 |
| 25 | Nemotron Ultra 550B (OR·免费) | OpenRouter | 推理 | 1444.55 | 48 | — | — | 37.5 | **78** | A | 高 |  |
| 26 | Kimi-K2 (HF) | HuggingFace | 文本/推理 | 1371 | 26.3 | — | — | 76.4 | **78** | A | 高 | 开源强推理;近期 network 不稳 |
| 27 | Step-3.7-Flash | 阶跃 StepFun | 多模态 | — | 30.3 | — | — | — | **76** | A | 高 | step_plan 订阅通道,速度快 |
| 28 | Gemini 3.1 Flash Lite | Google Gemini | 多模态 | 1432 | 34 | — | — | — | **76** | A | 高 |  |
| 29 | Nemotron-3-Super-120B (NIM) | NVIDIA NIM | 推理 | — | 36 | — | — | — | **74** | B | 中 |  |
| 30 | gpt-oss-120b (Cloudflare) | Cloudflare | 推理 | 1365 | 24 | — | — | 46.09 | **74** | B | 高 |  |
| 31 | agnes-2.5-pro-alpha | Agnes-AI | 文本/推理 | — | 39 | — | — | — | **74** | B | 中 |  |
| 32 | nemotron-3-120b (Cloudflare) | Cloudflare | 推理 | 1361 | 25 | — | — | 32.51 | **73** | B | 高 |  |
| 33 | Gemma 4 31B (OR·免费) | OpenRouter | 多模态 | 1441.69 | 39 | 52.4 | 58.11 | 59.4 | **73** | B | 高 | 免费档 |
| 34 | sensenova-6.7-flash-lite | 商汤 SenseNova | 多模态 | — | — | — | — | — | **72** | B | 中 | 商汤自家,当前会话在用 |
| 35 | glm-4.7-flash (Cloudflare) | Cloudflare | 推理 | 1353 | 23 | — | — | — | **72** | B | 高 |  |
| 36 | Qwen3-VL-30B (HF) | HuggingFace | 视觉/推理 | — | — | — | — | 65.4 | **72** | B | 中 |  |
| 37 | Step-3.7-Flash (NIM) | NVIDIA NIM | 多模态 | — | — | — | — | — | **70** | B | 中 |  |
| 38 | agnes-2.5-flash | Agnes-AI | 文本 | — | — | — | — | — | **70** | B | 中 | 实测 90.0 被低估,速度快 |
| 39 | GLM-4.6V-Flash (免费视觉) | 智谱 GLM API | 多模态 | — | — | — | — | — | **68** | B | 中 | 免费视觉,有 rate_limit |
| 40 | moondream3.1-9B (Cloudflare) | Cloudflare | 视觉 | — | — | — | — | — | **68** | B | 中 | 轻量视觉 |
| 41 | GLM-4.7-Flash (赠送) | 智谱 GLM API | 文本 | — | — | — | — | — | **66** | B | 低 | 实测两题采集失败,实际应更高 |
| 42 | Gemma 4 26B (OR·免费) | OpenRouter | 多模态 | 1434.69 | 26 | — | — | — | **66** | B | 高 | 免费档,近2轮 50% 不稳 |
| 43 | Qwen2.5-VL-72B (HF) | HuggingFace | 视觉 | — | — | — | — | — | **66** | B | 中 |  |
| 44 | Nemotron Super 120B (OR·免费) | OpenRouter | 推理 | 1410 | 36 | — | — | 34.4 | **64** | B | 高 |  |
| 45 | GPT-OSS-120B (NIM) | NVIDIA NIM | 推理 | 1353 | 33 | — | — | — | **63** | B | 高 | 编码 60.2/数学 68.9 |
| 46 | qwen3-30b-a3b (Cloudflare) | Cloudflare | 文本 | 1384 | 9.1 | — | — | 39.01 | **63** | B | 高 |  |
| 47 | agnes-2.0-flash | Agnes-AI | 文本/多模态 | — | — | — | — | — | **63** | B | 中 |  |
| 48 | step-1o-turbo-vision | 阶跃 StepFun | 多模态 | — | — | — | — | — | **62** | B | 中 | 视觉模型 |
| 49 | GLM-4.5-Air (赠送) | 智谱 GLM API | 文本 | 1373 | 17 | — | — | — | **62** | B | 高 |  |
| 50 | GLM-4.1V-Thinking-FlashX (资源包) | 智谱 GLM API | 多模态 | — | — | — | — | — | **62** | B | 中 | 视觉推理,快 |
| 51 | GLM-4.1V-Thinking-Flash (免费视觉) | 智谱 GLM API | 多模态 | — | — | — | — | — | **62** | B | 中 | 免费视觉推理 |
| 52 | qwq-32b (Cloudflare) | Cloudflare | 推理 | 1332 | 19.7 | — | — | 73.1 | **62** | B | 高 | LiveBench 推理强 |
| 53 | Ling 3.0 Flash (OR·免费) | OpenRouter | 文本 | — | — | — | — | — | **62** | B | 低 | 蚂蚁百灵 |
| 54 | Qwen-3.6-27B (Groq) | Groq | 文本 | — | — | — | — | — | **62** | B | 中 | 估分;Qwen3.6 中型 |
| 55 | deepseek-r1-distill-qwen-32b (Cloudflare) | Cloudflare | 推理 | — | 17.2 | — | — | 38.45 | **60** | C | 高 |  |
| 56 | Qwen3-4B (HF) | HuggingFace | 文本 | — | — | — | — | 63 | **60** | C | 中 |  |
| 57 | llama-4-scout-17b (Cloudflare) | Cloudflare | 多模态 | 1341 | 10 | — | — | — | **59** | C | 高 |  |
| 58 | llama-3.3-70b (Cloudflare) | Cloudflare | 文本 | 1344 | 9 | — | — | — | **58** | C | 高 | fp8 加速版 |
| 59 | Llama-3.3-70B-Versatile (Groq) | Groq | 文本 | 1344 | 9 | — | — | — | **58** | C | 高 | ≈Cloudflare 版,但 Groq 更快 |
| 60 | Laguna XS 2.1 (OR·免费) | OpenRouter | 文本 | — | — | — | — | — | **57** | C | 中 | Poolside;近2轮 50% 不稳 |
| 61 | mistral-small-3.1-24b (Cloudflare) | Cloudflare | 多模态 | 1271 | 15 | — | — | — | **54** | C | 高 |  |
| 62 | North Mini Code (OR·免费) | OpenRouter | 文本 | — | 33.4 | — | — | — | **54** | C | 中 | Cohere,编码特化 |
| 63 | GPT-OSS-20B (OR·免费) | OpenRouter | 推理 | 1348 | 14.9 | — | — | — | **52** | C | 高 |  |
| 64 | GPT-OSS-20B (Groq) | Groq | 推理 | 1348 | 14.9 | — | — | — | **52** | C | 高 |  |
| 65 | Llama-4-Scout-17B (HF) | HuggingFace | 多模态 | 1290 | 13.5 | — | — | — | **52** | C | 高 |  |
| 66 | GLM-Z1-Flash (免费) | 智谱 GLM API | 推理 | — | — | — | — | — | **47** | C | 低 | 免费推理模型,限流严重 |
| 67 | Nemotron Nano Omni 30B (OR·免费) | OpenRouter | 多模态 | — | 15 | — | — | — | **47** | C | 中 |  |
| 68 | Gemma-3-12B (HF) | HuggingFace | 多模态 | — | 5.51 | — | — | — | **46** | C | 高 |  |
| 69 | Nemotron Nano 30B (OR·免费) | OpenRouter | 文本 | 1360 | 14 | — | — | — | **45** | D | 高 |  |
| 70 | GLM-4-Flash-250414 (免费) | 智谱 GLM API | 文本 | — | — | — | — | — | **40** | D | 低 | 免费档,轻量 |
| 71 | granite-4.0-h-micro (Cloudflare) | Cloudflare | 文本 | — | 7.67 | — | — | — | **38** | D | 中 |  |
| 72 | Nemotron Nano 12B VL (OR·免费) | OpenRouter | 多模态 | — | 9 | — | — | — | **38** | D | 中 |  |
| 73 | Llama-3.1-8B-Instant (Groq) | Groq | 文本 | 1176 | 7.6 | — | — | — | **32** | D | 高 | 极快但弱 |
| 74 | Allam-2-7B (Groq) | Groq | 文本 | — | — | — | — | — | **30** | D | 低 | 估分;阿拉伯语小模型 |
| 75 | Auto（动态路由） | 智谱 ZAI | 路由 | — | — | — | — | — | **—** | — | - | 按任务自动路由,不参与评分 |

## 三、生成类模型（语音 / 图像 / 视频 / GUI，同类内相对分，不可与文本横比）

| # | 模型 | 厂商 | 类型 | AA | SuperCLUE | 综合 | 置信 |
|---|---|---|---|---|---|---|---|
| 1 | step-audio-r1.5 | 阶跃 StepFun | 语音 | — | — | **89** | 高 |
| 2 | step-audio-r1.1 | 阶跃 StepFun | 语音 | — | — | **88** | 中 |
| 3 | stepaudio-2.5-chat | 阶跃 StepFun | 语音 | — | — | **86** | 低 |
| 4 | step-audio-2 | 阶跃 StepFun | 语音 | — | — | **85** | 高 |
| 5 | step-gui | 阶跃 StepFun | GUI | — | 54.26 | **82** | 高 |
| 6 | step-audio-2-mini | 阶跃 StepFun | 语音 | — | — | **78** | 高 |
| 7 | agnes-image-2.1-flash | Agnes-AI | 图像生成 | 1191 | — | **76** | 中 |
| 8 | agnes-video-v2.0 | Agnes-AI | 视频生成 | 934 | — | **62** | 中 |
| 9 | step-1o-audio | 阶跃 StepFun | 语音 | — | — | **58** | 低 |

## 四、分级与使用建议

| 级别 | 综合分 | 数量 | 用途 |
|---|---|---|---|
| S | ≥87 | 10 | MoA 主力 / 重活主力 |
| A | 76–86 | 18 | MoA 助手 / 常规重活 |
| B | 62–75 | 26 | 轻量任务 / 并行扩样 |
| C | 46–61 | 14 | 凑数 / 小任务 |
| D | ≤45 | 6 | 不建议用于 MoA |

**口径说明**：综合指数为归一化估值（LMArena ELO≈1000–1480 / AA≈5–51 / OpenCompass≈52–65 / SuperCLUE≈49–1358 / LiveBench≈32–90 五源折算）；空值为该平台未收录。置信度：高=≥2 平台真实数据；中=1 平台或公开基准；低=基本预估。生成类模型综合分仅同类内可比。Auto（zai_auto）为动态路由模型，不参与评分。
