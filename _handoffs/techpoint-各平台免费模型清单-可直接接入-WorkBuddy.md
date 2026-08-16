---
layout: default
title: 技术点 · 各平台免费模型清单（可直接接入 WorkBuddy）
date: 2026-07-30 23:30:00 +0800
---

# 技术点 · 各平台免费模型清单（可直接接入 WorkBuddy）

> 来源：260730_各平台免费模型清单_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260730_各平台免费模型清单_handoff.md（编码探测：utf-8）
- > 数据来源：桌面 `1.txt` 里的 key + 平台官方 `/v1/models` 实时拉取（2026-07-30 晚）。
- > - ✅实测 = 本机用该 key 真实拉到 `/v1/models`
- > - 免费指"不按 token 计费"（多数有速率限制 / 每日配额）
- | **xAI (grok)** | — | — | — | ⚠️ key 有效但团队无额度，暂无免费模型 |
- > OpenRouter 接入：`url=https://openrouter.ai/api/v1`，`apiKey=sk-or-v1-...`（桌面 key 文件第4行）
- > NVIDIA 接入：`url=https://integrate.api.nvidia.com/v1`，`apiKey=nvapi-...`（桌面 key 文件第60行）
- 其中 `glm-4.5-air` 是已知免费层模型（已在 OmniRoute 用）；`glm-4.x+` 多为按量计费，免费层常见为 `glm-4-flash`/`glm-4-air`/`glm-4v-flash`（本 key 未列出，需在智谱控制台确认免费额度）。
- > 接入：`url=https://open.bigmodel.cn/api/paas/v4`，`apiKey=glm的key`（桌面第19行，格式 `xxxx.xxxx`）
- > 接入：`url=https://generativelanguage.googleapis.com/v1beta/openai/`，`apiKey=AQ.Ab8...`（桌面第16行）
- > 接入：`url=https://api.agnes-ai.cn/v1`，`apiKey=sk-vZIQ9...`（国内站 key，桌面第69行）
- > 接入：`url=https://api.groq.com/openai/v1`，`apiKey=gsk_...`（桌面第10行）。**注意：当前网络环境 Groq 直接 403，你可能仍需走代理或换网络。**

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
