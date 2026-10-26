---
layout: default
title: 技术点 · 事实核对报告（rev-r2 / att_mvjr5dc93soih）
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · 事实核对报告（rev-r2 / att_mvjr5dc93soih）

> 来源：261022_事实核对报告（rev-r2 _ att_mvjr5dc93soih）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
- 已修项：保持 `default_locale: zh-Hans-CN` + `limiter:false` + 字段名修正 + `method:POST` 不改；通过标准 `/healthz` 200、`/search?format=json` 200。
- 未解证实风险（真正该做的3件）：
  1. 反代层补 JSON 鉴权 → 裸 `GET /search` 返回 401/403。
  2. 稳住部署健康 → `/healthz` 200 且 `/search` 200。
  3. 降 brave 默认权重/禁用 + Tavily 兜底 duckduckgo → `unresponsive_engines` 不再持续超时。

### 关键技术要点（自动抽取）
- 本环境无 Bash/WebFetch，线上"实测"沿用输入文件 [E1]–[E8]（对 searxng-render-gn0d.onrender.com 的 2026-10-23 实测）。
- 3. **致命级 #3 `method: "POST"` 切断 GET → 证伪**。仓库 line68 仍保留 POST，且 [E2][E3] 是在 method:POST 生效实例上的 GET 成功实测（200 JSON）。`server.method` 只影响 HTML 表单，不限制 /search 路由。红队把"最危险第3"判错了。
- 6. **JSON 接口裸奔 [E7] → 证实且当前仓库仍未修**，是真正未解最高危项；红队未单列，被 #3 误判掩盖。
- 7. 方案A 直连绕过 → 维持**推测**；方案B token 方向 → **证实**。
- 2. 稳住部署健康 → `/healthz` 200 且 `/search` 200。
- 红队方向对（#1/#2 与字段名错误均证实且已修），但**最危险第3项（method:POST）判错（证伪）**，真正该紧急处理的是它没单列、且当前仓库仍裸奔的 **JSON 接口鉴权**。

## 三、关键产物与命令
- 主报告：`D:\AI work\workbuddy\2026-10-22-22-03-16\评审输出_事实核对_20261023.md`

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
