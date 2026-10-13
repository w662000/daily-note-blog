---
layout: default
title: 技术点 · Kanban — 多 Agent 配置文件协作
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Kanban — 多 Agent 配置文件协作

> 来源：261010_Kanban — 多 Agent 配置文件协作_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "基于 SQLite 的持久化任务看板，用于协调多个 Hermes 配置文件"
- Hermes Kanban 是一个持久化任务看板，在所有 Hermes 配置文件之间共享，允许多个具名 agent 协作完成工作，而无需脆弱的进程内子 agent 集群。每个任务都是 `~/.hermes/kanban.db` 中的一行记录；每次交接都是任何人都可以读写的一行记录；每个 worker 都是拥有独立身份的完整 OS 进程。
- **Agent 通过专用 `kanban_*` 工具集驱动看板** —— `kanban_show`、`kanban_list`、`kanban_complete`、`kanban_block`、`kanban_request_review`、`kanban_request_changes`、`kanban_heartbeat`、`kanban_comment`、`kanban_create`、`kanban_link`、`kanban_unblock`。调度器在 schema 中已内置这些工具来启动每个 worker；编排器（orchestrator）配置文件也可以通过 `kanban` 工具集显式启用。模型通过直接调用工具来读取和路由任务，*而不是*通过 shell 执行 `hermes kanban`。详见下方[Worker 如何与看板交互](#how-workers-interact-with-the-board)。
- **你（以及脚本和 cron）通过 CLI 上的 `hermes kanban …`、斜杠命令 `/kanban …` 或仪表盘驱动看板。** 这些界面面向人类和自动化场景——即没有工具调用模型的场合。
- 两个界面都通过同一个 `kanban_db` 层路由，因此读取视图一致，写入不会产生偏差。本页其余部分展示 CLI 示例，因为它们便于复制粘贴，但每个 CLI 动词都有模型使用的等效工具调用。
- **批量任务** —— 一个专家管理 N 个对象（50 个社交账号、12 个监控服务）。
- | 子级身份 | 匿名子 agent | 具有持久记忆的具名配置文件 |
- | 协调方式 | 层级式（调用方 → 被调用方） | 对等式 —— 任意配置文件可读写任意任务 |
- **一句话区别：** `delegate_task` 是函数调用；Kanban 是工作队列，每次交接都是任意配置文件（或人类）可见和编辑的一行记录。
- **Task（任务）** —— 包含标题、可选正文、一个受让人（配置文件名称）、状态（`triage | todo | ready | running | blocked | review | done | archived`）、可选租户命名空间、可选幂等键（用于重试自动化的去重）的一行记录。
- **Link（链接）** —— `task_links` 行，记录父 → 子依赖关系。当所有父任务变为 `done` 时，调度器将 `todo → ready`。
- `scratch`（默认）—— 在 `~/.hermes/kanban/workspaces/<id>/` 下（非默认看板为 `~/.hermes/kanban/boards/<slug>/workspaces/<id>/`）创建的临时目录。**任务完成时删除** —— scratch 按设计是临时性的。通过 `kanban_complete(artifacts=[...])` 明确声明的文件会在清理前复制到持久的任务附件存储；旧版完成摘要中已存在的交付文件路径也会得到同样处理。其他 scratch 文件仍会被删除。如果声明的 scratch 交付文件不存在，任务会保持进行中，worker 可修正路径后重试。需要保留整个工作区时，请使用 `worktree:` 或 `dir:<path>`。在某次安装中首次创建 scratch 工作区时，调度器会记录警告并在任务上发出 `tip_scratch_workspace` 事件（可通过 `hermes kanban show <id>` 查看）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
在每个 profile 一个 gateway 的部署中（单一调度器，`writer`、`admin` 等各自
运行独立的 gateway 进程 —— 参见[多 gateway 指南](./kanban-multi-gateway.md)），
调度与投递的归属是分开的：

- **调度保持单一所有者。** 只有一个 gateway 保持
  `kanban.dispatch_in_gateway: true` 并运行调度器；其余 gateway 都设为
  `false`。
- **通知投递按 profile 归属。** 每个 gateway —— 包括非调度 gateway ——
  都运行通知器，且只轮询标记了其所托管 profile 的订阅。从 `writer`
  profile 的 Telegram 创建的任务，其 `completed`/`blocked` 消息由
  `writer` gateway 投递，即使调度是由 `default` gateway 完成的。
- **遗留订阅**（在 profile 标记之前创建、行上没有 `notifier_profile`
  的订阅）只由实际持有调度器单例锁的 gateway 投递，因此两个 gateway
  永远不会争抢它们。

board 数据库中的原子化逐事件认领可防止跨 gateway 的重复投递。不需要中继、
凭证共享或额外的调度器 —— 每个 profile gateway 只通过它自己的适配器投递。
