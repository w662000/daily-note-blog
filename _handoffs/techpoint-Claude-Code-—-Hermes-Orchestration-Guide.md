---
layout: default
title: 技术点 · Claude Code — Hermes Orchestration Guide
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Claude Code — Hermes Orchestration Guide

> 来源：261010_Claude Code — Hermes Orchestration Guide_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **Auth:** run `claude` once to log in (browser OAuth for Pro/Max, or set `ANTHROPIC_API_KEY`)
- **Console auth:** `claude auth login --console` for API key billing
- ```
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```
- ```
# Start a tmux session
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")

# Launch Claude Code inside it
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")

# Wait for startup, then send your task
# (after ~3-5 seconds for the welcome screen)
terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor the auth module to use JWT tokens' Enter")

# Monitor progress by capturing the pane
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")

# Send follow-up tasks
terminal(command="tmux send-keys -t claude-work 'Now add unit tests for the new JWT code' Enter")

# Exit when done
terminal(command="tmux send-keys -t claude-work '/exit' Enter")
```
- Claude Code presents up to two confirmation dialogs on first launch. You MUST handle these via tmux send-keys:
- ```
❯ 1. Yes, I trust this folder    ← DEFAULT (just press Enter)
  2. No, exit
```
- **Handling:** `tmux send-keys -t <session> Enter` — default selection is correct.
- ```
❯ 1. No, exit                    ← DEFAULT (WRONG choice!)
  2. Yes, I accept
```
- ```
tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter
```
- ```
# Launch with permissions bypass
terminal(command="tmux send-keys -t claude-work 'claude --dangerously-skip-permissions \"your task\"' Enter")

# Handle trust dialog (Enter for default "Yes")
terminal(command="sleep 4 && tmux send-keys -t claude-work Enter")

# Handle permissions dialog (Down then Enter for "Yes, I accept")
terminal(command="sleep 3 && tmux send-keys -t claude-work Down && sleep 0.3 && tmux send-keys -t claude-work Enter")

# Now wait for Claude to work
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -60")
```
- | `claude auth login` | Sign in (add `--console` for API billing, `--sso` for Enterprise) |
- | `claude setup-token` | Set up long-lived auth token (requires subscription) |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
