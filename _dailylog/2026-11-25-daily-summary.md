---
layout: default
title: 每日工作总结 · 2026-11-25
date: 2026-11-25 23:30:00 +0800
---

# 多 Agent 每日工作日志 · 2026-11-25

> 数据源：wb-cn / wb-intl / autoclaw-115 / zcode 四个 Agent 的当天日志，按 agent 分节；某 agent 当天无日志就写「今日无机器日志记录」，不许编造。

## 一、WB 国内版（wb-cn）
- 更新 SenseNova 免费模型清单并写入 WB 活清单 (`models.json`)，新增 `glm-5.3`、`deepseek-flash`、`sensenova-6.8-flash`、`kimi-k3` 等模型。
- 根据用户要求执行三项指令：删除 `glm-5.2`、修正模型 ID 冲突（通过显示名区分并改回官方 ID 以消除 404 隐患）、同步其他 Agent。
- 完成 6 个可用模型向 DSH、Hermes、Hermes Studio、龙虾及 AutoClaw 2.0 的同步工作。
- 针对 AutoClaw 2.0 凭证孤儿文件问题，使用当前 key 全量重建凭证为 `wb-bridge` 占位。
- 准备了针对 AutoClaw 1.x 的 SenseNova 更新脚本 `AutoClaw1x_更新SenseNova_关进程后运行.py`。
- 生成的文件：`models.json.bak-sensenova-20261125-110013`、`SenseNova免费模型清单更新_20261125.md`、`SenseNova更新_五端同步报告_20261125.md`。

## 二、WB 国际版（wb-intl）
- 执行中转站方案：通过 GitHub + jsDelivr 将 `cf.7z` 分发至法国纯 IPv6 VPS，并验证了 `cloudflared` 参数顺序（`--edge-ip-version 6` 需在 `run` 之前）及 jsDelivr 的 20MB 单文件限制。
- 排查 Xray 会话底部无尾标问题，确认原因为新定死的会话 ID 规则仅对新回复生效，不回填历史会话。
- 补跑星图扫描任务 `scan_projects.py`，节点从 179 增至 181。
- 生成的文件：`Xray部署决策指南.md`、`星图预览.html`。

## 三、AutoClaw 1.15（autoclaw-115）
- 完成 skill-creator 回灌分发：通过合并 3 个本地补丁（解决 emoji 崩溃、UTF-8 重配置、PyYAML 降级及 encoding 问题）实现 8 端全绿，并完成备份。
- 升级星图每日编排器 `run_daily_star_scan.py` 至 v1.2，将冒烟测试挂载至流水线，支持 `--smoke-only` 参数。
- 上线“绿灯闸”机制（`sync_skill.py` v1.1），实现分发后自动跑 `smoke_common_skills.py` 进行强制校验，成功拦截语法错误的脚本。
- 复核十边形画像数据（包括 stocks.db、星图节点、涨停天梯及雷达图几何复算）的一致性。
- 生成的文件：`workspace\smoke_tests\冒烟测试报告_共有skill_20261125.html` 以及多个备份文件夹。

## 四、ZCode（zcode）
今日无机器日志记录

## 五、总计 / 待办
- **当天有日志的 Agent 数**：3
- **日志总字符数**：约 3650
- **跨 Agent 待办**：
    - 用户需手动关闭 AutoClaw 1.x 进程后，运行 wb-cn 准备的 `AutoClaw1x_更新SenseNova_关进程后运行.py` 脚本。
    - 用户需在确认 VPS 完成 `cf.7z` 下载后，执行 `gh repo delete w662000/temp-cf-20261125-wb --yes` 删除临时仓库。