---
layout: default
title: 技术点 · Built-in Plugins
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Built-in Plugins

> 来源：261010_Built-in Plugins_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
hermes plugins enable disk-cleanup
```
- ```
plugins:
  enabled:
    - disk-cleanup
```
- ```
hermes plugins disable disk-cleanup
# or: remove it from plugins.enabled in config.yaml
```
- | `image_gen/openai` | image backend | OpenAI GPT Image 2 and 2.5 Flare/Sunburst generation and editing (API key) |
- ```
/disk-cleanup status                     # breakdown + top-10 largest
/disk-cleanup dry-run                    # preview without deleting
/disk-cleanup quick                      # run safe cleanup now
/disk-cleanup deep                       # quick + list items needing confirmation
/disk-cleanup track <path> <category>    # manual tracking
/disk-cleanup forget <path>              # stop tracking (does not delete)
```
- Traces Hermes turns, LLM calls, and tool invocations to [Langfuse](https://langfuse.com) — an open-source LLM observability platform. One span per turn, one generation per API call, one tool observation per tool call. Usage totals, per-type token counts, and cost estimates come out of Hermes' canonical `agent.usage_pricing` numbers, so the Langfuse dashboard sees the same breakdown (input / output / `cache_read_input_tokens` / `cache_creation_input_tokens` / `reasoning_tokens`) that appears in `hermes logs`.
- ```
hermes tools          # → Langfuse Observability → Cloud or Self-Hosted
```
- The wizard collects your keys, `pip install`s the `langfuse` SDK, and adds `observability/langfuse` to `plugins.enabled` for you. Restart Hermes and the next turn ships a trace.
- ```
pip install langfuse
hermes plugins enable observability/langfuse
```
- ```
HERMES_LANGFUSE_PUBLIC_KEY=pk-lf-...
HERMES_LANGFUSE_SECRET_KEY=sk-lf-...
HERMES_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```
- | `pre_api_request` / `pre_llm_call` | Open (or reuse) a per-turn root span "Hermes turn". Start a `generation` child observation for this API call with serialized recent messages as input. |
- | `post_api_request` / `post_llm_call` | Close the generation, attach `usage_details`, `cost_details`, `finish_reason`, assistant output + tool calls. If no tool calls and non-empty content, close the turn. |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
