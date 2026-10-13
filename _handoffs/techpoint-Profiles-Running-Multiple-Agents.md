---
layout: default
title: 技术点 · Profiles: Running Multiple Agents
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Profiles: Running Multiple Agents

> 来源：261010_Profiles_ Running Multiple Agents_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Run multiple independent Hermes agents on the same machine — each with its own config, API keys, memory, sessions, skills, and gateway state.
- [bot token](#different-bot-tokens) identifies that platform account.
- ```
hermes profile create coder       # creates profile + "coder" command alias
coder setup                       # configure API keys and model
coder chat                        # start chatting
```
- ```
hermes profile create mybot
```
- Creates a fresh profile with bundled skills seeded. Run `mybot setup` to configure API keys, model, and gateway tokens.
- ```
hermes profile create researcher --description "Reads source code and external docs, writes findings."
```
- ```
hermes profile create work --clone
```
- Copies your current profile's `config.yaml`, `.env`, `SOUL.md`, skills, and the curated memory files `memories/MEMORY.md` and `memories/USER.md` into the new profile — memory is treated as part of the agent's identity, like `SOUL.md`. If `config.yaml` selects an external memory provider (`memory.provider`), that provider's own config travels too — its `<provider>/` directory or `<provider>.json` under the profile home, e.g. `hindsight/config.json` — so the clone's memory is available instead of silently off; a cloned `local_embedded` hindsight config still shares the source's embedded daemon and bank until you give the clone its own hindsight `profile`/`bank_id` ([#81815](https://github.com/NousResearch/hermes-agent/issues/81815)). Sessions, `state.db`, cron jobs and everything else start empty. For a blank memory as well, create the profile without `--clone` or delete the two files afterwards; the agent never falls back to another profile's memory when they are absent. Edit `~/.hermes/profiles/work/.env` for different API keys, or `~/.hermes/profiles/work/SOUL.md` for a different personality.
- ```
hermes profile create work --clone --sync-imports
hermes -p work import-agent --sync        # pulls changes from the same ~/.claude / ~/.codex
```
- ```
hermes profile create backup --clone-all
```
- Copies **everything** — config, API keys, personality, all memories, skills, plugins. A complete working snapshot. Per-profile history is excluded (session history, `state.db`, `backups/`, `state-snapshots/`, `checkpoints/`) — these belong to the source profile and can reach tens of GB. When cloning from the default profile, the local-model runtime trees (`models/`, `runtimes/`, `node/` — downloaded weights and managed binaries, re-fetched on demand) are skipped too, as `hermes backup` already does. **Cron jobs are not cloned** either: they are scheduled work bound to the source profile and its delivery channel, and a clone that inherited them would run every job twice (two gateways, same job ids). The new profile starts with an empty `cron/`. For a full backup including history and cron jobs, use `hermes profile export` or `hermes backup` instead.
- Anthropic (Claude Pro/Max), OpenAI Codex, and xAI OAuth logins use **single-use refresh tokens** — a copy of one is not a second credential, it is the same credential with two owners, and the first profile to refresh it revokes it for every other copy. `--clone-all` (and the dashboard's credential mirroring) therefore drops those OAuth rows from the clone. The new profile keeps reading the login from the root `~/.hermes/auth.json`, and a token refresh performed inside any profile is written back to root, so all profiles stay signed in. Static API keys are copied as usual. To give a profile its own separate OAuth login, run `hermes -p <name> auth add <provider>` inside it.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
