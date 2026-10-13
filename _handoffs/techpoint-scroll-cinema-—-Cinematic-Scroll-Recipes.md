---
layout: default
title: 技术点 · scroll-cinema — Cinematic Scroll Recipes
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · scroll-cinema — Cinematic Scroll Recipes

> 来源：261010_scroll-cinema — Cinematic Scroll Recipes_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Stack default 2026: **GSAP 3.13 + ScrollTrigger 3.13 (free), Lenis 1.3, Three.js r170+, CSS scroll-driven animations (Chrome 115+ / Safari 26) with `@supports` fallback on GSAP. View Transitions API — 88.64% global support.**
- | Mood/state shift between two AI-generated keyframes | WebGL displacement shader transition |
- | Page-to-page continuity, shared-element morphs | View Transitions API |
- ```
# H.264 baseline for Safari/old Android, VP9 for Chrome
ffmpeg -i source.mp4 -c:v libx264 -profile:v baseline -level 3.1 -pix_fmt yuv420p \
  -movflags +faststart -crf 23 hero.mp4
ffmpeg -i source.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 hero.webm

# Teaser (first 1-2s, < 200KB) — poster effect while main loads
ffmpeg -i source.mp4 -t 2 -c:v libx264 -profile:v baseline -level 3.1 -crf 28 teaser.mp4
```
- ```
<video id="hero" src="/hero.webm" muted playsinline preload="metadata"></video>
```
- ```
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import Lenis from 'lenis'

gsap.registerPlugin(ScrollTrigger)

const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
gsap.ticker.lagSmoothing(0)

const video = document.querySelector('#hero')
video.pause()

ScrollTrigger.create({
  trigger: video,
  start: 'top top',
  end: '+=400%',
  pin: true,
  scrub: 0.5,          // 0 = instant, number = smoothing in seconds; use 0.3–0.8
  onUpdate: (self) => {
    video.currentTime = self.progress * video.duration
  },
})
```
- ```
# From video/CGI at 30 fps:
ffmpeg -i render.mp4 -vf "fps=30" -q:v 5 frames/frame_%04d.jpg
# WebP (smaller):
ffmpeg -i render.mp4 -vf "fps=30" -lossless 0 -compression_level 4 -q:v 70 frames/frame_%04d.webp
```
- ```
<canvas id="seq" width="1920" height="1080" role="img" aria-label="Product animation"></canvas>
<div style="height: 400vh"></div>
```
- ```
const canvas = document.getElementById('seq')
const ctx = canvas.getContext('2d')
const FRAME_COUNT = 120
const frames = new Array(FRAME_COUNT)

function preloadFrame(i) {
  return new Promise(resolve => {
    const img = new Image()
    img.onload = () => { frames[i] = img; resolve() }
    img.onerror = resolve  // don't crash on a broken frame
    img.src = `/frames/frame_${String(i + 1).padStart(4, '0')}.webp`
  })
}

async function preloadAll() {
  // batch 8 at a time — avoids saturating the network
  for (let i = 0; i < FRAME_COUNT; i += 8) {
    await Promise.all(
      Array.from({ length: 8 }, (_, k) => i + k)
        .filter(k => k < FRAME_COUNT)
        .map(k => preloadFrame(k))
    )
  }
}

function draw(progress) {
  const idx = Math.min(FRAME_COUNT - 1, Math.floor(progress * FRAME_COUNT))
  if (frames[idx]) ctx.drawImage(frames[idx], 0, 0, canvas.width, canvas.height)
}

// Drive with ScrollTrigger (raw scroll listeners are banned by this skill):
preloadAll().then(() => {
  ScrollTrigger.create({
    trigger: '#seq',
    start: 'top top',
    end: '+=400%',
    pin: true,
    scrub: 0.3,
    onUpdate: (self) => draw(self.progress),
  })
})
```
- **Use when:** pixel-accurate product spin, text-in-frame scenes, A/B-swappable keyframes.
- ```
npm i gsap lenis
# ScrollTrigger is free since 2024; only SplitText and MorphSVG are Club-only
```
- ```
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import Lenis from 'lenis'
import 'lenis/dist/lenis.css'

gsap.registerPlugin(ScrollTrigger)

const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)      // keep ScrollTrigger in sync with Lenis
gsap.ticker.add((time) => lenis.raf(time * 1000))
gsap.ticker.lagSmoothing(0)                  // prevent GSAP catching up after tab blur
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
