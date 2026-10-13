---
layout: default
title: 技术点 · FAQ & Troubleshooting
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · FAQ & Troubleshooting

> 来源：261010_FAQ & Troubleshooting_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Hermes Agent works with any OpenAI-compatible API. Supported providers include:
- **[OpenRouter](https://openrouter.ai/)** — access hundreds of models through one API key (recommended for flexibility)
- **Anthropic** — Claude models (direct API, OAuth via `hermes auth add anthropic`, OpenRouter, or any compatible proxy)
- **Google** — Gemini models (direct API via `gemini` provider, OpenRouter, or compatible proxy)
- Set your provider with `hermes model` or by editing `~/.hermes/.env`. See the [Environment Variables](./environment-variables.md) reference for all provider keys.
- API calls go **only to the LLM provider you configure** (e.g., OpenRouter, your local Ollama instance). Hermes Agent does not collect telemetry, usage data, or analytics. Your conversations, memory, and skills are stored locally in `~/.hermes/`.
- ```
hermes model
# Select: Custom endpoint (enter URL manually)
# API base URL: http://localhost:11434/v1
# API key: ollama
# Model name: qwen3.5:27b
# Context length: 64000   ← Hermes minimum; set this to match your server's actual context window
```
- ```
model:
  default: qwen3.5:27b
  provider: custom
  base_url: http://localhost:11434/v1
```
- If you set a custom `num_ctx` in Ollama (e.g., `ollama run --num_ctx 64000`), make sure to set the matching context length in Hermes — Ollama's `/api/show` reports the model's *maximum* context, not the effective `num_ctx` you configured.
- Hermes Agent itself is **free and open-source** (MIT license). You pay only for the LLM API usage from your chosen provider. Local models are completely free to run.
- ```
from run_agent import AIAgent

agent = AIAgent(model="anthropic/claude-opus-4.7")
response = agent.chat("Explain quantum computing briefly")
```
- See the [Python Library guide](../user-guide/features/code-execution.md) for full API usage.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
