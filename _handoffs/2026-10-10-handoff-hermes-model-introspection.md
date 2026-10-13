---
layout: default
title: 交接文档 · Hermes Model Introspection
date: 2026-10-13 23:30:00 +0800
---

# Hermes Model Introspection

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\hermes\hermes-model-introspection\SKILL.md

---
name: hermes-model-introspection
description: Find the active Hermes model and provider; never guess.
---

# Hermes Model Introspection

## When to use
- User asks "你是哪个模型" / "what model are you" / "which model is running"
- User runs `hermes --version` and you need to map version -> provider setup
- Before editing model/provider config and you need the current baseline
- Any task where you are about to *state* the active model/provider

## Steps
1. **Agent version** — run `hermes --version` (`--ver` is NOT recognized). Prints
   version, install dir, Python, SDK version.
2. **Find the provider plugin** — provider plugins live under the install dir's
   `plugins/model-providers/<name>/`, e.g. `D:/hermes-agent/plugins/model-providers/`.
   Each plugin dir contains `plugin.yaml` (name/kind/description only) and `__init__.py`
   (the REAL config: `base_url`, `default_headers`, model aliases, `default_aux_model`).
3. **Read the plugin** — `read_file` the `__init__.py`. Find the registered
   `ProviderProfile(...)` instance: note its `base_url`, `default_headers`, and
   `default_aux_model`. This tells you keyed vs keyless and the relay URL.
4. **Confirm exact active model ID** — GET `<base_url>/models` with the provider's
   headers. Returns internal IDs (e.g. `hy3-free`, `deepseek-v4-flash-free`).
   The system prompt's `Model:` / `Provider:` lines are the authoritative active values.
5. **Probe behavior** — POST a minimal chat completion (`max_tokens` small). Inspect
   `reasoning_content` and `completion_tokens_details.reasoning_tokens`: if present,
   it is a **reasoning / thinking model**.

## Pitfalls
- **NEVER guess the model identity from memory or display names.** I once answered
  "DeepSeek V4 Flash" from a hunch and was wrong — the real config was `hy3-free`
  via `opencode-free`. Always verify from config + endpoint before stating it.
- **`/v1/models` IDs hide the vendor.** `hy3-free` does not reveal it is Hunyuan;
  the list only shows `owned_by: opencode`. Infer vendor from behavior (reasoning
  language/style) or ask the user who configured it. Do not present a guessed vendor
  as fact.
- **OpenCode free tier is keyless.** `opencode-free` sends an EMPTY `Authorization`
  header because the relay 401s any unrecognized bearer. Do NOT inject a fake API key.
  Pass only `HTTP-Referer` / `X-Title` headers if the relay expects them.
- **Web search may be unavailable** in a given session (no `web_search` tool, or
  search endpoints block bots). Prefer the local config + provider endpoint probe —
  it is authoritative and needs only the provider's own API.

## references/
- `references/probe-recipe.md` — exact curl commands to list models and detect
  reasoning behavior.
