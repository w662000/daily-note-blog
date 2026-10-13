---
layout: default
title: 技术点 · Memory Providers
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Memory Providers

> 来源：261010_Memory Providers_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
hermes memory setup      # interactive picker + configuration
hermes memory status     # check what's active
hermes memory off        # disable external provider
```
- ```
memory:
  provider: openviking   # or honcho, mem0, holographic, retaindb, byterover, supermemory,
                         # or hindsight (plugin catalog — run `hermes plugins install hindsight` first)
```
- | **Requires** | `pip install honcho-ai` + [API key](https://app.honcho.dev) or self-hosted instance |
- `contextCadence` — how often the base layer refreshes (API call frequency)
- ```
hermes memory setup        # select "honcho" — runs the Honcho-specific post-setup
```
- **Headless / remote machines:** for cloud auth on a box without a browser (SSH, remote VM), pick **device** at the wizard's auth-method prompt. The CLI prints a short code and a verification link; open the link in a browser on any other machine, approve, and setup completes — no API key copy-paste. The wizard defaults to this option automatically when it detects no usable local browser.
- | Key | Default | Description |
- | `apiKey` | -- | API key from [app.honcho.dev](https://app.honcho.dev) |
- | `aiPeer` | host key | AI peer identity (one per profile) |
- | `workspace` | host key | Shared workspace ID |
- | `contextTokens` | `null` (uncapped) | Token budget for auto-injected context per turn. Truncates at word boundaries |
- | `contextCadence` | `1` | Minimum turns between `context()` API calls (base layer refresh) |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
