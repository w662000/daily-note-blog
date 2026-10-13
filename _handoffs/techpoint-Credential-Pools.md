---
layout: default
title: 技术点 · Credential Pools
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Credential Pools

> 来源：261010_Credential Pools_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: Pool multiple API keys or OAuth tokens per provider for automatic rotation and rate limit recovery.
- Credential pools let you register multiple API keys or OAuth tokens for the same provider. When one key hits a rate limit or billing quota, Hermes automatically rotates to the next healthy key — keeping your session alive without switching providers.
- This is different from [fallback providers](./fallback-providers.md), which switch to a *different* provider entirely. Credential pools are same-provider rotation; fallback providers are cross-provider failover. Pools are tried first — if all pool keys are exhausted, *then* the fallback provider activates.
- :::warning Key rotation resets the prompt cache
- Provider-side prompt caches (Anthropic, OpenAI, OpenRouter) are scoped to the account/API key that made the request. When the pool rotates to a different key mid-session, the new key has no cached prefix for your conversation — the next request re-reads the full history at undiscounted input price, and rotating back later is another full re-read unless the earlier key's cache TTL is still alive. Rotation keeps your session running, which is the point, but on long conversations each rotation costs one full-price pass over the context.
- Credential pools are mainly for API-key providers (OpenRouter, Anthropic). A single [Nous Portal](../../integrations/nous-portal.md) OAuth covers 300+ models, so most users don't need a pool when on Portal.
- ```
Your request
  → Pick key from pool (round_robin / least_used / fill_first / random)
  → Send to provider
  → 429 rate limit?
      → Plan/usage limit reached (e.g. ChatGPT/Codex "usage limit reached")?
          → Rotate to next pool key immediately (no retry — the cap won't clear on retry)
      → Generic / transient 429?
          → Retry same key once (transient blip)
          → Second 429 → rotate to next pool key
      → All keys exhausted → fallback_model (different provider)
  → 402 billing error?
      → Immediately rotate to next pool key (1h cooldown)
  → 401 auth expired?
      → Try refreshing the token (OAuth)
      → Refresh failed → rotate to next pool key
  → 400 "model is not supported when using Codex with a ChatGPT account"?
      → Bench this key for that model only, rotate to the next key (other models stay usable)
      → Every key rejects the model → fallback_model; the model is skipped for the session
  → HTTP 200 but `response.status: failed` (ChatGPT/Codex reports usage limits this way)?
      → Same rules as above, keyed on the embedded error code/message:
        quota/billing/auth → pool rotation first, provider fallback only once the pool is exhausted;
        content-policy and other failures → no rotation
  → Success → continue normally
```
- If you already have an API key set in `.env`, Hermes auto-discovers it as a 1-key pool. To benefit from pooling, add more keys:
- ```
# Add a second OpenRouter key
hermes auth add openrouter --api-key sk-or-v1-your-second-key

# ...or let a browser login mint one (OpenRouter OAuth PKCE; stored as a plain API key)
hermes auth add openrouter --type oauth

# Add a second Anthropic key
hermes auth add anthropic --type api-key --api-key sk-ant-api03-your-second-key

# Add an Anthropic OAuth credential (requires Claude Max plan + extra usage credits)
hermes auth add anthropic --type oauth
# Opens browser for OAuth login
```
- ```
hermes auth list
```
- ```
openrouter (2 credentials):
  #1  OPENROUTER_API_KEY   api_key id=ab12cd34 priority=0 env:OPENROUTER_API_KEY ←
  #2  backup-key           api_key id=ef56gh78 priority=1 manual

anthropic (3 credentials):
  #1  hermes_pkce          oauth   id=ab12cd34 priority=0 hermes_pkce ←
  #2  claude_code          oauth   id=cd34ef56 priority=1 claude_code
  #3  ANTHROPIC_API_KEY    api_key id=ef56gh78 priority=2 env:ANTHROPIC_API_KEY
```
- ```
hermes auth
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
