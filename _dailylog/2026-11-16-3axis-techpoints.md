---
layout: default
title: 技术点 · 2026-11-16
date: 2026-11-16 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-16.md

## 10:12 开机自启生效，任务自动续跑中
- 10:09:40 YD_Rebuild 随登录自动启动，进度日志确认：PHASE 1 收集 worklog 20 页/1000 篇（~88s/10 页）。
- 已核实脚本为最终修复版：acc[label]=[] 全量重扫不漏收（L48）、CREATE_NO_WINDOW 无黑窗（L33）、删除阶段断点跳过已删 ID。
- 预计：收集 1~1.5h → 15 路并发删除 ~30min → 重传 ~20min，中午前后出三目录干净计数。
- ⚠️ 重传阶段若撞上 10:15 晨检有道云补发会互踩（今晨已避开，任务 10:09 启动晚于晨检无冲突）。

## wb-intl（WB 国际版）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）