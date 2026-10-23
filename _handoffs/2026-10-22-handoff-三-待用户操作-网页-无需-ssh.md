---
layout: default
title: 交接文档 · 三、待用户操作（网页，无需 SSH）
date: 2026-10-23 23:30:00 +0800
---

# 三、待用户操作（网页，无需 SSH）

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\进度\进度_20261022_2210.md（日志提炼）

## 项目概述
1. GitHub 建公开仓库，上传 `searxng-render/` 下 4 个文件到根目录。
2. Render → New → Web Service → 连仓库；Runtime=Docker，Build/Start 留空，Free 套餐。
3. 环境变量：`SEARXNG_SECRET`（Render 的 G

## 完成内容
1. GitHub 建公开仓库，上传 `searxng-render/` 下 4 个文件到根目录。
2. Render → New → Web Service → 连仓库；Runtime=Docker，Build/Start 留空，Free 套餐。
3. 环境变量：`SEARXNG_SECRET`（Render 的 Generate 按钮或本地 python 生成）、
   `SEARXNG_BASE_URL=https://实际域名.onrender.com/`；Health Check Path 填 `/healthz`。
4. 部署后按 README 第六节验证（/healthz、/config、JSON 搜索）。
5. 需要的话配 UptimeRobot 每 10 分钟 ping /healthz 保活。

## 关键产物 / 文件
- （见源文档）

## 当前状态
（见源文档）

## 后续事项 / 风险
- （见源文档）
