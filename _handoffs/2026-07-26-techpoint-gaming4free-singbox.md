---
layout: default
title: 技术点 · gaming4free-singbox（受限游戏 VPS 二进制入口注入，技术成功但封号）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · gaming4free-singbox：锁 shell 容器下注入自定义进程（技术可行但违反 ToS）

> 对应项目轴 Handoff：`2026-07-26-handoff-gaming4free-singbox`
> 目的：从「Gaming4Free 免费游戏 VPS 注入 sing-box 多协议」提炼可复用技术资产——翼龙/Pterodactyl 受限容器下替换入口二进制的注入技巧、单二进制代理内核选型、以及「技术可行 ≠ 合规可用」的选型纪律。作为反面教材也很有价值。

## 一、技术选型（这个项目用了哪些技术栈 / 组件，怎么定的）

| 选型项 | 选定 | 落选 | 选型依据 |
|---|---|---|---|
| 平台 | **Gaming4Free（翼龙面板游戏 VPS）** | Wispbyte / Serv00 / Oracle | 比 Wispbyte 大方 5 倍、可多开端口铺多协议（但**只适合真玩游戏**） |
| 代理内核 | **sing-box v1.11.0** | gost（Wispbyte 方案） | 单二进制、无依赖、免 root、内置 SS/VLESS/Hysteria2 多协议，适合非 root 容器（T1） |
| 注入点 | **替换真实二进制 `TerrariaServer.bin.x86_64` 为 wrapper** | MOTD 变量 / Console 命令 / `.real` 改名 | MOTD/Console/原 wrapper 均未被调用，只有替换真实入口二进制才生效（T1 实测） |
| 文件传输 | **SFTP（端口 2022，FileZilla）** | 网页 Console 粘贴 | 网页 Console 多行粘贴被吞、不支持 Ctrl+C，SFTP 上传文件再执行更稳（T1） |
| 续约 | **`g4f_renew.py`（cURL Cookie 重放 Extend 按钮）** | 标准 Pterodactyl API | 标准 API 只有 start/stop/restart，无延长租约端点（T1） |

## 二、实施要点与关键技术（落地用了哪些做法）

1. **注入链路（最终成功写法）**：把真实二进制 `TerrariaServer.bin.x86_64`（6MB）改名为 `.real`，新建同名 shell wrapper——先后台注入 `deploy_sing-box.sh`（拉起 sing-box 三协议），再用 `exec` 交棒真实二进制，保持 PID 1 语义让面板存活检测正常（T1）。
2. **三协议端口**：SS `13986` / VLESS `13987` / Hysteria2 `13988`；端口须在面板 Allocations 申请才能通外网（T1）。
3. **非 root 容器落盘**：所有文件放 `/home/container/`（sing-box、`g4f-ss.json`、`inject.log` 等），不依赖 apt 安装（T1）。
4. **续约脚本只用标准库 + 系统 curl**：`g4f_renew.py` 复制浏览器 F12 的 Extend 按钮 cURL + Cookie 重放；注意自动续约**也可能违反 ToS**（T1，待核实边界）。
5. **封号根因**：非游戏进程（sing-box）或异常网络行为触发 ToS 风控，SFTP 突然认证失败即为被封第一信号，进面板见 `ACCOUNT BANNED — suspended for violating Terms of Service`（T1 实测）。
6. **网页 Console 极不友好**：多行粘贴被吞成一行、不支持 Ctrl+C，部署一律改 SFTP 上传文件再执行（T1）。

## 三、模块职责划分（系统 / 组件如何分工）

- **翼龙面板**：容器编排、启动命令定义、Allocations 端口分配、存活检测（看 PID 1）。
- **启动二进制**：注入点——被替换成 wrapper 后，既拉起自定义进程又交棒原游戏进程。
- **wrapper 脚本**：进程编排器，先起旁路进程（sing-box）再 `exec` 主进程，保持单 PID 1。
- **sing-box 配置 `g4f-ss.json`**：三协议监听定义，无 root 下运行。
- **续约脚本 `g4f_renew.py`**：延长租约，依赖 Cookie 重放（非官方 API）。
- **SFTP 通道**：文件上传与登录，被封时首先失效的入口。

## 四、如何选型（可复用的决策方法论）

- **先问 ToS 再问技术**：免费平台能否承载你的负载，第一约束是服务条款而非技术可行性。游戏 VPS 的进程/网络行为监控会一跑非游戏负载就封——要在动手前把「合规」排在第一位。
- **受限 shell 的注入层级**：优先改面板 Startup Command（Wispbyte 可用）→ 其次替换入口二进制 → 再次启动前钩子 → 末位才是 MOTD/Console（本项目实测后两者无效）。按「改动越小、越靠近启动入口」的优先级试。
- **内核选型看依赖**：受限非 root 容器优先选「单静态二进制、无依赖、免 root」的内核（sing-box / gost），避免编译型方案（3proxy 卡 root）。
- **把封号当高概率风险**：技术验证成功 ≠ 账号安全；评估损失（时间 + 账号）是否在可接受范围，再决定投入。

## 五、深化学习指引（想深入看这些）

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Pterodactyl / 翼龙面板启动机制与进程模型 | pterodactyl.io 文档 | 官方文档 | T0 |
| sing-box 配置（SS/VLESS/Hysteria2 单二进制） | sing-box.com 文档 | 官方文档 | T0 |
| 入口二进制替换 + `exec` 交棒注入技巧 | 本项目 `TerrariaServer.bin.x86_64` wrapper 实测 | 自己实测 | T1 |
| Gaming4Free / FalixNodes 类游戏 VPS ToS（禁非游戏进程） | 平台服务条款原文 | 官方条款 | T1 |
| 免费代理可用平台清单（Wispbyte/Serv00/Oracle） | 本项目「免费服务器资源汇总」实测 | 自己实测 | T1 |
| 自动续约是否触发封号的精确阈值 | 平台风控实测 | 印象级，待核实 | T2 |

## 六、技术结合点（这些技术怎么协同，1+1>2）

- **替换二进制 + `exec` 交棒**：两者组合才既注入自定义进程、又让面板存活检测通过——只替换不 `exec` 会让游戏进程起不来、面板判定崩溃重启；只 `exec` 不替换则没机会插自定义进程。
- **单二进制内核 + 非 root 容器**：sing-box 免依赖特性正好适配非 root 沙箱，使「在受限容器跑多协议」从编译地狱变成文件上传即可运行。
- **SFTP + 非交互脚本**：SFTP 上传 + 非交互 `deploy_sing-box.sh` 绕开了网页 Console 的输入限制，是受限面板下唯一可行的部署路径。
- **技术可行性 × 合规可行性**：本项目的核心教训——两者是乘积关系，任一为 0 则整体不可用。注入技巧本身（入口替换）是可复用资产，但用在此类平台必封号，应转移到 Wispbyte/Serv00/Oracle 等允许的背景下。

---
> 本文为技术点轴（对应 Handoff 2026-07-26-gaming4free-singbox）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合。每个 Handoff 都应有一篇对应技术点，与项目轴一一对应。
