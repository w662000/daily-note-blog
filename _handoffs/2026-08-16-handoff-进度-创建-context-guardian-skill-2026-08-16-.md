---
layout: default
title: 交接文档 · 进度：创建 context-guardian skill（2026-08-16 17_31）
date: 2026-08-17 23:30:00 +0800
---

# 进度：创建 context-guardian skill（2026-08-16 17:31）

- **日期**：2026-08-16
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-16-10-57-55\进度_20260816_1731_skill.md

## 任务
用户要求：写一个 skill，用特定触发词启动，并在 WB 会话中发挥作用。
- 功能（用户选定 q-0）：① 强化上下文记忆（防失忆）② 根据当前会话用更清晰指令让模型更易执行。
- 范围（用户选定 q-1）：用户级（跨所有项目可用）。

## 产物
- 目录：`C:\Users\Administrator\.workbuddy\skills\context-guardian\`
- `SKILL.md`：frontmatter 含 `agent_created: true` + 触发词 `description`；body = 两大能力（记忆强化 / 指令澄清）+ Workflow + Notes。
- `scripts/recall_memory.py`：只读脚本，自动定位并输出用户级 `~/.workbuddy/MEMORY.md` + 项目 `.workbuddy/memory/` 今日及近 7 天日 log（参数 `--project` `--days`）。
- 打包校验：`C:\Users\Administrator\.workbuddy\skills\dist\context-guardian.zip`（✅ valid）。

## 触发词（写进 description，用户可改）
- 中文：记忆核查 / 上下文强化 / 防失忆 / 记忆官 / 理清需求 / 指令澄清 / 清晰化指令 / 强化上下文 / 上下文守护
- 英文：context boost / clarify instruction / recall memory
- 机制：WB 按对话内容匹配 description，用户说出上述词即**自动加载**本 skill 并在当前会话生效（无需手动点）。

## 踩坑
- `package_skill.py` 校验禁止 description 含 `<` / `>` → 初版用 YAML 折叠块 `>-`（含 `>`）被拒；改为单引号单行字符串后通过。

## 验证
- `recall_memory.py` 实测：成功读回 USER MEMORY + 项目日 log（head 截断仅显示前半）。
- `package_skill.py`：✅ Skill is valid。
