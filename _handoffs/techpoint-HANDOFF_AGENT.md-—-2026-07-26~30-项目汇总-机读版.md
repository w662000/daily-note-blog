---
layout: default
title: 技术点 · HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）
date: 2026-07-29 23:30:00 +0800
---

# 技术点 · HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）

> 来源：260729_HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260729_HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）_handoff.md（编码探测：utf-8）
- > ⚠️ 本件为「时间轴打包」退化件（多天多项目汇总），按 2026-08-02 裁定 A 预置 bak 以堵幂等缺口，不作项目 handoff 外发。
- **26-28 已交付（11 项，详细 handoff 在 `D:\AI work\workbuddy\handoff\bak\`）**：云南旅居分析、Hermes Docker/Windows 部署、58 无锡爬虫、Wispbyte+gost 代理、Gaming4Free、Serv00 监控×2、bbs1org/phpBB MCP 论坛。
- **7-29 发布体系维护**：博客永久链接撞车修复(`:name` 替代 `:slug`)、Gridea 白屏修复(posts.json 索引重建)、7-28 论坛缺失补发。
- 1. 网关部署修复（better-sqlite3 ABI 错配；实例 `D:\Program Files\OmniRoute\OmniRoute.exe`；网关 `:20128/v1`；key `sk-e48c3ff46edc69cd-c29371-48eb33a9`；数据 `C:\Users\Administrator\AppData\Roaming\omniroute\`）。
- 2. 10 家 provider key 接入：OpenRouter/Groq/Cloudflare/智谱GLM/Gemini/NVIDIA/HuggingFace/Cerebras/Agnes/xAI。
- 6. Agnes 国内站接入（Base URL `https://api.agnes-ai.cn/v1`，4 模型）。
- 8. handoff 四端发布体系（handoff_flow.py + publish_forum_now.py，幂等）。
- 编码：`groq/llama-3.3-70b-versatile`、`openrouter/inclusionai/ling-3.0-flash:free`
- 1. OmniRoute 免费层 `auto` 路由硬卡死 → pin 具体模型。
- 4. Agnes 国内站 `https://api.agnes-ai.cn/v1`（非 apihub/非 .com）。
- 5. OmniRoute DATA_DIR 必须无空格路径；GUI 启动只能用户桌面双击。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
