---
layout: default
title: 58的无锡买房租房项目搭建 · 交接文档
date: 2026-07-25 23:30:00 +0800
---

# 无锡买房 / 租房 · 58同城爬虫 — 交接文档（人读）

> 更新于 2026-07-25（**买房 7/7 + 租房 7/7 全部完成，项目整体交付**）。项目根目录：`D:\AI work\workbuddy\2026-07-24-11-46-09\`
> 给接手的同学看。AI/agent 接手请直接读同目录的 `HANDOFF_AGENT.md`（更详细、含可执行命令）。

---

## 0. 项目成功交付总结（一句话看成果）

**无锡 58 同城「二手房 + 租房」两套数据系统已全部上线，7/7 区全齐，看板可看全城数据：**

| 站点 | 状态 | D1 已落数据 | 说明 |
|---|---|---|---|
| **买房（wx-houseing）** | ✅ 已完成 | **7/7 区，3685 条** | 看板已可用，无需再动 |
| **租房（wxzf）** | ✅ 已完成 | **7/7 区，7466 条** | 全部区已落 D1，看板已可用 |

**最大突破**：58 对沙箱出口 IP 在租房频道做了主动验证码墙（code=300），一度以为"浏览器验证救不了沙箱"。实测发现**用户在浏览器里手动过一次验证码，能给沙箱 IP 开一个宽松窗口**——一次手动验证竟连跑锡山+新吴+江阴+宜兴 **4 个整区（各 50 页、0 撞墙）**。

---

## 1. 我们在做什么

做一个「爬 58 同城 → 存云端 → 看板展示」的无锡房产数据系统，分两个独立频道：买房（wx-houseing，二手房 ershoufang）、租房（wxzf，租房 zufang）。
架构（**务必保留**）：本地 Playwright 爬虫 → local_crawl.db → `db_to_sql.py` 生成 import_data.sql → `wrangler d1 execute --remote` 直连 Cloudflare D1 → Worker + Pages 看板。
> 为什么绕远：国内 `*.workers.dev` 的 POST 被网络拦截，爬虫不能直推 Worker，必须落盘后 `wrangler` 直连 D1。

---

## 2. 已经完成的事（时间线）

1. **CF 全套资源已建好并部署**：2 个 D1、2 个 KV、2 个 Worker、2 个 Pages 看板。
2. **买房站 100% 完成**：7 区全爬完灌 D1（3685 条）。
3. **租房站梁溪区**：本地 782 → 过滤有效 673 已灌 D1。
4. **租房站滨湖区（7-24 晚）**：用户手动过验证码后，本地 50 页 1291 条 → 过滤 1119 条灌 D1（district_id=2），0 撞墙。
5. **租房站惠山区（7-24 晚）**：同窗口跑通，50 页 1279 条 → 1116 条灌 D1（district_id=3），0 撞墙。
6. **两个致命 bug 已修**（写进 crawler.py）：Playwright `asyncio` 冲突（进程内只 `sync_playwright().start()` 一次，跨区只重开浏览器）；`http.cookiejar` 吞 Cookie（改拼原始 Cookie 请求头注入）。
7. **租房站锡山/新吴/江阴/宜兴（7-25 上午）**：同一次手动验证窗口连跑 4 个整区，各 50 页 0 撞墙，分别灌 D1：锡山 1140 / 新吴 1143 / 江阴 1121 / 宜兴 1154。**租房 7/7 全部完成。**

---

## 3. 当前卡点 & 关键认知修正

**根因**：58 对「沙箱出口 IP」在租房频道做了主动验证码墙（code=300），要求浏览器执行 JS 生成 `fzq_h` token，纯 HTTP 永远过不了；即便 Playwright，沙箱固定出口 IP 被 58 单独列进验证码墙。
**认知修正**：用户手动过验证码有效（沙箱 IP 开宽松窗口）；代理 `127.0.0.1:10808` 对国内 58 是 no-op；光猫重启未必换 IP（CGNAT），手动验证才是可靠刷新方式。

---

## 4. 标准续跑流程

节奏：用户刷新窗口（手动过验证码 或 重启光猫）→ 说「重启完毕继续任务」→ 直跑下一个缺失区。
每个区标准动作：① 清本区 `listings`（`DELETE FROM listings WHERE district_code='<区>'`，**绝不清全表**）；② `USE_PW=1 python crawler.py --district <区> --no-push`；③ `DELETE FROM listings WHERE crawl_batch='seed'`；④ `python db_to_sql.py wxzf/local-crawler wx 58`；⑤ D1 只删该区叶子再导入；⑥ wrangler 查 count 校验。
**严禁**：拿到新窗口先做 `--test`/探针，会把额度耗光。

---

## 5. 绝对不要再踩的坑（11 条铁律）

1. 别用 `--test`/探针消耗宽限额度，直奔目标区。
2. 别死认"浏览器验证救不了沙箱"，先让用户手动过验证码。
3. 灌 D1 前必须 DELETE 叶子表；`import_data.sql` 是普通 INSERT，重复导入会翻倍 → 用「只删本区」DELETE，不能全删 `price_records`。
4. 每跑一个区前先清本区 `listings`，否则 `import_data.sql` 混入旧区脏数据。
5. Playwright 实例只启一次，跨区重开浏览器（`pw_close_browser`）。
6. 全程 `env -u HTTP_PROXY ...` 直连（沙箱有死代理 127.0.0.1:10808）。
7. 用受管 venv 的 python 跑爬虫（已装 playwright）：`C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`。
8. `db_to_sql.py` 丢「无小区名」房源是正常（1291→1119）。
9. 清表触发自动播种（seed）污染：爬虫见空库会从备份 `seed_from_backup` 播种 liangxi 297 条 → 跑完必须 strip seed；**不要 `DELETE FROM listings`（全清）**。
10. Git Bash 没 `pgrep`，用 `ps aux | grep crawler.py` 或监测日志文件大小。
11. `import_data.sql` 不是 INSERT OR IGNORE，混合导入会翻倍 → 导入前确保本地只含目标区，或导入前把 SQL 涉及的所有区叶子都 DELETE。

---

## 6. 关键命令速查

```bash
cd "D:/AI work/workbuddy/2026-07-24-11-46-09/wxzf/local-crawler"
"$PY" -c "import sqlite3;c=sqlite3.connect('local_crawl.db');c.execute(\"DELETE FROM listings WHERE district_code='huishan'\");c.commit()"
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy USE_PW=1 "$PY" crawler.py --district huishan --no-push
"$PY" -c "import sqlite3;c=sqlite3.connect('local_crawl.db');c.execute(\"DELETE FROM listings WHERE crawl_batch='seed'\");c.commit()"
cd "D:/AI work/workbuddy/2026-07-24-11-46-09"
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy "$PY" db_to_sql.py wxzf/local-crawler wx 58
WR="env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2/node.exe C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/wrangler/bin/wrangler.js"
$WR d1 execute wxzf-db --remote --file=local-crawler/delete_leaves_huishan.sql
$WR d1 execute wxzf-db --remote --file=local-crawler/import_data.sql
```
区 code：`liangxi`梁溪(1) `binhu`滨湖(2) `huishan`惠山(3) `xishan`锡山(4) `xinwu`新吴(5) `jiangyin`江阴(6) `yixing`宜兴(7)

---

## 7. 文件 / 日志索引

- 项目根：`D:\AI work\workbuddy\2026-07-24-11-46-09\`
- 爬虫：`wxzf/local-crawler/crawler.py`、`wx-houseing/local-crawler/crawler.py`；本地库 `local_crawl.db`
- 转换：`db_to_sql.py`；去重模板 `wxzf/local-crawler/dedup_binhu.sql`；删叶子模板 `delete_leaves_<code>.sql`
- 技能：`C:\Users\Administrator\.workbuddy\skills\cf-58-scraper-replicate\SKILL.md`
- 诊断：`ANTIBOT_DIAGNOSIS.md`、`WORKFLOW_REVIEW.md`

## 8. 线上资源

- 买房看板：`https://wx-houseing-worker.wxatp.workers.dev`；租房看板：`https://wxzf-worker.wxatp.workers.dev`
- D1：`wx-houseing-db` / `wxzf-db`；KV：`wx-houseing-worker-cache` / `wxzf-worker-cache`

## 9. 发布去向

- 博客 `daily-note-blog/_posts/2026-07-25-handoff.md`；语雀 `w662000/ylv5l7`（`workbuddy-260725-handoff-58-wuxi-58`）；Gridea Pro 待发布（`260725-58的无锡买房租房项目搭建.md`，`published: true`）；归档 `handoff/260725_58的无锡买房租房项目搭建_handoff.md`。