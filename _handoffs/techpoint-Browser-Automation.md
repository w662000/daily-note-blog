---
layout: default
title: 技术点 · Browser Automation
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Browser Automation

> 来源：261010_Browser Automation_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: Control browsers with multiple providers, local Chromium-family browsers via CDP, or cloud browsers for web interaction, form filling, scraping, and more.
- **Firecrawl cloud mode** via [Firecrawl](https://firecrawl.dev) for cloud browsers with built-in scraping
- Key capabilities:
- If you have a paid [Nous Portal](https://portal.nousresearch.com) subscription, you can use browser automation through the **[Tool Gateway](tool-gateway.md)** without any separate API keys. New installs can run `hermes setup --portal` to log in and turn on every gateway tool at once; existing installs can pick **Nous Subscription** as the browser provider via `hermes model` or `hermes tools`.
- ```
# Add to ~/.hermes/.env
BROWSER_USE_API_KEY=***
```
- Get your API key at [browser-use.com](https://browser-use.com).
- ```
# Add to ~/.hermes/.env
BROWSERBASE_API_KEY=***
BROWSERBASE_PROJECT_ID=your-project-id-here
```
- The `.env` keys above supply **credentials only**. The active cloud browser is chosen by the `browser.cloud_provider` selection written by `hermes tools` → Browser Automation (`browserbase`, `browser-use`, `camofox`, or `nous` for the Nous Subscription). Once a selection exists, adding or removing a key does not switch providers — and a selected provider with a missing key errors with guidance to run `hermes tools` instead of silently rerouting. Never-configured setups still autodetect from available credentials.
- ```
# Add to ~/.hermes/config.yaml
browser:
  backend: "off"
```
- Browser Use's own cloud browsers need `browser-use auth login` or `BROWSER_USE_API_KEY`; other browser sources use their existing credentials unchanged.
- ```
# Add to ~/.hermes/.env
FIRECRAWL_API_KEY=fc-***
```
- Get your API key at [firecrawl.dev](https://firecrawl.dev). Then select Firecrawl as your browser provider:

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
