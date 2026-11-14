---
layout: default
title: 交接文档 · 启动器要点（按 win-py-daemon-launcher + windows-launcher-safety）
date: 2026-11-14 23:30:00 +0800
---

# 启动器要点（按 win-py-daemon-launcher + windows-launcher-safety）

- **日期**：2026-11-12
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-11-12-23-22-49\进度\进度_20261113_1257.md（日志提炼）

## 项目概述
- 纯 ASCII、无 BOM、CRLF（Node 校验：nonASCII=0、bareLF=0、BOM=false → PASS）
- 不用 `chcp 65001`、不用模糊 `taskkill /IM`
- `start "" /min node.exe server_8852.js`：Node 无 nodew，

## 完成内容
- 纯 ASCII、无 BOM、CRLF（Node 校验：nonASCII=0、bareLF=0、BOM=false → PASS）
- 不用 `chcp 65001`、不用模糊 `taskkill /IM`
- `start "" /min node.exe server_8852.js`：Node 无 nodew，用最小化独立窗口常驻，服务自己写日志
- 端口预检：已监听则只开浏览器，不重复启动
- 25 秒就绪轮询，避免「连接被拒绝」竞态
- `>nul` 仅用于 findstr 探测输出，launcher.log 全程记录

## 关键产物 / 文件
- `start "" /min node.exe server_8852.js`：Node 无 nodew，用最小化独立窗口常驻，服务自己写日志

## 当前状态
（见源文档）

## 后续事项 / 风险
- （见源文档）
