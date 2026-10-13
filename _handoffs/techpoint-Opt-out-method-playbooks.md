---
layout: default
title: 技术点 · Opt-out method playbooks
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Opt-out method playbooks

> 来源：261010_Opt-out method playbooks_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **non-broker tools / APIs / wrong-jurisdiction** (skip). The skip-lists live in `site-playbooks.md`.
- 3b. **Operator-browser path (the reliable unblock for anti-bot sites).** Cloudflare/DataDome key on
- Browserbase cloud browser (`setup --auto` selects it when `BROWSERBASE_API_KEY` is set). Being a
- **Do NOT defeat** behavioral / token challenges: a Cloudflare Turnstile that will not auto-clear,
- (`auto` picks Browserbase when `BROWSERBASE_API_KEY` is present - now also read from
- `$HERMES_HOME/.env`, not just the shell env, so `doctor`/`setup --auto` detect the key Hermes

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
