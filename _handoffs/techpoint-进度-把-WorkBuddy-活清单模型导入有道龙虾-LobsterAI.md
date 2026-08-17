---
layout: default
title: 技术点 · 进度：把 WorkBuddy 活清单模型导入有道龙虾(LobsterAI)
date: 2026-08-17 23:30:00 +0800
---

# 技术点 · 进度：把 WorkBuddy 活清单模型导入有道龙虾(LobsterAI)

> 来源：260817_进度：把 WorkBuddy 活清单模型导入有道龙虾(LobsterAI)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 有道龙虾「JSON 导入模型」的真实机制 = 写入 `AppData\Roaming\LobsterAI\openclaw\state\openclaw.json` 的 `models.providers`（provider 模式：baseUrl+apiKey+models[]），**无需改 app.asar**。
- openclaw 的 `openai-completions` 是 base 直拼 `/chat/completions`（不自带 /v1）；参照 lobsterai-server base 末尾 `/v1`。DeepSeek 活清单 URL 为 `https://api.deepseek.com`（给 WB 客户端用，会自加 /v1），对 openclaw 须改成 `https://api.deepseek.com/v1`，已改。
- **重启有道龙虾** 让配置生效（启动时加载）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
- openclaw 的 `openai-completions` 是 base 直拼 `/chat/completions`（不自带 /v1）；参照 lobsterai-server base 末尾 `/v1`。DeepSeek 活清单 URL 为 `https://api.deepseek.com`（给 WB 客户端用，会自加 /v1），对 openclaw 须改成 `https://api.deepseek.com/v1`，已改。
