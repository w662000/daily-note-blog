---
layout: default
title: 交接文档 · autoclaw-nim-100模型清单
date: 2026-08-16 23:30:00 +0800
---

# nim-100模型清单（AutoClaw 项目表）— 交接文档

- **日期**：2026-08-12
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260812_autoclaw-nim-100模型清单_handoff.md（编码探测：utf-8）


- 来源：`https://integrate.api.nvidia.com/v1/models`（Hermes Studio 动态拉取的全量目录）
- 状态：✅ 显示 10 个（你保留的）/ 🔒 隐藏 90 个
- 生效范围：Hermes Studio → 模型选择器 → `nvidia-nim` 提供商（Profile: default）

## 保留显示的 8 个

| 模型 ID | 说明 |
|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b` | Nemotron 3 Ultra（550B MoE 旗舰，2026-06） |
| `nvidia/nemotron-3-super-120b-a12b` | Nemotron 3 Super（120B 主力，2026-03） |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | Nemotron 3 Nano Omni（30B 推理，2026-04） |
| `z-ai/glm-5.2` | GLM-5.2（智谱，2026-06） |
| `moonshotai/kimi-k2.6` | Kimi K2.6（月之暗面，2026-04） |
| `minimaxai/minimax-m3` | MiniMax M3（多模态，2026-06） |
| `openai/gpt-oss-120b` | GPT-OSS 120B（OpenAI 开源） |
| `openai/gpt-oss-20b` | GPT-OSS 20B（OpenAI 开源） |
| `deepseek-ai/deepseek-v4-flash-0731` | DeepSeek V4-Flash 正式版（2026-07-31 发布，最新） |
| `stepfun-ai/step-3.7-flash` | Step 3.7 Flash（阶跃星辰，2026-05-29 开源） |

## 国内模型排查（隐藏中的）

### 推荐（2026-02 之后发布，国内厂商）

| 模型 ID | 说明 | 当前状态 |
|---|---|---|
| `deepseek-ai/deepseek-v4-flash-0731` | DeepSeek V4-Flash 正式版（2026-07-31 发布，最新） | 显示 |
| `stepfun-ai/step-3.7-flash` | Step 3.7 Flash（阶跃星辰，2026-05-29 开源） | 显示 |

### 其余国内模型（较老）

| 模型 ID | 说明 | 当前状态 |
|---|---|---|
| `01-ai/yi-large` | Yi-Large（零一万物，2024 老模型） | 隐藏 |
| `baai/bge-m3` | BGE-M3 向量模型（智源，2024-01） | 隐藏 |
| `deepseek-ai/deepseek-coder-6.7b-instruct` | DeepSeek Coder 6.7B（2024 老模型） | 隐藏 |

## 全部 100 个（含隐藏）

| # | 状态 | 模型 ID | 厂商 |
|---|------|---------|------|
| 1 | 🔒 隐藏 | `01-ai/yi-large` | 01-ai |
| 2 | 🔒 隐藏 | `adept/fuyu-8b` | adept |
| 3 | 🔒 隐藏 | `ai21labs/jamba-1.5-large-instruct` | ai21labs |
| 4 | 🔒 隐藏 | `aisingapore/sea-lion-7b-instruct` | aisingapore |
| 5 | 🔒 隐藏 | `baai/bge-m3` | baai |
| 6 | 🔒 隐藏 | `bigcode/starcoder2-15b` | bigcode |
| 7 | 🔒 隐藏 | `databricks/dbrx-instruct` | databricks |
| 8 | 🔒 隐藏 | `deepseek-ai/deepseek-coder-6.7b-instruct` | deepseek-ai |
| 9 | ✅ 显示 | `deepseek-ai/deepseek-v4-flash-0731` | deepseek-ai |
| 10 | 🔒 隐藏 | `google/codegemma-1.1-7b` | google |
| 11 | 🔒 隐藏 | `google/codegemma-7b` | google |
| 12 | 🔒 隐藏 | `google/deplot` | google |
| 13 | 🔒 隐藏 | `google/diffusiongemma-26b-a4b-it` | google |
| 14 | 🔒 隐藏 | `google/gemma-2b` | google |
| 15 | 🔒 隐藏 | `google/gemma-3-12b-it` | google |
| 16 | 🔒 隐藏 | `google/gemma-3-4b-it` | google |
| 17 | 🔒 隐藏 | `google/gemma-4-31b-it` | google |
| 18 | 🔒 隐藏 | `google/recurrentgemma-2b` | google |
| 19 | 🔒 隐藏 | `ibm/granite-3.0-3b-a800m-instruct` | ibm |
| 20 | 🔒 隐藏 | `ibm/granite-3.0-8b-instruct` | ibm |
| 21 | 🔒 隐藏 | `ibm/granite-34b-code-instruct` | ibm |
| 22 | 🔒 隐藏 | `ibm/granite-8b-code-instruct` | ibm |
| 23 | 🔒 隐藏 | `meta/codellama-70b` | meta |
| 24 | 🔒 隐藏 | `meta/llama-3.1-70b-instruct` | meta |
| 25 | 🔒 隐藏 | `meta/llama-3.1-8b-instruct` | meta |
| 26 | 🔒 隐藏 | `meta/llama-3.2-11b-vision-instruct` | meta |
| 27 | 🔒 隐藏 | `meta/llama-3.2-1b-instruct` | meta |
| 28 | 🔒 隐藏 | `meta/llama-3.2-3b-instruct` | meta |
| 29 | 🔒 隐藏 | `meta/llama-3.2-90b-vision-instruct` | meta |
| 30 | 🔒 隐藏 | `meta/llama-3.3-70b-instruct` | meta |
| 31 | 🔒 隐藏 | `meta/llama-guard-4-12b` | meta |
| 32 | 🔒 隐藏 | `meta/llama2-70b` | meta |
| 33 | 🔒 隐藏 | `microsoft/kosmos-2` | microsoft |
| 34 | 🔒 隐藏 | `microsoft/phi-3-vision-128k-instruct` | microsoft |
| 35 | 🔒 隐藏 | `microsoft/phi-3.5-moe-instruct` | microsoft |
| 36 | ✅ 显示 | `minimaxai/minimax-m3` | minimaxai |
| 37 | 🔒 隐藏 | `mistralai/codestral-22b-instruct-v0.1` | mistralai |
| 38 | 🔒 隐藏 | `mistralai/mistral-7b-instruct-v0.3` | mistralai |
| 39 | 🔒 隐藏 | `mistralai/mistral-large` | mistralai |
| 40 | 🔒 隐藏 | `mistralai/mistral-large-2-instruct` | mistralai |
| 41 | 🔒 隐藏 | `mistralai/mistral-nemotron` | mistralai |
| 42 | 🔒 隐藏 | `mistralai/mixtral-8x22b-v0.1` | mistralai |
| 43 | ✅ 显示 | `moonshotai/kimi-k2.6` | moonshotai |
| 44 | 🔒 隐藏 | `nv-mistralai/mistral-nemo-12b-instruct` | nv-mistralai |
| 45 | 🔒 隐藏 | `nvidia/ai-synthetic-video-detector` | nvidia |
| 46 | 🔒 隐藏 | `nvidia/cosmos-reason2-8b` | nvidia |
| 47 | 🔒 隐藏 | `nvidia/embed-qa-4` | nvidia |
| 48 | 🔒 隐藏 | `nvidia/ising-calibration-1.5-31b` | nvidia |
| 49 | 🔒 隐藏 | `nvidia/llama-3.1-nemoguard-8b-content-safety` | nvidia |
| 50 | 🔒 隐藏 | `nvidia/llama-3.1-nemoguard-8b-topic-control` | nvidia |
| 51 | 🔒 隐藏 | `nvidia/llama-3.1-nemotron-51b-instruct` | nvidia |
| 52 | 🔒 隐藏 | `nvidia/llama-3.1-nemotron-70b-instruct` | nvidia |
| 53 | 🔒 隐藏 | `nvidia/llama-3.1-nemotron-nano-8b-v1` | nvidia |
| 54 | 🔒 隐藏 | `nvidia/llama-3.1-nemotron-nano-vl-8b-v1` | nvidia |
| 55 | 🔒 隐藏 | `nvidia/llama-3.1-nemotron-safety-guard-8b-v3` | nvidia |
| 56 | 🔒 隐藏 | `nvidia/llama-3.1-nemotron-ultra-253b-v1` | nvidia |
| 57 | 🔒 隐藏 | `nvidia/llama-3.2-nemoretriever-1b-vlm-embed-v1` | nvidia |
| 58 | 🔒 隐藏 | `nvidia/llama-3.2-nv-embedqa-1b-v1` | nvidia |
| 59 | 🔒 隐藏 | `nvidia/llama-3.3-nemotron-super-49b-v1` | nvidia |
| 60 | 🔒 隐藏 | `nvidia/llama-3.3-nemotron-super-49b-v1.5` | nvidia |
| 61 | 🔒 隐藏 | `nvidia/llama-nemotron-embed-1b-v2` | nvidia |
| 62 | 🔒 隐藏 | `nvidia/llama-nemotron-embed-vl-1b-v2` | nvidia |
| 63 | 🔒 隐藏 | `nvidia/llama3-chatqa-1.5-70b` | nvidia |
| 64 | 🔒 隐藏 | `nvidia/mistral-nemo-minitron-8b-8k-instruct` | nvidia |
| 65 | 🔒 隐藏 | `nvidia/nemoretriever-parse` | nvidia |
| 66 | 🔒 隐藏 | `nvidia/nemotron-3-embed-1b` | nvidia |
| 67 | 🔒 隐藏 | `nvidia/nemotron-3-nano-30b-a3b` | nvidia |
| 68 | ✅ 显示 | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | nvidia |
| 69 | ✅ 显示 | `nvidia/nemotron-3-super-120b-a12b` | nvidia |
| 70 | ✅ 显示 | `nvidia/nemotron-3-ultra-550b-a55b` | nvidia |
| 71 | 🔒 隐藏 | `nvidia/nemotron-3.5-content-safety` | nvidia |
| 72 | 🔒 隐藏 | `nvidia/nemotron-4-340b-instruct` | nvidia |
| 73 | 🔒 隐藏 | `nvidia/nemotron-4-340b-reward` | nvidia |
| 74 | 🔒 隐藏 | `nvidia/nemotron-mini-4b-instruct` | nvidia |
| 75 | 🔒 隐藏 | `nvidia/nemotron-nano-12b-v2-vl` | nvidia |
| 76 | 🔒 隐藏 | `nvidia/nemotron-nano-3-30b-a3b` | nvidia |
| 77 | 🔒 隐藏 | `nvidia/nemotron-parse` | nvidia |
| 78 | 🔒 隐藏 | `nvidia/neva-22b` | nvidia |
| 79 | 🔒 隐藏 | `nvidia/nv-embed-v1` | nvidia |
| 80 | 🔒 隐藏 | `nvidia/nv-embedcode-7b-v1` | nvidia |
| 81 | 🔒 隐藏 | `nvidia/nv-embedqa-e5-v5` | nvidia |
| 82 | 🔒 隐藏 | `nvidia/nv-embedqa-mistral-7b-v2` | nvidia |
| 83 | 🔒 隐藏 | `nvidia/nvclip` | nvidia |
| 84 | 🔒 隐藏 | `nvidia/nvidia-nemotron-nano-9b-v2` | nvidia |
| 85 | 🔒 隐藏 | `nvidia/riva-translate-4b-instruct` | nvidia |
| 86 | 🔒 隐藏 | `nvidia/riva-translate-4b-instruct-v1.1` | nvidia |
| 87 | 🔒 隐藏 | `nvidia/riva-translate-4b-instruct-v2` | nvidia |
| 88 | 🔒 隐藏 | `nvidia/vila` | nvidia |
| 89 | ✅ 显示 | `openai/gpt-oss-120b` | openai |
| 90 | ✅ 显示 | `openai/gpt-oss-20b` | openai |
| 91 | 🔒 隐藏 | `poolside/laguna-xs-2.1` | poolside |
| 92 | 🔒 隐藏 | `snowflake/arctic-embed-l` | snowflake |
| 93 | ✅ 显示 | `stepfun-ai/step-3.7-flash` | stepfun-ai |
| 94 | 🔒 隐藏 | `thinkingmachines/inkling` | thinkingmachines |
| 95 | 🔒 隐藏 | `writer/palmyra-creative-122b` | writer |
| 96 | 🔒 隐藏 | `writer/palmyra-fin-70b-32k` | writer |
| 97 | 🔒 隐藏 | `writer/palmyra-med-70b` | writer |
| 98 | 🔒 隐藏 | `writer/palmyra-med-70b-32k` | writer |
| 99 | ✅ 显示 | `z-ai/glm-5.2` | z-ai |
| 100 | 🔒 隐藏 | `zyphra/zamba2-7b-instruct` | zyphra |

> 说明：这些模型只是 NIM 平台的模型清单（元数据），不是已下载的模型；隐藏不影响调用，只是不在选择器里显示。恢复全部显示：Settings → Models → nvidia-nim → 可见模型控制改回 all。
