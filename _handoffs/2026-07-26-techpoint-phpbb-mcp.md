---
layout: default
title: 技术点 · phpbb-mcp（phpBB 子目录安装 + 平铺单文件 MCP 扩展）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · phpbb-mcp：phpBB 论坛 + 平铺单文件 MCP 扩展（真子版块 + Markdown→BBCode）

> 对应项目轴 Handoff：`2026-07-26-handoff-phpbb-mcp`
> 目的：从「my-place.us 的 /AIblog 子目录 Softaculous 装 phpBB + 自写 mcp.php」提炼可复用技术资产——老框架 bootstrap 约束下平替扩展形态、PHP 全局变量冲突规避、BBCode 转换状态机、新建版块 ACL 自动赋权。与同批 bbs1org 共用 WAF/代理穿透方案，差异点在此篇。

## 一、技术选型（这个项目用了哪些技术栈 / 组件，怎么定的）

| 选型项 | 选定 | 落选 | 选型依据 |
|---|---|---|---|
| 论坛 | **phpBB 3.3（Softaculous 一键装，子目录 `/AIblog`）** | bbs1org | 需要真·无限级子版块（bbs1org 是扁平结构，无 parent_id）（T1） |
| MCP 形态 | **平铺单文件 `mcp.php`（include common.php）** | 正规 ext 扩展 `wb/mcpserver/` | phpBB 3.3 bootstrap 禁用超全局 + `submit_post()` 强依赖 `$user->data`/`$auth->acl()`，ext 加载器约束难满足；平铺文件直接拿 DI 容器更稳（T1 实测） |
| 鉴权 | **`X-Mcp-Token`（优先）+ 回退 Authorization/getallheaders** | 仅 Authorization | 同 iFastNet 代理剥离 Authorization，自定义头穿透（T1） |
| 富文本 | **Markdown→BBCode 状态机** | 直接存 Markdown | phpBB 的 s9e 只认 BBCode 不认 Markdown，存 Markdown 会裸显 `##`/`**`（T1） |
| 配置位置 | **`~/.workbuddy/mcp.json`（无点）** | `.mcp.json`（带点） | WorkBuddy 只直读 `mcp.json`，误建带点文件不生效（T1 实测） |

## 二、实施要点与关键技术（落地用了哪些做法）

1. **`$request` 全局冲突（隐蔽坑）**：JSON-RPC 分发里把 `json_decode` 结果命名为 `$request` 会覆盖 phpBB 全局 `$request`，导致 `submit_post` 调 `$request->variable()` 报 "Call to a member function variable() on array"。改局部变量 `$rpc`（T1）。
2. **文本格式化双路径**：`create_topic`/`create_reply` 用 `generate_text_for_storage` 生成 BBCode；`get_topic` 读取不依赖 style 上下文（否则抛 "Undefined array key style_id"），改用自写 `wb_render_text()` 正则解码 s9e 存储格式成纯文本（T1）。
3. **Markdown→BBCode 转换（`wb_md_to_bbcode` + `wb_md_inline`）**：标题→`[size]`、粗体→`[b]`、斜体→`[i]`、行内代码→`[b]`、链接→`[url]`、列表→`[list]`、围栏代码→`[code]`、分割线→`[hr]`、引用→`[quote]`；需维护 list/quote/code 状态机（T1）。
4. **新版块首页不可见（ACL 关键）**：phpBB `display_forums()` 检查 `f_list` 权限，新建版块在 `acl_groups` 无记录 → `f_list=NO` → 看不到。`wb_create_forum()` 改进：INSERT 后把父版块（或 forum_id=2）的组角色 `INSERT ... SELECT` 复制到新 forum，并 `acl_clear_prefetch()` + 删 `cache/production/data_acl_*`/`data_global*`/`data_sql_*`（T1）。
5. **保留原日期**：`create_topic`/`create_reply` 加可选 `created_at`（Unix 时间戳），不传则 `time()`；迁移脚本用 frontmatter date(+0800) 保留原日期（T1）。
6. **限流退避**：phpBB flood-control "请 N 秒后重试" → `migrate_logs.py` 解析 N + 加 3s 等待重试，每篇 6s 间隔，标题幂等跳过（T1）。
7. **一键建机器人 founder**：`mcp.php?setup=1` 创建 WorkbuddyBot（`USER_FOUNDER`，group_id=5 ADMINISTRATORS）+ 设 `wb_mcp_actor` config（T1）。
8. **WAF/代理穿透**：同 bbs1org，需 `Cookie: __test=` + `X-Mcp-Token` + 浏览器 UA（T1）。

## 三、模块职责划分（系统 / 组件如何分工）

- **phpBB 核心（common.php + DI 容器）**：数据模型、权限（acl）、发帖（`submit_post`）、版块树。
- **`mcp.php`（适配层）**：MCP 协议分发 + 7 工具 + `X-Mcp-Token` 认证 + `?setup=1` 建账号；把框架不提供的「自动 ACL 赋权 / Markdown 支持 / 时间戳」补在这里。
- **转换函数 `wb_md_to_bbcode` / `wb_render_text`**：Markdown↔BBCode 边界，写入走官方存储、读取走自写解析。
- **`migrate_logs.py`**：批量把日志经 MCP 迁入，控制节奏与幂等。
- **`waf_*.py`**：同 bbs1org 的网关票据生成，主机层复用。

## 四、如何选型（可复用的决策方法论）

- **先探针后定形态**：不确定框架能否加载扩展时，先用最小脚本 `include common.php` + 调一个核心函数（如 `submit_post`），能跑就走平铺单文件，绕开 ext 加载器的全局约束。本项目中正规 ext 实测受阻，平铺文件是更快出路。
- **富文本先看存储格式**：目标系统存什么格式（BBCode / Markdown / HTML），决定转换方向；若官方渲染函数依赖 UI 上下文，就自写只读解析器。
- **ACL 默认空白是隐形坑**：任何「程序建资源」都要检查默认权限表是否有记录、是否有缓存，建完配套复制权限 + 清缓存，否则资源存在但不可见。
- **全局作用域变量命名**：老框架大量使用超全局，自写脚本所有局部变量加独特前缀（如 `wb_` / `$rpc`），避免与框架全局同名覆盖。
- **配置路径以客户端实际读取为准**：WorkBuddy 只读 `mcp.json`，别凭直觉建带点文件。

## 五、深化学习指引（想深入看这些）

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| phpBB 3.3 架构 / common.php / DI 容器 | phpbb.com 开发文档 | 官方文档 | T0 |
| phpBB `submit_post` / `generate_text_for_storage` | phpBB 函数参考 | 官方文档 | T0 |
| phpBB ACL（acl_groups / acl_clear_prefetch） | phpBB 权限系统文档 | 官方文档 | T0 |
| s9e TextFormatter（BBCode 存储格式） | s9e.github.io | 官方文档 | T0 |
| `$request` 全局冲突 + 平铺单文件替代 ext | 本项目实测 | 自己实测 | T1 |
| 新建版块 ACL 复制 + 缓存文件清单 | 本项目 `wb_create_forum()` 实测 | 自己实测 | T1 |
| phpBB flood-control 具体阈值配置 | ACP 后台配置项 | 印象级，待核实 | T2 |

## 六、技术结合点（这些技术怎么协同，1+1>2）

- **include common.php + 平铺文件**：既拿到 phpBB 全部框架能力（DI、权限、发帖），又不受 ext 加载器的全局禁用约束——是「复用老框架」与「不被框架束缚」的折中。
- **写入官方存储 + 读取自写解析**：`generate_text_for_storage` 保证数据符合框架规范，`wb_render_text` 绕过 style 依赖做只读输出，两条路径各取所需。
- **版块创建 + ACL 复制 + 缓存清理**：三步配套才让「程序建版块」真正可用（否则建了也看不到），把权限系统的一致性规则固化进适配层。
- **保留原时间戳 + 幂等标题 + 退避重试**：让 8 篇历史日志迁移可中断续跑、顺序正确、零重复——批量 MCP 写入的可靠管道范式。
- **与 bbs1org 共用网关方案**：WAF `waf_*.py` 与 `X-Mcp-Token` 头在主机层解决一次，两个论坛复用，证明「网关穿透」是平台级资产而非单站点资产。

---
> 本文为技术点轴（对应 Handoff 2026-07-26-phpbb-mcp）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合。每个 Handoff 都应有一篇对应技术点，与项目轴一一对应。
