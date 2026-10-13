---
layout: default
title: 技术点 · Plugins
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Plugins

> 来源：261010_Plugins_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
~/.hermes/plugins/my-plugin/
├── plugin.yaml      # manifest
├── __init__.py      # register() — wires schemas to handlers
├── schemas.py       # tool schemas (what the LLM sees)
└── tools.py         # tool handlers (what runs when called)
```
- ```
name: hello-world
version: "1.0"
description: A minimal example plugin
```
- ```
"""Minimal Hermes plugin — registers a tool and a hook."""

import json


def register(ctx):
    # --- Tool: hello_world ---
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name to greet",
                }
            },
            "required": ["name"],
        },
    }

    def handle_hello(params, **kwargs):
        del kwargs
        name = params.get("name", "World")
        return json.dumps({"success": True, "greeting": f"Hello, {name}!"})

    ctx.register_tool(
        name="hello_world",
        toolset="hello_world",
        schema=schema,
        handler=handle_hello,
    )

    # --- Hook: log every tool call ---
    def on_tool_call(tool_name, params, result):
        print(f"[hello-world] tool called: {tool_name}")

    ctx.register_hook("post_tool_call", on_tool_call)
```
- Every `ctx.*` API below is available inside a plugin's `register(ctx)` function.
- | Inject messages | `ctx.inject_message(content, role="user", session_key=...)` - see [Injecting Messages](#injecting-messages) |
- | Gate on env vars | `requires_env: [API_KEY]` in plugin.yaml — prompted during `hermes plugins install` |
- ```
plugins:
  enabled:
    - my-tool-plugin
    - disk-cleanup
  disabled:       # optional deny-list — always wins if a name appears in both
    - noisy-plugin
  # Optional: deadline (seconds) for each Git clone, fetch or checkout
  # during plugin installation, including automatic memory-provider migration.
  # Default 300; values above 3600 are clamped. A subdirectory install
  # (owner/repo/path/to/plugin) downloads only that folder's files.
  clone_timeout_seconds: 300
  # Optional: wall-clock cap (seconds) for timeout-bounded in-process Python
  # plugin hook callbacks (hot-path observers + pre_tool_call). Default 30;
  # set 0 to disable; values above 600 are clamped. Timed-out pre_tool_call
  # callbacks fail closed (block the tool). Caller-thread hooks such as
  # subagent_stop are never moved onto a timeout worker.
  # Shell hooks keep their own per-entry timeout under the top-level hooks: key.
  hook_callback_timeout: 30
  # Optional: deadline (seconds) for one plugin's import + register() at load.
  # A plugin that overruns it is skipped with the reason "load timed out after
  # Ns" (reported like any other load failure: the startup warning and the
  # in-session `/plugins` listing) and the remaining plugins keep loading; the
  # stuck thread is abandoned. Default 10; set 0 to disable; values above 600
  # are clamped.
  load_timeout_seconds: 10
```
- ```
hermes plugins                    # interactive toggle (space to check/uncheck)
hermes plugins enable <name>      # add to allow-list
hermes plugins disable <name>     # remove from allow-list + add to disabled
```
- ```
hermes plugins install owner/repo --ref 0123456789abcdef0123456789abcdef01234567
```
- stale or revoked token cannot break a public install. Only when the remote
- 1. `GITHUB_TOKEN` or `GH_TOKEN` from your `.env` (GitHub hosts only).
- `hermes doctor` sends a configured `GITHUB_TOKEN`/`GH_TOKEN` to `api.github.com`

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
