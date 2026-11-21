---
layout: default
title: 项目流 · 2026-11-21
date: 2026-11-21 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-21-12-57-35\.workbuddy\memory\2026-11-21.md, D:\AI work\workbuddy\2026-11-21-15-45-05\.workbuddy\memory\2026-11-21.md

## 免费海外 SSH 资源调研（新会话首任务）
- 需求：自建搜索查近3个月可免费领、支持 SSH 的海外 VPS/容器/沙箱，要有效信息。
- 方法：自建 SearXNG（`D:\workspace\workbuddyai\agent-teams\.env` 读 URL/key，Python urllib 传中文）4 批查询；B站无登录按 `order=pubdate` 排序抓近期视频（Playwright MCP），视频元数据走 `api.bilibili.com/x/web-interface/view?bvid=` 批量取简介+精确发布时间；抖音/小红书网页搜索强制登录无法抓。
- 交付物：`免费SSH资源调研_20261121.html`（筛选卡片+排除区+风险提示+纯文本复制区）；进度备份在 `进度/进度_20261121_1300.md`。
- 结论资源：TheVibeHosting(首推)、InstaBox(首推)、Oracle Always Free、natbox、VPSFree.io、AlwaysData、GCP e2-micro、Kamatera、Openworld。排除 Cloudzyro/1free.eu/GratisVPS.net。
- 会话 ID：wb|45815896-74dc-496f-a938-9f32b13638f9

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-21-14-56-40\.workbuddy-ai\memory\2026-11-21.md, D:\workspace\workbuddyai\2026-11-21-20-00-45\.workbuddy-ai\memory\2026-11-21.md

## 14:57-15:35 InstaBox 备用 xray 节点部署完成（会话 2026-11-21-14-56-40）

- 平台：instabox.sh 免费档 1 台（instabox261121，Debian 13，4C/8G/20G，auto-pause 30m，runtime 2h→8h）。规则调研：instabox 与 Simular box 是两家，勿混淆。
- **方案 A（REALITY 直连）判死**：机器 IPv4 16.146.121.170 是纯 NAT 出口，监听 9999 外部打不进、机器侧零入站；instabox 自带边缘域名 *.instabox.tech TLS ClientHello 被 reset（疑似 GFW SNI 干扰）。
- **方案 B（CF 命名隧道）落地**，全部走 systemd：
  - xray 26.11.9：REALITY 443(0.0.0.0，备用) + VLESS-WS 8080(127.0.0.1)，UUID 605f1841-6c61-45f0-a669-195d2b8ec93d，path /wgnqo4kj，systemd enable（xray.service）
  - cloudflared 2026.11.1：命名隧道 instabox-2021（ID 4e2a005d-54eb-4c35-a466-f2c85b7067a4）→ instabox.780.de5.net，systemd enable（cloudflared.service）
  - CF 授权复用昨天流程：tunnel login URL → Tabbit 浏览器（wxatp2022@gmail.com 登录态）选 zone 780.de5.net 授权，cert.pem 落机器并备份本地
- 端到端验证通过：出口 IP=机器 IPv6 ✅ google 200 ✅ youtube 200 ✅
- 交付物在 D:\workspace\workbuddyai\2026-11-21-14-56-40\instabox-node\：vless-link.txt（InstaBox-WS-CF）、ssh-token.txt、cf-cert.pem.bak、client-test.json、deploy-xray.sh、notes.md
- 踩坑：①新版 xray x25519 输出格式变了（PrivateKey:/Password (PublicKey):）；②curl --noproxy '*' 连 -x 测试代理一起禁（坑再现，查了两次才想起昨天已记档）；③Bash 工具的前台 & 后台进程随命令结束被杀，常驻客户端要用 run_in_background；④机器 SSH 网关 ssh.instabox.sh:2222，token 用户名免密；⑤家目录在 /data（持久盘），cloudflared 凭证放 ~/ 恰好持久。
- 遗留：instabox CLI 有无无头 resume 手段未查；机器暂停/到点停机后需用户手动 Resume（外部连接无法唤醒）。

## 19:03-19:40 OpenList 影视下载服务打通 + ⚠️ 机器被风控锁定 24h

- OpenList+qBittorrent 离线下载全链路打通（详见 instabox-node/notes.md「OpenList 影视下载服务」节）：
  - OpenList v4.2.10 API 坑：加离线任务字段是 **urls（数组）** 不是 url（传错静默返回 tasks:[]）；set_qbit body 是扁平 {"url":...,"seedtime":...}；工具配置页在管理后台→设置；任务在 /api/admin/task/offline_download_transfer/ 下（不在 copy/upload/move）
  - /data/media 必须 chown 1001:1001（容器 UID），否则 transfer permission denied
  - 端到端实测：SimpleHttp 下 1MB mp4 → 自动搬到 /media → 外网 https://media.780.de5.net/p/media/...?sign=... 返回 200 video/mp4 ✅
  - BT 磁力已推入 qB（metaDL 等 DHT），已加 5 个公共 tracker，**验证未完成即遇锁机**
- **⚠️ 重大事件（19:22 发现）**：InstaBox 免费档风控锁定机器至 **2026-11-22T11:23:29Z（≈北京时间 11-22 19:23）**。原因：免费档 Terms 2(e) 禁止代理服务器，xray 在 8080 被检测第二次 → 自动锁。数据保留，解锁后容器应自动恢复。三个选项待用户拍板：①等解锁继续跑（有再封风险）②xray 迁走（华为云SG/曼谷），InstaBox 只留影视下载 ③instabox feedback 复核。

## 17:15-17:30 Uptime-Kuma 部署 + 126邮件通知上线（用户拍板：邮件方案，不用 ntfy）

- Kuma docker 部署在 InstaBox：/data/kuma 持久卷，127.0.0.1:3001，--restart=always；CF 隧道加第二条 ingress kuma.780.de5.net → 3001，CNAME 已 route dns。
- 管理员 admin/Kuma-5724fbf6259d1290992c4504（notes.md 有记录）。用户邮箱 w662000@126.com（历史会话确认）。
- 关键发现：**126 SSL SMTP 端口是 994**，465/587/25 从美国机器全 ECONNREFUSED；用 python3 smtplib 实发验证通过。
- 通知"126邮件"已存（默认开启+应用所有监控）；4 条监控全 Up：InstaBox节点(400算Up)/Kuma面板/SG-xray TCP443/BKK TCP25055。
- Kuma UI 自动化坑：顶部 uk-latest-warning 拦截点击要先 remove；checkbox 必须 Playwright 真实 click（evaluate 改 checked 不触发 Vue）；监控类型文案是"TCP Port"非"TCP 端口"。
- 用户的手机端 126 邮件推送速度待观察（轮询型 App 可能延迟几分钟），Kuma 侧随时可加 ntfy 做第二通道。

## 16:46 SG 华为云服务清单对比评估（结论：曼谷/InstaBox 都不需要补装）

- SG 华为云（root@111.91.31.39，800Mi 内存）：swap 2G(/swapfile) + chrony/fail2ban/vnstat/netdata/xray。这些是为"小内存+公网22暴露"场景配的。
- InstaBox：7.8G 内存 + 平台已配 4G swap(/data/swapfile)，不用调；sshd 不暴露公网（网关证书认证）不需要 fail2ban；timesyncd 被平台 mask 但时钟实测零偏差（UTC 对比），不用管；vnstat/chrony/netdata 在 Debian13 仓库都没有包（trixie 移除）。
- 曼谷 Altare（proot）：swap 无权管理（proot 无内核控制，宿主 /proc 显示 263G 内存/0 swap），时钟共享宿主内核，无需任何补装，netdata 已装。

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）