---
layout: default
title: 交接文档 · 每日工作总结多端自动发布系统
date: 2026-07-22 23:30:00 +0800
---

# 每日工作总结多端自动发布系统 — 交接文档（人读）

> 更新于 2026-07-26（跨度 7.22–7.26）。脚本根目录：`D:\AI work\workbuddy\`（publish_daily_summary.py / sync_logs_to_github.py / handoff/handoff_flow.py）。
> 给接手的同学看。本系统把每天的工作日志自动分发到多个端，是周期内**持续时间最长、文件/自动化最多**的工程之一。

---

## 0. 一句话成果

搭了一套「每日工作总结 → 多端自动发布」流水线：23:30 生成总结并推 GitHub（博客源+语雀源）、23:35 写 Gridea 浓缩版、23:35 本机发语雀、23:30 handoff 自动发布；含失败兜底/failover/离线兜底、Gridea 浓缩版生成、博客暗亮主题。

---

## 1. 背景与目标

- 分发端：GitHub Pages 博客（`daily-note-blog`）、语雀知识库（`w662000/ylv5l7`）、Gridea Pro 浓缩版、Ech0（说说，7-23 移除）、flomo（早期，已移除）。
- 目标：零人工、幂等、失败不致命（push 失败落本地，等网络/gh 就绪即生效）。

---

## 2. 时间线（已完成）

- **7-22**：Ech0 本地备份部署（端口 6277/6278）；23:59 三端发布跑通（Gridea 待手动同步、语雀改云端 Action 防 429）。
- **7-23 上午**：Gridea 浓缩版固化为 23:35 自动化（`automation-1784789409252`），≤200 字，待手动点同步。
- **7-23 17:01**：健康检查三触发器 ACTIVE；教会 Hermes 兜底发布（脚本副本进 `.hermes\memories\`，Hermes cron 建两个 paused 任务）。
- **7-23 20:10**：从自动发布链路移除 Ech0。
- **7-24 晚**：语雀发布改**本机 23:35**（不再依赖云端 Action）→ `automation-1784824382385`。
- **7-25**：handoff 自动发布流程（`handoff_flow.py`，23:30）；Gridea 重复文件去重修复。
- **7-26**：handoff 会话感知（`handoff_config.json`）；博客加暗/亮主题（与 github.io 统一，共享 `flavor-theme` 键）。

---

## 3. 关键认知 / 必踩的坑

1. **语雀 429 限流**：本地与云端双发会顶满额度 → 语雀统一由单一通道发（先云端 Action，后改本机 23:35）。`publish_daily_summary.py` 默认跳过语雀（`WB_LOCAL_PUBLISH_YUQUE=1` 才强发）。
2. **语雀 v2 API 成功响应无 `status` 字段**（结构 `{"data":{...},"meta":{...}}`）→ 判定成功用 `HTTP 200 and data.id 存在`，否则误报 FAIL（已在 handoff_flow.py 修）。
3. **requests 死代理**：默认读环境 `HTTP_PROXY=127.0.0.1:10808` → 连不上语雀。必须 `proxies={"http":None,"https":None}` 强制直连。
4. **git push 失败不致命**：`git_commit_push` 失败仅提示，内容已落本地仓库，配好 `gh` 后下次 push 即生效；`handoff_flow.py` 还做 `pull --rebase` 重试抗 fast-forward。
5. **Gridea 草稿不发布**：`published: false` 永不发布，必须 `published: true`（两次踩同款）。Gridea 仍需用户在 Gridea Pro 手动点「同步」才真正上线。
6. **Gridea 重复文件**：脚本生成稿与手动草稿 frontmatter `title` 相同 → Gridea 显示两份。`handoff_flow.py` 的 `gen_gridea()` 加幂等防御：扫描 `posts/*.md`，凡 `title==GRIDEA_TITLE` 且文件名≠目标的一律删。
7. **沙箱无外网但 git push 通**：Bash/Python urllib 抓外网永远 `HTTP 000`（rc=35），但 git push 走另一套 egress 是通的。勿因早期 curl 测不出网就默认不能 push。
8. **博客暗亮主题统一**：改写 `daily-note-blog/_layouts/default.html`，`:root` 暗色变量照搬 flavor-theme，`.theme-light` 亮色，共用 `localStorage['flavor-theme']`；修暗绿标题（`--accent`→`--fg`）。

---

## 4. 部署状态

- 博客：`https://w662000.github.io/daily-note-blog/`（GitHub Pages，Jekyll，`deploy.yml` push master 自动构建）
- 语雀知识库：`w662000/ylv5l7`（repo id 81530735）
- Gridea Pro：待发布目录 `C:\Users\Administrator\Documents\Gridea Pro\posts\`（手动同步）
- Ech0（已移除自动发布，仍本地运行）：`D:\shuoshuo\data`，端口 6277/6278

---

## 5. 关键文件清单

- `workbuddy/publish_daily_summary.py` — 发布当日总结（默认跳过语雀）
- `workbuddy/sync_logs_to_github.py` — 23:30 复制到 `workbuddy-daily-note/summaries/`（语雀源）+ `daily-note-blog/_posts/`（博客源）并 push
- `workbuddy/handoff/handoff_flow.py` — handoff 自动发布（归档+Gridea+博客+语雀直连），会话感知 `handoff_config.json`
- `C:\Users\Administrator\.hermes\memories\publish_daily_summary.py` / `sync_logs_to_github.py` / `gridea_write_condensed.py` / `DAILY_PUBLISH_WORKFLOW.md` — Hermes 兜底副本
- `D:\AI work\workbuddy-daily-note\` — 语雀源仓库
- `D:\AI work\daily-note-blog\` — 博客仓库（`_layouts/default.html` 暗亮主题、`_posts/`、`.github/workflows/`）

---

## 6. 发布记录（自动化 cron）

- **23:30 每日总结生成**（`automation-1784700756809`）：生成总结 + 推博客源 + 语雀源。
- **23:35 写 Gridea 浓缩版**（`automation-1784789409252`）：写 Gridea 待发布稿（手动同步）。
- **23:35 发布语雀（本机）**（`automation-1784824382385`）：本机 `publish_to_yuque.py`。
- **23:30 handoff 自动发布**（`automation-1784951947030`）：跑 `handoff_flow.py`。
- 历史：23:59 语雀云端 Action 早期主通道，后改本机 23:35；00:15/09:30/10:00 为 failover/离线兜底（含 Ech0 巡检已删）。