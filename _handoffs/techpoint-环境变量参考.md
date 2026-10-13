---
layout: default
title: 技术点 · 环境变量参考
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · 环境变量参考

> 来源：261010_环境变量参考_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- title: "环境变量"
- description: "Hermes Agent 使用的所有环境变量完整参考"
- | `OPENROUTER_API_KEY` | OpenRouter API 密钥（推荐，灵活性强） |
- | `AI_GATEWAY_API_KEY` | Vercel AI Gateway API 密钥（[ai-gateway.vercel.sh](https://ai-gateway.vercel.sh)） |
- | `OPENAI_API_KEY` | 自定义 OpenAI 兼容端点的 API 密钥（与 `OPENAI_BASE_URL` 配合使用） |
- | `COPILOT_GITHUB_TOKEN` | 用于 Copilot API 的 GitHub token——最高优先级（OAuth `gho_*` 或细粒度 PAT `github_pat_*`；经典 PAT `ghp_*` **不支持**） |
- | `GH_TOKEN` | GitHub token——Copilot 第二优先级（也供 `gh` CLI 使用） |
- | `GITHUB_TOKEN` | GitHub token——Copilot 第三优先级 |
- | `HERMES_COPILOT_ACP_COMMAND` | 覆盖 Copilot ACP CLI 二进制路径（默认：`copilot`） |
- | `GLM_API_KEY` | z.ai / ZhipuAI GLM API 密钥（[z.ai](https://z.ai)） |
- | `ZAI_API_KEY` | `GLM_API_KEY` 的别名 |
- | `Z_AI_API_KEY` | `GLM_API_KEY` 的别名 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
