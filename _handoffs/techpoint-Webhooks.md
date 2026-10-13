---
layout: default
title: 技术点 · Webhooks
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Webhooks

> 来源：261010_Webhooks_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
hermes gateway setup
```
- ```
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644        # default
WEBHOOK_SECRET=your-global-secret
```
- ```
curl http://localhost:8644/health
```
- ```
{"status": "ok", "platform": "webhook"}
```
- Routes define how different webhook sources are handled. Each route is a named entry under `platforms.webhook.extra.routes` in your `config.yaml`. Adapter settings (`port`, `host`, `secret`, `routes`) may also be written directly under `platforms.webhook:` — both spellings reach the adapter; a value nested under `extra:` wins if the same key appears in both places.
- | `toolsets` | No | List of toolset keys (e.g. `["terminal", "file", "web"]`) that **replaces** the platform-level webhook toolset for runs triggered by this route only. Manual config edit only — not settable via `hermes webhook subscribe`, so agent-created subscriptions cannot self-grant elevated tools. Names are validated the same way as `platform_toolsets` entries (unknown or platform-restricted names are dropped). See [Per-route toolsets](#per-route-toolsets). |
- | `deliver_extra` | No | Additional delivery config — keys depend on `deliver` type (e.g. `repo`, `pr_number`, `chat_id`). Values support the same `{dot.notation}` templates as `prompt`. |
- | `coalesce` | No | Debounce rapid distinct events on the same logical entity into one agent run. Block with a required `key` (payload field or template identifying the entity, e.g. `pull_request.number`), optional `window_seconds` (quiet window, default 30) and `max_wait_seconds` (dispatch cap, default 300). See [Event Coalescing](#event-coalescing). Mutually exclusive with `deliver_only` and `cron_job`. |
- ```
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "global-fallback-secret"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review this pull request:
            Repository: {repository.full_name}
            PR #{number}: {pull_request.title}
            Author: {pull_request.user.login}
            URL: {pull_request.html_url}
            Diff URL: {pull_request.diff_url}
            Action: {action}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
        deploy-notify:
          events: ["push"]
          secret: "deploy-secret"
          prompt: "New push to {repository.full_name} branch {ref}: {head_commit.message}"
          filters:
            - field: "ref"
              equals: "refs/heads/main"
          deliver: "telegram"
```
- ```
platforms:
  webhook:
    extra:
      routes:
        todoist:
          events: ["item:updated"]
          secret: "todoist-secret"
          filters:
            - field: "payload.labels"
              contains: "hermes"
            - any:
                - field: "payload.priority"
                  equals: 4
                - field: "payload.project_id"
                  in_file: "~/.hermes/data/todoist/watchlist.json"
          prompt: "Todoist task changed: {payload.content}"
```
- `contains` for strings, lists, and dict keys
- `in_file` for JSON arrays, JSON objects (keys are used), or newline-delimited text files

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
