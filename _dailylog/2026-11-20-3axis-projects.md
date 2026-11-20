---
layout: default
title: 项目流 · 2026-11-20
date: 2026-11-20 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-19-19-59-56\.workbuddy\memory\2026-11-20.md, D:\AI work\workbuddy\2026-11-20-16-30-22\.workbuddy\memory\2026-11-20.md

## 会话 ID 补捞 + managed Python 环境确认报废（10:49–10:55，✅ 完成）
- 用户问会话 ID，get_session_id.py 跑不了：managed Python 3.13.12 残缺安装（无 Lib/，`No module named 'encodings'`），envs/default venv、D:/hermes-agent/venv 全部连带挂（pyvenv.cfg home 指向废 base）。
- 解法：Node 24 内置 `node:sqlite` 直读 `~/.workbuddy/workbuddy.db` sessions 表。
- 两个坑：①只拷主库查不到当前会话（当前行在 -wal 里，需 db+wal+shm 一起拷）；②交互会话 `is_background_automation` 是 NULL 不是 0，`where =0` 会漏，必须 `coalesce(...,0)=0`。
- 当前会话 ID：`58817e6a-b613-4387-8c43-337426c6e7ce`（cwd=本工作区，updated 10:51:59）。
- 已把 Node 备用方案追加进 agent-session-id SKILL.md。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-20-19-46-45\.workbuddy-ai\memory\2026-11-20.md

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）