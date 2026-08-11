---
layout: default
title: 技术点 · wuxi-58（58 同城多区爬虫 + Cloudflare D1 全栈落库）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · wuxi-58：58 同城多区爬虫 → Cloudflare D1 全栈落库

> 对应项目轴 Handoff：`2026-07-25-handoff-wuxi-58`
> 目的：从「无锡 58 同城买房/租房两套数据系统」提炼可复用技术资产——受限出口 IP 下绕过反爬、本地落盘经 wrangler 直连 D1 的离线同步架构、分区增量幂等灌库。下次做「分类信息站点爬虫 + 云端看板」直接复用，不必重踩坑。

## 一、技术选型（这个项目用了哪些技术栈 / 组件，怎么定的）

| 选型项 | 选定 | 落选 | 选型依据 |
|---|---|---|---|
| 抓取方式 | **Playwright 无头 Chromium** | 纯 urllib/requests | 58 升级了 code=300 验证码网关，单凭 Cookie 的 HTTP 请求过不了，必须真浏览器执行 JS 生成新鲜 `fzq_h` 令牌（T1 实测） |
| 数据中转 | **本地 SQLite `local_crawl.db`** | 爬虫直推 Worker | 国内 `*.workers.dev` 的 POST 被网络拦截；落盘后可离线重放，与网络可达性解耦（T1） |
| 云端库 | **Cloudflare D1（SQLite 协议）** | PostgreSQL/MySQL 托管 | 免费、与 Pages/Worker 同生态、SQL 即建即用（T0） |
| 看板 | **Worker + Pages** | 自建前端服务器 | 静态托管零运维，Worker 做只读查询代理（T0/T1） |
| 写库通道 | **`wrangler d1 execute --remote --file=import_data.sql`** | 经 Worker API 写 | 绕开 POST 拦截，本地生成 SQL 文件后直连 D1（T1） |
| Cookie 注入 | **原始 `Cookie` 请求头** | `http.cookiejar` | cookiejar 会吞掉复杂 Cookie 导致鉴权失效（T1） |
| Python 运行时 | **受管 venv**（已装 playwright） | 系统 python | 避免依赖缺失；路径 `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`（T1） |

## 二、实施要点与关键技术（落地用了哪些做法）

1. **反爬令牌靠「真浏览器 + 新鲜 `fzq_h`」**：带 Cookie 的 urllib 已无法过网关；必须 Playwright 跨频道「热身」生成 `fzq_h`，且每区重开浏览器拿干净会话——冷启动直冲目标频道会被主动验证码墙拦（T1）。
2. **Playwright 实例只启一次**：进程内只 `sync_playwright().start()` 一次，跨区只重开浏览器（`pw_close_browser`），否则事件循环冲突报 `asyncio` 错误，后续区全跳（T1）。
3. **Cookie 用原始请求头注入**：放弃 `http.cookiejar`，改拼 `headers={"Cookie": "..."}` 原样发送（T1）。
4. **绕过死代理直连**：沙箱有残留代理 `127.0.0.1:10808`（对国内 58 是 no-op 且拖慢），全程 `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy` 剥离（T1）。
5. **IP 信誉窗口靠「人工浏览器过验证」刷新**：沙箱出口 IP 被 58 在租房频道做了主动验证码墙（code=300），纯 HTTP 永久过不了；**用户在自家浏览器手动过一次验证，能给同一住宅出口 IP 开宽松窗口**——一次手动验证连跑 4 个整区各 50 页、0 撞墙（T1 实测，推翻了「必须重启光猫换 IP」的旧结论）。
6. **分区增量灌库三步幂等**：① 清本区 `DELETE FROM listings WHERE district_code='<区>'`（**绝不清全表**）；② `python db_to_sql.py <项目> <城市> <站点>` 生成单区 SQL；③ `wrangler d1 execute --remote --file=import_data.sql` 导入。重复导入因 `import_data.sql` 是普通 INSERT（非 OR IGNORE）会翻倍——所以导入前必须确保本地只含目标区，或把涉及区叶子全 DELETE（T1）。
7. **seed 污染处理**：跑前全清 `listings` 会触发 `seed_from_backup` 自动播种旧数据污染；跑完必须 `DELETE FROM listings WHERE crawl_batch='seed'` 清掉（T1）。
8. **完成判定不看实时行数**：Python stdout 缓冲会吞日志；以「日志末尾出现『爬取完成』或日志文件大小 ≥20s 不变」为准，进程查 `ps aux | grep crawler.py`（Git Bash 无 `pgrep`）（T1）。
9. **严禁消耗宽限额度做探针**：拿到新验证窗口先 `--district <目标区>` 直奔目标，勿先 `--test`/探针，否则额度耗光全撞墙（T1）。

## 三、模块职责划分（系统 / 组件如何分工）

- **爬虫 `crawler.py`**：只负责抓取 + 写本地 `local_crawl.db`；不碰网络远端，挂了可单独重跑。
- **转换层 `db_to_sql.py`**：读本地库 listings → 生成 `import_data.sql`；参数化按项目/城市/站点，保证产出单区 SQL 实现幂等。
- **区级清理器（DELETE 语句）**：灌库前的「先删范围」，与 import 配合构成幂等单元，杜绝翻倍。
- **`wrangler` 直连通道**：唯一写远端 D1 的入口，把「被网络拦截的写入」转成「离线文件 + 直连执行」。
- **Worker + KV**：读侧查询代理 + 看板缓存，用户浏览器访问；爬虫链路与其完全解耦。
- **Pages 看板**：纯静态展示，数据源来自 Worker。

## 四、如何选型（可复用的决策方法论）

- **先判反爬层级**：带 Cookie 仍被拦 → 不是 Cookie 级，是请求头/JS 执行级（需真浏览器）；换 Cookie 同 IP 仍被拦 → 是 IP 级信誉墙（需换出口或刷信誉）。同住宅 IP 下人工过验证能放行自动化，是「IP 信誉可共享」的信号。
- **通道选择从简到繁**：能直推就直推；被网络拦截就退到「本地落盘 + CLI 直连远端」（wrangler），换来与网络环境解耦、可重放。
- **幂等优先于约束**：D1 表无唯一约束时，不依赖数据库兜底去重，而在应用层用「先删范围 + 单区 SQL」保证可重复执行。
- **把「验证窗口」当有限资源**：任何消耗额度的动作（探针/测试）都计入成本，先规划目标再行动。
- **运行时用受管 venv**：避免「我装了但运行时找不到」的依赖错位，把 playwright 等重依赖锁定在固定 venv。

## 五、深化学习指引（想深入看这些）

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Playwright 无头浏览器 / `fzq_h` 类反爬令牌生成 | playwright.dev 官方文档 | 官方文档 | T0 |
| Cloudflare D1（SQLite 协议）/ `wrangler d1 execute` | developers.cloudflare.com/d1 | 官方文档 | T0 |
| Cloudflare Workers + Pages 看板 | developers.cloudflare.com | 官方文档 | T0 |
| 58 二手房/租房反爬机制（code=300 + 手动验证刷新 IP 信誉） | 本项目日志实测（7-24/7-25） | 自己实测 | T1 |
| `http.cookiejar` 吞复杂 Cookie 的确切条件 | Python `http.cookiejar` 源码 / 实测 | 社区+实测 | T1 |
| 受管 venv 路径与 playwright 安装 | WorkBuddy 内置 python 环境 | 平台特性 | T1 |
| 重启光猫换公网 IP（CGNAT 下是否真换） | 运营商网络环境实测 | 印象级，待核实 | T2 |

## 六、技术结合点（这些技术怎么协同，1+1>2）

- **真浏览器 + 原始 Cookie 头**：Playwright 解决 `fzq_h` 生成（JS 执行），原始头解决复杂 Cookie 不被吞——两者缺一，自动化都过不了网关。
- **手动验证 + 直奔目标区**：人工在浏览器过验证刷新 IP 信誉窗口，自动化立即「不带探针、直接抓目标区」，把有限窗口的利用率拉满；若先做 `--test` 就把窗口浪费在探测上。
- **SQLite 中转 + wrangler 直连**：被拦截的「爬虫→Worker」网络路径，被重构成「爬虫→本地文件→wrangler→D1」可重放路径，网络不通也能离线完成灌库。
- **单实例 Playwright + 每区重开浏览器**：既避免 asyncio 冲突（只启一次），又拿到干净会话（每区重开），是「稳定 + 反封」兼得的写法。
- **先删范围 + 单区 SQL**：两项组合才让「分区增量补数」幂等，单独任一项都会出现翻倍或脏数据混入。

---
> 本文为技术点轴（对应 Handoff 2026-07-25-wuxi-58）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合。每个 Handoff 都应有一篇对应技术点，与项目轴一一对应。
