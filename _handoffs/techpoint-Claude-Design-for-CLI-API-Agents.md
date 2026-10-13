---
layout: default
title: 技术点 · Claude Design for CLI/API Agents
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Claude Design for CLI/API Agents

> 来源：261010_Claude Design for CLI_API Agents_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Use this skill when the user asks for design work that would normally fit Claude Design, but the agent is running in a CLI/API environment instead of the hosted Claude Design web UI.
- **Before starting, check for other web-design skills like `popular-web-designs` (ready-to-paste design systems for Stripe, Linear, Vercel, Notion, etc.) and `design-md` (Google's DESIGN.md token spec format).** If the user wants a known brand's look, load `popular-web-designs` alongside this one and let it supply the visual vocabulary. If the deliverable is a token spec file rather than a rendered artifact, use `design-md` instead. Full decision table below.
- | **claude-design** (this one) | Design *process and taste* — how to scope a brief, gather context, produce variants, verify a local HTML artifact, avoid AI-design slop | a from-scratch designed artifact (landing page, prototype, deck, component lab, motion study) with no specific brand or token system dictated |
- | **design-md** | Google's DESIGN.md spec format — author/validate/diff/export design-token files, WCAG contrast checking, Tailwind/DTCG export | a formal, persistent, machine-readable design-system *spec file* (tokens + rationale) that lives in a repo and gets consumed by agents over time |
- **Author the tokens spec itself** → design-md
- These compose: use `popular-web-designs` for the visual vocabulary, `claude-design` for how to turn a brief into a thoughtful local HTML file, and `design-md` when the output is the token file rather than a rendered artifact.
- You are running in **CLI/API mode**, not the Claude Design hosted web UI.
- design-systems designer for tokens, components, and visual rules
- Do not use this skill for pure DESIGN.md token authoring unless the user specifically asks for a DESIGN.md file. Use `design-md` for that.
- 4. design tokens
- token files
- 7. **Command / Inspect** — the user is driving by keyboard or drilling into one object (command bars, inspectors, detail panes, property editors). Speed and focus over breadth.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
