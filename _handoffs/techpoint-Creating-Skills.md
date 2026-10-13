---
layout: default
title: 技术点 · Creating Skills
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Creating Skills

> 来源：261010_Creating Skills_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- It wraps an external CLI or API that the agent can call via `terminal` or `web_extract`
- It doesn't need custom Python integration or API key management baked into the agent
- It requires end-to-end integration with API keys, auth flows, or multi-component configuration
- ```
skills/
├── research/
│   └── arxiv/
│       ├── SKILL.md              # Required: main instructions
│       └── scripts/              # Optional: helper scripts
│           └── search_arxiv.py
├── productivity/
│   └── ocr-and-documents/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
└── ...
```
- ```
---
name: my-skill
description: Brief description (shown in skill search results)
version: 1.0.0
author: Your Name
license: MIT
platforms: [macos, linux]          # Optional — restrict to specific OS platforms
                                   #   Valid: macos, linux, windows
                                   #   Omit to load on all platforms (default)
metadata:
  hermes:
    tags: [Category, Subcategory, Keywords]
    related_skills: [other-skill-name]
    requires_toolsets: [web]            # Optional — only show when these toolsets are active
    requires_tools: [web_search]        # Optional — only show when these tools are available
    fallback_for_toolsets: [browser]    # Optional — hide when these toolsets are active
    fallback_for_tools: [browser_navigate]  # Optional — hide when these tools exist
    config:                              # Optional — config.yaml settings the skill needs
      - key: my.setting
        description: "What this setting controls"
        default: "sensible-default"
        prompt: "Display prompt for setup"
    blueprint:                              # Optional — marks this skill a runnable automation
      schedule: "0 9 * * *"              #   cron expr / "every 2h" / ISO timestamp
      deliver: origin                    #   optional (default origin)
      prompt: "Task instruction for each run"  # optional
      no_agent: false                    # optional
required_environment_variables:          # Optional — env vars the skill needs
  - name: MY_API_KEY
    prompt: "Enter your API key"
    help: "Get one at https://example.com"
    required_for: "API access"
---

# Skill Title

Brief intro.

## When to Use
Trigger conditions — when should the agent load this skill?

## Quick Reference
Table of common commands or API calls.

## Procedure
Step-by-step instructions the agent follows.

## Pitfalls
Known failure modes and how to handle them.

## Verification
How the agent confirms it worked.
```
- ```
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders)
platforms: [macos, linux]     # macOS and Linux
platforms: [windows]          # Windows only
```
- ```
metadata:
  hermes:
    requires_toolsets: [web]           # Hide if the web toolset is NOT active
    requires_tools: [web_search]       # Hide if web_search tool is NOT available
    fallback_for_toolsets: [browser]   # Hide if the browser toolset IS active
    fallback_for_tools: [browser_navigate]  # Hide if browser_navigate IS available
```
- **Use case for `fallback_for_*`:** Create a skill that serves as a workaround when a primary tool isn't available. For example, a `duckduckgo-search` skill with `fallback_for_tools: [web_search]` only shows when the web search tool (which requires an API key) is not configured.
- **Use case for `requires_*`:** Create a skill that only makes sense when certain tools are present. For example, a web scraping workflow skill with `requires_toolsets: [web]` won't clutter the prompt when web tools are disabled.
- ```
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: "Tenor API key"               # Shown when prompting user
    help: "Get your key at https://tenor.com"  # Help text or URL
    required_for: "GIF search functionality"   # What needs this var
```
- ```
terminal:
  env_passthrough:
    - MY_CUSTOM_VAR
    - ANOTHER_VAR
```
- Use `required_environment_variables` when a skill needs an API key or token. Missing values do **not** hide the skill from discovery. Instead, Hermes prompts for them securely when the skill is loaded in the local CLI.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
