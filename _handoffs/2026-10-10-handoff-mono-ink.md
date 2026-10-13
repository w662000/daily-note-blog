---
layout: default
title: 交接文档 · mono-ink
date: 2026-10-13 23:30:00 +0800
---

# mono-ink

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\creative\baoyu-article-illustrator\references\palettes\mono-ink.md

Black ink on pure white with sparse semantic accent colors

## Background

- Color: Pure White (#FFFFFF)
- Texture: Clean, no grain, no tint

## Colors

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Pure White | #FFFFFF | Canvas |
| Primary | Near Black | #1A1A1A | All lines, text, figures, arrows |
| Accent (risk/emphasis) | Coral Red | #E8655A | Risk, problem, gap, key emphasis |
| Accent (positive) | Muted Teal | #5FA8A8 | Positive, solution, "after" state |
| Accent (neutral tag) | Dusty Lavender | #9B8AB5 | Neutral tags, category labels |
| Soft Fill | Pale Gray | #F0F0F0 | Subtle zone backgrounds (optional) |

## Accent

Use black ink for all structural elements — lines, text, figures. Accent colors appear only for semantic highlighting: coral red for risks/gaps/problems, muted teal for positive/solution/after-states, dusty lavender for neutral category tags. Total colored pixels must remain under 10% of canvas. Pale gray may back a subtle zone but must never dominate.

## Semantic Constraint

Black ink on white canvas. Accent colors for semantic highlighting only — total colored pixels under 10% of canvas. Do NOT render color names, hex codes, or role labels as visible text in the image.

## Compatible With

- `ink-notes` (primary, default pairing)
- `minimal` (strict monochrome variation, drops the style's built-in accent)
- `sketch` (pencil + ink hybrid look)

## Not Recommended With

- `sketch-notes` — its "no pure white backgrounds" rule conflicts
- `warm`, `elegant`, `watercolor`, `fantasy-animation` — color-heavy by design, mono-ink strips their identity

## Best For

Professional visual notes, Before/After essays, tech manifestos, framework analogies, whiteboard-presentation explainers
