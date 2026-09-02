---
layout: default
title: 技术点 · [WeChat] Deepseek-v4-flash 接入 DSH + Hermes（2026-08-18 23:22）
date: 2026-08-18 23:30:00 +0800
---

# 技术点 · [WeChat] Deepseek-v4-flash 接入 DSH + Hermes（2026-08-18 23:22）

> 来源：260818_[WeChat] Deepseek-v4-flash 接入 DSH + Hermes（2026-08-18 23_22）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- url: `https://chatapi.weixin.qq.com/openai/v1`
- apiKey: Vz9uhg...（敏感，写入 .credentials.yaml / hermes config.yaml，勿外泄）
- 1. `~/.dsh/.credentials.yaml` → 追加 `WB_KEY_12: <key>`（WB_KEY_1..11 → 12）
- 2. `~/.dsh/settings.yaml` → `llm-pi-ai.providers.wechat`（apiKeyEnv=WB_KEY_12, baseURL=chatapi.weixin.qq.com/openai/v1, models=[Deepseek-v4-flash]）

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
