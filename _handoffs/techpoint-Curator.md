---
layout: default
title: 技术点 · Curator
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Curator

> 来源：261010_Curator_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- It exists so that skills created via the [self-improvement loop](./skills.md#agent-managed-skills-skill_manage-tool) don't pile up forever. Every time the agent solves a novel problem and saves a skill, that skill lands in `~/.hermes/skills/`. Without maintenance, you end up with dozens of narrow near-duplicates that pollute the catalog and waste tokens.
- 2. **LLM consolidation** (single aux-model pass with a high iteration ceiling — a full curation sweep typically takes 50–100 API calls) — **OFF by default**. When `curator.consolidate: true`, the forked agent surveys the agent-created skills, can read any of them with `skill_view`, and decides per-skill whether to keep, patch (via `skill_manage`), consolidate overlapping ones into class-level umbrellas, or archive (via `skill_manage action=delete` with an `absorbed_into` target — the pass has no terminal). The candidate list it is given contains only skills it can actually read and write: bundled built-ins (even with `prune_builtins: true`, which only affects the deterministic archival pass) and skills in `skills.disabled` (which `skill_view` refuses) are never offered to it, so the pass cannot burn its tool budget on refused reads or writes. Consolidation treats a skill as a full package: if a skill has `references/`, `templates/`, `scripts/`, `assets/`, or relative links to those paths, the curator must either keep it standalone, re-home the needed support files and rewrite paths, or archive the entire package unchanged — not flatten only `SKILL.md` into another skill's `references/` file.
- By default the curator only **prunes** — the deterministic inactivity pass marks skills stale and archives long-unused ones. The opinionated LLM **consolidation** pass (umbrella-building, merging overlapping skills) is off by default because it costs aux-model tokens on every run and makes broad structural changes to your library. Turn it on with `curator.consolidate: true`, or run it once on demand with `hermes curator run --consolidate`.
- ```
curator:
  enabled: true
  interval_hours: 168          # 7 days
  min_idle_hours: 2
  stale_after_days: 14
  archive_after_days: 30
  consolidate: false           # LLM umbrella-building pass — opt-in (prune-only by default)
  prune_builtins: false        # opt in to archiving unused bundled built-in skills too (hub skills always exempt)
```
- ```
hermes model                   # → "Auxiliary models — side-task routing"
                               # → pick "Curator" → pick provider → pick model
```
- ```
auxiliary:
  curator:
    provider: openrouter
    model: google/gemini-3-flash-preview
    timeout: 600               # generous — reviews can take several minutes
```
- Earlier releases used a one-off `curator.auxiliary.{provider,model}` block. That path still works but emits a deprecation log line — please migrate to `auxiliary.curator` above so the curator shares the same plumbing (`hermes model`, dashboard Models tab, `base_url`, `api_key`, `timeout`, `extra_body`) as every other aux task.
- ```
hermes curator status         # last run, counts, pinned list, LRU top 5
hermes curator run            # trigger a run now (blocks until done). Prune-only unless curator.consolidate: true
hermes curator run --consolidate # force the LLM consolidation pass on for this run, overriding the config default
hermes curator run --background  # fire-and-forget: start the run in a background thread
hermes curator run --dry-run  # preview only — report without any mutations
hermes curator backup         # take a manual snapshot of ~/.hermes/skills/
hermes curator rollback       # restore from the newest snapshot
hermes curator rollback --list     # list available snapshots
hermes curator rollback --id <ts>  # restore a specific snapshot
hermes curator rollback -y         # skip the confirmation prompt
hermes curator pause          # stop runs until resumed
hermes curator resume
hermes curator pin <skill>    # never auto-transition this skill
hermes curator unpin <skill>
hermes curator adopt <skill>    # hand an unmanaged skill to the curator
hermes curator adopt --all-unmanaged   # hand over every unmanaged skill
hermes curator list-unmanaged   # itemize skills with no provenance marker
hermes curator restore <skill>  # move an archived skill back to active
hermes curator list-archived    # list skills currently in ~/.hermes/skills/.archive/
hermes curator archive <skill>  # manually archive a single skill now
hermes curator prune [--days N] # bulk-archive agent-created skills idle >= N days (default: `archive_after_days`, 30)
hermes curator ledger           # list the per-mutation audit ledger (all actors)
hermes curator ledger --skill <name> --limit 50  # filter/paginate ledger entries
hermes curator rollback <entry-id>  # undo a single mutation from the ledger
hermes curator purge [--days N] [--dry-run]  # delete archived skills older than the TTL (explicit only)
```
- ```
hermes curator rollback        # restore newest snapshot (with confirmation)
hermes curator rollback -y     # skip the prompt
hermes curator rollback --list # see all snapshots with reason + size
```
- ```
curator:
  backup:
    enabled: true
    keep: 2
```
- ```
hermes curator ledger                  # newest 20 entries
hermes curator ledger --skill my-skill --limit 50
hermes curator rollback <entry-id>     # restore that one mutation's before-state
```
- ```
skills:
  ledger: false
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
