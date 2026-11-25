---
layout: default
title: 项目流 · 2026-11-25
date: 2026-11-25 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-25.md, D:\AI work\workbuddy\2026-11-25-10-55-54\.workbuddy\memory\2026-11-25.md

（该 Agent 当天日志中未检出此类段落）

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-10-29-16-13-56\.workbuddy-ai\memory\2026-11-25.md, D:\workspace\workbuddyai\2026-11-25-13-25-06\.workbuddy-ai\memory\2026-11-25.md

## 中转站方案：cf.7z → GitHub + jsDelivr → 法国纯 IPv6 VPS

- 背景：放弃本地 IPv6/chisel，国内 Windows 上传走 GitHub，VPS 用 `wget -6` 从 jsDelivr 拉 cloudflared。
- 事实核查（本机 DNS/官方源，T1）：
  - `cdn.jsdelivr.net` 有 AAAA（`2a04:4e42:400::485` 等，Fastly）。
  - 用户断言"raw.githubusercontent.com 无 AAAA"是错的：实测有 `2606:50c0:8001/2/3::154`。
  - jsDelivr 单文件限制是 **20 MB**（非用户说的 50MB）；cf.7z 为 17,105,827 B，在限内。
  - cloudflared 源码：`--edge-ip-version` 是 tunnel 层 flag，必须写在 `run` **之前**：`cloudflared tunnel --edge-ip-version 6 run --token ...`；放 run 后面不生效。
- 执行：用本机已登录的 `gh`（账号 w662000，repo scope）建公开临时仓库 `w662000/temp-cf-20261125-wb`，git clone → cp → commit → push 成功。未用网页/curl 上传，未超时。
- CDN 链接：`https://cdn.jsdelivr.net/gh/w662000/temp-cf-20261125-wb@main/cf.7z`
- 验证：`purge.jsdelivr.net` 同路径返回 status=finished（CF/FY 已清缓存）；`data.jsdelivr.com/v1/package/gh/...@main` 列出 cf.7z，size=17105827，与本地一致。本地 curl 因宿主代理 TLS 握手失败无法直连验证，不影响 VPS 侧。
- SHA256（本地 cf.7z）：`5c94bbab06728f24ba32e37b861c65e76f7871b36c3f201fbdd5cdea321a28b4`
- 压缩包内实际文件名：`cloudflared-linux-amd64`（40,334,417 B），不是 `cloudflared`；解压后需 `mv cloudflared-linux-amd64 /usr/local/bin/cloudflared`。若 VPS 非 x86_64 需换包。
- 仓库暂留，等用户确认 VPS 下载完成后再删（`gh repo delete w662000/temp-cf-20261125-wb --yes`）；本地克隆在 `C:\tmp\temp-cf-20261125-wb`。

## au 国内版 Xray 会话缺尾标排查（用户提问）
- 用户问"au国内版 Xray部署方案 会话底部为何无会话ID"：实际会话标题是「Xray部署指南」，创建 2026-11-16 14:50Z、最后更新 2026-11-16 17:19Z（北京 11-17 01:19），对应 `52083aa0-...jsonl`，276 条 assistant 回复 0 条带尾标。
- 原因：会话ID规则 11-17 才定死（`AGENTS.md.bak-sid-20261117` 时间 2026-11-17 14:18），规则只管往后新回复、不回填历史。对照 11-24 会话 `160eadc8` 109/109 条有尾标。AGENTS.md 第 302 行规则仍在，非配置丢失。
- 附注：11-25 会话 `b9e73b36` 首条 user 消息正文为空（text=''），162 条 assistant 0 尾标，属另一异常。

## Xray 部署决策指南（交付文档）
- 用户总结部署方法论（VPS 一键脚本 / 容器看环境 / 端口少走 xray-core+CF隧道），要求结合修正做 md。
- 产出 `D:\workspace\workbuddyai\2026-11-25-13-25-06\Xray部署决策指南.md`：核心修正=判断标准改为"国内能否主动连进来"而非 VPS/容器（InstaBox 完整 VM 但 NAT 无入站反例）；补两坑=平台条款（InstaBox 因 ToS 锁机 24h）、持久化+端到端实测；含路线 A/B/C、纯 IPv6 jsdelivr 中转要点、cloudflared flag 顺序、案例对照表、来源可信度分级。


# 2026-11-25 工作日志

## 22:46 星图扫描汇报（自动化任务 9585354d）

- 今天 22:30 计划任务无记录，补跑 `scan_projects.py`（15.2 秒，正常）。
- 结果：节点 179→181（p180 wb-cn 会话目录、p181 loomy neoheberg 法国 VPS 指南）；边 193→195；日期前推 5；待确认候选 10；schema `discovery-v2-20261115` 正常，无漏收异常。
- 未改写已有节点名/星座/连线；已交付 `星图预览.html`。

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-25.md

## 上午复核（十边形画像 + 冒烟首测）
- 画像 8.1 分证据抽查 7 条全落实（stocks.db 273.5MB=262MiB、星图 159 节点、涨停天梯 52 期、雷达图几何复算吻合）
- 首轮冒烟抓到 skill-creator 三版本漂移（au 最新/6 端旧/lobsterai 最旧）→ 本轮已消除
- 报告：`workspace\smoke_tests\冒烟测试报告_共有skill_20261125.html`

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）