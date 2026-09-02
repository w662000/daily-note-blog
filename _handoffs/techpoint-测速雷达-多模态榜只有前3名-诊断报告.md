---
layout: default
title: 技术点 · 测速雷达「多模态榜只有前3名」诊断报告
date: 2026-08-29 23:30:00 +0800
---

# 技术点 · 测速雷达「多模态榜只有前3名」诊断报告

> 来源：260829_测速雷达「多模态榜只有前3名」诊断报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 项目：D:\AI work\workbuddy\model-speed-radar（端口 8848）
- 接口 `/api/aggregated` 实测返回：`window: 5/5`，`text: 5` 条，`multi: 5` 条 —— 后端数据是满的。
- | 模型 | 报错 | 性质 |
- | gemini-3.1-flash-lite | HTTP 400 `User location is not supported for the API use.` | 大陆 IP 地区封锁，无解（除非换出口） |
- | thinkingmachines/inkling | HTTP 410 | 模型已下线，应从配置移除 |
- | nvidia/nemotron-3-super-120b-a12b | `'latin-1' codec can't encode character '\u2026' in position 13` | **配置 bug，见下节** |
- | 模型 | 长期失败率 | 本轮报错 |
- ```
"id": "nvidia/nemotron-3-super-120b-a12b",
"apiKey": "nvapi-…oR5T"     ← 长度只有 11，中间是 U+2026 省略号
```
- 这个 key 当初被人为用 `…` 截断保存了。后果：
- 1. urllib 发请求时 header `Authorization: Bearer nvapi-…oR5T` 含非 ASCII 字符
- 2. `http.client` 用 latin-1 编码 header，第 13 位（正好是 `…`）直接抛异常
- 报错 position 13 完全吻合（`Bearer nvapi-` 是 0~12，`…` 落在 13）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
