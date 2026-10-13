---
layout: default
title: 技术点 · hermes_cli/ + cli.py — CLI, slash commands, config, skins, updater, profiles
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · hermes_cli/ + cli.py — CLI, slash commands, config, skins, updater, profiles

> 来源：261010_hermes_cli_ + cli.py — CLI, slash commands, config, skins, u_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- `cli_billing_mixin.py`, `cli_tui_mixin.py` (widgets, keybindings, panels), `cli_tui_runtime_mixin.py`
- light mode, markdown, `_cprint`, panel wrap), `cli_terminal_input.py` (file drops, paste/Enter-key
- handles input + autocomplete; `KawaiiSpinner` (`agent/display.py`) animates API calls and prints
- (late binding on `hermes_cli.gateway`), so monkeypatch on the facade; mutable state such as
- migrate/transform existing config (rename keys, restructure); new keys deep-merge automatically.
- **.env = SECRETS ONLY** (keys, tokens, passwords): add to `OPTIONAL_ENV_VARS` with
- set/get/unset <NAME>` route any bare name registered in `OPTIONAL_ENV_VARS` / `_EXTRA_ENV_KEYS`
- round-trip merge): comments, key order, quoting and blank lines survive, absent keys are
- `hermes_time`/`hermes_logging`: user file + managed overlay + `${VAR}` expansion + model-key
- canon, NO defaults — for presence-sensitive readers). If the CLI sees a key and the gateway
- **Every `DEFAULT_CONFIG` key has a runtime reader, and every reader a registry entry.** Both drift
- modes are silent: a registered key nothing reads (a knob that does nothing) and a reader of a key

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
