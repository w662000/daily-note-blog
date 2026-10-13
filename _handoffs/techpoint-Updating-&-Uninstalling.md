---
layout: default
title: 技术点 · Updating & Uninstalling
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Updating & Uninstalling

> 来源：261010_Updating & Uninstalling_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
hermes update
```
- ```
hermes config set updates.check false
```
- 8. **Multiplex migration (multi-profile installs)** — once the fleet is verified on the new code, an install with two or more profiles that still run **one gateway per profile** is folded into a single multiplexed default gateway when nothing blocks it (same as `hermes gateway migrate --multiplex --yes`); if a blocker exists (a bot token shared by two profiles, a secondary profile binding a port with no `/p/<profile>/` ingress) the update prints the blockers with their fixes and changes nothing. Single-profile installs are never touched. See [Migrating from per-profile gateways](../user-guide/multi-profile-gateways.md#migrating-from-per-profile-gateways).
- The restart is drain-first: the running gateway refuses new turns, then waits for in-flight work (chat turns, cron jobs, API runs) to finish before exiting, capped by `agent.restart_after_turn_timeout` (30 minutes by default) so a long-running job is never cut off mid-run. While that wait is in progress the updater prints, every 30 seconds, what the gateway is still holding for — for example:
- ```
  → hermes-gateway: draining (up to 1875s)...
  ⏳ still draining — 1560s left before the forced restart
     waiting on 1 active work unit(s):
       • cron job 6ba19dab68df (nightly-scout) in external worker pid 573597, running 6m40s
     finish or kill the work above to release the drain now; agent.restart_after_turn_timeout in config.yaml caps this wait
```
- Chat turns show their session key, model and current tool; cron jobs show the job id, name and the process running them (an external restart-safe worker on systemd installs, otherwise the gateway itself). `hermes gateway status` lists the same units while the gateway is draining. To stop waiting, finish or kill the listed work, or lower `agent.restart_after_turn_timeout` in `config.yaml` (`0` enters the forced drain immediately).
- ```
hermes update --branch release-candidate
hermes update --check --branch experimental   # preview behindness only
```
- ```
# ~/.hermes/config.yaml
updates:
  non_interactive_local_changes: stash   # default: keep + auto-restore
  # non_interactive_local_changes: discard  # throw local source edits away
```
- ```
cd ~/.hermes/hermes-agent   # or your install root
git stash list --format='%gd %H %s'   # find the hermes-update-autostash entry
git stash apply stash@{0}
```
- ```
hermes update --backup
```
- ```
# ~/.hermes/config.yaml
updates:
  pre_update_backup: full
```
- ```
$ hermes update
✗ Another hermes.exe is running:
    PID 12345  hermes.exe

  Updating now would fail to overwrite ...\venv\Scripts\hermes.exe because
  Windows blocks REPLACE on a running executable.

  Close Hermes Desktop, exit any open `hermes` REPLs, and
  stop the gateway (`hermes gateway stop`) before retrying.
  Override with `hermes update --force` if you've already
  confirmed those processes will not write to the venv.
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
