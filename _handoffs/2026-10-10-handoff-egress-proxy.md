---
layout: default
title: 交接文档 · Egress proxy
date: 2026-10-13 23:30:00 +0800
---

# Egress proxy

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\website\docs\user-guide\egress\index.md

---
title: Egress proxy
sidebar_position: 1
---

# Egress proxy

Optional outbound credential-injection firewall for remote terminal sandboxes. The sandbox only ever holds opaque proxy tokens; real API keys never leave the host.

- [iron-proxy](./iron-proxy) — single-binary TLS-intercepting proxy from [ironsh/iron-proxy](https://github.com/ironsh/iron-proxy), lazy-installed and managed by `hermes egress`.
