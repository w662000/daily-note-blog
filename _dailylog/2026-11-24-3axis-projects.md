---
layout: default
title: 项目流 · 2026-11-24
date: 2026-11-24 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-24-10-36-47\.workbuddy\memory\2026-11-24.md, D:\AI work\workbuddy\2026-11-24-15-41-39\.workbuddy\memory\2026-11-24.md

## 签到+喵旅行任务改造为开机自启（10:42 完成）
- 需求：把每2小时重复的签到+喵旅行 automation 改为「开机后 WB 启动就跑一次」。
- 方案：automation 调度器无「开机触发」开关 → 用 Windows 启动项 vbs + 停用原 rrule 任务。
- 产物：
  - 新建 `D:\AI work\workbuddy\scripts\daily_combo_autostart.py`（等token≤5分钟→跑一次喵旅行+签到，幂等）。
  - 部署 `%APPDATA%\...\Startup\WB-DailyCombo-AutoStart.vbs`（pythonw 静默，纯ASCII无BOM）。
  - `automation-1785848159433`（原每2小时）→ PAUSED，改名 `[已停用·改为开机自启]...`（保留未删）。
  - `automation-1786765573442`（每日11:00查漏补缺）保持 ACTIVE 作兜底。
- 验证：10:42 实跑成功——喵旅行出发(咖啡馆,轮换1/4)、签到连续55天；日志 `~/.workbuddy/daily_combo.log`。
- 二次验证（11:08）：pythonw 无窗口直跑包装脚本退出码0、幂等生效（旅行中/已签自动跳过）；cscript/wscript 被沙箱拦（LOLBin），vbs 真实验证节点=下次重启。11:00 兜底任务截至 11:10 未在日志出现，暂观察（automation 拉起 agent 有延迟）。
- 沉淀：新 skill `~/.workbuddy/skills/wb-task-to-boot-autostart/SKILL.md`（定时任务→开机自启改造全流程+踩坑）。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-24-10-51-31\.workbuddy-ai\memory\2026-11-24.md, D:\workspace\workbuddyai\2026-11-24-15-39-14\.workbuddy-ai\memory\2026-11-24.md

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-24.md

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）