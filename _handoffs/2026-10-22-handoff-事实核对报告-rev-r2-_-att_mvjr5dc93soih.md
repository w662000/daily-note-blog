---
layout: default
title: 交接文档 · 事实核对报告（rev-r2 _ att_mvjr5dc93soih）
date: 2026-11-14 23:30:00 +0800
---

# 事实核对报告（rev-r2 / att_mvjr5dc93soih）

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\旧团队产物备份_searxng评审\rev-r2\att_mvjr5dc93soih\report.md

## 任务
逐条证实/证伪红队挑错评审的结论，并对证实项给带通过标准的落地做法。

## 方法
- Read 了红队评审全文、仓库真实三文件（settings.yml / entrypoint.sh / Dockerfile）、输入原文第2节。
- 本环境无 Bash/WebFetch，线上"实测"沿用输入文件 [E1]–[E8]（对 searxng-render-gn0d.onrender.com 的 2026-10-23 实测）。
- 关键发现：仓库 settings.yml 已是**修正后版本**（文件头8条修正），红队所指字段名/致命错误在仓库中已被作者修正。

## 核心结论
1. **致命级 #1 `ui.default_locale: zh_CN`（下划线）→ 证实**（仓库已改为 `zh-Hans-CN`，证明原错误真实存在且已修）。
2. **致命级 #2 `limiter: true` + botdetection 段 → 证实**（仓库已 `limiter: false`、删 botdetection，证明修正生效）。
3. **致命级 #3 `method: "POST"` 切断 GET → 证伪**。仓库 line68 仍保留 POST，且 [E2][E3] 是在 method:POST 生效实例上的 GET 成功实测（200 JSON）。`server.method` 只影响 HTML 表单，不限制 /search 路由。红队把"最危险第3"判错了。
4. **8 条字段名错误 → 全部证实**（对照输入原文确有，且仓库已逐条修正）。
5. **`SEARXNG_LIMITER_ENABLED` 误用 → 证实**；**`${...}` 插值风险 → 证伪**（entrypoint.sh line20-43 实际做替换，风险已化解）。
6. **JSON 接口裸奔 [E7] → 证实且当前仓库仍未修**，是真正未解最高危项；红队未单列，被 #3 误判掩盖。
7. 方案A 直连绕过 → 维持**推测**；方案B token 方向 → **证实**。

## 落地做法（仅证实项，附通过标准）
- 已修项：保持 `default_locale: zh-Hans-CN` + `limiter:false` + 字段名修正 + `method:POST` 不改；通过标准 `/healthz` 200、`/search?format=json` 200。
- 未解证实风险（真正该做的3件）：
  1. 反代层补 JSON 鉴权 → 裸 `GET /search` 返回 401/403。
  2. 稳住部署健康 → `/healthz` 200 且 `/search` 200。
  3. 降 brave 默认权重/禁用 + Tavily 兜底 duckduckgo → `unresponsive_engines` 不再持续超时。

## 一句话
红队方向对（#1/#2 与字段名错误均证实且已修），但**最危险第3项（method:POST）判错（证伪）**，真正该紧急处理的是它没单列、且当前仓库仍裸奔的 **JSON 接口鉴权**。

## 产物
- 主报告：`D:\AI work\workbuddy\2026-10-22-22-03-16\评审输出_事实核对_20261023.md`
