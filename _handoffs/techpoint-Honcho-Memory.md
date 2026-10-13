---
layout: default
title: 技术点 · Honcho Memory
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Honcho Memory

> 来源：261010_Honcho Memory_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- [Honcho](https://github.com/plastic-labs/honcho) is an AI-native memory backend that adds dialectic reasoning and deep user modeling on top of Hermes's built-in memory system. Instead of simple key-value storage, Honcho maintains a running model of who the user is — their preferences, communication style, goals, and patterns — by reasoning about conversations after they happen.
- | Cross-session persistence | ✔ File-based MEMORY.md/USER.md | ✔ Server-side with API |
- ```
hermes memory setup    # select "honcho" from the provider list
```
- ```
# ~/.hermes/config.yaml
memory:
  provider: honcho
```
- ```
echo 'HONCHO_API_KEY=***' >> ~/.hermes/.env
```
- Get an API key at [honcho.dev](https://honcho.dev).
- Both layers are concatenated and truncated to the `contextTokens` budget (if set).
- | `contextCadence` | Turns between `context()` API calls (base layer refresh) | `1` |
- When pointing Hermes at a self-hosted Honcho server, `hermes honcho setup` (and `hermes memory setup`) ask for a **local JWT / bearer token** after the base URL. Paste a JWT signed with the server's `AUTH_JWT_SECRET` (the Honcho compose env var) to enable authenticated access; leave it blank for servers running with `AUTH_USE_AUTH=false`. The local token is stored under the host block (`hosts.<host>.apiKey` in `honcho.json`), separate from any cloud `apiKey`, so you can flip the `Cloud or local?` prompt back to `cloud` later without losing either credential.
- | Key | Default | Description |
- | `contextTokens` | `null` (uncapped) | Token budget for auto-injected context per turn. Set to an integer (e.g. 1200) to cap. Truncates at word boundaries |
- | `contextCadence` | `1` | Minimum turns between `context()` API calls (base layer refresh) |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
