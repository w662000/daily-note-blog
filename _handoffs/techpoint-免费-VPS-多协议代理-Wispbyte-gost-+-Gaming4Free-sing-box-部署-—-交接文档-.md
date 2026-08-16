---
layout: default
title: 技术点 · 免费 VPS 多协议代理 · Wispbyte/gost + Gaming4Free/sing-box 部署 — 交接文档（人读）
date: 2026-07-25 23:30:00 +0800
---

# 技术点 · 免费 VPS 多协议代理 · Wispbyte/gost + Gaming4Free/sing-box 部署 — 交接文档（人读）

> 来源：260725_免费VPS代理与Gaming4Free部署_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260725_免费VPS代理与Gaming4Free部署_handoff.md（编码探测：utf-8）
- > 给接手的同学看。AI/agent 接手请直接读同目录的 `HANDOFF_AGENT.md`（更详细、含可执行命令）。
- > 本文已同步发布到博客 `daily-note-blog`（Jekyll/GitHub Pages）、Gridea Pro 待发布队列、语雀知识库，见第 9 节。
- **Wispbyte 免费 VPS**：gost 单二进制 SOCKS5 代理（罗马尼亚，IP `78.154.103.35:13986`）已稳定运行，客户端 FIclash 走该节点加速 GitHub/pypi/raw.github。**YouTube 因免费机房 IP 被流媒体拉黑，无解**（开发加速够用，不追求流媒体）。
- **Gaming4Free 免费游戏 VPS**：技术上成功用「替换真实二进制 wrapper」注入部署 sing-box 三协议（SS/VLESS/Hysteria2），但账号因运行非游戏进程违反 TOS 被封。**结论：Gaming4Free 只适合真玩游戏，不能跑代理/bot。**
- 附带产出：免费服务器资源调研报告、Discord 自建 bot 推荐 10 款、Gaming4Free 自动续约脚本与指南。
- 目标：找一台免费/低成本的 VPS，部署多协议代理（Shadowsocks/VLESS/Hysteria2 等），客户端（FIclash/Clash/V2rayN）连上后能加速 GitHub、pypi 等开发资源（不追求解锁流媒体）。顺带调研免费服务器资源、Discord bot 自部署、Gaming4Free 自动续约。
- 1. **Wispbyte 部署 gost SOCKS5（下午）**：改 Startup 为 `/bin/sh` 拿 shell → 部署 go-gost v3.2.6 单二进制 SOCKS5（带认证）→ FIclash 客户端连上，罗马尼亚 IP，GitHub/pypi 加速成功。
- 2. **YouTube 封禁定位**：从 VPS 回环测 YouTube 偶尔 200，但走代理访问被 reset/不可达交替 → 判定为免费机房 IP 被流媒体主动拉黑，非配置问题，免费套餐无解。
- 3. **sing-box 多协议尝试（Wispbyte，后放弃）**：单端口 13986 下停 gost 试 sing-box shadowsocks，命令已存档；因网页 Console 多行粘贴被吞、无 Ctrl+C，用户嫌卡放弃，回退 gost SOCKS5。
- 4. **免费服务器资源全网搜索（21:53）**：产出 `免费服务器资源汇总_2026-07.md`，分类对比 Wispbyte / FalixNodes / Gaming4Free / Oracle / Serv00 等。
- 6. **Gaming4Free sing-box 注入部署（23:xx）**：MOTD 变量注入 ❌ / Console 游戏命令 ❌ / `TerrariaServer` wrapper ❌（未被调用）→ 最终**替换真实二进制 `TerrariaServer.bin.x86_64` 为 wrapper 脚本** ✅，sing-box v1.11.0 三协议部署成功（文件全落盘）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 服务器地址（已封，仅供参考）：`g4f-ger-01.gaming4free.net:2022`（SFTP），Terraria v1.4.5.6 监听 25727
- 注入方式：把 `TerrariaServer.bin.x86_64`（6MB 真实二进制）改名 `.real`，新建同名 shell wrapper 先后台注入 `deploy_sing-box.sh` 再 `exec` 真实二进制
- sing-box 三协议：SS `13986` / VLESS `13987` / Hysteria2 `13988`（端口需在面板 Allocations 申请，账号被封前未确认是否申请成功）
- 部署脚本/配置/日志均在 `/home/container/` 落盘（`sing-box`、`g4f-ss.json` 等、`inject.log`）
- **封号根因**：非游戏进程（sing-box）或异常网络行为触发 TOS 风控
- **教训**：此类平台只玩游戏；代理/bot 换 Serv00 / Oracle / Wispbyte

---

## 7、关键文件
| 文件 | 说明 |
|---|---|
| `wispbyte-clash.yaml` | FIclash 客户端配置（本机 `C:\Users\Administrator\`） |
| `免费服务器资源汇总_2026-07.md` | 免费服务器调研报告 |
| `Discord_Bot_自建推荐_2026.md` | Discord 自建 bot 推荐 10 款 |
| `Gaming4Free_sing-box_部署指南_2026-07.md` | Gaming4Free sing-box 部署教程 |
| `Gaming4Free_SFTP部署指南_2026-07.md` | SFTP 部署教程 |
| `Gaming4Free_自动续约指南_2026-07.md` | 自动续约指南 |
| `g4f_renew.py` | 自动续约脚本（纯标准库 + 系统 curl） |
| `deploy_sing-box.sh` | sing-box 部署脚本（非交互版） |
| `TerrariaServer.bin.x86_64` | 注入 wrapper 脚本（已上传服务器，现账号封禁） |
| `TerrariaServer_modified` | 早期 wrapper 修改版 |
| `gaming4free_startup.sh` | 启动模板 |

---

## 8、发布记录
- 博客 `daily-note-blog/_posts/2026-07-25-handoff.md`（Jekyll / GitHub Pages 自动渲染）
- Gridea Pro 待发布队列（需在 Gridea Pro 手动点「同步」上线）
- 语雀知识库 `w662000/ylv5l7`，标题 `workbuddy-260725-handoff-free-vps-gaming4free`
- handoff 归档 `D:\AI work\workbuddy\handoff\250725_免费VPS代理与Gaming4Free部署_handoff.md`

---
