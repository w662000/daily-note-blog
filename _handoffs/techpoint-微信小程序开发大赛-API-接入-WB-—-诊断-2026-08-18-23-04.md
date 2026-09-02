---
layout: default
title: 技术点 · 微信小程序开发大赛 API 接入 WB — 诊断(2026-08-18 23:04)
date: 2026-08-18 23:30:00 +0800
---

# 技术点 · 微信小程序开发大赛 API 接入 WB — 诊断(2026-08-18 23:04)

> 来源：260818_微信小程序开发大赛 API 接入 WB — 诊断(2026-08-18 23_04)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：2026-08-18-12-42-34\进度_20260818_2304_微信大赛API.md
- 2. **`GLM-5.2` 也存在,但当前 token 无权限**:实测返回 `user has no access`(429)。不是名字错,是 token 没被授权(可能还没开通,或本次比赛 token 只给 Deepseek-v4-flash)。
- 这说明该 API **严格大小写敏感**,且后台显示的拼写就是真实 model id。
- 字段只有:`id, name, vendor, url, apiKey, supportsToolCall, supportsImages, supportsReasoning, useCustomProtocol, caps`。**无独立 `model` 覆盖字段** → `id` 即发给 API 的 model 名。
- 现有 `id='GLM-5.2'` 条目:`vendor=SenseNova, url=https://token.sensenova.cn/v1`。
- A: 把现有 GLM-5.2 槽位改成 WeChat(改 url+apiKey,id 保持 GLM-5.2,显示名改 [WeChat] GLM-5.2)—— 会丢失 SenseNova 的 GLM-5.2。
- B: 保留 SenseNova,不往 WB 加 WeChat(已有 GLM-5.2 可用,但走的是 SenseNova 不是比赛 token)。
- C: 用户先去 chatapi.weixin.qq.com 后台确认 token 已激活、GLM-5.2 已开通,再决定。
- `url` 保持 `https://chatapi.weixin.qq.com/openai/v1`(无尾斜杠,对齐 OpenAI 兼容约定)。
- **遗留**:若后台之后开通 `GLM-5.2`,可再追加一条 `id='GLM-5.2'`(大写,与 SenseNova 的 `glm-5.2` 不撞车);目前该 token 调 `GLM-5.2` 仍返回 429 `user has no access`。
- 端点:`https://chatapi.weixin.qq.com/openai/v1/chat/completions`(OpenAI 兼容)
- key:`Vz9uhggBEAEaIAgBEhwxNzg3MDY1Mjk1MTk4MzAwNDMzOE9BdlNkV2Y5IhgIAxIUCAMSEA+H/iNO3ic9JBkQyWuufRg=`(敏感,仅本次会话使用,勿外泄)

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
