---
layout: default
title: 项目流 · 2026-11-22
date: 2026-11-22 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-22-10-52-32\.workbuddy\memory\2026-11-22.md

## 12:38 小批完成 + 全量启动
- 小批结果：148 个全部「已注册」，可注册 0，错误 0（2位数字和2位英文单词全被抢光）。产物 result_small.jsonl / summary_small_*.csv / AVAILABLE_small_*.txt(空) / run_small.log。
- 全量：把 result_small.jsonl 复制成 result_full.jsonl 复用断点，跳过148个，实际查1122个；后台任务 wEt1oC 跑中（约40分钟）。抽查 [149/1270] 000.us.ci 已注册，正常无限流。
- 进度：`进度/进度_20261122_1238_DNSHE全量查询进行中.md`。
- 经验：后台任务句柄可能随会话重建失效（ePNzml 找不到了），此时直接读结果文件 + run_*.log 判断进度/完成情况。

## 18:48 DNSHE 全量查询完成（19:20 汇总）
- 最终：1270/1270 全查完，0 错误。**可注册 589 个**（2位数字0、2位英文0、3位数字587、3位英文2个：pkg/gov）。681 个已被注册。
- 结论：2位域名 100% 被抢光；3位数字近六成空（035-097 大面积空缺，100+ 随机）；pkg.us.ci 和 gov.us.ci 是仅剩的3位英文。
- 产物：`DNSHE_usci查询最终报告.md`、AVAILABLE_full_20261122_184801.txt（589个）、summary_full_20261122_184801.csv、result_full.jsonl。
- 脚本 dnshe_usci_check.py 可复用：改 ROOT 变量即查 cc.cd / de5.net / bot.cd 等后缀；断点续查可用。
- 提醒用户：清单是 18:48 快照，注册前先在控制台复核。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-10-29-16-13-56\.workbuddy-ai\memory\2026-11-22.md, D:\workspace\workbuddyai\2026-11-22-12-57-38\.workbuddy-ai\memory\2026-11-22.md

## LightVela 反向隧道（2026-11-22 完成）
- 跳板：华为云新加坡 ECS root@111.91.31.39，密钥 C:\Users\Administrator\.ssh\id_ed25519_huawei_sg（来源：autoclaw 会话 52083aa0）
- 方案：两跳 SSH 零安全组改动——沙箱生成专用密钥（authorized_keys 加 restrict,port-forwarding，只能转发端口）→ ssh -R 127.0.0.1:15244:127.0.0.1:5244 → 本地 ssh -L 15244
- 会话被踢（"signed in on another device"）时：点 Reconnect → 侧栏 "Get hardware information" 恢复旧线程
- 本地 bat：C:\Users\Administrator\Desktop\LightVela-OpenList-Tunnel.bat（照 SG-Server-Monitor.bat proven 模板，纯 ASCII + curl 探针 + wmic 按 name 过滤），check_launcher PASS
- 验证：本地 curl 127.0.0.1:15244/ping→pong，视频 Range 206（含 1MB seek），README 200
- 自启：systemd service lightvela-tunnel（Restart=always）或 crontab @reboot，agent 配置中

## 部署流程已沉淀为 Skill 并跨 Agent 分发（2026-11-22）
- 源头：`C:\Users\Administrator\.workbuddy\skills\lightvela-openlist-aria2-tunnel\`
- 内容：SKILL.md + references(openlist-api/troubleshooting/cdp-notes) + assets(compose/aria2.conf/systemd service/纯 ASCII CRLF bat 启动器) + scripts(cdp_eval.js/check_launcher.py)，共 10 文件
- 敏感信息处理：admin 密码、RPC secret、跳板机 IP 全部用 CHANGE_ME 占位，未写入密钥/真实密码
- 校验：quick_validate PASS；启动器 check_launcher PASS(WITH WARNINGS，仅 >nul 探针警告)；跨 agent dry-run 全部 new install
- 分发：`sync_skill.py lightvela-openlist-aria2-tunnel --to primary` 成功到 wb-intl / au / au-ws / zcode / lobsterai / loomy / raccoon 7 个目标，每个目标均 10 文件且 SKILL.md 存在；多数 agent 需新会话才重读 skill

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）