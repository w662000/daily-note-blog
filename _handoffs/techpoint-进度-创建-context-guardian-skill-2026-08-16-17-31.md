---
layout: default
title: 技术点 · 进度：创建 context-guardian skill（2026-08-16 17:31）
date: 2026-08-16 23:30:00 +0800
---

# 技术点 · 进度：创建 context-guardian skill（2026-08-16 17:31）

> 来源：260816_进度：创建 context-guardian skill（2026-08-16 17_31）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- `scripts/recall_memory.py`：只读脚本，自动定位并输出用户级 `~/.workbuddy/MEMORY.md` + 项目 `.workbuddy/memory/` 今日及近 7 天日 log（参数 `--project` `--days`）。

## 三、关键产物与命令
- 目录：`C:\Users\Administrator\.workbuddy\skills\context-guardian\`
- `SKILL.md`：frontmatter 含 `agent_created: true` + 触发词 `description`；body = 两大能力（记忆强化 / 指令澄清）+ Workflow + Notes。
- `scripts/recall_memory.py`：只读脚本，自动定位并输出用户级 `~/.workbuddy/MEMORY.md` + 项目 `.workbuddy/memory/` 今日及近 7 天日 log（参数 `--project` `--days`）。
- 打包校验：`C:\Users\Administrator\.workbuddy\skills\dist\context-guardian.zip`（✅ valid）。

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
- `package_skill.py` 校验禁止 description 含 `<` / `>` → 初版用 YAML 折叠块 `>-`（含 `>`）被拒；改为单引号单行字符串后通过。
