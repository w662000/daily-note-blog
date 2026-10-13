---
layout: default
title: 技术点 · Environment Variables Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Environment Variables Reference

> 来源：261010_Environment Variables Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Hermes reads environment variables from the process environment and, for user-managed secrets, from `~/.hermes/.env`. Keep API keys, bot tokens, OAuth secrets, and other credentials in `.env`; prefer `config.yaml` for non-secret behaviour settings when a config key exists. Some variables below are process-only overrides or internal bridge variables and should not be committed to `.env` just because they are documented here.
- | `OPENROUTER_API_KEY` | OpenRouter API key (recommended for flexibility) |
- | `FIREWORKS_API_KEY` | Fireworks AI API key ([app.fireworks.ai](https://app.fireworks.ai/settings/users/api-keys)). Configure endpoint overrides with `model.base_url` in `config.yaml`. |
- | `AI_GATEWAY_API_KEY` | Vercel AI Gateway API key ([ai-gateway.vercel.sh](https://ai-gateway.vercel.sh)) |
- | `OPENAI_API_KEY` | API key for custom OpenAI-compatible endpoints (used with `OPENAI_BASE_URL`) |
- | `LM_API_KEY` | API key for LM Studio (`lmstudio` provider). Often a placeholder for local servers |
- | `COPILOT_GITHUB_TOKEN` | GitHub token for Copilot API — first priority (OAuth `gho_*` or fine-grained PAT `github_pat_*`; classic PATs `ghp_*` are **not supported**) |
- | `GH_TOKEN` | GitHub token — second priority for Copilot (also used by `gh` CLI) |
- | `GITHUB_TOKEN` | GitHub token — third priority for Copilot |
- | `COPILOT_API_BASE_URL` | Override the Copilot API base URL (`copilot` provider) |
- | `GLM_API_KEY` | z.ai / ZhipuAI GLM API key ([z.ai](https://z.ai)) |
- | `ZAI_API_KEY` | Alias for `GLM_API_KEY` |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
