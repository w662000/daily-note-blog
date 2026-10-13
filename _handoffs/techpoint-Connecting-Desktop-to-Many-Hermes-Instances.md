---
layout: default
title: 技术点 · Connecting Desktop to Many Hermes Instances
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Connecting Desktop to Many Hermes Instances

> 来源：261010_Connecting Desktop to Many Hermes Instances_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | **Remote gateway** | "A Hermes gateway reachable over HTTP(S) — LAN, Tailscale, or the internet." | session token or OAuth |
- | **SSH** | "A Hermes install reached over SSH." The app opens the tunnel and starts the dashboard for you | SSH key + adopted token |
- reorder it, or focus the header and use Space, arrow keys, then Space to place
- **Authentication** — choose **Session token** or **OAuth**:
- **Session token** — paste the dashboard session token from the
- token."*
- **OAuth** — sign in through the Nous Portal browser flow; no token
- port optional). Your SSH key is used; the app adopts a dashboard
- token over the tunnel. Remote probes run under the account's login
- with the same idle-reaping as local per-profile backends — background agents
- keeps the same profile rail and keyboard flow as before.
- installs, env keys, and MCP setup all land on the selected agent's backend.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
