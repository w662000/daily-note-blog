---
layout: default
title: 技术点 · Verify
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Verify

> 来源：261010_Verify_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
cd <build project>
npm i playwright-core                       # once

node <skill>/scripts/serve.mjs --root . --port 4500 &
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/shots
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/mobile --width 390 --height 844
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/reduced --reduced-motion
```
- available, so a high-key page can report clean over text that is failing. The
- **Cues are keyed by their text.** Two cues that share a string, which
- if nothing else is generating against the same key. When builds run in parallel,
- (codecs, keyframes, resolution). **"One clip works and another does not, on
- **Keyboard.** Tab through. Focus order matches visual order, the focus ring is
- | Keyboard focus landing on a control nobody can see | The browser's scroll-into-view parks the element barely on screen, which is where its cue has not opened, and the opacity check still passes. **The engine now centres it on `focusin`** when the element is inside a `[data-sc-act]` and its cue is under 0.85. That fixes the off-screen half. See the note below for what it does not fix |
- ```
curl -s http://localhost:45XX | grep -o "<title>.*</title>"
curl -s -o /dev/null -w "%{http_code}
" http://localhost:45XX/assets/leg01.mp4
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
