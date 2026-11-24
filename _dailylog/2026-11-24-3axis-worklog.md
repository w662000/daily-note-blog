---
layout: default
title: 多 Agent 工作日志 · 2026-11-24
date: 2026-11-24 23:30:00 +0800
---

# 多 Agent 每日工作日志 · 2026-11-24

> 机器汇总（模型不可用，原文按 agent 分节保留，未做润色）

## 一、WB 国内版（wb-cn）

今日无机器日志记录。

## 二、WB 国际版（wb-intl）

今日无机器日志记录。

## 三、AutoClaw 1.15（autoclaw-115）
> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-24.md


# 2026-11-24

## 修复 AutoClaw 国际版会话 ID（01:03 用户请求）

**问题**：国际版 AutoClaw2 每个会话答复结尾都是同一个 ID。

**根源**（三层）：
1. AutoClaw 国际版 = `D:\Program Files\AutoClaw\AutoClaw2\`（zwork 2.5.3，进程 AutoClaw2.exe），与国内版（AutoClaw.exe + openclaw gateway :18889）**完全不同架构**：无 openclaw gateway，会话存 `AppData\Roaming\AutoClaw-oversea-official\accounts\<hash>\runtime\runtime.sqlite` 的 `work_sessions` 表（26 条，ISO8601 UTC 时间戳）。
2. 旧脚本 `get_session_id.py` 只有 `--agent au`（读国内版 `.openclaw-autoclaw\agents\main\sessions\sessions.json`），没有国际版读取器 → 国际版跑 `--agent au` 拿到的永远是国内版的最新会话 ID。
3. 国际版常驻规则（`accounts\0f1c9b...\instruction-packs\agent-main.md` 第 225-229 行，11-17 分发时写入）也写死了 `--agent au` → 每个会话追加的都是国内版 ID。

**修复内容**：
- `get_session_id.py` v2：新增 `au-intl` 读取器（`_au_intl_db()` 定位 mtime 最新的 runtime.sqlite，复制含 -wal/-shm 后读 work_sessions，过滤 deleted_at/archived_at，ISO8601 转本地时间+毫秒戳）；7→8 个 agent。已分发三处（国内 workspace skills、国内全局 skills、国际版 zwork-agent\skills），MD5 一致。
- SKILL.md：7→8，全名对照加「AutoClaw 国际版=autoclaw国际版」，存储位置表加 au-intl 行，常驻指令文件表加国际版行。三处同步一致。
- 国际版 agent-main.md 规则块：标题改「2026-11-24 修复国际版」，标记格式改 `【autoclaw国际版会话ID<完整会话ID>】`，命令改 `--agent au-intl`，明确**禁止用 `--agent au`**。
- 国内版 AGENTS.md 规则：补一句 au=国内版、国际版用 au-intl。
- 国际版技能 `_store_meta.json`：按 zwork i7e 算法（main.cjs：`f/d\0相对路径\0大小\0`+内容流，目录名排序）重算 contentSha256，更新 description 为 8-agent 版。
- 验证：au-intl=fa4ed6ab-0775-4bf9-9d77-a7159302b51e（越南主机IP与Cloudflare关系，国际版真实最新会话），au=70c81a1b-...（本会话），两版彻底分离。

**备份**：`workspace\backups\agent-session-id-20261124\`（7 个文件：两版脚本+SKILL.md+agent-main.md）。

**关键认知**：
- AutoClaw 国际版是智谱 zwork 内核（runtime.sqlite + work_sessions + instruction-packs + zwork-agent\skills），与国内版 openclaw 内核（sessions.json + AGENTS.md + skills）并存，装同一个 skill 要落两套位置。
- `%APPDATA%` 下并存：autoclaw（国内版 Electron userData）、AutoClaw-official（旧国际版残留，11-17 后停更）、AutoClaw-oversea-official（现国际版 userData）。
- zwork 技能导入哈希 = i7e：遍历排序条目，`d|f\0<相对路径>\0<size>\0` 喂 sha256，文件再喂内容流；跳过 `_store_meta.json`。
- instruction-packs\*.md 是国内版 AGENTS.md 的国际版等价物（按 agent 分文件：agent-main.md / agent-auto-designer.md 等）。

## 四、ZCode（zcode）

今日无机器日志记录。

## 五、总计

- 当天有日志的 agent：1/4
- 日志总字符数：2106