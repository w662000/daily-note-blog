---
layout: default
title: 技术点 · yunnan-housing
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · yunnan-housing（Cloudflare 全栈 + 本地住宅 IP 爬虫 + 快照型数据模型）

> 对应项目轴 Handoff：`2026-07-19-handoff-yunnan-housing.md`
> 目的：从该项目提炼**可复用技术资产**——数据采集类系统的选型逻辑、反爬对抗手法、快照型数据建模、Windows 定时任务工程化。下次做「任意城市 / 任意分类信息站」的采集看板可直接复用，不必重踩坑。

## 一、技术选型

| 选型项 | 选定 | 落选 | 依据 |
|---|---|---|---|
| 云端运行时 | **Cloudflare Workers** | 自建 VPS / 云函数 | 免运维、免费额度足、自带 Cron Trigger（T1 实测） |
| 数据库 | **D1（SQLite）** | KV 直存 / 外部 MySQL | 需要 SQL 聚合与走势查询；D1 有 `wrangler d1 execute --remote` 可绕 HTTP 直写（T1） |
| 缓存 | **KV** | — | 看板热点查询降 D1 读次数（T1） |
| 看板托管 | **Workers Static Assets** | CF Pages 独立站点 | 与 Worker 同域省跨域配置，一次部署（T1） |
| 采集执行位置 | **本地住宅 IP** | CF Workers 云端直爬 | CF 机房 IP 被 58/贝壳/安居客/优居全封，云端直爬 100% 失败（T1 实测，硬结论） |
| 数据源 | **58 同城** | 贝壳/链家（强制登录）、优居/Q房（连不上）、房天下（空壳） | 逐个实测后仅 58 可用；解析器针对 58 结构，70 条/页解析率近 100%（T1） |
| 数据回传通道 | **`wrangler d1 execute --remote --file=x.sql`** | HTTP POST 到 workers.dev | 国内 IP 对 workers.dev 的 POST 被拦（SSL EOF），GET 正常（T1） |
| 反爬突破（后期升级） | **Playwright 无头 Chromium** | urllib + Cookie 头 | 58 加验证码网关（code=300）后，纯 HTTP 请求过不了，必须真浏览器执行 JS 生成 `fzq_h` 令牌（T1，7-24 日志） |
| 定时调度 | **Windows 计划任务 + PowerShell** | CF Cron | 爬虫必须在本地住宅 IP 跑，云端 Cron 只能管 API 侧（T1） |

## 二、实施要点与关键技术

1. **云端直爬失败 → 改「本地采集 + 云端存储」双层结构**。这是全项目最大的架构转折：目标站按 IP 段封禁云厂商机房，任何 serverless 直爬方案都不成立。回传走 `wrangler d1 execute --remote --file=import_data.sql`，完全绕开 HTTP 层（T1）。

2. **登录态 Cookie 的正确导出方式**：`F12 → Network → 刷新 → 任选请求 → Headers → cookie 请求头 → 右键 Copy value`，存为 `local-crawler/cookies.env`。三个坑（T1）：
   - Cookie-Editor 插件默认只导单条追踪 Cookie（`xxzlxxid`）**无效**，必须点插件底部 **Export** 导全部 10~30 条；
   - 加载优先级 `json > txt > env`，遗留的坏 `cookies.json` 会抢先生效；
   - `cookies.env` 有时效，过期需重导（配 `check_cookies.bat` 自检 + 自动备份）。

3. **会话级风控对抗组合拳**（T1）：Referer 链条伪造 + 撞墙后刷新会话重试（`WALL_RETRY=2`）+ 请求间冷却 20–40s + 全局撞墙早退（`GLOBAL_WALL_ABORT=2`）+ UA 池 + 单次 500 条上限（`--safe`）。

4. **IP 信誉才是硬墙，Cookie 救不了**（T1，7-24/7-25 日志的关键认知修正）：
   - 目标站按出口 IP 信誉判 gate，代理和 Cookie 都无法绕过；
   - **用户在自家浏览器手动过一次验证码，可给同出口 IP 开一个宽松窗口**——此结论推翻了早期"必须重启光猫换 IP"的判断；
   - 一次手动验证的额度远超预期，实测可连跑 4 个整区；
   - **严禁用宽限额度跑 `--test` 探针**，实测因反复测试把新 IP 额度耗光导致后 3 个区全撞墙。

5. **Playwright 使用时序**（T1，7-24 日志）：
   - 必须「跨频道热身」（先访问租房频道再进买房频道）才能生成有效 `fzq_h`，冷启动直冲目标频道会被主动墙；
   - **Playwright 实例全程只启一次**，每个区只重开 **browser** 拿干净会话；重复启实例会触发进程内 `asyncio` 事件循环冲突，导致后续分区全跳。

6. **数据模型：快照累积，不做全局去重**（T1，项目中期的重大纠错）：
   - 早期把 17534 条折叠成 580 条"唯一房源"是**误判**——价格走势需要同一房源在不同 `crawled_at` 的多行记录；
   - migrate 脚本改为**只加列不删数据**；
   - `import_data.sql` 是普通 `INSERT`（非 `INSERT OR IGNORE`，且 `price_records` 表无唯一约束），重复导入会翻倍 → 必须生成单区 SQL，或导入前 `DELETE FROM price_records/listing_snapshots WHERE district_id=...`，**只删本区叶子，绝不全删**（全删会冲掉已补好的其他区）。

7. **清表触发自动播种污染**（T1）：`DELETE FROM listings` 后爬虫见空库会从最新备份走 `seed_from_backup` 播种旧数据 → 跑完必须 `DELETE FROM listings WHERE crawl_batch='seed'` 清掉种子行。

8. **Windows 脚本编码三铁律**（T1）：
   - `.bat` 必须纯 ASCII——cmd.exe 按 GBK 解 UTF-8 会乱码炸脚本；`echo` 里不能出现 `>`、`(`、`)`；中文提示一律放到 Python/PowerShell 运行时输出；
   - `.ps1` 含中文必须存 **UTF-8 BOM**（Python 侧用 `utf-8-sig` 写）；
   - PowerShell **变量名不区分大小写**：带 `[ValidateSet]` 的参数 `$Action`，脚本里再定义局部变量 `$action` 会报 `ValidateSetFailure` → 改名 `$taskAction`。

9. **camelCase / snake_case 字段名不匹配**（T1）：Python 侧写 `h.get('unit_price')`，而源站 JSON 键是 `unitPrice` → 字段全 NULL、看板展开 0 条。双修：脚本改读 `unitPrice`，并在库里回填 `UPDATE ... SET unit_price=ROUND(listing_price*10000.0/area)`。

10. **移动端跨域超时**（T1）：前端 `window.API_BASE` 硬编码 `*.workers.dev` 导致手机端无数据。改 `API_BASE=''` 走相对路径 + 自定义域名，一次解决跨域与国内可达性。

11. **进程与完成态判断**（T1，7-25 日志）：Python stdout 有缓冲会吞日志，**不能只看实时行数**判断是否跑完；正确做法是看日志尾部有无"爬取完成"标记，或监测日志文件大小 ≥20s 无变化；查进程用 `ps aux | grep crawler.py`（Git Bash 无 `pgrep`）。

## 三、模块职责划分

- **本地爬虫（`crawler.py`）**：唯一持有住宅出口 IP 与登录态，负责抓取 + 解析 + 写本地 SQLite 快照库（`local_crawl.db`）。
- **本地 SQLite（`local_crawl.db`）**：采集缓冲区/真相源，断网、云端故障都不丢数据。
- **SQL 生成器（`db_to_sql.py` / `backup_to_sql.py`）**：本地库 → 单区 `import_data.sql`，是"只删本区叶子"策略的执行单元。
- **`wrangler` CLI**：唯一的数据回传通道，替代 HTTP API。
- **Worker（`src/{index,api,db}.js`）**：只做查询 API + 静态看板托管，**不承担采集职责**。
- **D1**：走势与聚合查询；**KV**：热点缓存。
- **调度层（`schedule_crawler.ps1` / `install_schedule.bat` / `run_daily.bat`）**：本机定时、参数校验、桌面 toast 通知。

一句话：**采集在本地，存储与展示在云端，两者之间用 CLI 而非 HTTP 连接。**

## 四、如何选型（可复用的决策方法论）

- **数据源选型先做"可达性实测"再写代码**：把候选源逐个用真实请求打一遍（是否强制登录 / 是否空壳 / 解析率多少），别按知名度选。本项目 5 个源实测只剩 1 个可用。
- **判断"能否 serverless 直爬"的标准动作**：先用云函数发一次裸请求看是否被封。被封则整个云端采集路线作废，立刻转本地采集，不要在云端反复调 UA/Header 浪费时间。
- **通道选型优先绕过被干扰的协议层**：当 HTTP POST 被中间链路拦截时，找厂商官方 CLI（`wrangler`）走另一条 egress，比死磕 HTTP 划算。同类经验：沙箱里 `curl` 全 000 但 `git push` 通——**不同工具走不同 egress，一条不通不代表全不通**。
- **数据模型选型先问"要回答什么问题"**：要做走势 → 必须快照累积；只做当前列表 → 才可以去重。搞反了会把真实数据当垃圾删掉。
- **反爬对抗的成本排序**：改 Header/UA（最便宜）→ 补登录态 Cookie → 降频+会话管理 → 真浏览器（Playwright，最贵）。逐级升级，不要一上来就上浏览器。
- **额度型资源要先规划再消费**：IP 信誉窗口、手动验证窗口都是稀缺额度，拿到后直奔目标，禁止用于探针测试。

## 五、深化学习指引

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Workers / D1 / KV / Static Assets | developers.cloudflare.com | 官方文档 | T0 |
| `wrangler d1 execute --remote --file` | Cloudflare Wrangler CLI 文档 | 官方文档 | T0 |
| Cron Triggers 配置 | Cloudflare Workers Cron 文档 | 官方文档 | T0 |
| Playwright 无头浏览器与会话管理 | playwright.dev | 官方文档 | T0 |
| SQLite 快照表设计 / 时序去重 | SQLite 官方 + 时序建模资料 | 官方+社区 | T1 |
| 58 登录态 Cookie 导出与失效周期 | 自己实测（本项目） | 实测 | T1 |
| 58 IP 信誉网关 / 手动验证放行窗口 | 自己实测（7-24、7-25 日志） | 实测 | T1 |
| `fzq_h` 令牌生成机制与热身时序 | 自己实测；内部机制未逆向 | 实测+推测 | T2（机制细节待核实） |
| bat/GBK 与 PowerShell ValidateSet 陷阱 | 自己实测 | 实测 | T1 |
| 复刻手册 | 本机 skill `cf-58-scraper-replicate` | 自建资产 | T1 |

## 六、技术结合点

- **本地住宅 IP + `wrangler` 直连 D1**：前者解决"能不能抓到"，后者解决"抓到能不能传上去"。只做前者会卡在 POST 被拦，只做后者没有数据源——两者合起来才构成完整链路，这是全项目的核心组合。
- **快照模型 + 单区 SQL 导入 + strip seed**：三件套共同保证数据既能累积走势又不翻倍、不被种子污染。缺任何一环，库里的数字都不可信。
- **Cookie 登录态 + 会话级风控对抗 + 手动验证窗口**：Cookie 解决"有没有资格看"，风控对抗解决"看多久不被踢"，手动验证窗口解决"IP 层被判死"。三层各管一层墙，缺一层就在对应层被挡。
- **Playwright 跨频道热身 + 单实例多 browser**：热身产出通行令牌，单实例避免事件循环冲突——两者配合才能连续跑完多个分区，任一漏做都是"第一个区成功、后面全跳"。
- **本地 SQLite 缓冲 + 云端 D1 展示**：本地保真相、云端保可访问性，任一端故障不影响另一端，这是"采集类系统"最省心的分层。

---
> 本文为技术点轴文章（对应 Handoff 2026-07-19）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合点。
