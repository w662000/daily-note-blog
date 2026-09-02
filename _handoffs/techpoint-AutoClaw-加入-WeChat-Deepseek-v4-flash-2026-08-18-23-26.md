---
layout: default
title: 技术点 · AutoClaw 加入 [WeChat] Deepseek-v4-flash（2026-08-18 23:26）
date: 2026-08-18 23:30:00 +0800
---

# 技术点 · AutoClaw 加入 [WeChat] Deepseek-v4-flash（2026-08-18 23:26）

> 来源：260818_AutoClaw 加入 [WeChat] Deepseek-v4-flash（2026-08-18 23_26）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **模型配置真身**：`C:\Users\Administrator\.openclaw-autoclaw\openclaw.json` → `models.providers`（dict，key=`<provider>__<uuid>`，apiKey **明文**）
- `AppData\Roaming\autoclaw\settings.json` 的 `models.catalog` 只是 UI 视图，由 openclaw.json 自动同步生成，**不要手动改**
- ```
"wechat__6d8ca8d1-963a-48ff-910a-1bfb7ebee082": {
  "baseUrl": "https://chatapi.weixin.qq.com/openai/v1",
  "api": "openai-completions",
  "apiKey": "Vz9uhg...(微信大赛key)",
  "models": [{
    "id": "Deepseek-v4-flash",
    "name": "[WeChat] Deepseek-v4-flash (小程序大赛)",
    "contextWindow": 200000,
    "maxTokens": 32000,
    "reasoning": true
  }]
}
```
- 重启 AutoClaw（当前 6 个进程运行中，装在 D:\Program Files\AutoClaw\）。重启后模型列表应见 `[WeChat] Deepseek-v4-flash (小程序大赛)`。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
