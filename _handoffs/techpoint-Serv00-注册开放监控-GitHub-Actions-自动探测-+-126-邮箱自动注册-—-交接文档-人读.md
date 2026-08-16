---
layout: default
title: 技术点 · Serv00 注册开放监控 · GitHub Actions 自动探测 + 126 邮箱自动注册 — 交接文档（人读）
date: 2026-07-26 23:30:00 +0800
---

# 技术点 · Serv00 注册开放监控 · GitHub Actions 自动探测 + 126 邮箱自动注册 — 交接文档（人读）

> 来源：260726_Serv00 注册开放监控（自动注册）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260726_Serv00 注册开放监控（自动注册）_handoff.md（编码探测：utf-8）
- > 给接手的同学看。AI/agent 接手请直接读同目录的 `HANDOFF_AGENT.md`（更详细、含可执行命令）。
- > 本文已同步发布到博客 `daily-note-blog`（Jekyll/GitHub Pages）、Gridea Pro 待发布队列、语雀知识库。
- **部署了一套 Serv00 免费主机注册开放自动监控系统**：GitHub Actions 每 10 分钟探测 serv00.com 注册页，一旦放出免费名额，自动填表注册 → 用 126 邮箱 IMAP 读验证码邮件 → 点激活链接 → 把账户信息（用户名/密码/SSH 地址）发到 126 邮箱。
- **现已验证健康**：手动 Run workflow 跑通，日志 `[启动] 配置自检 4×True` → `[启动] 邮件服务器 smtp.126.com:465/imap.126.com:993` → `[未开放] HTTP 200，10 分钟后重试`（Serv00 当前限流中，属正常）。
- 目标：申请 **Serv00**（免卡、永久、FreeBSD 真 shell 免费主机，3GB SSD / 512MB RAM / SSH），用于建站/SSH 练手。但 Serv00 免费注册长期处于限流（注册页提示 `The server user limit has been reached. Registering a new account is currently not possible.`），手动蹲守效率低。本任务要一个**全自动、云端常驻、不依赖本机开机**的方案：开放即自动抢注并邮件通知。
- 2. **遇限流**：注册页 `server user limit reached`，需自动探测开放时刻。
- 3. **本机探测脚本（被否）**：写了 `serv00_monitor.py` + `serv00_monitor.bat`（10 分钟弹窗探测）。但沙箱无外网、且本机非 24h 开机 → 用户否掉，改云端。
- 4. **ClawBot 微信推送（放弃）**：用户在 WorkBuddy 绑定 ClawBot，但 WorkBuddy 不向本地落 `bot_token` 明文（翻遍 `settings.json`/SQLite/`app/` 全无），官方文档也不提供查看入口 → GitHub Actions 云端读不到凭据，放弃。
- 5. **邮件通道（落地）**：改用 126 邮箱（网易系，IMAP/SMTP 客户端授权码）。重写 `monitor.py`：探测 + 自动填表注册 + IMAP 读验证码 + 邮件通知，塞进 `daily-note-blog` 仓库的 GitHub Actions。
- 6. **调试两轮报错并修复**：
- 空 Secret 注入空串 → `int("")` 崩溃（GitHub 引用不存在的 Secret 会注入空串而非报错）；

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 仓库：`github.com/w662000/daily-note-blog`
  - `.github/workflows/serv00-monitor.yml` — GitHub Actions，cron 每 10 分钟触发（云端常驻）
  - `serv00-monitor/monitor.py` — 探测 + 自动注册 + IMAP 读验证码 + 邮件通知
- GitHub Secrets（5 个，均已填）：
  - `MAIL_USER` = `w662000@126.com`（专用于此）
  - `MAIL_AUTH` = 126 邮箱 **客户端授权码**（非登录密码）
  - `SERV00_USER` = 自定义 Serv00 用户名
  - `SERV00_PASS` = 自定义强密码
  - `AUTO_REGISTER` = `on`
  - （`MAIL_SMTP_HOST/PORT`、`MAIL_IMAP_HOST/PORT`、`NOTIFY_TO` 均**不填**，代码按 `@126.com` 域名自动识别 `smtp.126.com:465` / `imap.126.com:993`）
- 邮箱：126 邮箱 `w662000@126.com`（每个邮箱只能注册一个免费 Serv00 号，专号专用）

---

## 7、关键文件
| 文件 | 说明 |
|---|---|
| `serv00-monitor/monitor.py` | 监控主脚本（探测+自动注册+IMAP读验证码+邮件通知），已推 GitHub |
| `.github/workflows/serv00-monitor.yml` | GitHub Actions 工作流（10 分钟 cron） |
| `serv00_monitor.py` / `serv00_monitor.bat` | 早期本机探测脚本（已弃用，沙箱无网+非24h开机） |

---

## 8、发布记录
- 博客 `daily-note-blog/_posts/2026-07-26-handoff.md`（Jekyll / GitHub Pages）
- Gridea Pro 待发布队列（`published: true`，需在 Gridea Pro 手动点「同步」上线）
- 语雀知识库 `w662000/ylv5l7`，标题 `workbuddy-260726-handoff-serv00-monitor`
- handoff 归档 `D:\AI work\workbuddy\handoff\260726_Serv00 注册开放监控（自动注册）_handoff.md`

---
