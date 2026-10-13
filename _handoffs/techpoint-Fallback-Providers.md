---
layout: default
title: 技术点 · Fallback Providers
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Fallback Providers

> 来源：261010_Fallback Providers_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 1. **[Credential pools](./credential-pools.md)** — rotate across multiple API keys for the *same* provider (tried first)
- Credential pools handle same-provider rotation (e.g., multiple OpenRouter keys). This page covers cross-provider fallback. Both are optional and work independently.
- ```
hermes fallback
```
- ```
fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
```
- ```
fallback:
  min_switch_reset_seconds: 120   # 0 (default) = always switch
```
- | Key | Default | Effect |
- `google-ai-studio`. On Google's native API endpoint, all use the native Gemini
- `fallback_providers` (plural, list) is the current config shape and supports multiple fallbacks tried in order. `fallback_model` (singular) is the legacy single-fallback key — Hermes still honors it for back-compat, but `hermes fallback` writes the current `fallback_providers` key and migrates legacy config on write. When both are set, `fallback_providers` takes priority.
- | AI Gateway | `ai-gateway` | `AI_GATEWAY_API_KEY` |
- | OpenRouter | `openrouter` | `OPENROUTER_API_KEY` |
- | GitHub Copilot | `copilot` | `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN` |
- | Anthropic | `anthropic` | `ANTHROPIC_API_KEY` or Claude Code credentials |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
