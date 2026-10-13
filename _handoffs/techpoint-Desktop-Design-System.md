---
layout: default
title: 技术点 · Desktop Design System
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Desktop Design System

> 来源：261010_Desktop Design System_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- concern, tokens over literals, flat over boxed.** If you reach for a raw color,
- **Named contracts** (tokens, `Button` variants, primitive names) are the
- design system's current API. They are maintained *with* the code: if you
- change a primitive, token, or variant, update its entry here **in the same
- structure may use token hairlines sparingly.
- 4. **Tokens, not literals.** Reference CSS vars (`--ui-*`, `--shadow-nous`,
- **One action, one home.** A command may have keyboard, palette, and visible
- ```
shadow-nous           /* downward-weighted, layered contact→ambient falloff */
border-(--stroke-nous) /* currentColor hairline, theme-adaptive */
```
- one-offs; if elevation needs to change, change the token.
- Drag affordances may use tokenized
- keyed list, retaining the current item when more arrive. Inline and floating
- on button/keyboard decisions. Consumers supply the existing surface tokens and

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
