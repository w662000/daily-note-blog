---
layout: default
title: 技术点 · 定时任务（Cron）
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · 定时任务（Cron）

> 来源：261010_定时任务（Cron）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 将结果回传到来源会话、本地文件或已配置的平台目标
- 以**无 agent 模式**运行——按计划执行脚本，其 stdout 原样投递，零 LLM 参与（参见下方[无 agent 模式](#no-agent-mode-script-only-jobs)章节）
- 由**外部事件触发**——设置了 `cron_job` 的 webhook 路由会在事情发生的那一刻（PR 收到反馈、服务发出告警）立即触发任务，而不是等待下一次定时 tick。参见[事件触发的 Cron 任务](../messaging/webhooks.md#event-triggered-cron-jobs)。
- ```
/cron add 30m "Remind me to check the build"
/cron add "every 2h" "Check server status"
/cron add "every 1h" "Summarize new feed items" --skill blogwatcher
/cron add "every 1h" "Use both skills and combine the result" --skill blogwatcher --skill maps
```
- ```
hermes cron create "every 2h" "Check server status"
hermes cron create "every 1h" "Summarize new feed items" --skill blogwatcher
hermes cron create "every 1h" "Use both skills and combine the result" \
  --skill blogwatcher \
  --skill maps \
  --name "Skill combo"
```
- ```
Every morning at 9am, check Hacker News for AI news and send me a summary on Telegram.
```
- ```
cronjob(
    action="create",
    skill="blogwatcher",
    prompt="Check the configured feeds and summarize anything new.",
    schedule="0 9 * * *",
    name="Morning feeds",
)
```
- ```
cronjob(
    action="create",
    skills=["blogwatcher", "maps"],
    prompt="Look for new local events and interesting nearby places, then combine them into one short brief.",
    schedule="every 6h",
    name="Local brief",
)
```
- ```
# 独立 CLI（schedule 和 prompt 为位置参数）
hermes cron create "every 1d at 09:00" \
  "Audit open PRs, summarize CI health, and post to #eng" \
  --workdir /home/me/projects/acme
```
- ```
# 在聊天中，通过 cronjob 工具
cronjob(
    action="create",
    schedule="every 1d at 09:00",
    workdir="/home/me/projects/acme",
    prompt="Audit open PRs, summarize CI health, and post to #eng",
)
```
- 路径必须是已存在的绝对目录——相对路径和不存在的目录在创建/更新时会被拒绝
- 每次 agent 运行都会将其 `workdir` 绑定到该次运行的唯一任务标识。设置了 workdir 的任务因此可使用正常的并行池，不会修改进程全局终端状态，也不会在并发运行之间泄漏路径。如需限制 cron 的总并发量，请设置 `cron.max_parallel_jobs`。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
