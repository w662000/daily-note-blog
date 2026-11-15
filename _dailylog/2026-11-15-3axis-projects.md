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

## 5 端发布审计（11:08-11:20，只读自查）
- ✅ 正常：博客（b196d5a 10:22:59 已推、线上 towertop.kdns.fr/daily-note-blog HTTP 200 含 11-15 内容）；bbs1org#2 / phpBB#10 今日工作日志帖；phpBB#11 今日项目流/技术点 + 2 handoff；Gridea 稿件源 261115×4 + techpoint×7；有道云 handoff 链昨晚 2 篇交接文档。
- ❌ 缺口：① Gridea 线上渲染停 11-14 21:41（step7 被杀没跑）；② bbs1org#3 缺今日 2 帖（phpBB#11 有）→ 0c 假成功；③ 有道云 3 轴缺（工作日志目录最新 11-01），0c 假成功，但 11:12 晨检 automation 正在补发（youdao_tmp 活跃，发「技术点 · 用户级 Skill 清单」等）；④ step6 没跑 → #2/#10 缺 11-13/11-12 补发；⑤ handoff 收件箱 15 篇积压。
- 根因：① schtasks ExecutionTimeLimit PT30M << 列车总最坏耗时（11-14 遗留待办①实锤），连续两轮（11-14 23:15、11-15 10:20）被强杀且 print 缓冲丢失 → 主日志 0 字节；② pw.post/_save_youdao 假成功（返回 ok 服务端未落库），failures 空 → 0c 报 OK。
- 待用户拍板：PT30M→PT2H + 日志 flush；0c 发后回查校验；补发（等晨检结束，避免撞车）。审计报告：会话目录 `审计报告_5端发布_20261115.md`；论坛只读审计脚本 `audit_forums_readonly.py`。


# 2026-11-15 会话日志

## 5 端发布审计（11:08-11:20，只读）
- 结论：博客/论坛工作日志（bbs#2、phpBB#10）/phpBB#11/有道云 handoff 链正常；缺口=Gridea 线上渲染（停 11-14 21:41）、bbs1org#3 今日 2 帖、有道云 3 轴笔记、step6 历史补发（11-13/11-12）、收件箱 15 篇积压。
- 根因：PT30M 强杀列车（连续两轮日志 0 字节）+ 0c 的 pw.post/_save_youdao 假成功。11:00 晨检正在补有道云（youdao_tmp 11:12 活跃）。
- 交付：`审计报告_5端发布_20261115.md` + `audit_forums_readonly.py`。

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

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）