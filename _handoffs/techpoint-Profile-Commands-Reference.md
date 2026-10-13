---
layout: default
title: 技术点 · Profile Commands Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Profile Commands Reference

> 来源：261010_Profile Commands Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
hermes profile <subcommand>
```
- ```
hermes profile list
```
- ```
$ hermes profile list
  default
* work
  dev
  personal
```
- ```
hermes profile use <name>
```
- ```
hermes profile use work
hermes profile use default
```
- ```
hermes profile create <name> [options]
```
- ```
# Blank profile — needs full setup
hermes profile create mybot

# Clone config only from current profile
hermes profile create work --clone

# Clone everything from current profile
hermes profile create backup --clone-all

# Clone config from a specific profile
hermes profile create work2 --clone-from work

# Clone everything from a specific profile
hermes profile create work2-backup --clone-from work --clone-all
```
- ```
hermes profile describe [<name>] [options]
```
- ```
# Read the current description
hermes profile describe researcher

# Set it explicitly
hermes profile describe researcher --text "Reads source code and writes findings."

# Let the LLM generate one
hermes profile describe researcher --auto

# Fill in descriptions for every profile that doesn't have one
hermes profile describe --all --auto
```
- ```
hermes profile delete <name> [options]
```
- ```
hermes profile delete mybot
hermes profile delete mybot --yes
```
- ```
hermes profile show <name>
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
