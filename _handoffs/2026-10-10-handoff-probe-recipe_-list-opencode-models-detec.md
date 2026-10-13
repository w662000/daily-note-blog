---
layout: default
title: 交接文档 · Probe recipe_ list OpenCode models & detect reasoning behavi
date: 2026-10-13 23:30:00 +0800
---

# Probe recipe: list OpenCode models & detect reasoning behavior

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\hermes\hermes-model-introspection\references\probe-recipe.md

## List available models (free + paid) under a provider
```bash
curl -s --max-time 15 "https://opencode.ai/zen/v1/models" \
  -H "HTTP-Referer: https://hermes-agent.nousresearch.com" \
  -H "X-Title: Hermes Agent"
```
Returns `{object:list, data:[{id, owned_by}]}`. Free-tier IDs end in `-free`
(e.g. `hy3-free`, `deepseek-v4-flash-free`, `laguna-s-2.1-free`). `owned_by`
is `opencode` — it does NOT reveal the real vendor.

## Minimal chat completion to probe behavior
```bash
curl -s --max-time 20 "https://opencode.ai/zen/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: https://hermes-agent.nousresearch.com" \
  -H "X-Title: Hermes Agent" \
  -d '{"model":"hy3-free","messages":[{"role":"user","content":"reply with exactly one word: hi"}],"max_tokens":5}'
```
## Read the result
- `reasoning_content` present (non-empty) + `usage.completion_tokens_details.reasoning_tokens > 0`
  => the model is a **reasoning / thinking model**.
- `model` field echoes the internal ID you passed in.

## Note for keyless free tier
Do NOT send an `Authorization` header at all (the relay 401s unknown bearers).
Only `HTTP-Referer` / `X-Title` are needed.
