---
layout: default
title: 技术点 · 进度 — b.ai 接入 DSH + Hermes（2026-08-18 13:05）
date: 2026-08-18 23:30:00 +0800
---

# 技术点 · 进度 — b.ai 接入 DSH + Hermes（2026-08-18 13:05）

> 来源：260818_进度 — b.ai 接入 DSH + Hermes（2026-08-18 13_05）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 用户提供 b.ai API key（sk-jfsms...），要求只接入 `deepseek-v4-flash` 一个模型。
- `~/.workbuddy/models.json` 加 b.ai 条目，id=`deepseek-v4-flash`（裸名，与 API 一致）。
- **踩坑**：最初 id 写成 `b.ai/deepseek-v4-flash` → WB 把前缀直接发给 API → b.ai 返回 404 model_not_found。已改为裸名；原 SenseNova 同名条目改名 `deepseek-v4-flash-sensenova` 避撞。
- `~/.dsh/.credentials.yaml`：追加 `WB_KEY_11: sk-jfsms...`（b.ai key）。
- ```
  b-ai:
    apiKeyEnv: WB_KEY_11
    displayName: '[b.ai] DeepSeek-V4-Flash'
    api: openai-completions
    baseURL: https://api.b.ai/v1
    models:
      - id: deepseek-v4-flash
        name: '[b.ai] DeepSeek-V4-Flash'
        input: [text]
```
- ```
  - name: b-ai
    base_url: https://api.b.ai/v1
    api_key: sk-jfsms...
    models: [deepseek-v4-flash]
    discover_models: false
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
