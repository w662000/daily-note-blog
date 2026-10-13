---
layout: default
title: 技术点 · CLI Interface
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · CLI Interface

> 来源：261010_CLI Interface_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "Master the Hermes Agent terminal interface — commands, keybindings, personalities, and more"
- ```
# Start an interactive session (default)
hermes

# Single query mode (non-interactive)
hermes chat -q "Hello"

# Single query from a file or stdin — nothing is shell-interpreted, so
# arbitrary text (quotes, $(...), backticks) arrives verbatim
hermes chat --query-file prompt.txt
hermes chat --query-file - < prompt.txt

# With a specific model
hermes chat --model "anthropic/claude-sonnet-4"

# With a specific provider
hermes chat --provider nous        # Use Nous Portal
hermes chat --provider openrouter  # Force OpenRouter

# With specific toolsets
hermes chat --toolsets "web,terminal,skills"

# Start with one or more skills preloaded
hermes -s hermes-agent-dev,github-auth
hermes chat -s github-pr-workflow -q "open a draft PR"

# Resume previous sessions
hermes --continue             # Resume the most recent CLI session (-c)
hermes --resume <session_id>  # Resume a specific session by ID (-r)
hermes --resume latest        # Resume the most recent session (same as -c)
hermes --resume latest --in ./dir  # Resume ./dir's latest session, staying in ./dir

# Verbose mode (debug output)
hermes chat --verbose

# Isolated git worktree (for running multiple agents in parallel)
hermes -w                         # Interactive mode in worktree
hermes -w -z "Fix issue #123"     # Single query in worktree
```
- ```
hermes worktree list              # audit: age, size, verdict, reason per tree
hermes worktree list --json       # machine-readable audit (trees, external trees, branches)
hermes worktree prune             # remove safe trees + delete merged branches
hermes worktree prune --dry-run   # show the plan without changing anything
hermes worktree prune --older-than 7   # only reap trees idle for 7+ days
hermes worktree prune --trees-only     # leave local branches alone
hermes worktree prune --branches-only  # leave worktrees alone
```
- ```
hermes plugins install owner/repository --no-enable
hermes plugins list
hermes plugins enable <plugin-name>
hermes plugins disable <plugin-name>
hermes plugins update <plugin-name>
hermes plugins remove <plugin-name>
```
- ```
 ☤ claude-sonnet-4-20250514 │ 12.4K/200K │ [██████░░░░] 6% │ $0.06 │ 15m
```
- | Token count | Context tokens used / max context window; `~` marks an estimate |
- | Cost | Estimated session cost (or `n/a` for unknown/zero-priced models). Rates come from Hermes' bundled official price table, then the provider's `/models` listing; on a direct first-party API (OpenAI, xAI, Anthropic, Google, DeepSeek, Xiaomi) a model missing from both is priced at the vendor's list price from models.dev. Proxies, relays and custom endpoints serving the same model id stay `n/a` rather than inherit that price. |
- Use `/usage` for a detailed breakdown including per-category costs (input vs output tokens).
- On macOS, `F6`/`F7` mean the physical function keys, not the media/system controls shown on the top row. Hold **Fn** (the **globe** key on newer keyboards) while pressing the function key, or enable **Use F1, F2, etc. keys as standard function keys** in **System Settings → Keyboard → Keyboard Shortcuts → Function Keys**. The reliable terminal fallbacks are **Ctrl+T** for `F6` and **Ctrl+R** for `F7`.
- | Key | Action |
- | `Ctrl+B` | Start/stop voice recording when voice mode is enabled (`voice.record_key`, default: `ctrl+b`) |
- | `Ctrl+R` / `F7` | Toggle the live work dock between its multi-row preview and a single summary line without moving composer focus. `Ctrl+R` is the reliable fallback when macOS reserves the function-key row. Besides subagents and background processes, the dock shows a standing `/goal` (active, parked or paused, with turns used) on its top row and the prompts waiting in `/queue` on its bottom rows. |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
