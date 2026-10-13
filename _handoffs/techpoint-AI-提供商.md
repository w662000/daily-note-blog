---
layout: default
title: 技术点 · AI 提供商
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · AI 提供商

> 来源：261010_AI 提供商_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 本页介绍如何为 Hermes Agent 配置推理提供商——从 OpenRouter、Anthropic 等云端 API，到 Ollama、vLLM 等自托管端点，再到高级路由与故障转移配置。使用 Hermes 至少需要配置一个提供商。
- 你需要至少一种方式连接到 LLM。使用 `hermes model` 交互式切换提供商和模型，或直接配置：
- | 提供商 | 配置方式 |
- | **GitHub Copilot** | `hermes model`（OAuth 设备码流程，`COPILOT_GITHUB_TOKEN`、`GH_TOKEN` 或 `gh auth token`） |
- | **GitHub Copilot ACP** | `hermes model`（在本地生成 `copilot --acp --stdio` 子进程） |
- | **Anthropic** | `hermes model`（Claude Max + 额外用量积分，通过 OAuth；也支持 Anthropic API key 或手动 setup-token——见下方说明） |
- | **OpenRouter** | `~/.hermes/.env` 中的 `OPENROUTER_API_KEY` |
- | **NovitaAI** | `~/.hermes/.env` 中的 `NOVITA_API_KEY`（provider: `novita`，200+ 模型，Model API、Agent Sandbox、GPU Cloud） |
- | **AI Gateway** | `~/.hermes/.env` 中的 `AI_GATEWAY_API_KEY`（provider: `ai-gateway`） |
- | **z.ai / GLM** | `~/.hermes/.env` 中的 `GLM_API_KEY`（provider: `zai`） |
- | **Kimi / Moonshot** | `~/.hermes/.env` 中的 `KIMI_API_KEY`（provider: `kimi-coding`） |
- | **Kimi / Moonshot（中国）** | `~/.hermes/.env` 中的 `KIMI_CN_API_KEY`（provider: `kimi-coding-cn`；别名：`kimi-cn`、`moonshot-cn`） |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
