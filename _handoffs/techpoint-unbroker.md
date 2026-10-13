---
layout: default
title: 技术点 · unbroker
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · unbroker

> 来源：261010_unbroker_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- one it detects, reading credentials from the shell env **and from `$HERMES_HOME/.env`** so keys
- **Cloud browser (recommended default): `BROWSERBASE_API_KEY`.** `setup --auto` selects it
- whenever the key is present, and it is the intended baseline: a real residential-IP cloud
- ("hard") challenges the browser genuinely cannot pass fall back to a human task. Without the key,
- ```
PDD="python scripts/pdd.py"
```
- re-fetches key URLs to confirm a `found` before trusting it (this cuts both ways: it caught a real
- CAPTCHA policy: never defeat behavioral/token/slider challenges; OK to read a static distorted-text or
- Subagent reports are self-reports: the parent re-verifies key claims (listing URLs, match basis) before
- Browserbase when its key exists, `age` encryption when the binary exists, `autonomy=full`). Then
- ```
   while true:
     q = $PDD next <subject>
     if q.actions is empty: break
     execute EVERY action in order; record each outcome via $PDD record
```
- The parent re-verifies key `found` claims from subagents before trusting them.
- `$PDD setup --encryption age` - it generates a local `age` key and encrypts dossiers + ledgers (the

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
