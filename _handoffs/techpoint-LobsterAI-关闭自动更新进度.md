---
layout: default
title: 技术点 · LobsterAI 关闭自动更新进度
date: 2026-09-19 23:30:00 +0800
---

# 技术点 · LobsterAI 关闭自动更新进度

> 来源：260919_LobsterAI 关闭自动更新进度_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 1. 关闭 LobsterAI 进程。
- **Patch 3**：`getState()` 返回状态前强制检查，若状态为 `Ready` 或存在 `readyFilePath`，立即重置为 `Idle`，永远不把 Ready 状态暴露给渲染进程。
- 路径：`C:\Users\Administrator\AppData\Roaming\LobsterAI\updates\lobsterai-update-auto-1789800971150.exe`（约 255MB）
- `DELETE FROM kv WHERE key='app_update_ready_file:auto';`（删除 1 行）
- ```
cp "D:\AI work\workbuddy\2026-09-19-12-31-24\lobsterai_asar_patches\app.asar.bak_20260919_132749" "D:\Program Files\LobsterAI\resources\app.asar"
```
- 自动更新服务器域名：`api-overmind.youdao.com`

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
