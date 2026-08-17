---
layout: default
title: 交接文档 · BazaarLink 两个模型接入配置（已调通）
date: 2026-08-17 23:30:00 +0800
---

# BazaarLink 两个模型接入配置（已调通）

- **日期**：2026-08-15
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-15-20-54-11\bazaarlink_模型接入_20260816.md

## 结论

- **不是 AutoClaw 端 bug，也不是 key 失效**。根因见同目录 `bazaarlink调试_20260816.md`：Cloudflare 1010 封的是 UA/请求指纹。
- **DeepSeek V4 Flash** 和 **Qwen3.7 Flash** 都已在 WorkBuddy 环境用 bazaarlink 官方 API 调通。
- 之前偶发的 `free_global_rate_limited` / `429` 是 bazaarlink **全站免费模型额度瞬时满**，不是配置错。稍后重试即可恢复。

---

## 推荐配置（在 AutoClaw 中填写）

### 通用参数

| 项 | 值 |
|---|---|
| Base URL | `https://bazaarlink.ai/api/v1` |
| API Key | `sk-bl--QiRGJ-4sUrg1c3ErN6loFuFZVYAMfGmbQZcXb4bbCzGxiIa` |
| Authorization 头格式 | `Bearer <key>` |
| 必须额外加的请求头 | `X-Free-Fallback: false` |
| 建议的 User-Agent | 任意正常浏览器/产品 UA，例如 `Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...` |

### 两个模型的 ID

| 显示名 | 推荐填写的 model ID | 实测状态 |
|---|---|---|
| DeepSeek: Deepseek V4 Flash | `deepseek-v4-flash` | ✅ 200，返回 `model: deepseek/deepseek-v4-flash` |
| Qwen: Qwen3.7 Flash | `qwen/qwen3.7-flash` | ✅ 200，回复正常 |

---

## 实测记录（WorkBuddy managed Node.js）

### DeepSeek V4 Flash
```text
model: deepseek-v4-flash
status: 200
usage: {"prompt_tokens":16,"total_tokens":117,"completion_tokens":101,"reasoning_tokens":100,"cost":0}
注意：content 字段可能为空，思考过程在 reasoning_content 中（DeepSeek-R1 风格）。
```

### Qwen3.7 Flash
```text
model returned: qwen/qwen3.7-flash
status: 200
content: Hi! I am Qwen, a large language model developed by Alibaba Group's Tongyi Lab...
```

---

## AutoClaw 配置建议

1. **添加 Provider 时选择 "OpenAI Compatible" / "自定义 OpenAI 兼容"**
2. **Base URL** 填 `https://bazaarlink.ai/api/v1`
3. **API Key** 填上面的 `sk-bl-...`
4. **自定义请求头 (Custom Headers)** 必须加：
   - `X-Free-Fallback: false`
   - `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36`
5. **模型 ID** 分别填 `deepseek-v4-flash` 和 `qwen/qwen3.7-flash`
6. 保存后先点 **Test / 验证** 看 `/models` 能不能通；如果还是 403/1010，优先检查 `User-Agent` 头有没有被 AutoClaw 转发层覆盖/丢失。

---

## 错误码速查

| HTTP | 错误码 | 含义 | 怎么办 |
|---|---|---|---|
| 403 | `1010` / `browser_signature_banned` | Cloudflare 封 UA/请求指纹 | 加正常浏览器 UA 头，不要用 Python-urllib 等脚本 UA |
| 401 | `invalid_api_key` | 密钥错/失效 | 在 bazaarlink 控制台重新生成 key |
| 429 | `free_global_rate_limited` | 全站免费额度满 | 等几分钟重试，或换付费模型 |
| 402 | `insufficient_credits` | 余额不足 | 充值或换 `:free` 后缀模型 |

---

## 可用但没必要填的备选 ID

`/models` 返回的相关 ID 很多，以下也能工作，但 AutoClaw 里直接按上面推荐填即可：
- `deepseek/deepseek-v4-flash:free`
- `deepseek/deepseek-v4-flash`
- `deepseek-v4-flash-0731`
- `qwen3.7-flash`
- `qwen/qwen3.7-flash:free`

**不推荐带 `:free` 后缀的作为主力**，因为它们更容易触发 `free_global_rate_limited` / `Free model daily limit reached`。
