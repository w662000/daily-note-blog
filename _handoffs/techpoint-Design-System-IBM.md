---
layout: default
title: 技术点 · Design System: IBM
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Design System: IBM

> 来源：261010_Design System_ IBM_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- > <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
- IBM's website is the digital embodiment of enterprise authority built on the Carbon Design System — a design language so methodically structured it reads like an engineering specification rendered as a webpage. The page operates on a stark duality: a bright white (`#ffffff`) canvas with near-black (`#161616`) text, punctuated by a single, unwavering accent — IBM Blue 60 (`#0f62fe`). This isn't playful tech-startup minimalism; it's corporate precision distilled into pixels. Every element exists within Carbon's rigid 2x grid, every color maps to a semantic token, every spacing value snaps to the 8px base unit.
- What defines IBM's visual identity beyond monochrome-plus-blue is the reliance on Carbon's component token system. Every interactive state maps to a CSS custom property prefixed with `--cds-` (Carbon Design System). Buttons don't have hardcoded colors; they reference `--cds-button-primary`, `--cds-button-primary-hover`, `--cds-button-primary-active`. This tokenized architecture means the entire visual layer is a thin skin over a deeply systematic foundation — the design equivalent of a well-typed API.
- **Key Characteristics:**
- Carbon token system (`--cds-*`) driving all semantic colors, enabling theme-switching at the variable level
- | Focus | `2px solid #0f62fe` inset + `1px solid #ffffff` | Keyboard focus ring |
- Reference `--cds-*` token names when implementing (e.g., `--cds-button-primary`, `--cds-text-primary`)
- | Name | Width | Key Changes |
- 7. Use `--cds-` prefix for token naming to stay Carbon-compatible

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
