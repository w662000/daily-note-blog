---
layout: default
title: 技术点 · TUI
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · TUI

> 来源：261010_TUI_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
# Launch the TUI
hermes --tui

# Resume the latest TUI session (falls back to the latest classic session)
hermes --tui -c
hermes --tui --continue
hermes --tui --resume latest

# Resume a specific session by ID or title
hermes --tui -r 20260409_000000_aa11bb
hermes --tui --resume "my t0p session"

# Resume the latest session for a specific project directory
hermes --tui --resume latest --in ./my-project

# Run source directly — skips the prebuild step (for TUI contributors)
hermes --tui --dev
```
- ```
export HERMES_TUI=1
hermes          # now uses the TUI
hermes chat     # same
```
- ```
display:
  interface: tui   # "cli" (default) or "tui"
```
- Same [skins](features/skins.md) and [personalities](features/personality.md) apply. Switch mid-session with `/skin ares`, `/personality pirate`, and the UI repaints live. See [Skins & Themes](features/skins.md) for the full list of customizable keys and which ones apply to classic vs TUI — the TUI honors the banner palette, UI colors, prompt glyph/color, session display, completion menu, selection bg, `tool_prefix`, and `help_header`.
- ```
export HERMES_TUI_DIR=/path/to/prebuilt/ui-tui
hermes --tui
```
- Keybindings match the [Classic CLI](cli.md#keybindings) exactly. The only behavioral differences:
- On macOS, `F7` means the physical F7 function key. MacBook keyboards may use that row for system controls instead; hold **Fn** (the **globe** key on newer keyboards) while pressing **F7**, or enable **Use F1, F2, etc. keys as standard function keys** in **System Settings → Keyboard → Keyboard Shortcuts → Function Keys**. If the terminal still does not forward it, use the equivalent **Ctrl+R** binding below.
- **`Ctrl+R`** toggles the live dock between its default preview and one summary line. **`F7`** remains an optional alias where the terminal sends function keys through. This does not open the monitor or move composer focus; the choice lasts for this TUI process without changing config.
- | `/help` | Overlay with categorized commands, arrow-key navigable |
- | `/usage` | Rich token / cost / context panel |
- | `/agents` (alias `/tasks`) | Observability overlay — live subagent tree with kill/pause controls, per-branch cost / token / file rollups, turn-by-turn history |
- | `/reload` | Re-reads `~/.hermes/.env` into the running TUI process so newly added API keys take effect without a restart |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
