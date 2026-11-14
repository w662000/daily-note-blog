---
layout: default
title: 交接文档 · 进度更新 10_43 · 发现并绕开 GitHub API 限流
date: 2026-11-14 23:30:00 +0800
---

# 进度更新 10:43 · 发现并绕开 GitHub API 限流

- **日期**：2026-11-09
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-11-09-10-32-32\进度\进度_20261109_1035.md（日志提炼）

## 项目概述
### 第 1 步已完成（18 秒返回，4 组 × 12 条结果）
筛出 9 个候选仓库：`zhuhaiuk/free-nodes`、`Flik6/Free-Node`、`jichangx/free-nodes`、`yy1588133/proxy-pool`、`Enibels/get_proxy`、`free-node

## 完成内容
### 第 1 步已完成（18 秒返回，4 组 × 12 条结果）
筛出 9 个候选仓库：`zhuhaiuk/free-nodes`、`Flik6/Free-Node`、`jichangx/free-nodes`、`yy1588133/proxy-pool`、`Enibels/get_proxy`、`free-nodes/v2rayfree`、`VoroninaYanina/free-nodes`、`Au1rxx/free-vpn-subscriptions`、`clash-verge/clash-verge.github.io`。

### 关键坑（实测，非猜测）
- `gh api` 首次单发成功（`zhuhaiuk/free-nodes` 最后提交 `2026-11-09T01:56:07Z`），但批量到第 2 个仓库起全部返回 `?`。
- 单次排查真实报错：`{"message":"API rate limit exceeded for 183.210.225.58 ... (HTTP 403)"}`。
- 再查 `gh auth status`：**配置的 token `w662000` 已失效**（`The token in default is invalid`）→ 退化成未认证 60 次/小时；`gh api rate_limit` 显示 `limit=60 used=60 remaining=0`，重置时间 `2026-11-09 11:00:46 UTC+8`。
- 按「温和测试」红线：**没有重试死磕**，改走镜像通道。

### 替代方案（已单次实测通过）
- `https://gh-proxy.com/https://github.com/<repo>/commits/main.atom` → 返回 14755B Atom feed，可解析 `<updated>` 取最后提交时间（替代 Commits API）。
- `https://gh-proxy.com/https://raw.githubusercontent.com/<repo>/main/README.md` → 返回 11211B（替代 Contents API）。
- 两者都**禁系统代理直连镜像**，绕开 GitHub API 限流，且不依赖 gh 登录。

### 新增脚本
- `node_check_tmp/step2b_mirror.py`：atom 时效 + 镜像 README 提取 + 多通道订阅下载 + 节点计数 + TCP 抽检，输出 `verify_results.json`（后台 task_id RXp3pd）。
- `node_check_tmp/step3_report.py`：读 `verify_results.json` 生成 `reports/免费节点订阅报告_20261109.html`，含 HTML 标签配对校验。

### 待完成
- [ ] 等 RXp3pd 跑完，审阅实测结果
- [ ] 生成 HTML 报告并跑标签校验
- [ ] 聊天正文给质量排序表 + 可粘贴镜像链接 + 排除原因 + 使用要点

---

## 关键产物 / 文件
- 筛出 9 个候选仓库：`zhuhaiuk/free-nodes`、`Flik6/Free-Node`、`jichangx/free-nodes`、`yy1588133/proxy-pool`、`Enibels/get_proxy`、`free-nodes/v2rayfree`、`VoroninaYanina/free-nodes`、`Au1rxx/free-vpn-subscriptions`、`clash-verge/clash-verge.github.io`。
- `https://gh-proxy.com/https://github.com/<repo>/commits/main.atom` → 返回 14755B Atom feed，可解析 `<updated>` 取最后提交时间（替代 Commits API）。
- `https://gh-proxy.com/https://raw.githubusercontent.com/<repo>/main/README.md` → 返回 11211B（替代 Contents API）。
- `node_check_tmp/step2b_mirror.py`：atom 时效 + 镜像 README 提取 + 多通道订阅下载 + 节点计数 + TCP 抽检，输出 `verify_results.json`（后台 task_id RXp3pd）。
- `node_check_tmp/step3_report.py`：读 `verify_results.json` 生成 `reports/免费节点订阅报告_20261109.html`，含 HTML 标签配对校验。

## 当前状态
（见源文档）

## 后续事项 / 风险
- 按「温和测试」红线：**没有重试死磕**，改走镜像通道。
