---
layout: default
title: 技术点 · 无锡买房 / 租房 · 58同城爬虫 — 交接文档（人读）
date: 2026-07-25 23:30:00 +0800
---

# 技术点 · 无锡买房 / 租房 · 58同城爬虫 — 交接文档（人读）

> 来源：260725_58的无锡买房租房项目搭建_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260725_58的无锡买房租房项目搭建_handoff.md（编码探测：utf-8）
- > 给接手的同学看。AI/agent 接手请直接读同目录的 `HANDOFF_AGENT.md`（更详细、含可执行命令）。
- > 本文已同步发布到博客 `daily-note-blog`（Jekyll/GitHub Pages）与 Gridea Pro 待发布队列，见第 9 节。
- ```
本地 Playwright 无头浏览器爬虫  ──写入──>  local_crawl.db (listings 表)
        │
        │  db_to_sql.py 读 listings → 生成 import_data.sql
        ▼
wrangler d1 execute --remote  ──直连──>  Cloudflare D1  (wx-houseing-db / wxzf-db)
        │
        ▼
Worker (读接口) + Pages 看板 (用户浏览器访问)
```
- 1. **CF 全套资源已建好并部署**：2 个 D1（`wx-houseing-db` / `wxzf-db`）、2 个 KV、2 个 Worker、2 个 Pages 看板。
- Playwright `asyncio` 冲突：进程内只 `sync_playwright().start()` 一次，跨区只重开**浏览器**（`pw_close_browser`），不再重开整个实例。
- **根因：58 对「沙箱出口 IP」在租房频道做了主动验证码墙（code=300）。**
- 58 现在要求浏览器执行 JS 生成新鲜 `fzq_h` 反爬 token。纯 HTTP 请求（urllib）永远过不了。
- 之前结论"用户浏览器验证/复制 Cookie/走代理都救不了沙箱 IP，必须重启光猫"——**部分错了**：
- **证伪（Cookie 粘贴无效，仍成立）**：之前用户给新鲜 Cookie + 代理，沙箱仍返回 `ws:<IP>` 墙。
- **新证据（手动过验证码有效！）**：用户说"手动点了 58 租房验证"后，沙箱爬虫把**滨湖整区 50 页全爬通、0 撞墙**，紧接惠山也整区通。说明**用户在浏览器里交互式过掉验证码，有可能给沙箱出口 IP 开一个宽松窗口**（机制不明，可能是 58 后端按 IP 解封一段时间，或 `fzq_h` 这类 token 跨会话被认可）。
- **代理 `127.0.0.1:10808` 对国内 58 是 no-op**（走直连），改变不了 `ws:` IP，这条仍成立。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. **别再用 `--test` / 探针消耗宽限额度**。每次 fresh 窗口只够 1–2 个租房区（甚至更多），探针一次就废掉一个区的额度。拿到窗口直接 `--district <区>` 跑。
2. **修正：别再死认"浏览器验证救不了沙箱"**。实测用户手动过验证码后沙箱整区 50 页全通。下次先让用户手动过验证码试试，不行再重启光猫。但**单纯粘贴 Cookie / 走代理仍无效**（历史上验证过）。
3. **灌 D1 前必须 DELETE 叶子表**。`price_records` 无唯一约束，`import_data.sql` 用的是**普通 INSERT（非 OR IGNORE）**，所以**重复导入同一区会翻倍**。租房是**分区增量补**，要用「只删该区」的 DELETE（见下）再导入，**不能 `DELETE FROM price_records` 全删**（会冲掉其他区）；也**绝不可把含多区的混合 SQL 直接导入**（见坑 #11）。
4. **每跑一个区前先清本区 `listings`**：爬虫不会自动清表（只有 `CREATE TABLE IF NOT EXISTS` + 按 listing_key 去重插入），不清的话 `import_data.sql` 会混入之前区的脏数据。
5. **Playwright 实例只启一次**。跨区重开浏览器（`pw_close_browser`）即可，绝不在循环里再调 `sync_playwright().start()`，否则第 2 区起报 `asyncio` 错、后续区全跳。
6. **全程 `env -u HTTP_PROXY ...` 直连**。沙箱有死代理（127.0.0.1:10808），wrangler/npm/任何外网命令都要先 unset 代理变量，否则超时/连不上。
7. **用受管 venv 的 python 跑爬虫**（已装 playwright）：`C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`。受管 runtime 的 `python.exe` 没装 playwright。
8. **`db_to_sql.py` 会丢「无小区名」的房源**：本地 `listings` 1291 条 → SQL 里 1119 条（172 条因社区名为空被过滤）。这是正常行为，不是 bug。
9. **🆕 清表会触发自动播种（seed）污染**：爬虫发现本地 `listings` 为空时，会从最新备份 JSON 自动 `seed_from_backup` 播种 **liangxi 297 条**（batch='seed'）。这些不是本次数据，**推库前务必 `DELETE FROM listings WHERE crawl_batch='seed'` 剔除**，否则会把旧梁溪也推上去。→ 因此**不要 `DELETE FROM listings`（全清）**，用「只删本区」的针对性删除；即便误全清，跑完也记得 strip seed。
10. **Git Bash 里没有 `pgrep`**：判断爬虫是否在跑用 `ps aux | grep crawler.py`，或监测日志文件大小是否停止增长（≥20s 不变即结束）。
11. **🆕 `import_data.sql` 不是 INSERT OR IGNORE，混合导入会翻倍（踩过）**：`db_to_sql.py` 读本地**全部** listings 生成 SQL。若本地含多区（如 binhu+huishan），SQL 就含多区；若只 `DELETE 本区叶子` 再导入，其他区会在 D1 里被重复插一遍（滨湖因此变 2238）。**正确做法：导入前确保本地只含目标区**（跑前 `DELETE FROM listings WHERE district_code != '<区>'`，但别全清见坑#9），或导入前把 SQL 里涉及的所有区叶子都 DELETE。**翻车补救**：按 `listing_key` 去重（见 `dedup_binhu.sql` 模板）。

---
