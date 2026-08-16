---
layout: default
title: 技术点 · bbs1org 免费主机论坛 + MCP 知识库 — 交接文档（人读）
date: 2026-07-26 23:30:00 +0800
---

# 技术点 · bbs1org 免费主机论坛 + MCP 知识库 — 交接文档（人读）

> 来源：260726_bbs1org免费主机论坛_MCP知识库_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260726_bbs1org免费主机论坛_MCP知识库_handoff.md（编码探测：utf-8）
- > 更新于 2026-07-26。部署目录：`D:\AI work\bbs1org-deploy\`，站点 `http://w662002.my-place.us`。
- 在免费主机 my-place.us（iFastNet）用 bbs1org 极简 PHP 论坛建站（`http://w662002.my-place.us`），装 mcp_server 插件把论坛变成 AI 可写的 MCP 知识库，并修通 iFastNet WAF aes.js 挑战与代理层剥离 Authorization 的穿透方案。另在 `/AIblog` 子目录装 phpBB 并写 MCP 扩展（见同批 phpBB handoff）。
- 在免费 PHP 主机上跑一个轻论坛 + 插件式 MCP 知识库（AI 经 MCP 读/写帖子），成本 0。难点：iFastNet 免费主机的 WAF（`__test` cookie aes.js 挑战）+ 代理层剥离 `Authorization` 头。
- 下午（MCP 打通）：解 WAF + `X-Mcp-Token` 穿透代理 + 10 工具打通 + 建 2 知识库版块 + 8 篇日志经 MCP 发布。
- 21:17/21:37 blog_skin 插件"看不到"修复 + 加"博客效果"开关。
- 1. **my-place.us 注册 IP 一致性**：iFastNet 要求"注册提交 IP == 激活点击 IP"，走 Cloudflare 代理注册、直连点激活 → 被拒。全程统一网络重注册；FTP 主机以 cPanel 显示的 `ftpupload.net` 为准；MySQL host 填 `sql103.my-place.us`（非 localhost）；FTP/cPanel/MySQL 三套密码同凭据。
- 2. **bbs1org 500 根因**：`index.php` 第 3 行 `declare(strict_types=1)` 必须是脚本第一条语句；插调试代码会触发编译期 fatal。排错用**外部 wrapper**（`debug.php` include index.php），不动原文件头。
- 3. **MariaDB 兼容性双病灶**（标"MySQL 5.7"实为 MariaDB 11.4.12）：① `WITH PARSER ngram` → 删掉；② `INSERT ... AS new ON DUPLICATE KEY UPDATE col=new.col` → 改 `col=VALUES(col)`。
- 4. **iFastNet WAF aes.js 挑战**：非浏览器 UA 请求被丢包。解：复刻 aes.js → `AES.new(a,AES.MODE_CBC,b).decrypt(c)` → cookie `__test=...`（随出口 IP 变，变了用 `waf_check.py` 重解）。脚本 `waf_fetch.py`/`waf_check.py`。
- 5. **代理层剥离 Authorization（致命）**：实测 `HTTP_AUTHORIZATION` 全 missing、`getallheaders()` 不存在 → **自定义头 `X-Mcp-Token`/`X-Auth-Token` 能穿透**。MCP 客户端必须用它而非 `Authorization`。
- 6. **bbs1org 插件机制 = 从 DB 读 manifest，不读文件**：运行时从 `app_plugins.manifest_json` 读 hook，**直接 FTP 改 `plugin.php` 不生效**；必须触发 `plugin_registry_sync()`（把 `app_settings.plugin_sync_pending` 置 `1`，访问任意页即同步）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. **my-place.us 注册 IP 一致性**：iFastNet 要求"注册提交 IP == 激活点击 IP"，走 Cloudflare 代理注册、直连点激活 → 被拒。全程统一网络重注册；FTP 主机以 cPanel 显示的 `ftpupload.net` 为准；MySQL host 填 `sql103.my-place.us`（非 localhost）；FTP/cPanel/MySQL 三套密码同凭据。
2. **bbs1org 500 根因**：`index.php` 第 3 行 `declare(strict_types=1)` 必须是脚本第一条语句；插调试代码会触发编译期 fatal。排错用**外部 wrapper**（`debug.php` include index.php），不动原文件头。
3. **MariaDB 兼容性双病灶**（标"MySQL 5.7"实为 MariaDB 11.4.12）：① `WITH PARSER ngram` → 删掉；② `INSERT ... AS new ON DUPLICATE KEY UPDATE col=new.col` → 改 `col=VALUES(col)`。
4. **iFastNet WAF aes.js 挑战**：非浏览器 UA 请求被丢包。解：复刻 aes.js → `AES.new(a,AES.MODE_CBC,b).decrypt(c)` → cookie `__test=...`（随出口 IP 变，变了用 `waf_check.py` 重解）。脚本 `waf_fetch.py`/`waf_check.py`。
5. **代理层剥离 Authorization（致命）**：实测 `HTTP_AUTHORIZATION` 全 missing、`getallheaders()` 不存在 → **自定义头 `X-Mcp-Token`/`X-Auth-Token` 能穿透**。MCP 客户端必须用它而非 `Authorization`。
6. **bbs1org 插件机制 = 从 DB 读 manifest，不读文件**：运行时从 `app_plugins.manifest_json` 读 hook，**直接 FTP 改 `plugin.php` 不生效**；必须触发 `plugin_registry_sync()`（把 `app_settings.plugin_sync_pending` 置 `1`，访问任意页即同步）。
7. **版块缓存坑**：DB 直插版块后 MCP `list_forums` 仍只见默认 → 版块列表缓存在 `app_settings.cache_forums`（JSON），需 `DELETE FROM app_settings WHERE name LIKE 'cache_%'`。
8. **建管理员 WorkbuddyBot 的 DB 直连坑**：免费主机 MySQL 不允许远程直连 → 写 PHP 放服务器执行；`app/data/db.php` 首行 `if(!defined('APP_ROOT'))exit;` → include 前必须先 `define('APP_ROOT',__DIR__)`。
9. **MCP 无"建版块"工具**；版块=扁平结构（无 `parent_id`）；命名前缀"知识库 · XXX"表达分组。
10. **发帖频率限制**：脚本加 8s 间隔 + 解析 N 自动重试 + 标题幂等。
11. **时间戳排序**：网页按 `last_reply_at` 倒序 → 用 `wb_fixts.php` 写库重设 created_at+last_reply_at。
12. **cron 非必需**：空论坛（零插件）= 0 任务；仅 `seo_suite`/`bing_wallpaper` 两插件需 cron-job.org。

---

## 6、部署状态
- 站点：`http://w662002.my-place.us`（bbs1org 根目录）
- 账号：`mp_42500274`；管理员 `w662000` / `Mp151515`（建议改）
- DB：host `sql103.my-place.us` port 3306，db `mp_42500274_bbs`，user `mp_42500274`，pass `Mp151515`
- FTP：`ftpupload.net`，上传目录 `htdocs`
- MCP 端点：`index.php?a=mcp`（mcp_server 插件 v1.1.4）；token `bbs_`+64hex；**actor=WorkbuddyBot**
- WorkBuddy 配置：`~/.workbuddy/mcp.json` 加 bbs1org 条目（`X-Mcp-Token` + `Cookie: __test=` + 浏览器 UA），连接器页「信任」
- 知识库版块：id=2「知识库 · AI每日工作日志」、id=3「知识库 · AI项目组」
- 10 个 MCP 工具：list_forums/list_topics/search_topics/get_topic/list_notifications/create_topic/create_reply/edit_topic/edit_reply/reply_notification

---

## 7、关键文件
- `bbs1org-deploy/bbs1org-main/index.php` — bbs1org 核心（294KB 单文件）
- `bbs1org-deploy/bbs1org-main/app/plugins/mcp_server/` — MCP 知识库插件（v1.1.4）
- `bbs1org-deploy/patched/index.php` + `setup.func.php` — MariaDB 兼容补丁版
- `bbs1org-deploy/blog_skin_fixed.php` — blog_skin 插件（加"博客效果"开关，v1.3.0）
- `bbs1org-deploy/waf_fetch.py` / `waf_check.py` — 解 WAF `__test` cookie
- `bbs1org-deploy/publish_logs.py` — 批量发日志（限流重试+幂等）
- `bbs1org-deploy/bbs1org-mcp-token.txt` — MCP token
- `bbs1org-deploy/mcp.php` — **实为 phpBB MCP 扩展正本**（见同批 phpBB handoff，勿混淆）

---

## 8、发布记录
- 8 篇每日工作总结（7-18~25）经 MCP `create_topic` 发到版块 2（署名 WorkbuddyBot），bbs1org 支持 markdown 渲染。
