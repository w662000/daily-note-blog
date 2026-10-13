---
layout: default
title: 技术点 · Running Many Gateways at Once
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Running Many Gateways at Once

> 来源：261010_Running Many Gateways at Once_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Operate multiple [profiles](./profiles.md) — each with its own bot tokens,
- ```
# Create profiles (once)
hermes profile create coder
hermes profile create personal-bot
hermes profile create research

# Configure each
coder setup
personal-bot setup
research setup

# Install each gateway as a managed service
coder gateway install
personal-bot gateway install
research gateway install

# Start them all
coder gateway start
personal-bot gateway start
research gateway start
```
- (`/api/status` carries `multiplex_standalone_reason`). A single-profile install
- it is written for you. An unset key resolves on and is made explicit in the
- unset-key decision the same way an explicit `true` does.
- host gateway. There is no environment variable for this key.
- ```
hermes config set gateway.multiplex_profiles true
hermes gateway restart
```
- ```
gateway:
  multiplex_profiles: true
```
- keys** — credentials are never shared across profiles.
- ```
hermes -p coder gateway stop     # park coder; other profiles keep running
hermes -p coder gateway start    # unpark coder and serve it again
hermes -p coder gateway restart  # reconnect coder with its current configuration
```
- same thing: Stop parks it (`/api/gateway/stop?profile=coder` spawns
- and `/api/status` lists `parked_profiles`. Start on a named profile that is

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
