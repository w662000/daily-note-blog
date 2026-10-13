---
layout: default
title: 技术点 · 每日工作总结 · 两端自动发布流程（Gridea + 语雀）(Daily Summary Publish)
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · 每日工作总结 · 两端自动发布流程（Gridea + 语雀）(Daily Summary Publish)

> 来源：261010_每日工作总结 · 两端自动发布流程（Gridea + 语雀）(Daily Summary Publish)_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- > 目标：把当天的「每日工作总结」md 同步发布到 **Gridea Pro（静态博客·浓缩版）**、**语雀（知识库）** 两个平台（Ech0 / 说说 已于 2026-07-23 从自动发布链路移除，blog + 语雀 已够用）。
- ```
源文件: D:\AI work\workbuddy\<日期目录>\<日期>_每日工作总结.md
   │
   ├─→ Gridea Pro : 写 md 到 posts 目录        （之后用户手动点「同步」部署）
   └─→ 语雀 Yuque : API POST 到知识库           （全自动；23:59 由云端 Action 发布）
   （注：说说 Ech0 已于 2026-07-23 移除，不再自动发布）
```
- **推荐做法**：各端由独立脚本/任务处理（见 §5 与 §9）；`publish_daily_summary.py` 现仅负责语雀（且默认交由云端 Action 发布，本地不重复调用），两端均幂等。
- | Ech0 服务 | ~~容器运行，`http://localhost:6277` 可访问~~ **（已于 2026-07-23 从发布链路移除，无需此服务）** |
- | 语雀 Token | 有效（`I51oLvFNAsVQGuTRJjdnMOmYr4F5OTKSRmkNtRMg`，带 doc 权限） |
- WorkBuddy 运行脚本用：
- ```
C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe <脚本>.py
```
- Hermes 原生部署时改用其自带 venv（路径稳定、不随 WB 卸载消失）：
- ```
D:\hermes-agent\venv\Scripts\python.exe C:\Users\Administrator\.hermes\memories\<脚本>.py
```
- **特点：Agent 只负责把稿件文件写好，真正发布需要用户手动在 Gridea Pro 里点「同步」。**
- 配置文件：`C:\Users\Administrator\AppData\Roaming\Gridea Pro\config.json`（site path 指向上述目录）
- ```
---
id: 683fdj            # 6 位随机字母数字，每次生成即可
title: workbuddy-260722-每日工作总结
createdAt: "2026-07-22 23:59:00"
updated: "2026-07-22 23:59:00"
tags: ["workbuddy"]
tag_ids: []
categories: []
published: true
hideInList: false
feature: ""
isTop: false
---
# 每日工作总结 · 2026-07-22
（正文 = 源 md 内容）
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
