---
layout: default
title: 技术点 · Scheduled Tasks (Cron)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Scheduled Tasks (Cron)

> 来源：261010_Scheduled Tasks (Cron)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
/cron add "in 30m" "Remind me to check the build"
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
- the provider API key resolves (skipped for an unpinned job when a
- missing primary key; a pinned job does not use that chain, so it is always
- made** — a misconfigured job never spends tokens. The next healthy run clears
- ```
cron:
  preflight: false
```
- ```
hermes cron edit <job_id> --pin                                   # lock the current main model onto one job
hermes cron edit <job_id> --provider <provider> --model <model>   # pin an explicit model
hermes cron edit <job_id> --unpin                                 # follow the main model again
hermes config set cron.model <model>                              # every unpinned job, without touching chat
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
# Standalone CLI (schedule and prompt are positional)
hermes cron create "every 1d at 09:00" \
  "Audit open PRs, summarize CI health, and post to #eng" \
  --workdir /home/me/projects/acme
```
- ```
# From a chat, via the cronjob tool
cronjob(
    action="create",
    schedule="every 1d at 09:00",
    workdir="/home/me/projects/acme",
    prompt="Audit open PRs, summarize CI health, and post to #eng",
)
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
