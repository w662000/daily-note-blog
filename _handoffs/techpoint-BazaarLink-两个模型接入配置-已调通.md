---
layout: default
title: 技术点 · BazaarLink 两个模型接入配置（已调通）
date: 2026-08-15 23:30:00 +0800
---

# 技术点 · BazaarLink 两个模型接入配置（已调通）

> 来源：260815_BazaarLink 两个模型接入配置（已调通）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **不是 AutoClaw 端 bug，也不是 key 失效**。根因见同目录 `bazaarlink调试_20260816.md`：Cloudflare 1010 封的是 UA/请求指纹。
- **DeepSeek V4 Flash** 和 **Qwen3.7 Flash** 都已在 WorkBuddy 环境用 bazaarlink 官方 API 调通。
- 之前偶发的 `free_global_rate_limited` / `429` 是 bazaarlink **全站免费模型额度瞬时满**，不是配置错。稍后重试即可恢复。
- | Base URL | `https://bazaarlink.ai/api/v1` |
- | API Key | `sk-bl--QiRGJ-4sUrg1c3ErN6loFuFZVYAMfGmbQZcXb4bbCzGxiIa` |
- | Authorization 头格式 | `Bearer <key>` |
- ```
model: deepseek-v4-flash
status: 200
usage: {"prompt_tokens":16,"total_tokens":117,"completion_tokens":101,"reasoning_tokens":100,"cost":0}
注意：content 字段可能为空，思考过程在 reasoning_content 中（DeepSeek-R1 风格）。
```
- ```
model returned: qwen/qwen3.7-flash
status: 200
content: Hi! I am Qwen, a large language model developed by Alibaba Group's Tongyi Lab...
```
- 2. **Base URL** 填 `https://bazaarlink.ai/api/v1`
- 3. **API Key** 填上面的 `sk-bl-...`
- | 403 | `1010` / `browser_signature_banned` | Cloudflare 封 UA/请求指纹 | 加正常浏览器 UA 头，不要用 Python-urllib 等脚本 UA |
- | 401 | `invalid_api_key` | 密钥错/失效 | 在 bazaarlink 控制台重新生成 key |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
