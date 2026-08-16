---
layout: default
title: 技术点 · 云南旅居房分析系统（yunnan-housing）— 交接文档（人读）
date: 2026-07-19 23:30:00 +0800
---

# 技术点 · 云南旅居房分析系统（yunnan-housing）— 交接文档（人读）

> 来源：260719_云南旅居房分析系统_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260719_云南旅居房分析系统_handoff.md（编码探测：utf-8）
- 技术栈：CF Workers（原设计云端爬+API，后改**本地住宅 IP 爬虫 + `wrangler d1 execute` 直连 D1**）、D1（SQLite）、KV（缓存）、CF Pages / Workers Static Assets（Dashboard）。
- **2026-07-19 全天**（来源 `2026-07-19.md`）：MVP 12 文件搭建 → 部署 Worker+D1+KV（Cron 03:00）→ API 路由修复 → **架构变更**（CF IP 被 58/贝壳/安居客/优居全封，改本地爬虫 + `wrangler d1 execute` 直连）→ 仪表板增强（云南 16 城 + 数据源下拉）→ 爬虫安全加固（`--safe` + `schedule_crawler.ps1` 定时 22:30）→ 修复"在售=0"误解 → 全量模式 → `install_schedule.bat` 输入校验 → PowerShell `$Action`/`$action` 大小写冲突修复 → 桌面 toast 通知 → 房源列表可点击展开 → Cookie 登录墙绕过 → 会话级风控对抗 → `run_daily.bat` 重写（`--no-push` 绕过 workers.dev POST 拦截）→ bat 一闪而过/中文乱码修复 → cookies.env 自动备份 → **17534→580 唯一房源误判** → 增量去重 → **模型修正：放弃全局去重，改"快照累积"** → 仪表盘全量上传 + `unit_price` 回填 → 逐区爬取对比上传 → Android 无数据修复（`API_BASE=''` 相对路径）→ 新建贝壳 `beike_crawler.py` 三件套。
- 6. **PowerShell 变量名不区分大小写**：带 `[ValidateSet]` 的 `$Action` 参数，脚本里再用 `$action` 局部变量会 `ValidateSetFailure` → 改名 `$taskAction`。
- 9. **`unit_price` 字段名坑**：Python 用 `h.get('unit_price')`（snake）但 58 JSON 键是 `unitPrice`（camel）→ 全 NULL → 看板展开 0 条。修复：D1 回填 `UPDATE ... SET unit_price=ROUND(listing_price*10000.0/area)` + 脚本改 `unitPrice`。
- 10. **Android 无数据**：`window.API_BASE` 硬编码 `workers.dev` → 手机跨域超时。改 `API_BASE=''` 走自定义域名 `yn.w662000.cc.cd`。
- 看板自定义域名：`yn.w662000.cc.cd`（API_BASE 相对路径）
- `yunnan-housing/src/{index,crawler,parser,api,db}.js` — Worker 各模块

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. **CF Workers 机房 IP 被数据源封杀**：贝壳/安居客/58/优居全拦截 → 必须本地住宅 IP 爬，再用 `wrangler d1 execute --remote --file=xxx.sql` 直连 D1。
2. **workers.dev 对中国 IP 的 POST 被拦截**（GFW+CF 边缘）：GET 正常、POST 全失败（SSL EOF）→ 绕过 HTTP，用 `wrangler d1 execute` 直连。
3. **58 强制登录墙**：必须带浏览器登录态 Cookie。导出：`F12 → Network → 刷新 → 点任意请求 → Headers → cookie 请求头 → 右键 Copy value → 存为 `local-crawler/cookies.env``。坑：① Cookie-Editor 插件只导单条追踪 Cookie（`xxzlxxid`）无效，要点插件底部 **Export** 导全部 10~30 个；② 加载优先级 json > txt > env，留着坏 `cookies.json` 会抢先；③ `cookies.env` 有时效，过期重导。
4. **58 会话级风控**：同 IP 翻页多了被标记登录墙。对抗：Referer 链条 + 撞墙刷新会话 + 冷却 20–40s + 重试（`WALL_RETRY=2`）+ 全局撞墙早退（`GLOBAL_WALL_ABORT=2`）。
5. **bat 必须纯 ASCII**：cmd.exe 按 GBK 读 UTF-8 → 中文乱码；echo 里不能出现 `>` 和 `(`/`)`。中文提示放 Python/PowerShell 运行时输出。`ps1` 含中文必须 **UTF-8 BOM**（`utf-8-sig`）。
6. **PowerShell 变量名不区分大小写**：带 `[ValidateSet]` 的 `$Action` 参数，脚本里再用 `$action` 局部变量会 `ValidateSetFailure` → 改名 `$taskAction`。
7. **快照累积 vs 去重**：房价走势每套房源每次爬到存一条快照，**不能折叠/清空**。`import_data.sql` 是**普通 INSERT**，重复导入会翻倍 → 必须用单区 SQL 或导入前 `DELETE FROM price_records/listing_snapshots WHERE district_id=...`（只删本区叶子）。
8. **清表触发自动播种污染**：`DELETE FROM listings` 后爬虫见空库会从最新备份 `seed_from_backup` 播种旧区 → 跑完必须 `DELETE FROM listings WHERE crawl_batch='seed'`。
9. **`unit_price` 字段名坑**：Python 用 `h.get('unit_price')`（snake）但 58 JSON 键是 `unitPrice`（camel）→ 全 NULL → 看板展开 0 条。修复：D1 回填 `UPDATE ... SET unit_price=ROUND(listing_price*10000.0/area)` + 脚本改 `unitPrice`。
10. **Android 无数据**：`window.API_BASE` 硬编码 `workers.dev` → 手机跨域超时。改 `API_BASE=''` 走自定义域名 `yn.w662000.cc.cd`。

---

## 6、部署状态
- 云南买房 Worker：`https://yunnan-housing-worker.wxatp.workers.dev`（Cron 03:00）
- 看板自定义域名：`yn.w662000.cc.cd`（API_BASE 相对路径）
- Cloudflare 账号：`wxatp2022@gmail.com`，subdomain `wxatp`
- 无锡买房/租房：见 handoff #5（D1 `wx-houseing-db` 3685 条 / `wxzf-db` 7466 条）

---

## 7、关键文件
- `yunnan-housing/wrangler.toml` — Worker/D1/KV/Cron 绑定
- `yunnan-housing/src/{index,crawler,parser,api,db}.js` — Worker 各模块
- `yunnan-housing/local-crawler/crawler.py` — 58 二手房爬虫（Cookie 登录态 + 快照模式）
- `yunnan-housing/local-crawler/beike_crawler.py` + `beike_gen_sync_sql.py` + `beike_run_daily.bat` — 贝壳三件套
- `yunnan-housing/local-crawler/run_daily.bat` / `schedule_crawler.ps1` / `install_schedule.bat` — 定时与一键跑
- `yunnan-housing/local-crawler/cookies.env` / `check_cookies.bat` — 登录态 Cookie
- `yunnan-housing/local-crawler/local_crawl.db` — 本地快照仓库（SQLite）
- `yunnan-housing-new/`（= 无锡版）同结构，`crawler.py` 爬无锡 58 买房+租房

---

## 8、发布记录
- 无锡交付手册已发布（handoff #5）；云南本体（爬虫/看板）仅 handoff 文档对外，未单独发博客。
- 可复用技能：`C:\Users\Administrator\.workbuddy\skills\cf-58-scraper-replicate\SKILL.md`（完整复刻/排坑手册）。
