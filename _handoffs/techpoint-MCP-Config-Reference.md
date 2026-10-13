---
layout: default
title: 技术点 · MCP Config Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · MCP Config Reference

> 来源：261010_MCP Config Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "Reference for Hermes Agent MCP configuration keys, filtering semantics, and utility-tool policy"
- ```
mcp_servers:
  <server_name>:
    command: "..."      # stdio servers
    args: []
    env: {}

    # OR
    url: "..."          # HTTP servers
    headers: {}

    # Optional HTTP/SSE TLS settings:
    ssl_verify: true                # bool or path to a CA bundle (PEM)
    client_cert: "/path/to/cert.pem"  # mTLS client certificate (see below)
    # client_key: "/path/to/key.pem"  # optional, when key lives in a separate file

    enabled: true
    timeout: 120
    connect_timeout: 60
    supports_parallel_tool_calls: false
    tools:
      include: []
      exclude: []
      resources: true
      prompts: true
```
- | Key | Type | Applies to | Meaning |
- | `client_cert` | string or list | HTTP | mTLS client certificate. String = path to a PEM file containing cert + key. List `[cert, key]` = separate files. List `[cert, key, password]` = encrypted key |
- | `client_key` | string | HTTP | Path to the client private key, when `client_cert` is a string and the key is in a separate file |
- ```
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "${env:GITHUB_TOKEN}"   # same as "${GITHUB_TOKEN}"
```
- ```
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    env:
      CACHE_DIR: "${userHome}${/}.cache${/}mcp"
```
- | Key | Type | Meaning |
- ```
tools:
  include: [create_issue, list_issues]
```
- ```
tools:
  exclude: [delete_customer]
```
- ```
tools:
  include: [create_issue]
  exclude: [create_issue, delete_issue]
```
- ```
tools:
  resources: false
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
