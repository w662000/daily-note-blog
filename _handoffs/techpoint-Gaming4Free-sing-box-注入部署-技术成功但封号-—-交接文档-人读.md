---
layout: default
title: 技术点 · Gaming4Free sing-box 注入部署（技术成功但封号）— 交接文档（人读）
date: 2026-07-26 23:30:00 +0800
---

# 技术点 · Gaming4Free sing-box 注入部署（技术成功但封号）— 交接文档（人读）

> 来源：260726_Gaming4Free_sing-box注入部署_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260726_Gaming4Free_sing-box注入部署_handoff.md（编码探测：utf-8）
- > 给接手的同学看。本 handoff 只讲 **Gaming4Free 这条被封号的路径**；成功路径见同批「Wispbyte gost SOCKS5 跑通」。
- 在免费游戏 VPS **Gaming4Free** 上，技术上成功用「替换真实二进制 wrapper」注入部署 sing-box 三协议（SS/VLESS/Hysteria2），但账号因运行非游戏进程违反 TOS 被封。**结论：Gaming4Free 只适合真玩游戏，不能跑代理/bot。**
- Gaming4Free 提供免费游戏 VPS（翼龙/Pterodactyl 面板，锁 shell），想验证能否绕开限制部署多协议代理。技术目标是把 sing-box 跑起来。
- 1. **免费服务器资源全网搜索（21:53）**：产出 `免费服务器资源汇总_2026-07.md`，对比 Wispbyte / FalixNodes / Gaming4Free / Oracle / Serv00 等。
- 3. **sing-box 注入部署（23:xx）**：MOTD 变量注入 ❌ / Console 游戏命令 ❌ / `TerrariaServer` wrapper ❌（未被调用）→ 最终**替换真实二进制 `TerrariaServer.bin.x86_64` 为 wrapper 脚本** ✅，sing-box v1.11.0 三协议部署成功（文件全落盘）。
- 4. **账号被封（00:13）**：SFTP 突然认证失败，进面板发现 `ACCOUNT BANNED — suspended for violating Terms of Service`。根因：免费游戏 VPS 禁止非游戏进程，sing-box 触发风控。
- **免费游戏 VPS（Gaming4Free / FalixNodes 类）不适合跑代理/bot**：有进程/网络行为监控，非游戏负载一跑就封。要跑代理选 **Wispbyte（已验证可用）/ Serv00（免卡永久 FreeBSD 真 shell）/ Oracle Always Free（4C24G ARM，需信用卡）**。
- **注入技术本身成功**：证明「锁 shell 的翼龙面板，可通过替换真实二进制入口注入自定义进程」。这是可复用技巧（换号/换平台仍可用），但用在此类平台会封号。
- **Wispbyte 路径不同**：Wispbyte 允许直接改 Startup Command 写 `/bin/sh`，无需替换二进制（见同批 Wispbyte handoff）。
- 服务器地址（已封）：`g4f-ger-01.gaming4free.net:2022`（SFTP），Terraria v1.4.5.6 监听 25727
- sing-box 三协议：SS `13986` / VLESS `13987` / Hysteria2 `13988`（端口需在面板 Allocations 申请，账号被封前未确认是否申请成功）

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 服务器地址（已封）：`g4f-ger-01.gaming4free.net:2022`（SFTP），Terraria v1.4.5.6 监听 25727
- 注入方式：把 `TerrariaServer.bin.x86_64`（6MB 真实二进制）改名 `.real`，新建同名 shell wrapper 先后台注入 `deploy_sing-box.sh` 再 `exec` 真实二进制
- sing-box 三协议：SS `13986` / VLESS `13987` / Hysteria2 `13988`（端口需在面板 Allocations 申请，账号被封前未确认是否申请成功）
- 部署脚本/配置/日志均在 `/home/container/` 落盘（`sing-box`、`g4f-ss.json` 等、`inject.log`）
- **封号根因**：非游戏进程（sing-box）或异常网络行为触发 TOS 风控
- **教训**：此类平台只玩游戏；代理/bot 换 Serv00 / Oracle / Wispbyte

---

## 7、关键文件
- `deploy_sing-box.sh` — sing-box 部署脚本（非交互版）
- `TerrariaServer.bin.x86_64` — 注入 wrapper 脚本（已上传服务器，现账号封禁）
- `TerrariaServer_modified` — 早期 wrapper 修改版
- `gaming4free_startup.sh` — 启动模板
- `g4f_renew.py` — 自动续约脚本（纯标准库 + 系统 curl；注意自动续约也可能违反 TOS）
- `Gaming4Free_sing-box_部署指南_2026-07.md` / `Gaming4Free_SFTP部署指南_2026-07.md` / `Gaming4Free_自动续约指南_2026-07.md` — 文档

---

## 8、发布记录
- 同源 handoff「免费 VPS 代理与 Gaming4Free 部署」已拆分为本篇（Gaming4Free 封号路径）+ 同批「Wispbyte gost SOCKS5 跑通」（成功路径）。
