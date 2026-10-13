---
layout: default
title: 技术点 · Plugin compatibility manifest (temporary)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Plugin compatibility manifest (temporary)

> 来源：261010_Plugin compatibility manifest (temporary)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- files. **Internal import paths are not a stable API**, and after that PR the names below are no
- to the public equivalent or the new module. Test monkeypatch seams are likewise not preserved.
- | `is_claude_code_token_valid` | moved-lazy | `agent.anthropic_credentials` |
- | `resolve_anthropic_token` | moved-lazy | `agent.anthropic_credentials` |
- | `run_oauth_setup_token` | moved-lazy | `agent.anthropic_credentials` |
- | `hermes_home_key` | moved-lazy | `hermes_constants` |
- | `COMPRESSION_RETRY_TOKENS_STATUS_TEMPLATE` | moved-lazy | `agent.conversation_compression` |
- | `PRE_API_COMPRESSION_STATUS_TEMPLATE` | moved-lazy | `agent.conversation_compression` |
- | `anchored_context_tokens` | moved-lazy | `agent.model_metadata` |
- | `classify_api_error` | moved-lazy | `agent.error_classifier` |
- | `compose_user_api_content` | moved-lazy | `agent.turn_context` |
- | `estimate_messages_tokens_rough` | moved-lazy | `agent.model_metadata` |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
