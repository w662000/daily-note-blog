---
layout: default
title: 技术点 · LLM and Model Providers
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · LLM and Model Providers

> 来源：261010_LLM and Model Providers_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- This page covers setting up inference providers for Hermes Agent — from cloud APIs like OpenRouter and Anthropic, to self-hosted endpoints like Ollama and vLLM, to advanced routing and fallback configurations. You need at least one provider configured to use Hermes.
- | **GitHub Copilot** | `hermes model` (OAuth device code flow, `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `gh auth token`) |
- | **Anthropic** | `hermes model` (Claude Max + extra usage credits via OAuth; also supports Anthropic API key or manual setup-token — see note below) |
- | **OpenRouter** | `OPENROUTER_API_KEY` in `~/.hermes/.env`, or `hermes auth add openrouter --type oauth` (browser login via OpenRouter's PKCE flow; stores a key in the credential pool) |
- | **Ramp Router** | `RAMP_ROUTER_API_KEY` in `~/.hermes/.env` (provider: `router`; aliases: `ramp-router`, `ramp`, `router.com`; Responses-native gateway, live account-scoped catalog) |
- | **Fireworks AI** | `FIREWORKS_API_KEY` in `~/.hermes/.env` (provider: `fireworks`; aliases: `fireworks-ai`, `fw`) |
- | **NovitaAI** | `NOVITA_API_KEY` in `~/.hermes/.env` (provider: `novita`, 200+ models, Model API, Agent Sandbox, GPU Cloud) |
- | **AI Gateway** | `AI_GATEWAY_API_KEY` in `~/.hermes/.env` (provider: `ai-gateway`) |
- | **z.ai / GLM** | `GLM_API_KEY` in `~/.hermes/.env` (provider: `zai`) |
- | **Kimi / Moonshot** | `KIMI_API_KEY` in `~/.hermes/.env` (provider: `kimi-coding`) |
- | **Kimi / Moonshot (China)** | `KIMI_CN_API_KEY` in `~/.hermes/.env` (provider: `kimi-coding-cn`; aliases: `kimi-cn`, `moonshot-cn`) |
- | **Arcee AI** | `ARCEEAI_API_KEY` in `~/.hermes/.env` (provider: `arcee`; aliases: `arcee-ai`, `arceeai`) |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
