---
layout: default
title: 项目流 · 2026-11-17
date: 2026-11-17 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-16-23-10-26\.workbuddy\memory\2026-11-17.md, D:\AI work\workbuddy\2026-11-17-01-21-22\.workbuddy\memory\2026-11-17.md

## Xray/Hysteria2 双协议项目（新加坡服务器 111.91.31.39）
- 本会话没有该项目的 SSH 凭证和历史记录（部署会话在别处，conversation_search 未命中）
- 实测（01:21）：ping 75ms，TCP 443 通（REALITY 正常），UDP 8443 QUIC VN 探测静默 → 模糊：安全组未放行 或 hy2 未在 8443 监听，二者无法远程区分
- 最可能原因：华为云安全组规则没保存生效（上个会话中断在表单填写环节）
- 探测脚本：C:\Users\Administrator\AppData\Local\Temp\udp8443_probe\quic_probe.py（QUIC 版本协商法，比普通 UDP 探测准）
- 待办：①用户确认安全组规则列表有 UDP/8443/0.0.0.0-0；②服务器 `ss -ulnp | grep -E '8443|hysteria'` 确认 hy2；③都确认后用 v2rayN A/B 实测 REALITY vs hy2
- 进度文件：进度/进度_20261117_0130_UDP8443探测.md

## wb-intl（WB 国际版）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-17.md

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）