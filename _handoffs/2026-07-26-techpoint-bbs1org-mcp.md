---
layout: default
title: 技术点 · bbs1org-mcp（免费 PHP 主机论坛 + 插件式 MCP 知识库）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · bbs1org-mcp：免费 PHP 主机论坛改造为 AI 可写 MCP 知识库

> 对应项目轴 Handoff：`2026-07-26-handoff-bbs1org-mcp`
> 目的：从「iFastNet 免费主机上的 bbs1org 极简论坛 + mcp_server 插件」提炼可复用技术资产——免费主机 WAF/代理穿透、MariaDB 兼容性修正、插件式 MCP 鉴权与发布节奏。下次在受限 PHP 主机上挂 MCP 端点直接复用。

## 一、技术选型（这个项目用了哪些技术栈 / 组件，怎么定的）

| 选型项 | 选定 | 落选 | 选型依据 |
|---|---|---|---|
| 免费主机 | **my-place.us（iFastNet）** | 其他免费 PHP 主机 | 提供 PHP+MySQL，成本 0，可装论坛（T1） |
| 论坛 | **bbs1org 极简 PHP 论坛（单文件 294KB）** | phpBB | 单文件、无 composer 依赖、能跑在免费主机；phpBB 见同批 handoff（T1） |
| MCP 接入 | **mcp_server 插件（v1.1.4）** | 自写独立 Node MCP 服务 | 免费主机无法常驻 Node 进程，插件随 PHP 请求触发，零额外进程（T1） |
| 鉴权头 | **自定义 `X-Mcp-Token`** | `Authorization` | 代理层剥离 `Authorization`，自定义头能穿透（T1 实测） |
| 发布账号 | **专用管理员 WorkbuddyBot** | 用人类管理员账号 | MCP 操作以 actor=WorkbuddyBot 留痕，与人类管理分离（T1） |
| 发帖限流 | **脚本侧 8s 间隔 + 退避重试 + 标题幂等** | 不限流 | 防论坛 flood-control 触发，且幂等可重跑（T1） |

## 二、实施要点与关键技术（落地用了哪些做法）

1. **注册 IP 一致性**：iFastNet 要求「注册提交 IP == 激活点击 IP」。走 Cloudflare 代理注册、直连点激活会被拒；全程统一网络重注册。FTP 主机以 cPanel 显示的 `ftpupload.net` 为准；MySQL host 填 `sql103.my-place.us`（非 localhost）；FTP/cPanel/MySQL 三套同凭据（T1）。
2. **`declare(strict_types=1)` 头铁律**：bbs1org 的 `index.php` 第 3 行必须是脚本第一条语句，插调试代码会触发编译期 fatal（整站 500）。排错用**外部 wrapper**（`debug.php` include index.php），不动原文件头（T1）。
3. **MariaDB 兼容性双病灶**（标「MySQL 5.7」实为 MariaDB 11.4.12）：① `WITH PARSER ngram` 删掉；② `INSERT ... AS new ON DUPLICATE KEY UPDATE col=new.col` 改 `col=VALUES(col)`（T1）。
4. **WAF aes.js 挑战**：非浏览器 UA 请求被丢包。解法是复刻 `aes.js` → `AES.new(a,AES.MODE_CBC,b).decrypt(c)` 解出 `__test` cookie；该值随出口 IP 变，变了用 `waf_check.py` 重解。解 WAF 脚本：`waf_fetch.py` / `waf_check.py`（T1）。
5. **代理层剥离 Authorization（致命）**：实测 `HTTP_AUTHORIZATION` 全 missing、`getallheaders()` 不存在；**自定义头 `X-Mcp-Token` / `X-Auth-Token` 能穿透**。MCP 客户端必须用它而非 `Authorization`（T1 实测）。
6. **插件机制 = 从 DB 读 manifest，不读文件**：运行时从 `app_plugins.manifest_json` 读 hook，**直接 FTP 改 `plugin.php` 不生效**；必须触发 `plugin_registry_sync()`（把 `app_settings.plugin_sync_pending` 置 `1`，访问任意页即同步）（T1）。
7. **版块缓存坑**：DB 直插版块后 MCP `list_forums` 仍只见默认 → 版块列表缓存在 `app_settings.cache_forums`（JSON），需 `DELETE FROM app_settings WHERE name LIKE 'cache_%'`（T1）。
8. **建管理员走服务器脚本**：免费主机 MySQL 不允许远程直连 → 写 PHP 放服务器执行；`app/data/db.php` 首行 `if(!defined('APP_ROOT'))exit;` → include 前必须先 `define('APP_ROOT',__DIR__)`（T1）。
9. **MCP 无「建版块」工具**：版块=扁平结构（无 `parent_id`），用命名前缀「知识库 · XXX」表达分组（T1）。
10. **发帖频率 + 时间戳**：脚本加 8s 间隔 + 解析 N 自动重试 + 标题幂等；网页按 `last_reply_at` 倒序，用 `wb_fixts.php` 写库重设 `created_at`+`last_reply_at`（T1）。
11. **cron 非必需**：空论坛（零插件）= 0 任务；仅 `seo_suite`/`bing_wallpaper` 两插件需 cron-job.org（T1）。

## 三、模块职责划分（系统 / 组件如何分工）

- **iFastNet 主机（PHP + MariaDB）**：运行环境与数据存储，提供 HTTP 入口。
- **bbs1org 核心 `index.php`**：论坛数据模型、版块/帖子 CRUD、权限。
- **mcp_server 插件**：MCP 协议适配层，把论坛操作暴露为 10 个工具（list_forums / list_topics / search_topics / get_topic / list_notifications / create_topic / create_reply / edit_topic / edit_reply / reply_notification）。
- **WAF 会话脚本 `waf_fetch.py` / `waf_check.py`**：客户端侧解出 `__test` cookie，绕过 iFastNet 挑战。
- **`publish_logs.py`**：批量发日志到知识库版块（限流重试 + 标题幂等）。
- **客户端 `mcp.json`**：配置 `X-Mcp-Token` + `Cookie: __test=` + 浏览器 UA，连接器页「信任」后才可用。
- **WorkbuddyBot 账号**：MCP 操作的执行 actor，与人类管理员隔离。

## 四、如何选型（可复用的决策方法论）

- **免费主机先确认三件事**：能否跑自定义 PHP；是否禁远程 DB 直连（决定走服务器脚本还是本地连）；是否有 WAF / 代理会改写请求头（决定是否要自定义头 + WAF cookie）。这三条决定整体架构是否可行。
- **鉴权头先探针**：不确定 `Authorization` 能否到达时，用探针页检查 `HTTP_AUTHORIZATION` / `getallheaders()` 是否可用，而不是直接假设能用——实测发现代理层剥离后就改自定义头。
- **SQL 方言先查版本**：别信「MySQL 5.7」标签，实际可能是 MariaDB；`SELECT VERSION()` 后按真实方言写兼容 SQL（ngram / `AS new` 都是坑）。
- **配置读取机制决定生效方式**：插件若从 DB 读 manifest，改文件不生效，必须触发同步；这一点要先摸清再动手。
- **发布节奏内置退避 + 幂等**：任何对外写操作都假设会被 flood 限流，客户端侧加间隔、重试、幂等标题，让批量任务可安全重跑。

## 五、深化学习指引（想深入看这些）

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| MCP 协议（JSON-RPC / 工具定义） | modelcontextprotocol.io | 官方文档 | T0 |
| MariaDB vs MySQL 语法差异（ngram / ON DUPLICATE） | mariadb.com/kb、dev.mysql.com | 官方文档 | T0 |
| PHP `declare(strict_types=1)` 必须首行 | php.net 手册 | 官方文档 | T0 |
| iFastNet 免费主机 WAF（aes.js `__test` cookie）穿透 | 本项目 `waf_*.py` 实测 | 自己实测 | T1 |
| iFastNet 代理层剥离 `Authorization` 头 | 本项目实测（HTTP_AUTHORIZATION missing） | 自己实测 | T1 |
| bbs1org 插件 manifest 读 DB 而非文件 | 本项目 `plugin_registry_sync()` 实测 | 自己实测 | T1 |
| 论坛 flood-control / 版块缓存键名 | 各论坛源码实测 | 印象级，待核实 | T2 |

## 六、技术结合点（这些技术怎么协同，1+1>2）

- **WAF cookie + 自定义 token 头**：两者是绕过 iFastNet 网关的「双层门票」——`__test` 过 WAF 挑战，`X-Mcp-Token` 过代理层剥离；任一缺失，MCP 端点都不可达。
- **插件式 MCP + 免费主机**：不常驻进程、随 PHP 请求触发，把「AI 知识库」成本压到 0，是免费主机上唯一可行的 MCP 形态（独立 Node 服务跑不了）。
- **幂等标题 + 限流退避 + 时间戳修正**：三者组合让「8 篇历史日志批量迁入」可中途中断、可重跑、且顺序正确——这是把一次性迁移做成可靠管道的关键。
- **DB 直插 + 缓存清理 + 插件同步**：改 DB 后必须配套清缓存 / 触发同步，否则 MCP 看不到新数据；这是「直接写库」与「应用层视图」之间的一致性问题，通用到所有带缓存的 CMS。

---
> 本文为技术点轴（对应 Handoff 2026-07-26-bbs1org-mcp）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合。每个 Handoff 都应有一篇对应技术点，与项目轴一一对应。
