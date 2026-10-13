---
layout: default
title: 技术点 · Image Generation
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Image Generation

> 来源：261010_Image Generation_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- If you have a paid [Nous Portal](https://portal.nousresearch.com) subscription, you can use image generation through the **[Tool Gateway](tool-gateway.md)** without a FAL API key. Your model selection persists across both paths. New installs can run `hermes setup --portal` to log in and turn on every gateway tool at once; existing installs can pick **Nous Subscription** as the image-gen backend via `hermes tools`.
- If the managed gateway returns `HTTP 4xx` for a specific model, that model isn't yet proxied on the portal side — the agent will tell you so, with remediation steps (switch to FAL.ai in `hermes tools` with your own `FAL_KEY` for direct access, or pick a different model).
- 2. Generate an API key from your dashboard
- ```
hermes tools
```
- Navigate to **🎨 Image Generation**, pick your backend (Nous Subscription or FAL.ai), then the picker shows all supported models in a column-aligned table — arrow keys to navigate, Enter to select:
- ```
  Model                          Speed    Strengths                    Price
  fal-ai/flux-2/klein/9b         <1s      Fast, crisp text             $0.006/MP   ← currently in use
  fal-ai/flux-2-pro              ~6s      Studio photorealism          $0.03/MP
  fal-ai/z-image/turbo           ~2s      Bilingual EN/CN, 6B          $0.005/MP
  ...
```
- ```
image_gen:
  provider: fal                 # `nous` if you picked Nous Subscription
  model: fal-ai/flux-2/klein/9b
  max_parallel_requests: 4      # concurrent images in one tool-call batch
```
- `image_gen.provider` is the single selection key: `nous` routes through the managed Tool Gateway; a vendor name (`fal`, `openai`, `xai`, `krea`, ...) goes direct with your own key. The runtime always follows this stored selection — a `FAL_KEY` in `.env` is ignored while `provider: nous`, and `provider: fal` without `FAL_KEY` errors with `image_gen is configured to use fal (set via hermes tools), but FAL_KEY is not set. Run 'hermes tools' to change it.` rather than silently rerouting. Change providers via `hermes tools`, not by adding/removing keys. (The old `use_gateway` boolean is legacy — still read as `nous` when `true`, but never written anymore.)
- [Image API](https://openrouter.ai/docs/guides/overview/multimodal/image-generation)
- Optional per-request knobs for Image API models go under the scoped config
- section (or `OPENROUTER_IMAGE_API_*` env vars):
- ```
image_gen:
  provider: openrouter
  model: bytedance-seed/seedream-4.5
  openrouter:
    resolution: 2K        # model-dependent: 1K / 2K / 4K
    quality: high         # gpt-image models
    output_format: png
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
