---
layout: default
title: 技术点 · Skills 系统
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Skills 系统

> 来源：261010_Skills 系统_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Skills 是 agent 在需要时可以加载的按需知识文档。它们遵循**渐进式披露**（progressive disclosure）模式以最小化 token 用量，并兼容 [agentskills.io](https://agentskills.io/specification) 开放标准。
- 每个已安装的 skill 都会自动作为斜杠命令可用：
- ```
# 在 CLI 或任何消息平台中：
/gif-search funny cats
/axolotl help me fine-tune Llama 3 on my dataset
/github-pr-workflow create a PR for the auth refactor
/songsee analyze the frequency spread of this mix

# 只输入 skill 名称即可加载它，并让 agent 询问你的需求：
/excalidraw
```
- （计划模式的工作方式相同，但现在是内置命令：`/plan [request]` 告知 Hermes 在需要时检查上下文、编写 markdown 实现计划而非直接执行任务，并将结果保存在相对于当前工作区/后端工作目录的 `.hermes/plans/` 下。）
- ```
hermes chat --toolsets skills -q "What skills do you have?"
hermes chat --toolsets skills -q "Show me the axolotl skill"
```
- Skills 使用一种节省 token 的加载模式：
- ```
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Level 1: skill_view(name)        → Full content + metadata       (varies)
Level 2: skill_view(name, path)  → Specific reference file       (varies)
```
- ```
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]     # Optional — restrict to specific OS platforms
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]    # Optional — conditional activation (see below)
    requires_toolsets: [terminal]   # Optional — conditional activation (see below)
    config:                          # Optional — config.yaml settings
      - key: my.setting
        description: "What this controls"
        default: "value"
        prompt: "Prompt for setup"
---

# Skill Title

## When to Use
Trigger conditions for this skill.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes and fixes

## Verification
How to confirm it worked.
```
- ```
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders, FindMy)
platforms: [macos, linux]     # macOS and Linux
```
- 设置后，该 skill 会在不兼容的平台上自动从系统提示词、`skills_list()` 和斜杠命令中隐藏。若省略，则在所有平台上加载。
- 当 skill 响应（或任何 agent 响应）包含指向媒体文件的裸绝对路径时——例如 `/home/user/screenshots/diagram.png`——gateway 会自动检测到它，将其从可见文本中剥离，并以原生方式将文件传递给用户的聊天界面（Telegram 图片、Discord 附件等），而不是在消息中留下原始路径。
- 如果响应（或其中任何文本——通常是最后一行）包含字面指令 `[[as_document]]`，则从该响应中提取的每个媒体路径都会作为文档/文件附件传递，而不是图片气泡：

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
