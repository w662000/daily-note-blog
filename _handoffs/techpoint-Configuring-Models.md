---
layout: default
title: 技术点 · Configuring Models
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Configuring Models

> 来源：261010_Configuring Models_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Portal subscribers also get **10% off token-billed providers**.
- On a brand-new install the bundled default config has `model: ""` (an empty string sentinel meaning "not configured yet"). The first time you run `hermes setup` or `hermes model`, that key is upgraded in-place to a mapping with `provider`, `default`, `base_url`, and `api_mode` sub-keys — the shape shown throughout this page and in [`profiles.md`](./profiles.md) / [`configuration.md`](./configuration.md). If you ever see an empty string in `config.yaml`, run `hermes model` (or click **Change** in the dashboard) and Hermes will write the dict form for you.
- 2. **Usage analytics** — ranked cards showing every model that ran a session in the selected period, with token counts, cost, and capability badges.
- **Left** — authenticated providers. Only providers you've set up (API key set, OAuth'd, or defined as a custom endpoint) show up here. If a provider is missing, head to **Keys** and add its credential.
- Prompt caches are keyed to the model serving the request, so any mid-conversation model change — an explicit `/model` switch, an [automatic fallback](./features/fallback-providers.md), or a [credential-pool](./features/credential-pools.md) rotation onto a different account — means the next message re-reads the entire conversation at full input-token price instead of the cached (~75–90% discounted) rate. On a long session this one-time re-read can dwarf the per-token difference between the two models. Switch when you need to, but prefer doing it early in a conversation or right after starting a fresh session.
- Because of that one-time re-read cost, Hermes asks for **explicit confirmation** before applying a mid-session switch when the live session already holds a large context (default: **100,000 tokens**, measured from the latest provider-billed prompt size). The confirmation renders through the same selection-guard prompt as the expensive-model and data-training warnings wherever a live session is switching: the CLI and TUI `/model` command and picker, and a typed gateway `/model` in a chat with an active agent. Tune or disable it in `config.yaml`:
- ```
model:
  # Ask before mid-session switches when the session exceeds this many
  # context tokens (the next reply re-reads them uncached). 0 disables.
  switch_context_confirm_tokens: 100000
```
- ```
hermes config set security.allow_data_training_tiers_noninteractive true
```
- Hermes still prints the full data-policy warning and the acknowledgement key on every unattended startup, so worker logs retain an audit trail. This setting does not approve expensive-model or provider-routing warnings, and it does not replace the interactive confirmation prompt. Revoke it with `hermes config unset security.allow_data_training_tiers_noninteractive`.
- | **Compression** | When you're burning reasoning tokens on Opus/M2.7 just to summarize context. A fast chat model does the job at 1/50th the cost. |
- ```
model:
  provider: openrouter
  default: anthropic/claude-opus-4.7
  base_url: ''        # cleared on provider switch
  api_mode: chat_completions
```
- ```
auxiliary:
  vision:
    provider: openrouter
    model: google/gemini-2.5-flash
    base_url: ''
    api_key: ''
    timeout: 120
    extra_body: {}
    download_timeout: 30
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
