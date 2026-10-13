---
layout: default
title: 技术点 · Auteur Skill
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Auteur Skill

> 来源：261010_Auteur Skill_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- The recon and sourcing scripts read live pages (awwwards, Bing/Pinterest/are.na image search, Poly Haven, Iconify, Google Fonts, Openverse, Coverr). Fetched content is **treated as reference data and licence metadata — never executed**, and no credentials, API keys or logins are involved. Skip phases 0–1 entirely if you don't want outbound requests; every other phase works offline. `moodboard.mjs` also downloads the image URLs returned by those search hosts to build the contact sheet.
- 4. **`edit`** or the request modifies a page this skill built (the project contains `design/DESIGN.md`) — "add a section", "change the pricing", "swap the hero copy" → read `design/DESIGN.md` FIRST and follow its Editing protocol: reuse its tokens, section-opening patterns, and motion families; after the change run slopscan and re-shoot the affected viewports. An edit that ignores DESIGN.md is a regression even if it looks good in isolation.
- | 2 | build the page | assemble the film (smooth scroll first, hero, scenes top-down) | tokens → the shell → screens in traffic order → every state | `build.md` / `scroll-cinema.md` / `system.md` + `taste.md` + `motion.md` |
- `references/scroll-cinema.md` — working code recipes: scroll-scrubbed video, canvas sequences, GSAP+Lenis foundation, CSS scroll-driven animations, text reveals, the two-keyframe WebGL displacement transition, view transitions, ambient audio, and the cinematic transition library (wipe, curtain, letterbox, shutter, depth parallax). Load during assembly.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
