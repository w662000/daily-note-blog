---
layout: default
title: 技术点 · Hermes Agent Quickstart
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Hermes Agent Quickstart

> 来源：261010_Hermes Agent Quickstart_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```
- ```
iex (irm https://hermes-agent.nousresearch.com/install.ps1) 
```
- ```
source ~/.bashrc   # or source ~/.zshrc
```
- ```
hermes model
```
- ```
hermes setup --portal
```
- **Quick Setup (Nous Portal)** — OAuth login, no API keys to manage; sets up a model plus the Tool Gateway tools, billed to your [Nous Portal subscription](../integrations/nous-portal.md). The recommended fast path.
- **Full Setup** — walk through every provider, tool, and option yourself (bring your own keys).
- | **Anthropic** | Claude models directly — Max plan + extra usage credits (OAuth), or API key for pay-per-token | `hermes model` → OAuth login (requires Max + extra credits), or an Anthropic API key |
- | **OpenRouter** | Multi-provider routing across many models | Enter your API key |
- | **Fireworks AI** | Direct OpenAI-compatible model API | Set `FIREWORKS_API_KEY` |
- | **Z.AI** | GLM / Zhipu-hosted models | Set `GLM_API_KEY` / `ZAI_API_KEY` (also accepts `Z_AI_API_KEY`) |
- | **Kimi / Moonshot** | Moonshot-hosted coding and chat models | Set `KIMI_API_KEY` (or the Kimi-Coding-specific `KIMI_CODING_API_KEY`) |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
