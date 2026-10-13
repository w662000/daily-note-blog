---
layout: default
title: 技术点 · CLI Commands Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · CLI Commands Reference

> 来源：261010_CLI Commands Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
hermes [global-options] <command> [subcommand/options]
```
- | `--resume <session>`, `-r <session>` | Resume a previous session by ID or title. The keyword `latest` resumes the most recent session (workspace-scoped, same lookup as `-c`). |
- | `hermes whatsapp-cloud` | Configure the official Meta WhatsApp Business Cloud API adapter (Business account + public webhook required). Distinct from `hermes whatsapp` (Baileys personal-account bridge). |
- | `hermes secrets` | Manage external secret sources (currently Bitwarden Secrets Manager) for pulling API keys at process startup instead of from `~/.hermes/.env`. |
- | `hermes insights` | Show token/cost/activity analytics. |
- | `hermes dashboard` | Launch the web dashboard for managing config, API keys, and sessions. |
- ```
hermes chat [options]
```
- | `--provider <provider>` | Force a provider: `auto`, `openrouter`, `nous`, `openai-codex` (aliases `chatgpt`, `chatgpt-codex`), `copilot-acp`, `copilot`, `anthropic`, `gemini`, `huggingface`, `novita` (aliases `novita-ai`, `novitaai`), `openai-api`, `zai`, `kimi-coding`, `kimi-coding-cn`, `minimax`, `minimax-cn`, `minimax-oauth`, `kilocode`, `xiaomi`, `arcee`, `gmi`, `upstage` (alias `solar`), `alibaba`, `alibaba-cn`, `alibaba-coding-plan` (alias `alibaba_coding`), `alibaba-coding-plan-cn`, `alibaba-token-plan`, `alibaba-token-plan-cn`, `deepseek`, `nvidia`, `ollama-cloud`, `xai` (alias `grok`), `xai-oauth` (alias `grok-oauth`), `qwen-oauth`, `bedrock`, `opencode-zen`, `opencode-go`, `commandcode`, `commandcode-anthropic`, `ai-gateway`, `azure-foundry`, `lmstudio`, `stepfun`, `tencent-tokenhub` (alias `tencent`, `tokenhub`), `router` (aliases `ramp-router`, `ramp`), `nebius-token-factory` (aliases `nebius`, `nebius-tf`, `tokenfactory`), `tencent-tokenplan` (aliases `tokenplan`, `tencent-lkeap`). |
- ```
hermes
hermes chat -q "Summarize the latest PRs"          # seeds an interactive session
hermes chat --oneshot -q "Summarize the latest PRs"  # answer and exit
hermes chat --provider openrouter --model anthropic/claude-sonnet-4.6
hermes chat --toolsets web,terminal,skills
hermes chat --quiet -q "Return only JSON"
hermes chat -q "Inspect this repository" --format stream-json
hermes chat --worktree -q "Review this repo and open a PR"
hermes chat --ignore-user-config --ignore-rules -q "Repro without my personal setup"
hermes chat --safe-mode -q "Is this bug mine or Hermes'?"
```
- scraping terminal output. It requires `-q` / `--query` (or `--query-file`), implies
- ```
hermes chat -q "Summarize this repository" --format stream-json
```
- | `result` | `session_id`, `exit_code`, `text`, `tokens` (`input`, `output`, `total`, `cache_read`, `cache_write`), `duration_ms`; `error` when the turn failed |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
