---
layout: default
title: 交接文档 · bazaarlink 模型聚合网关接入参考
date: 2026-10-13 23:30:00 +0800
---

# bazaarlink 模型聚合网关接入参考

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\hermes-model-management\references\bazaarlink-provider-setup.md

> 来源：2026-08-15 实际接入记录
> 目标：将 bazaarlink.ai 作为 Hermes config.yaml 的 custom_providers 接入

## 基本信息

| 项 | 值 |
|---|---|
| Base URL | `https://bazaarlink.ai/api/v1` |
| API Key 前缀 | `sk-bl-` |
| 鉴权方式 | `Authorization: Bearer <key>` |
| 协议 | OpenAI Chat Completions 兼容 |
| 本机接入的模型 | `deepseek-v4-flash`、`qwen/qwen3.7-flash` |

## config.yaml 配置格式

```yaml
custom_providers:
  - name: bazaarlink
    base_url: https://bazaarlink.ai/api/v1
    api_key: sk-bl-你的Key
    models:
      - id: deepseek-v4-flash
        label: "[bazaarlink] DeepSeek V4 Flash"
      - id: qwen/qwen3.7-flash
        label: "[bazaarlink] Qwen3.7 Flash"
```

## 注意事项

### 必须带 User-Agent 头
bazaarlink 网关有 UA 校验（类似 Groq 的 Cloudflare 1010 问题），必须带 Chrome UA，否则可能 403。Hermes 的 `custom_providers` 配置不支持直接设置 headers，但 Hermes 默认会使用通用 UA。

### 免费模型容量限制
`qwen/qwen3.7-flash` 有全站免费容量限制，繁忙时返回：
```
The site-wide free-model capacity is currently full.
```
此时需改用付费模型或稍后重试。

### 模型 ID 以 API 返回为准
请求时用 `deepseek-v4-flash`，但 API 返回的模型名是 `deepseek/deepseek-v4-flash`（带厂商前缀）。两套 ID 都可用，以 API 实际返回为准。

### DeepSeek V4 Flash 是 reasoning 模型
返回中有 `reasoning_content` 字段，max_tokens 需给足（≥300），否则只返回推理过程不生成文本。
