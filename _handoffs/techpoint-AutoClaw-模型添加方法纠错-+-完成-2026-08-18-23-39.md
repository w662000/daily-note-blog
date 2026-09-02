---
layout: default
title: 技术点 · AutoClaw 模型添加方法纠错 + 完成（2026-08-18 23:39）
date: 2026-08-18 23:30:00 +0800
---

# 技术点 · AutoClaw 模型添加方法纠错 + 完成（2026-08-18 23:39）

> 来源：260818_AutoClaw 模型添加方法纠错 + 完成（2026-08-18 23_39）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
往 settings.json 的 models.catalog 追加（字段对齐现有 sensenova 条目）：
```json
{
  "provider": "wechat",
  "model": "Deepseek-v4-flash",
  "alias": "[WeChat] Deepseek-v4-flash (小程序大赛)",
  "apiKey": "<明文微信key>",
  "baseUrl": "https://chatapi.weixin.qq.com/openai/v1",
  "api": "openai-completions",
  "isCustom": true,
  "configId": "33f001d6-82ee-4864-bc94-41adca4f75d8",
  "reasoning": true
}
```
以及 b-ai 条目（configId=62b5c153-8656-4dd1-bd9b-a134e6b19222）。

### 关键技术要点（自动抽取）
- `index.js:31520` withSafeEncryptedSecrets 写盘自动加密明文 key
- `index.js:742` getGatewayProviderKey = `provider__configId`
- ```
{
  "provider": "wechat",
  "model": "Deepseek-v4-flash",
  "alias": "[WeChat] Deepseek-v4-flash (小程序大赛)",
  "apiKey": "<明文微信key>",
  "baseUrl": "https://chatapi.weixin.qq.com/openai/v1",
  "api": "openai-completions",
  "isCustom": true,
  "configId": "33f001d6-82ee-4864-bc94-41adca4f75d8",
  "reasoning": true
}
```
- 写盘后 AutoClaw 运行中自动把明文 key 加密成 enc:（已核实非空）

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
