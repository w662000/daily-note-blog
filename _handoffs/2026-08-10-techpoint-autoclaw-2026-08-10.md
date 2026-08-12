---
layout: default
title: 技术点 · AutoClaw 2026-08-10
date: 2026-08-12 23:30:00 +0800
---

# 技术点 · AutoClaw 2026-08-10

> 来源：AutoClaw 工作日志 2026-08-10

## 会话记录

- **09:08** 清理自启动目录的 `Hermes-AutoStart.vbs.bak-20260810`（Windows 报 bak 无法启动），删除后目录剩 desktop.ini / Hermes-AutoStart.vbs / Radars-AutoStart.lnk
- **09:27** 排查"资金流动看板"未运行：8850 服务（主力资金流向白名单版）正常运行、HTTP 200、数据接口通；当时 9:27 未开盘（9:30 开盘）所以 f62 为空；无浏览器进程打开界面；看板无开机自启
- **10:07** 修复 sector-fund-flow-dashboard.html（v1.4→v1.5）：根因是系统代理 127.0.0.1:7897 掐断东财直连（实测：绕代理 200 / 走代理 000）；新增 local8850 本地代理源（最高优先级）
- **10:14** 新建 8851 面板：`D:\AI work\workbuddy\板块资金流看板8851\`（app.py 端口 8851 + index.html 复用现成看板界面）；桌面新建 `主力资金流向看板（端口 8851）.bat`（仿 8850 脚本）；踩坑：bat 必须 GBK 编码 + CRLF 行尾，否则 cmd 解析错乱
- **10:19** 数据源实测：push2/82.push2/push2his 域名被东财风控（000），push2delay 通；sina/tencent/聚源全通。重排优先级：local8851(0)→sina(1)→gildata(2)→eastmoney(3)→eastmoney_bak(4)；local8851 改同源 fetch；app.py 缓存 180s + stale-while-error；工作区 v1.6 同步
- **10:27** 刷新默认 30s；排序支持升降序切换（默认降序）；8851 v2.1 / 工作区 v1.7
- **10:29** 批准 evo-2026-08-10-fundflow-dashboard-config-preferences：资金流向看板配置偏好（30s 刷新、行业/概念/地域、升降序默认降序）已写入 MEMORY.md
- **10:30-10:34** 8851/8850 服务同时挂掉（最小化 python 控制台窗口被误关）；8851 先改 pythonw 无窗口（app.py print→log），8850 随后同样改造（用户确认）；两服务均恢复正常

## 关键环境事实

- 系统代理：127.0.0.1:7897（Clash 类），东财 push2 系域名被掐断/风控，本地服务必须 clear_proxy 直连
- 8850/8851 服务上游用 push2delay.eastmoney.com（当前唯一通的东财域名）