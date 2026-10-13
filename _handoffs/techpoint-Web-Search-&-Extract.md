---
layout: default
title: 技术点 · Web Search & Extract
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Web Search & Extract

> 来源：261010_Web Search & Extract_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | **Firecrawl** (default) | `FIRECRAWL_API_KEY` (optional — keyless when selected) | ✔ | ✔ | 500 credits/mo · keyless cloud when selected |
- | **Brave Search (free tier)** | `BRAVE_SEARCH_API_KEY` | ✔ | — | 2 000 queries/mo |
- | **DDGS (DuckDuckGo)** | — (no key) | ✔ | — | ✔ Free |
- | **Exa** | `EXA_API_KEY` (optional) | ✔ | ✔ | ✔ Keyless ring member · 1 000 searches/mo with key |
- | **Parallel** | `PARALLEL_API_KEY` (optional) | ✔ | ✔ | ✔ Keyless ring member · paid with key |
- | **Tavily** | `TAVILY_API_KEY` (optional) | ✔ | ✔ | ✔ Opt-in keyless when selected |
- | **Perplexity** | `PERPLEXITY_API_KEY` | ✔ | ✔ (query-relevant snippets) | Paid (per-request Search API pricing) |
- | **Keenable** | `KEENABLE_API_KEY` (optional) | ✔ | ✔ | ✔ Keyless ring member · paid with key |
- | **xAI (Grok)** | `XAI_API_KEY` or `hermes auth add xai-oauth` | ✔ | — | Paid (SuperGrok or per-token) |
- Brave Search, DDGS, xAI, and OpenAI Native are **search-only** — pair any of them with Firecrawl/Tavily/Perplexity/Keenable/Exa/Parallel when you also need `web_extract`. DDGS uses the [`ddgs` Python package](https://pypi.org/project/ddgs/) under the hood; if it isn't already installed, run `pip install ddgs` (or let Hermes lazy-install it on first use). xAI runs Grok's server-side `web_search` tool on the Responses API — results are LLM-generated rather than index-backed, so titles, descriptions, and URL choice are all model output (see the [trust-model caveat](#xai-grok) below). OpenAI Native declares the same kind of provider-executed tool on the Codex Responses endpoint (see [below](#openai-native)).
- :::info Works out of the box — keyless free-tier rotation
- A fresh install with **no web credentials at all** gets working `web_search` and `web_extract` out of the box: requests rotate round-robin across the ring vendors' public free tiers — **Exa, Parallel, Firecrawl, and Keenable** — spreading load evenly, and a rate-limited request automatically retries on the next vendor in the ring (multi-hop, until one serves or all are throttled). No signup, no key. This tier is strictly last-resort — any configured backend or present API key always wins — and requests carry no user identifiers (only a random per-process session id, rotated on restart). For guaranteed, unthrottled service, set up a keyed provider. Disable the keyless tier entirely with `web.keyless_fallback: false`.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
