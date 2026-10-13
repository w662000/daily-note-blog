---
layout: default
title: 技术点 · Skills System
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Skills System

> 来源：261010_Skills System_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Skills are on-demand knowledge documents the agent can load when needed. They follow a **progressive disclosure** pattern to minimize token usage and are compatible with the [agentskills.io](https://agentskills.io/specification) open standard.
- ```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --no-skills
```
- ```
hermes profile create research --no-skills
```
- ```
hermes skills opt-out            # stop future seeding — nothing on disk is touched
hermes skills opt-out --remove   # also delete UNMODIFIED bundled skills (confirms first)
hermes skills opt-in --sync      # undo: remove the marker and re-seed now
```
- ```
# In the CLI or any messaging platform:
/gif-search funny cats
/axolotl help me fine-tune Llama 3 on my dataset
/github-pr-workflow create a PR for the auth refactor
/songsee analyze the frequency spread of this mix

# Just the skill name loads it and lets the agent ask what you need:
/excalidraw
```
- at the start — every leading `/skill` token (up to 5) is loaded, and the rest
- ```
/github-pr-workflow /test-driven-development fix issue #123 and open a PR
```
- Parsing stops at the first token that isn't an installed skill, so arguments
- ```
/ocr-and-documents ~/.hermes/cache/scratch/scan.pdf extract the tables   # loads one skill; ~/.hermes/cache/scratch/scan.pdf is the argument
```
- ```
hermes chat --toolsets skills -q "What skills do you have?"
hermes chat --toolsets skills -q "Show me the axolotl skill"
```
- ```
# A local SDK or doc directory — read with read_file / search_files
/learn the REST client in ~/projects/acme-sdk, focus on auth + pagination

# An online doc page — fetched with web_extract
/learn https://docs.example.com/api/quickstart

# The workflow you just walked the agent through in this conversation
/learn how I just deployed the staging server

# Pasted notes / a described procedure
/learn filing an expense: open the portal, New > Expense, attach the receipt, submit

# A whole book, paper stack, or large docs corpus — becomes a knowledge-base skill
/learn ~/books/designing-data-intensive-applications.pdf
```
- Skills use a token-efficient loading pattern:

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
