---
layout: default
title: 技术点 · AutoClaw 工作日志 · 2026-08-12
date: 2026-08-12 23:30:00 +0800
---

# 技术点 · AutoClaw 工作日志 · 2026-08-12

> 来源：260812_autoclaw-工作日志-2026-08-12_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260812_autoclaw-工作日志-2026-08-12_handoff.md（编码探测：utf-8）
- 用户反馈"昨天部署的系统还有错误"，排查发现 4 个叠加问题：
- 现象：内核 uptime 39 分钟不变，但 systemd (PID 1) 每 1-3 分钟重启一次（apport socket 反复 Closed/Listening），所有服务跟着被杀重启 → 8000 端口时有时无、任务中断
- 元凶：`wsl-pro.service`（Ubuntu Pro 桥接服务）因 interop 问题持续失败（exec format error 调 cmd.exe），NRestarts 一路涨到 8+，每 2 秒循环一次拖垮 systemd
- 修复：`systemctl disable --now wsl-pro.service` → PID 1 elapsed 稳定增长，不再崩溃
- 昨天部署时配了 cron `@reboot /root/tacn-watchdog.sh`（每 60 秒检查端口、nohup 拉起）+ systemd enable 自启 → 两套 uvicorn/worker/vite 抢 8000/3000
- 修复：crontab -r 清除 watchdog（脚本已备份 tacn-watchdog.sh.bak-20260812），保留 systemd 单一管理
- 新增 tacn_killall.sh 清理脚本备用
- POST token.sensenova.cn/v1/chat/completions → 429 insufficient_quota（"Allocated quota exceeded"）
- 修复：system_configs version 8→9，sensenova enabled=false（保留记录），agnes priority=10→100，调度脚本模型 deepseek-v4-flash → agnes-2.5-flash
- BaoStock 被封"黑名单用户"（昨频繁登录触发），股票信息/财务数据走 akshare（同步 5543 条成功）
- akshare 新闻接口报 "Invalid regular expression: invalid escape sequence: \u"（东财新闻正则 bug），FinnHub key 还是占位符 your_finnhub..._here

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 崩溃根源在 WSL 层（systemd 被 wsl-pro 拖垮），与部署方式无关，Docker 同样跑在 WSL 上
- Docker 方式多一层容器自愈（restart=always），更抗单点崩溃，但底层 WSL 不稳一样会断
- 已修复到可用状态，如再出现 systemd 反复重启，第一反应检查 `systemctl status wsl-pro`
