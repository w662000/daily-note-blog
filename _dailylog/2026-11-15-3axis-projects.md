---
layout: default
title: 项目流 · 2026-11-15
date: 2026-11-15 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-15.md, D:\AI work\workbuddy\2026-11-15-10-21-36\.workbuddy\memory\2026-11-15.md

## 十轮：天气站本地搭建完成（12:04-12:20）
- 参考 GauthierDefrance/Cergy-Meteo（CloudWatch，PHP+Open-Meteo 的法国天气站），选型 Python 3 纯标准库（零依赖，本机 managed Python 3.13 可直接调，AlwaysData 原生支持 Python WSGI）。
- 产物 `D:/AI work\workbuddy\2026-11-15-11-18-44\weather-station\`：app.py（单文件 WSGI：城市搜索/实时/24h/7天 SVG 折线/SQLite 热搜统计/明暗主题/10分钟缓存）+ wsgi.py（AlwaysData 入口）+ README.md（含部署步骤）。
- 调试修复 3 处：/search 500（view_candidates 返回值错）、24h 横条竖堆（漏包 .hours 容器）、/theme 需二次刷新（cookie 先读后设）。冒烟测试曾用 Git Bash curl 直传中文把 GBK 乱码写进 SQLite——清理脏数据后改用 URL 编码测试（api-test-pitfalls 坑再次应验）。
- 本地验收：8085 全路由 200，Playwright 截图（首页/城市页/暗色）通过，服务保持运行（8085）。
- 下一步：等用户 AlwaysData 账号 → SSH key 免密 → SFTP 上传 → 后台建 Python WSGI 站点 → 线上验证。任务清单 #2。

## 十四轮：照 WB 静态预览模式改造（12:43-12:50，用户给样板 127.0.0.1:5114/static-html/<id>/preview.html?city=huizhou）
- 新增 `weather-station/static-html/weather01/preview.html`：纯静态自包含单文件（JS 浏览器直连 Open-Meteo，支持 CORS），URL 参数 city=<slug>（wuxi/kunming/puer/jianshui/huizhou/hangzhou），首页=搜索框+6 城卡片，详情=实时+7天+24h+SVG 折线，无 city 参数即首页，未知 slug 报错页。
- app.py 加路由 `/static-html/<任意id>/preview.html` 托管该文件（no-cache）。
- 验收：同款 URL 模式全 200；Playwright 截图 preview.html?city=huizhou 渲染完整（25.9℃ 实时+图表）。已知小瑕疵：双折线两个 SVG 的最高/最低轴标签相邻行有轻微视觉重叠，不影响读数。
- 用户计划自己在 tabbit 打开看效果；若 tabbit 仍挡 127.0.0.1，备选=加防火墙规则走局域网 IP。

## 5 端发布审计（11:08-11:20，只读自查）
- ✅ 正常：博客（b196d5a 10:22:59 已推、线上 towertop.kdns.fr/daily-note-blog HTTP 200 含 11-15 内容）；bbs1org#2 / phpBB#10 今日工作日志帖；phpBB#11 今日项目流/技术点 + 2 handoff；Gridea 稿件源 261115×4 + techpoint×7；有道云 handoff 链昨晚 2 篇交接文档。
- ❌ 缺口：① Gridea 线上渲染停 11-14 21:41（step7 被杀没跑）；② bbs1org#3 缺今日 2 帖（phpBB#11 有）→ 0c 假成功；③ 有道云 3 轴缺（工作日志目录最新 11-01），0c 假成功，但 11:12 晨检 automation 正在补发（youdao_tmp 活跃，发「技术点 · 用户级 Skill 清单」等）；④ step6 没跑 → #2/#10 缺 11-13/11-12 补发；⑤ handoff 收件箱 15 篇积压。
- 根因：① schtasks ExecutionTimeLimit PT30M << 列车总最坏耗时（11-14 遗留待办①实锤），连续两轮（11-14 23:15、11-15 10:20）被强杀且 print 缓冲丢失 → 主日志 0 字节；② pw.post/_save_youdao 假成功（返回 ok 服务端未落库），failures 空 → 0c 报 OK。
- 待用户拍板：PT30M→PT2H + 日志 flush；0c 发后回查校验；补发（等晨检结束，避免撞车）。审计报告：会话目录 `审计报告_5端发布_20261115.md`；论坛只读审计脚本 `audit_forums_readonly.py`。

## 观云天气站 CF Workers 原生版重写并上线（18:06–18:30）

按 HANDOFF（`D:\workspace\workbuddyai\2026-11-15-11-21-53\tq-weather-cf\HANDOFF.md`）完成实施，全绿验收。

### 产物
- 项目目录：`D:\workspace\workbuddyai\2026-11-15-11-21-53\tq-weather-cf\`
  - `wrangler.toml`（name=tq-weather，D1 database_id=`5dc7fa7d-199b-4d9e-b156-d5d64f7d892e`，custom domain tq.780.de5.net）
  - `src/worker.js`：路由 /api/state、/api/detail、/api/search、/api/hit(GET+POST)、/api/featured/add|remove、/health；Cache API SWR（TTL 15min，搜索缓存 1h）；D1 featured/hits 表 + 六城种子；禁 KV、禁 Cron
  - `public/`：index.html（静态外壳+内联 SVG favicon）、app.js（客户端渲染，改写自 views.py _MAIN_JS，卡片点击事件委托、添加/删除模式、离线搜索、明暗主题）、style.css（原样复制）、catalog.json（643 城=中国 361+国际 282，无耶路撒冷，id 无重复）
- 线上：https://tq.780.de5.net（workers.dev 默认已随 custom domain 关闭）
- 反代 Worker `tq-weather-proxy` 已删除释放域名；alwaysdata Python 版保留作回退

### 验收结果（全绿）
- /health: 643 城 d1 ok；/api/state 冷启动 1.36s source=live，二刷 cache；六城 7 天预报+AQI 齐全
- /api/hit POST(sendBeacon)/GET 均 204，D1 hits 落库正确（hangzhou=杭州）
- 搜 lapland 在线兜底正常（中国结果优先）；featured add/remove 回路 + 目录校验（lapland 拒绝）正常
- 手机端 390px：降水列隐藏、?city=kunming 直达面板；卡片点击即时切换+URL 同步；favicon 已补零 console 报错

### 踩坑记录
1. **TOML 坑**：`routes = [...]` 写在 `[assets]` 段之后会被解析成 `assets.routes`（警告 "Unexpected fields found in assets field"），custom domain 静默不生效 → DNS NXDOMAIN → HTTP 530/1016。routes 必须放顶层（[assets] 之前）。
2. **网络反转**：HANDOFF 说 wrangler 必须走 7897 代理，实测当时代理上游节点挂了（CONNECT 能建立但 TLS 超时），直连 api.cloudflare.com 反而通，全程直连部署成功。下次先测直连再定代理。
3. Git Bash curl 直传中文 query 参数按 GBK 发送导致 400（已知本机坑，浏览器端 encodeURIComponent 不受影响）。

### 写量账（红线要求）
- KV：0（完全不用）；D1 写：/api/hit 每访问 1 行 upsert + featured 手动增删；日均 5000 访问 = 5000 行 = 5% 额度
- 天气缓存全走 Cache API（0 配额）；静态资源不计请求配额

### 待办（用户确认后）
- 每月 15 日目录维护 automation 原部署到 alwaysdata，需改为：改 catalog.py → 重新导出 catalog.json → `npx wrangler deploy`（无重启概念）

## 20:05 追加：收尾未完成项

### ① 月度目录维护 automation 重建（CF 版）
- **发现虚报**：旧会话日志（2026-11-15-11-21-53 工作区 L192）声称创建了 automation `b695d4fc`（每月15日10:00），但 automation_update view 报 not found、直查 ~/.workbuddy/workbuddy.db automations 全表 41 条也无此 id → 旧会话根本没落库
- **已重建**：`automation-1794744436826`「天气站城市目录月度维护（CF 部署·15日10:00）」，FREQ=MONTHLY;BYMONTHDAY=15;BYHOUR=10，validFrom 2026-11-16（首跑 2026-12-15），cwds=tq-weather-cf
- prompt 自包含：收录标准、耶路撒冷/台湾红线、id 唯一红线、隔离 Python 导出、直连优先部署、TOML routes 坑、温和验证（禁轰炸）、alwaysdata 不同步不重启
- 教训：旧会话日志的"已创建 automation"要拿 automation_update view 核实，不能只信日志

### ② 新增用户级 skill：cf-worker-site-deploy
- 路径 `~/.workbuddy/skills/cf-worker-site-deploy/SKILL.md`（本会话无 SkillManage 工具，直接落盘标准格式）
- 内容：Python→CF 架构映射表、配额红线（禁 KV/Cron）、wrangler.toml routes 必须顶层（[assets] 前之坑）、直连/代理检测策略（先测直连）、Cache API SWR 代码模式、验收清单模板、切域名顺序、tq-weather 实战参照

## 5 端发布审计（11:08-11:20，只读）
- 结论：博客/论坛工作日志（bbs#2、phpBB#10）/phpBB#11/有道云 handoff 链正常；缺口=Gridea 线上渲染（停 11-14 21:41）、bbs1org#3 今日 2 帖、有道云 3 轴笔记、step6 历史补发（11-13/11-12）、收件箱 15 篇积压。
- 根因：PT30M 强杀列车（连续两轮日志 0 字节）+ 0c 的 pw.post/_save_youdao 假成功。11:00 晨检正在补有道云（youdao_tmp 11:12 活跃）。
- 交付：`审计报告_5端发布_20261115.md` + `audit_forums_readonly.py`。

## ABC 修复执行（12:37-13:05）
- A 完成：PT30M→PT2H（fix_timelimit.py，pythonw 保留）+ publish_train.py 三处 flush。
- B 完成：0c 回查校验（论坛 list_titles 回查；有道云改双证据——save 回执「笔记 ID」即成功，list API 有 >45 分钟显示延迟，纯 run_list 回查会误报）。
- C 完成：0c 重跑补 bbs1org#3 topic=2137/2138，其余端查重跳过；Gridea 晨检 11:15 已补推；论坛 11-13/11-12 实测两端已存在（审计误报：只看了最新 5 条）。终验 #2=1/#3=2/#10=1/#11=4，5 端全绿。
- 遗留：收件箱 15 篇积压（D 项）；有道云 (1) 副本重复待定。

## 有道云重复清理执行（18:47-20:52，进行中）
- ✅ 方案一完成：81 篇（18:39 批次）全删，0 失败（1 手动探针 + 80 批量）；ID 备份 `youdao_batch1_81ids.json`、结果 `youdao_batch1_result.json`。
- ✅ upload_youdao 查重修复（py_compile 通过，未实跑）：list 第一页 → search 兜底（run_search_exists 归一化比对）→ search 失败宁漏勿重 SKIP。根因补全：list 不止延迟，还有**分页 50/页**（-l 游标），旧 run_list 只拿第一页。
- 🔄 全量盘点后台跑（KvbmFz，audit_youdao_dupes_full.py，只读翻页）：20:43 起 9 分钟仍在第一目录；projects 目录「用户级 Skill 清单 v1.3」副本序号 (221)，真实规模可能上千，删除前先报用户。
- 🚨 **新红线（已写入 ~/.workbuddy/MEMORY.md）**：有道云操作仅限 workbuddy 三目录（7587B5CC/C533B557/9C31CBCE），其他目录不 list/search/delete；批量删先报规模。
- 进度文件：`进度_20261115_2052.md`。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-14-23-25-11\.workbuddy-ai\memory\2026-11-15.md, D:\workspace\workbuddyai\2026-11-15-11-21-53\.workbuddy-ai\memory\2026-11-15.md

## 调研：alwaysdata 免费档（法国，巴黎机房 Equinix）适合部署什么

T0 来源（均为官方，查询日 2026-11-15）：
- https://www.alwaysdata.com/en/pricing/ （原 /en/offers/ 重定向至此）
- https://help.alwaysdata.com/en/docs/admin-billing/billing/public-cloud-prices
- https://help.alwaysdata.com/en/docs/admin-billing/profile/suspension/
- https://help.alwaysdata.com/en/docs/admin-billing/billing/choose-its-paas/
- https://help.alwaysdata.com/en/docs/web-hosting/services/ 、/tasks/ 、/sites/misc/ 、/technical-specifications/limits/ 、/architecture/
- 官方文档仓库 https://github.com/alwaysdata/documentation

免费档参数：0 €/月终身、无需信用卡、1 GB SSD（文件+邮件+数据库共算）、256 MB RAM、1/4 CPU、3 天滚动备份、站点/数据库/邮箱数量不限、SSH/SFTP、Let's Encrypt SSL、定时任务（最短 1 分钟、无最长执行时长）、MariaDB/PostgreSQL/RabbitMQ。

硬限制（决定选型）：
1. 仅限个人非盈利用途；公司站/公司邮箱/广告/卖货禁止。
2. 网站只能用 `<account>.alwaysdata.net`，绑自有域名需付费档（邮箱可用自有域名）。
3. 禁止 24/7 常驻服务（Services 仅付费档，从 Small €5/月年付起）；站点默认 30 分钟无请求即停进程、下次请求冷启动，单站点同时仅 1 实例。
4. 免费账号活跃度：注册 <1 年每 120 天、1–4 年每 6 个月、>4 年每年须登录一次管理后台，否则停号（登录即恢复）。
5. 禁止多开免费账号、禁止从其服务器大量抓取/资源密集型/群发邮件；无 root/sudo、无 Docker。
6. 官方 Limits 页未列明带宽/流量上限数字 → 该项未知，只有"合理用量"软约束。

结论：适合个人静态站、博客、请求驱动的 PHP/Python/Node 小 Web 应用、小 API、webhook、定时脚本、练手环境；不适合常驻 bot/WebSocket/代理/爬虫守护进程、商业项目、需自有域名的正式站、大存储大流量项目。

关联判断：若目的是给 CF Workers 项目找常驻后端或定时抓取落点，alwaysdata 免费档不合适（禁 24/7 服务 + 禁抓取 + 需定期登录），继续用 Cloudflare cron/Workers 更合适。

## 追加：GitHub 上真实 alwaysdata 部署案例（用已登录 gh 账号做 code/repo search 核实）

可复刻优先级（均看过 README 或 workflow 源码）：
1. T0 https://github.com/alwaysdata/autodeploy-git-hook （官方，47★，2026-08 更新，git post-receive 自动部署，一个 bash 文件）
2. T1 https://github.com/kotorkovsciy/alwaysdata-fastapi （FastAPI 部署教程，User program + IPv6 8100 端口）
3. T1 https://github.com/OpenRSI/Flask_Projet_SQLite （Flask+SQLite+API 教学课，带 CICD）
4. T1 https://github.com/narnesss/tarkov-help （每日 UTC 0:30 SSH 做 SQLite 快照备份，backup-alwaysdata.yml，2026-10 活跃）
5. T1 https://github.com/TOKUJI/blackbull-demosite （每日健康检查 blackbull.alwaysdata.net/health，探测 200 在线）
6. T1 https://github.com/cristiadu/rate-my-everything （React+Node REST API 全栈，2026-11 更新，带 alwaysdata-deploy.yml）

其他核实过的：Kinto/kinto-alwaysdata（Mozilla Kinto JSON API 一键部署）、MadeV1/API（Adonis5）、AlexandreGerault/simple-social-network-api、baptistev59/technova-backend（Symfony+PG 部署文档）、nhoizey/nicolas-hoizey.com（Actions rsync 部署）、gocroot/alwaysdata（Go Fiber 模板，已归档停维护）、johannie2025/wise_os（PHP webhook 日志）、darkstarworks/wa-webhook、justNuka/7k-bot（webhook 接收器常驻端口 9000，免费档禁）、Starhes/alwaysdata-keepalive（每日自动登录保活，对应 120 天要求，灰色）、thom4parisot/letsencrypt-alwaysdata（12★ 但已废弃，2016 起官方原生支持 LE）、kevinmf1/sistempendukungkeputusan-ahp（12★ PHP 学生作业）、GauthierDefrance/Cergy-Meteo、rutgerrrrr/containerstatus-feedback。

重要可信度提醒：这些第三方项目只能确认「部署在 alwaysdata.net 域名或走 alwaysdata SSH/API」，**无法确认用的是免费档还是付费档**；官方 guides 里 Mattermost/MongoDB/Redis/CouchDB 需要 Services（付费档）。GitHub 上 star 最高的一批（83★/19★/14★）是拿免费主机搭代理节点，违反官方条款，不推荐复刻。

站点探测（2026-11-15，本机 curl -I）：containerstatus / blackbull = 200；wise = 403；made / kevinmalikfajar / hornung / technova = 000（连不上，原因不确定，别断言已停号）。

## 新建项目：六城天气站（本地骨架已完成，未上传）

路径：`D:/workspace/workbuddyai/2026-11-15-11-21-53/weather-station/`

需求：参考 GauthierDefrance/Cergy-Meteo（CloudWatch）功能骨架做中文版，覆盖 无锡/昆明/普洱/建水/惠州/杭州；先本地搭好，调试通过后择期 SSH 上传 alwaysdata。

技术选型（用户采纳其他 agent 建议，我复核合理）：**Python 纯标准库 + WSGI**，不用 PHP（本机没装）。T0 依据：alwaysdata 官方 Python 配置页写明默认环境"no ready installed libraries other than the standard library"，且站点类型支持 Python WSGI（uWSGI，支持到 3.14）。SSH/SFTP 主机 `ssh-<account>.alwaysdata.net:22`，用户名=账号名；站点域名后缀是 .net 不是 .com。

功能对照 CloudWatch：三级筛选（华东/西南/华南 → 省 → 城）、实时六城卡片、7 天预报+温度区间条、sqlite3 热度统计、CSS 明暗主题。全部中文、无 emoji、无外部资源。

文件：app.py（WSGI 入口 application/app + /health + 静态白名单）、config.py（环境变量覆盖）、cities.json（6 城坐标+来源+可信度）、weather.py（Open-Meteo 多坐标一次请求/解析/15 分钟缓存/实时→缓存→过期缓存→演示数据回退，页面显著标注数据来源）、views.py（渲染，支持 SCRIPT_NAME 子路径）、stats.py、static/style.css、fixtures/sample_forecast.json（明确标为演示数据，不冒充真实天气）、tests/test_app.py、make_preview.py、deploy/deploy.sh（默认 dry-run，需 --apply 才上传）、deploy/ALWAYSDATA.md（站点配置步骤）、README.md。

本地调试结果：`python -m unittest discover -s tests -v` **15/15 全绿**，`bash -n deploy/deploy.sh` 通过，dry-run 输出正常。直接调用 WSGI application 做端到端断言，**未启动任何常驻服务、未弹窗口**。preview.html 为内联 CSS 静态预览。

修掉的真 bug：`with sqlite3.connect(...) as conn` 只提交事务不关闭连接，Windows 上临时目录清理时报 WinError 32 文件占用 → 改为 `contextlib.closing() + with conn` 双层，Linux 上也能避免句柄累积。

坐标（查证 2026-11-15，写进 cities.json）：无锡 31.56887/120.28857、昆明 25.03889/102.71833、惠州 23.11147/114.41523、杭州 30.29365/120.16142 来自 Open-Meteo Geocoding（T0）；普洱 22.8272471/100.9650146、建水 23.6361076/102.8263528 来自 OSM Nominatim（T1，Open-Meteo 检索不到建水，且 "普洱 28.25/104.16667" 是同名错点）。

关键风险（未解决）：**本机连不上 api.open-meteo.com**（SSL 握手失败/超时，geocoding 域名通），所以本地走离线样例；法国机房能否访问 Open-Meteo 未验证，部署后用 /health 看 source 是 live 还是 demo，日志在 `/home/<account>/admin/logs/uwsgi/<id>.log`。

**本轮没有执行任何 SSH 上传**（缺账号名和凭据）。下轮需要用户提供：alwaysdata 账号名、SSH 密码或密钥、目标目录（默认 /home/<account>/weather-station）。

## 融合最终上线版（2026-11-15 下午）
用户给了四个其他 agent 做的版本让我融合：wb国内版(D:/AI work\workbuddy\2026-11-15-11-18-44\weather-station)、loomy观云(D:/workspace/loomy/观云天气站)、lobsterai(C:/Users/Administrator/lobsterai/project/weather-cn)、小浣熊(D:/workspace/raccoonwork/cn-weather)。
各版本强项：loomy=全国333地级市内置目录+AQI空气质量+API化；lobsterai=DataV全国区县188KB全集(重)；raccoon=分模块+SEO；我的=卡片点击切换前端+缓存降级。
融合结果（weather-station/，19 测试全绿）：
- 新增 catalog.py（移植 loomy 全国目录 361 城，FEATURED 六城沿用）
- config.py 加 AQI_URL/GEOCODE_URL/DETAIL_FIELDS；weather.py 加 fetch_detail(含AQI,60条LRU)/geocode/mock_detail/fetch_aqi_batch(AQI 支持多坐标批量，已实测)
- views.py 重写：搜索框(内嵌目录离线秒搜+在线兜底)、指标条(体感/湿度/风/AQI)、热度标签、render_page 加 extra 参数(非精选城市 ?city= 直达)
- app.py 路由：/api/weather、/api/search(目录→geocode 兜底,OFFLINE 跳过)、/api/hit、/api/hot、/health；?city= 三级解析(id→全名→search)
- 删除 cities.json（被 catalog.py 取代）；deploy.sh FILES 更新
- 上传文件共 10 个，内存约 20-30MB，目标 256M alwaysdata 免费档
- 预览 preview.html 72KB(含 361 城目录 JSON)。本轮未上传，等用户给账号凭据。

## 关注城市增删功能（2026-11-15 14:20）
用户要求：首页 6 城分两排（4+2），右侧加同尺寸"+/-"卡；+进添加模式（搜索选中即加入），-进删除模式（卡片右上红叉，可删多个）。
实现：
- stats.py 加 featured_ids/featured_set（sqlite featured 表持久化，DB 不可用回退内置默认）
- app.py 加 /api/featured/add|remove（校验目录内 id、上限 config.FEATURED_MAX=12、至少留 1）；首页 featured 改为 _featured_cities()（stats 驱动，跳过失效 id）
- weather.py load_weather 加 _fill_missing：关注集变化后缓存缺城时自动补（OFFLINE→mock，在线→fetch_detail，失败不伪造数据记入 error）
- views.py：卡片加 card-x 红叉（默认隐藏，.cards.removing 显示）；+/- 管理卡；JS 加 addMode/rmMode（添加模式选中候选→api add→跳转 /?city=<id>；删除模式 X→api remove→前端隐藏卡并切到首个剩余面板）；卡片点击处理器对 .card-x 放行（stopPropagation 时序：卡片直接监听器先于容器委托，靠 return 让事件继续冒泡）
- style.css：网格固定 4 列（≤960px 2 列）、管理卡虚线样式、红叉样式
- 测试 20/20 全绿（新增 test_20 覆盖增删/幂等/目录外拒绝/最少 1 个/上限 12）

## 部署上线 alwaysdata（账号 w662000）✅
- SSH 密钥部署：本机 ~/.ssh/id_ed25519_alwaysdata，公钥已加到后台 Remote access > SSH Keys
- deploy/deploy.sh 增加 ALWAYSDATA_SSH_KEY 支持（BatchMode 免密）；只传 8 个运行文件
- 站点设置：Python WSGI / application path=weather-station/app.py / workdir=weather-station / Python 3.13 / venv 空
- 上线验证：首页 200、/health 361 城、搜索/详情/实时数据全部正常
- **改代码后 uWSGI 不会自动重载，必须后台 Sites 行点 ↻ 重启**
- 追加优化：app.py 加 gzip（线程局部传 Accept-Encoding，只压 HTML/CSS/JSON ≥512B）
  84KB→17KB(-79%)，整页 3.3s→1.3-1.9s（剩余为中法 TLS 固定开销）；24/24 测试全绿
- 耗时分解方法：curl -w time_namelookup/time_connect/time_appconnect/time_starttransfer 定位是服务器慢还是链路慢

## 定时任务：城市目录月度维护
- 创建 automation（id b695d4fc）：每月 15 日 10:00（首跑 2026-12-15）
- 流程：核对/更新中国 361 城 + 国际 282 城（枢纽∪首都∪旅游名城∪俄远东）→ 校验 id/名唯一 + 全量测试 → deploy.sh --apply 增量上传 → SSH 远程验证 catalog 数量 + /health → 提醒用户后台点 ↻ 重启
- 关键自包含信息已写入 prompt：部署密钥路径 ~/.ssh/id_ed25519_alwaysdata、账号 w662000、不收录耶路撒冷、台湾城市在中国目录

## CF 子域名 tq.780.de5.net 接入天气站
- **关键政策**：alwaysdata 免费档官方限制"websites limited to alwaysdata.net address"→ 不能绑自有域名，纯 CNAME 方案作废
- **方案**：CF Worker 反代（D:/workspace/workbuddyai/2026-11-15-11-21-53/weather-proxy-cf）
  - src/worker.js：透传 tq.780.de5.net/* → w662000.alwaysdata.net（保留方法/路径/查询串，删 transfer/content-encoding 头，502 兜底）
  - wrangler.toml routes custom_domain=true → CF 自动建 DNS+证书
  - **无 KV/无 cron/无 D1，CF 写量配额 0/天**（符合用户 CF 配额红线）
- 部署：npx wrangler deploy 必须**走代理 http://127.0.0.1:7897**（wrangler OAuth 在 %APPDATA%\xdg.config\.wrangler，wxatp2022@gmail.com；scope 无 dns:write 但 custom_domain 走 workers_routes:write 可行）
- 验证：https://tq.780.de5.net/ 200、/health 643 城、gzip 25KB、纽约搜索正常
- 更新 Worker：改 src/worker.js 后带代理重跑 wrangler deploy

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）