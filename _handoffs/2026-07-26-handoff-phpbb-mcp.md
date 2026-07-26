---
layout: default
title: phpBB 免费主机论坛 + MCP 扩展 · 交接文档
date: 2026-07-26 23:30:00 +0800
---

# phpBB 免费主机论坛 + MCP 扩展 — 交接文档（人读）

> 更新于 2026-07-26。部署目录：`D:\AI work\bbs1org-deploy\`，站点 `https://w662002.my-place.us/AIblog/`。
> 给接手的同学看。phpBB 装在 my-place.us 的 `/AIblog` 子目录（Softaculous 一键装），原生支持无限级子版块；MCP 扩展为平铺单文件 `mcp.php`。bbs1org（扁平版块）见同批 handoff「bbs1org 免费主机论坛 + MCP 知识库」。

---

## 0. 一句话成果

在 my-place.us 的 `/AIblog` 子目录 Softaculous 装 phpBB，自写平铺单文件 `mcp.php`（内嵌式 MCP，X-Mcp-Token 穿透 iFastNet 代理），暴露 7 个工具，并把 8 篇每日日志经 MCP 发成帖子（Markdown→BBCode 渲染、保留原日期、ACL 自动赋权）。

---

## 1. 背景与目标

- bbs1org 是扁平版块（无 parent_id），用户要真子版块 + MCP + 免费主机可装 → 选 phpBB（Softaculous 一键装、原生无限级子版块、PHP/MySQL 不需 composer）。
- MCP 路线：仿 bbs1org 的 mcp_server 写**内嵌式** phpBB MCP 扩展（全在免费主机上跑，无需额外 Node 进程）。

---

## 2. 时间线（已完成，7.26）

- 18:52 论坛选型调研（phpBB 首选）。
- 19:02 决定 `/AIblog` 子目录 Softaculous 装 phpBB（URL `https://w662002.my-place.us/AIblog/`）。
- 下午收口：原计划写 ext 扩展 `wb/mcpserver/`，实测 phpBB 3.3 bootstrap 禁用超全局 + `submit_post()` 强依赖 `$user->data`/`$auth->acl()` → 改**平铺单文件 `mcp.php`**（include common.php 拿 DI 容器）。
- `mcp.php` 上传（~812 行，7 工具全绿）；8 篇日志经 `migrate_logs.py` 发到 forum_id=10（topic_id 10–17，保留原日期）。
- 20:30 MCP 配置路径踩坑（`.mcp.json` 误建，WorkBuddy 只读 `mcp.json`）。
- 20:36 phpBB 新版块首页不可见修复（ACL 复制）。
- 20:48 `create_forum` 自动赋权改进。
- 20:57 Markdown→BBCode 渲染改进 + 8 篇日志重新发布（topic_id 18–25）。

---

## 3. 关键认知 / 必踩的坑

1. **iFastNet 代理层剥离 Authorization**（同 bbs1org）：用 **`X-Mcp-Token`** 头穿透。mcp.php 的 `wb_token()` 优先读 `HTTP_X_MCP_TOKEN`，回退 `HTTP_AUTHORIZATION`/`getallheaders()`。
2. **WAF aes.js 挑战**：MCP 客户端不执行 JS → 必须带 `Cookie: __test=...`（随出口 IP 变，变了用 `waf_check.py` 重解）。WorkBuddy 配置须同时加 `X-Mcp-Token` + `Cookie: __test=` + 浏览器 UA。
3. **phpBB `$request` 全局冲突**：JSON-RPC 分发里把 `json_decode` 结果命名为 `$request` 会覆盖 phpBB 全局 `$request` → `submit_post` 调 `$request->variable()` 报 "Call to a member function variable() on array"。改局部变量 `$rpc`。
4. **phpBB 文本格式化**：s9e 只认 BBCode 不认 Markdown。`get_topic` 渲染不用 `generate_text_for_display`（需 style 上下文，抛 "Undefined array key style_id"）→ 用 `wb_render_text()` 正则解码 s9e 存储格式成纯文本。`create_topic`/`create_reply` 用 `generate_text_for_storage` 生成 bbcode。
5. **Markdown→BBCode 转换**（`wb_md_to_bbcode` + `wb_md_inline`）：标题→`[size]`、粗体→`[b]`、斜体→`[i]`、行内代码→`[b]`、链接→`[url]`、列表→`[list]`、围栏代码→`[code]`、分割线→`[hr]`、引用→`[quote]`；维护 list/quote/code 状态机。
6. **新版块首页不可见（ACL）**：phpBB `display_forums()` 检查 `f_list` 权限，新建版块在 `acl_groups` 无记录 → `f_list=NO` → 看不到。`wb_create_forum()` 改进：INSERT 后把父版块（或 forum_id=2）的组角色 `INSERT ... SELECT` 复制到新 forum，并 `acl_clear_prefetch()` + 删 `cache/production/data_acl_*`/`data_global*`/`sql_*`。
7. **MCP 配置路径坑（关键）**：WorkBuddy **只读 `mcp.json`（无点）**，误建 `.mcp.json`（带点）不生效。phpbb 条目须写进正确的 `mcp.json`，三个条目并列；新加连接器首次须手动点「信任」。已写入 `~/.workbuddy/MEMORY.md`。
8. **保留原日期**：`create_topic`/`create_reply` 加可选 `created_at`（Unix 时间戳）；不传则 `time()`。迁移脚本用 frontmatter date(+0800) 保留原日期。
9. **限流退避**：phpBB flood-control "请 N 秒后重试" → `migrate_logs.py` 解析 N + 加 3s 等待重试，每篇 6s 间隔，标题幂等跳过。
10. **建管理员 WorkbuddyBot**：phpBB 侧用 `mcp.php?setup=1` 一键建 founder（`USER_FOUNDER`，group_id=5 ADMINISTRATORS）+ 设 `wb_mcp_actor` config。

---

## 4. 部署状态

- 站点：`https://w662002.my-place.us/AIblog/`（phpBB，Softaculous 装于子目录）
- MCP 端点：`https://w662002.my-place.us/AIblog/mcp.php`
- Token：`phpbb_0faf73ae76ae8de08f6fa000e2fd8319f0eeca435e300e53fe38370eb1809b63`（X-Mcp-Token 头）
- 知识库版块：forum_id=9「知识库」(category)、10「AI每日工作日志」、11「AI项目组」（ACL 已自动赋权，匿名 f_list=YES）
- 8 篇日志：topic_id 18–25（forum 10），时间戳单调 18→25 正确
- WorkBuddy：`~/.workbuddy/mcp.json` 加 `phpbb` 条目（X-Mcp-Token + Cookie __test + UA），连接器页「信任」
- DB：phpBB 独立库（Softaculous 自动建），host `sql103.my-place.us`

---

## 5. 关键文件清单

- `bbs1org-deploy/mcp.php` — **phpBB MCP 扩展正本（~812 行）**：include common.php + functions_*；JSON-RPC 分发；7 工具；X-Mcp-Token 认证；`?setup=1` 建 WorkBuddyBot；wb_md_to_bbcode/wb_render_text 转换
- `bbs1org-deploy/migrate_logs.py` — 8 篇日志经 MCP 迁移（幂等 by title、保留原日期、限流退避、6s 间隔）
- `bbs1org-deploy/mcp_verify.py` — 全套 7 工具验证
- `bbs1org-deploy/waf_fetch.py` / `waf_check.py` — 解 WAF `__test` cookie
- `bbs1org-deploy/blog_skin_fixed.php` — bbs1org 根目录博客皮肤插件（同批 bbs1org handoff）

---

## 6. 发布记录

- 8 篇每日工作总结（7-18~25）经 MCP `create_topic` 发到 phpBB forum 10（署名 WorkbuddyBot，Markdown→BBCode 渲染，保留原日期）。