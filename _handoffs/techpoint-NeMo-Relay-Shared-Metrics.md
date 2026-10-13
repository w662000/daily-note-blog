---
layout: default
title: 技术点 · NeMo Relay Shared Metrics
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · NeMo Relay Shared Metrics

> 来源：261010_NeMo Relay Shared Metrics_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- execution intercepts, or manual tool-end APIs.
- ```
telemetry:
  shared_metrics:
    enabled: true
```
- ```
gateway:
  telemetry:
    session_segments:
      on_compaction: false  # rotate after context compaction
      max_turns: 0          # 0 = unlimited; N = turns per segment
```
- | Key | Default | Behavior |
- ```
Relay plugins are active process-wide and apply to all profiles hosted by this Hermes process.
```
- run Relay scope, LLM, tool, and mark APIs in that session context. New product
- ```
Hermes turn, API, tool, and approval hooks
  -> Relay session, task, LLM, tool, and mark lifecycle
  -> Hermes shared-metrics subscriber
  -> SQLite counters
  -> immutable JSON delta package
```
- provider attempts for the same Hermes API request ID; they do not inflate the
- ```
$HERMES_HOME/telemetry/shared_metrics/metrics.sqlite3
$HERMES_HOME/telemetry/shared_metrics/outbox/*.json
```
- ```
./.venv/bin/python scripts/smoke_nemo_relay_shared_metrics.py
```
- Transmission is a **separate opt-in** from collection, under a new config key:
- ```
telemetry:
  shared_metrics:
    enabled: false   # collect locally
    send: false      # NEW: transmit to the Nous telemetry service
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
