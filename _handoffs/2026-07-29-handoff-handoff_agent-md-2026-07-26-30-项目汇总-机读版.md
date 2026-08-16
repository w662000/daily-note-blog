---
layout: default
title: 交接文档 · HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）
date: 2026-08-16 23:30:00 +0800
---

# HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）

- **日期**：2026-07-29
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260729_HANDOFF_AGENT.md — 2026-07-26~30 项目汇总（机读版）_handoff.md（编码探测：utf-8）

> 来源：项目文档 `2026-07-29-23-09-10\HANDOFF_AGENT.md`
> 由 handoff_flow.py（scan 阶段）自动收集，标题取自文档 H1（即主要干的活），待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。
> ⚠️ 本件为「时间轴打包」退化件（多天多项目汇总），按 2026-08-02 裁定 A 预置 bak 以堵幂等缺口，不作项目 handoff 外发。


> 给 Hermes / 后续 agent 快速定位用。人类可读版见 HANDOFF.md。

## 项目分组
- **26-28 已交付（11 项，详细 handoff 在 `D:\AI work\workbuddy\handoff\bak\`）**：云南旅居分析、Hermes Docker/Windows 部署、58 无锡爬虫、Wispbyte+gost 代理、Gaming4Free、Serv00 监控×2、bbs1org/phpBB MCP 论坛。
- **7-29 发布体系维护**：博客永久链接撞车修复(`:name` 替代 `:slug`)、Gridea 白屏修复(posts.json 索引重建)、7-28 论坛缺失补发。
- **7-30 核心：OmniRoute 多平台模型网关接入线**：
  1. 网关部署修复（better-sqlite3 ABI 错配；实例 `D:\Program Files\OmniRoute\OmniRoute.exe`；网关 `:20128/v1`；key `sk-e48c3ff46edc69cd-c29371-48eb33a9`；数据 `C:\Users\Administrator\AppData\Roaming\omniroute\`）。
  2. 10 家 provider key 接入：OpenRouter/Groq/Cloudflare/智谱GLM/Gemini/NVIDIA/HuggingFace/Cerebras/Agnes/xAI。
  3. 三端链路：平台→OmniRoute:20128→WorkBuddy(models.json) 与 Hermes(:8642, custom_providers.omniroute)。
  4. WorkBuddy 多模型接入（models.json 第 303-331 行 OmniRoute 3 条 + Agnes 4 模型 + 各平台免费强模型）。
  5. Hermes 接入 OmniRoute（config.yaml 第 152-185 行，19 模型；`--provider omniroute` 显式锁定）。
  6. Agnes 国内站接入（Base URL `https://api.agnes-ai.cn/v1`，4 模型）。
  7. 各平台免费模型大盘点（OpenRouter 真免费 17 / NVIDIA 102 / GLM 8 / Gemini 59 / Agnes 4；已单发四端，现归档 bak）。
  8. handoff 四端发布体系（handoff_flow.py + publish_forum_now.py，幂等）。

## 强模型精选（接 WorkBuddy 优先）
- 超长上下文：`nvidia/nemotron-3-ultra-550b-a55b:free`（1M）
- 编码：`groq/llama-3.3-70b-versatile`、`openrouter/inclusionai/ling-3.0-flash:free`
- 推理：`agnes-2.5-pro-alpha`、`cloudflare-ai/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b`
- 视觉：`openrouter/google/gemma-4-31b-it:free`、`agnes-image-2.1-flash`

## 接入铁律
1. OmniRoute 免费层 `auto` 路由硬卡死 → pin 具体模型。
2. WorkBuddy models.json 改动须完全重启 WB（不热重载）。
3. Hermes 须显式 `--provider omniroute`，否则模型被原生 provider 抢注偷换。
4. Agnes 国内站 `https://api.agnes-ai.cn/v1`（非 apihub/非 .com）。
5. OmniRoute DATA_DIR 必须无空格路径；GUI 启动只能用户桌面双击。
6. Gridea 浓缩版需用户手动点同步才上线。
7. 测试温和，禁触发 429/503 限流。

## 发布链路（四端）
- 博客源：`D:\AI work\daily-note-blog\_handoffs\` + git push（GitHub Pages）
- 语雀：`w662000/ylv5l7`（直连 API，slug 见 handoff_config.json）
- bbs1org：my-place.us forum_id=3
- phpBB：my-place.us forum_id=11
- 脚本：`D:\AI work\workbuddy\handoff\handoff_flow.py`（博客+语雀）、`publish_forum_now.py`（论坛）
