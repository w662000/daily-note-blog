---
layout: default
title: 技术点 · Persistent Goals (`/goal`)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Persistent Goals (`/goal`)

> 来源：261010_Persistent Goals (`_goal`)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
/goal Fix every failing test in tests/hermes_cli/ and make sure scripts/run_tests.sh passes for that directory
```
- ```
/goal draft Migrate the auth service from session cookies to JWT
```
- ```
/goal Migrate auth to JWT
verify: pytest tests/auth passes
constraints: keep the /login response shape unchanged
boundaries: only touch services/auth and its tests
stop when: a DB schema migration is required
```
- ```
/goal Fix the flaky session tests
/goal gate add scripts/run_tests.sh tests/hermes_cli/test_goals.py
```
- ```
⏸ Goal paused — 20/20 turns used. Use /goal resume to keep going, or /goal clear to stop.
```
- Goal state lives in `SessionDB.state_meta` keyed by `goal:<session_id>`. That means `/resume` picks up right where you left off — set a goal, close your laptop, come back tomorrow, `/resume`, and the goal is still standing exactly as you left it (active, paused, or done).
- ```
goals:
  # Max continuation turns before Hermes auto-pauses and asks you to
  # /goal resume. Default 20. Lower this if you want tighter loops;
  # raise it for long-running refactors.
  max_turns: 20
```
- ```
auxiliary:
  goal_judge:
    provider: openrouter
    model: google/gemini-3-flash-preview
```
- The judge call is small (~200 output tokens) and runs once per turn, so a cheap fast model is usually the right call.
- ```
You: /goal Create four files ~/.hermes/cache/scratch/note_{1..4}.txt, one per turn, each containing its number as text

  ⊙ Goal set (20-turn budget): Create four files ~/.hermes/cache/scratch/note_{1..4}.txt, one per turn, each containing its number as text

Hermes: Creating ~/.hermes/cache/scratch/note_1.txt now.
  💻 echo "1" > ~/.hermes/cache/scratch/note_1.txt   (0.1s)
  I've created ~/.hermes/cache/scratch/note_1.txt with the content "1". I'll continue with the remaining files on the next turn as you specified.

  ↻ Continuing toward goal (1/20): Only 1 of 4 files has been created; 3 files remain.

Hermes: [Continuing toward your standing goal]
  💻 echo "2" > ~/.hermes/cache/scratch/note_2.txt   (0.1s)
  Created ~/.hermes/cache/scratch/note_2.txt. Two more to go.

  ↻ Continuing toward goal (2/20): 2 of 4 files created; 2 remain.

Hermes: [Continuing toward your standing goal]
  💻 echo "3" > ~/.hermes/cache/scratch/note_3.txt   (0.1s)
  Created ~/.hermes/cache/scratch/note_3.txt.

  ↻ Continuing toward goal (3/20): 3 of 4 files created; 1 remains.

Hermes: [Continuing toward your standing goal]
  💻 echo "4" > ~/.hermes/cache/scratch/note_4.txt   (0.1s)
  All four files have been created: ~/.hermes/cache/scratch/note_1.txt through ~/.hermes/cache/scratch/note_4.txt, each containing its number.

  ✓ Goal achieved: All four files were created with the specified content, completing the goal.

You: _
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
