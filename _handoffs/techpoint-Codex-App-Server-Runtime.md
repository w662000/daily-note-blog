---
layout: default
title: 技术点 · Codex App-Server Runtime
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Codex App-Server Runtime

> 来源：261010_Codex App-Server Runtime_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Run OpenAI agent turns against your **ChatGPT subscription** (no API key required) using the same auth flow Codex CLI uses.
- **`web_search`** / **`web_extract`** — Firecrawl-backed; tends to be cleaner than scraping for structured content.
- **Works on this runtime.** Goals persist in `state_meta` keyed by session id, the continuation prompt feeds back as a normal user message through `run_conversation()`, and codex executes the next turn natively. The goal judge runs via the auxiliary client (configured via `auxiliary.goal_judge` in config.yaml), independent of which runtime is active. The judge's "blocked, needs user input" verdict is a clean escape if codex stalls on approvals.
- Gateway commentary stays visible when token streaming is disabled, and
- ```
   npm i -g @openai/codex
   codex --version   # 0.130.0 or newer
```
- ```
   codex login                  # writes tokens to ~/.codex/auth.json
```
- ```
   providers:
     my-gateway:
       api: https://gateway.example.com/v1
       key_env: MY_GATEWAY_API_KEY
       default_model: gpt-5.4

   model:
     provider: custom:my-gateway
     default: gpt-5.4
     openai_runtime: codex_app_server
```
- ```
   [model_providers.my-gateway]
   name = "My Gateway"
   base_url = "https://gateway.example.com/v1"
   env_key = "MY_GATEWAY_API_KEY"
   wire_api = "responses"
```
- Hermes sends only `model` and `modelProvider = "my-gateway"` on `thread/start`; codex resolves `base_url` and reads the key from `env_key` in its own environment. **Hermes never forwards the API key**, so `MY_GATEWAY_API_KEY` must be present in the process environment Hermes runs in — `~/.hermes/.env` is loaded at startup and provider credentials are inherited by the codex subprocess. Auxiliary calls (titles, compression, memory review) still use Hermes' own `providers.my-gateway` entry.
- Caveats: the name after `custom:` is the `providers:` config key and must match the `[model_providers.<name>]` table name exactly — if it does not exist on the codex side, codex reports an unknown provider rather than silently using the Hermes endpoint. Anonymous `provider: custom` (a bare `base_url`) is not eligible: it has no stable name to hand to codex, so it stays on Hermes' standard runtime.
- ```
   codex plugin marketplace add openai-curated
   # then via codex's TUI, install Linear / GitHub / Gmail / etc.
```
- ```
/codex-runtime codex_app_server
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
