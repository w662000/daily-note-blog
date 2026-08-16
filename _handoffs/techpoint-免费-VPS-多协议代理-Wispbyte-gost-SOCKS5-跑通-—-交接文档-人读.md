---
layout: default
title: 技术点 · 免费 VPS 多协议代理 · Wispbyte gost SOCKS5 跑通 — 交接文档（人读）
date: 2026-07-25 23:30:00 +0800
---

# 技术点 · 免费 VPS 多协议代理 · Wispbyte gost SOCKS5 跑通 — 交接文档（人读）

> 来源：260725_免费VPS代理Wispbyte_gost跑通_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260725_免费VPS代理Wispbyte_gost跑通_handoff.md（编码探测：utf-8）
- > 给接手的同学看。本 handoff 只讲 **Wispbyte + gost SOCKS5 这条成功路径**（持续可用）；Gaming4Free 那条封号路径见同批 handoff「Gaming4Free sing-box 注入部署」。
- 在免费 VPS **Wispbyte** 上用单二进制 **gost** 部署 SOCKS5 代理（罗马尼亚，IP `78.154.103.35:13986`），客户端 FIclash 连上后成功加速 GitHub / pypi / raw.github。**YouTube 因免费机房 IP 被流媒体拉黑，无解**（开发加速够用，不追求流媒体）。
- 找一台免费/低成本的 VPS 部署多协议代理（Shadowsocks/VLESS/Hysteria2 等），客户端（FIclash/Clash/V2rayN）连上后加速 GitHub、pypi 等开发资源（不追求解锁流媒体）。Wispbyte 是验证可用的免费选项（允许自定义 Startup Command）。
- 2. **部署 go-gost v3.2.6 单二进制 SOCKS5（带认证）**：上传 gost 二进制 → 后台 `nohup` 跑 SOCKS5，监听 `0.0.0.0:13986`，账号密码认证。
- 4. **YouTube 封禁定位**：从 VPS 回环测 YouTube 偶尔 200，但走代理访问被 reset/不可达交替 → 判定为免费机房 IP 被流媒体主动拉黑，非配置问题，免费套餐无解。
- 5. **sing-box 多协议尝试（后放弃）**：单端口 13986 下停 gost 试 sing-box shadowsocks，命令已存档；因网页 Console 多行粘贴被吞、无 Ctrl+C，用户嫌卡放弃，回退 gost SOCKS5。
- **Wispbyte 路径不同于 Gaming4Free**：Wispbyte 允许直接改 Startup Command 写 `/bin/sh`，无需替换二进制；而 Gaming4Free 锁 shell、需替换真实二进制注入（见同批 Gaming4Free handoff）。
- **免费机房 IP 被流媒体拉黑是通病**：YouTube/Netflix 这类基本无解，代理定位在「开发资源加速」而非「流媒体解锁」。
- 服务器 `w662000`，IP `78.154.103.35`，端口 `13986`
- `C:\Users\Administrator\wispbyte-clash.yaml` — FIclash 客户端配置（本机）
- Wispbyte 服务器端：gost 二进制 + 启动命令（Startup Command 持久化）

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 服务器 `w662000`，IP `78.154.103.35`，端口 `13986`
- 账号 `w662000` / 密码 `vpspwd13543688`（已改掉默认弱密码，因公网扫描器狂暴 auth failure）
- 协议：gost SOCKS5（带认证），含 Google DNS resolver `8.8.8.8:53`
- 客户端：FIclash（Clash.Meta 内核），本地 yaml `C:\Users\Administrator\wispbyte-clash.yaml`，节点 `wispbyte-socks5`
- 验证：`curl -x socks5://w662000:vpspwd13543688@78.154.103.35:13986 https://github.com -o /dev/null -w "%{http_code}"` → 200
- 限制：YouTube 等流媒体被机房 IP 拉黑；免费套餐 512M 内存

---

## 7、关键文件
- `C:\Users\Administrator\wispbyte-clash.yaml` — FIclash 客户端配置（本机）
- Wispbyte 服务器端：gost 二进制 + 启动命令（Startup Command 持久化）

---

## 8、发布记录
- 同源 handoff「免费 VPS 代理与 Gaming4Free 部署」已拆分为本篇（Wispbyte 成功路径）+ 同批「Gaming4Free sing-box 注入部署」（封号路径）。
- 附带产出：免费服务器资源调研报告、Discord 自建 bot 推荐 10 款、Gaming4Free 自动续约脚本与指南（见对应调研文档）。
