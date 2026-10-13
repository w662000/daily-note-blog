---
layout: default
title: 技术点 · MCP (Model Context Protocol)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · MCP (Model Context Protocol)

> 来源：261010_MCP (Model Context Protocol)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- MCP lets Hermes Agent connect to external tool servers so the agent can use tools that live outside Hermes itself — GitHub, databases, file systems, browser stacks, internal APIs, and more.
- ```
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```
- ```
hermes chat
```
- ```
List the files in /home/user/projects and summarize the repo structure.
```
- 4. **Save.** Hermes saves the server configuration, the tokens and your setup
- values together, once the server has accepted the new token and the first
- connection has returned. If the server rejects the token, or you cancel
- configuration and tokens stay as they were, and a failed form reopens with
- tokens; Hermes asks you to authorize again only when they no longer work.
- ```
hermes mcp                   # interactive picker (default)
hermes mcp catalog           # plain-text list, scriptable
hermes mcp install deepwiki  # install a catalog entry by name
```
- ```
deepwiki     available              Ask questions about public GitHub repositories
linear       enabled                Linear issue/project management (remote OAuth)
github       installed (disabled)   GitHub repo + PR tools
```
- **API key** — Hermes prompts at install time and writes the value to

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
