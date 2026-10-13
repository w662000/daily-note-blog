---
layout: default
title: 交接文档 · WorkBuddy 工作日志生成指南
date: 2026-10-13 23:30:00 +0800
---

# WorkBuddy 工作日志生成指南

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\user-operational-guidelines\references\workbuddy-worklog-generation.md

> 从 workbuddy 日历文件夹读取每日工作总结并生成结构化日志

## 目录结构

workbuddy 使用日期命名的文件夹存放每日工作：
```
D:/AI work/workbuddy/
├── 2026-07-18-19-00-53/
│   └── 2026-07-18_每日工作总结.md
├── 2026-07-19-09-49-20/
│   └── 2026-07-19_每日工作总结.md
└── ...
```

## 读取策略

### 1. 列出日期文件夹
```bash
ls -d "D:/AI work/workbuddy/2026-07*" "D:/AI work/workbuddy/2026-08*" | sort
```

### 2. 查找每日总结文件
```bash
ls "D:/AI work/workbuddy/2026-07-18-19-00-53/"
# 输出: 2026-07-18_每日工作总结.md
```

### 3. 读取内容
使用 `read_file` 工具读取 `*_每日工作总结.md` 文件。

## 派生 Agent 并行读取

对于多日期范围，可派出多个 agent 并行读取：

| Agent | 日期范围 |
|-------|----------|
| Agent 1 | 7/18-7/21 |
| Agent 2 | 7/22-7/25 |
| Agent 3 | 7/27-7/30 |
| Agent 4 | 7/31-8/2 |
| Agent 5 | 8/3-8/4 |

## 生成每日日志

读取后生成结构化的每日工作日志：
```markdown
# 每日工作总结 · YYYY-MM-DD

## 一、今日完成事项
1. **项目/任务名称**：描述
2. ...

## 二、技术要点
- 关键点1
- 关键点2

## 三、遗留事项
- 待办1
```

## 保存路径

每日日志保存到：
```
D:/workspace/YYYY-MM-DD/work-log-YYYY-MM-DD.md
```

综合报告保存到：
```
D:/workspace/YYYY-MM-DD/工作总结学习报告-START-END.md
```
