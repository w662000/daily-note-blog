---
layout: default
title: 项目流 · 2026-11-23
date: 2026-11-23 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-23.md, D:\AI work\workbuddy\2026-11-23-10-45-04\.workbuddy\memory\2026-11-23.md

## 有道云 G5 周期对账（automation-1794800083381，只读巡检）
- 用隔离 venv Python 运行 `youdao_g5_reconcile.py`，输出「重建未完成（缺 youdao_final_state.json），跳过本轮对账，避免读中间态」，退出码 0。
- 判定：命中「重建未完成跳过」分支，无 ALERT，按口径简要汇报即可；**未删除/未写入任何云端笔记，未改脚本与有道云配置**。
- 核实：重建目录 `2026-11-15-10-21-36/` 存在，含 `collect_delete_rebuild_v3.py`、`youdao_reupload.log` 等清空+重传过程产物，但缺最终状态文件 → G5 撞车保护生效；本轮未生成 `logs/youdao_g5_2026-11-23.json`，logs 下无历史 G5 报告。
- 脚本只读性已核：仅 CLI `search`/`list`，只碰 3 个固定目录 ID，报告只写本地 logs。
- 进度快照：`进度/进度_20261123_1015.md`。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-22-12-57-38\.workbuddy-ai\memory\2026-11-23.md, D:\workspace\workbuddyai\2026-11-23-10-42-19\.workbuddy-ai\memory\2026-11-23.md

## 轻量无头浏览器方案调研（自建 SearXNG + GitHub API）
- 用户诉求：Playwright + Chrome 太费资源，找 GitHub 上低占用无头浏览器。
- 候选与 T0 元数据（2026-11-23 快照）：lightpanda-io/browser 42,386 star / AGPL-3.0 / 无 Windows 原生二进制（需 WSL2）；h4ckf0r0day/obscura 37,059 star / Apache-2.0 / 有 Windows x64 原生 + 截图/PDF/CDP；lexmount/moli 24,287 star / Apache-2.0 / Windows 原生 / 截图需 `--layout`；vercel-labs/agent-browser 53,475 star / Apache-2.0 / Rust CLI，`--engine` 可切 lightpanda/obscura。
- 关键事实（T1 官方文档）：Playwright 默认 headless 就用 chromium headless shell；只有显式 `channel:'chromium'` 或 headed 才跑完整 Chromium。Puppeteer 对应 `headless:'shell'`。
- 内存数字互相打架：Lightpanda README 自报 123MB/100 页 vs Chrome 2GB；Obscura README 自报 30MB vs 200+MB（无测试条件）；Moli README 引 Lexbench 92MiB 中位 vs Chrome 697MiB（该基准由 Moli 作者托管，有利益冲突）；独立单次复现（cognitive-unload，T2）商店页 100 次：Chrome 546MiB / Obscura 57MiB / Moli 104MiB / Lightpanda 25MiB，但 board 任务通过率 Chrome 11/11、Obscura 7/11、Lightpanda 2/11、Moli 1/11。结论：省内存和兼容性明显是 trade-off，必须按用户真实页面实测。
- 状态：只做调研，未安装任何方案；等用户确认场景（抓文本/截图/E2E、Windows 原生或 WSL2、并发量）后再落地。
- 会话 ID：wb-intl|16f2aa88-4e5f-4b4f-a9fe-453d6bcfbb76


# 2026-11-23 工作日志

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）