---
layout: default
title: 技术点 · 联想 N50-80 双系统部署实操（Win10 + Debian + Hermes 共享）
date: 2026-08-11 13:10:00 +0800
---

# 技术点 · 联想 N50-80 双系统部署（Win10 + Debian + Hermes 共享）

> 对应项目轴 Handoff：`2026-08-05-handoff-联想n50-80双系统部署win10与debian共享hermes数据`
> 目的：从该项目提炼**可复用技术资产**——技术选型、实施要点、模块职责、深化学习路径、技术协同点。下次类似「老机器 / 双系统 / Agent 节点部署」直接复用，不必重踩坑。

## 一、技术选型（这个项目用了哪些技术栈 / 组件，怎么定的）

| 选型项 | 选定 | 落选 | 选型依据 |
|---|---|---|---|
| 常开系统（跑 agent） | **Debian minimal** | Ubuntu | Ubuntu 默认带 snapd，系统开销大；Debian minimal 更轻，4GB 内存 + 5 代低压双核更友好（T1 社区实测） |
| 应急/兼容系统 | **Win10** | Win7 | Node18 / Py3.10 起不支持 Win7，Hermes 安装器需要这些版本；Win7 已停更（T0 官方） |
| 共享盘格式 | **NTFS** | exFAT | 双系统原生读写；NTFS 有权限位（uid/gid）适配 Linux 用户体系，exFAT 无（T1） |
| 内存 | 原装 4GB（建议加 DDR3L 到 8G） | — | N50-80 有 2 个 SO-DIMM 槽，DDR3L 1.35V 二手约 ¥20–40（T1） |
| 启动盘工具 | **Ventoy** | 反复格 U 盘 | 多 ISO 共存，免反复写盘（T1） |

## 二、实施要点与关键技术（落地用了哪些做法）

1. **双系统安装顺序**：先 Win10 后 Debian。反了 Windows 会覆盖 grub 导致 Debian 不可引导——硬规则，非建议（T1）。
2. **grub 接管引导**：Debian 装到整盘 `/dev/sda`，自动识别 Win10 加进菜单（T1）。
3. **共享盘 fstab 自动挂**：用 `LABEL=SHARED` 比 `/dev/sda4` 稳（设备名可能变）；挂载必须带 `uid=1000,gid=1000`，否则 Hermes 权限不足读不了配置（T1）。
4. **代码/数据分离共享**：Hermes 代码各留系统盘，只把数据子目录（sessions/skills/memory/config）真身放共享盘、两边软链（Debian 用 `ln -s`，Win 用 `mklink /J` junction）（T1）。
5. **关 Windows 快速启动**：否则 Win 关机是休眠、NTFS 锁卷、Debian 只读，整套方案废（T1）。
6. **本地时间对齐**：`timedatectl set-local-rtc 1` 让 Debian 用本地时间，避免和 Win 时间打架（T1）。

## 三、模块职责划分（系统 / 组件如何分工）

- **Debian = 主用 Agent 节点**：Hermes 数据主真身在此；常开跑 API 型 agent。
- **Win10 = 应急/兼容层**：独立 Hermes 副本，处理只能在 Windows 干的事；不常开。
- **共享 NTFS 盘 = 数据总线**：只承载 Hermes 纯数据子目录，代码绝不进共享盘（避免分平台代码互相覆盖）。
- **硬约束**：一次只启一个系统，避免双系统同挂一个 Hermes SQLite 库导致锁。

## 四、如何选型（可复用的决策方法论）

- **老机器系统选型**：先看硬件规格（内存/CPU 代际）→ 能本地推理就 Debian+轻量桌面，否则 Debian headless 跑远程 API。snapd 是 Ubuntu 劝退点。
- **共享盘格式**：双系统场景优先 NTFS（权限位适配 Linux）；纯 Win/Mac 才考虑 exFAT。
- **系统版本**：查官方生命周期 + 工具链最低要求（Node/Py 版本），别凭印象（曾误判 Win7 可行）。
- **代码 vs 数据**：任何「多系统共享同一应用」场景，先区分代码（分平台独立）和数据（可共享），否则安装器覆盖直接崩。

## 五、深化学习指引（想深入看这些）

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Debian 安装 / 双系统 / grub | Debian 官方安装指南 debian.org | 官方文档 | T0 |
| NTFS 在 Linux 挂载 / ntfs-3g | linux.die.net / ntfs-3g 官网 | 官方+社区 | T1 |
| Hermes Agent 安装 / 目录结构 | hermes-agent.nousresearch.com/docs | 官方文档 | T0 |
| Ventoy 多 ISO 启动盘 | ventoy.net | 官方 | T0 |
| Windows 快速启动锁盘原理 | Microsoft 电源管理文档 | 官方 | T0 |
| 老机器跑 agent 的硬件边界 | 社区实测（CPU/内存代际 vs 本地推理） | 社区 | T1 |
| 双系统/grub 视频教程 | 待补具体 B站/YouTube UP主 | 待补 | T2 |

## 六、技术结合点（这些技术怎么协同，1+1>2）

- **顺序 + 引导**：先 Win 后 Deb 是 grub 能干净接管的前提——顺序错，后面全白搭。
- **快速启动 + fstab**：关快速启动解锁 NTFS，fstab 才能稳定读写共享盘；两者任一漏做，Hermes 数据互通就断。
- **代码分离 + 软链**：代码各留系统盘（避免覆盖），数据软链共享盘（实时同一份）——这是整套方案"既能双系统又能数据互通"的核心，比"各留副本再 rsync"省事且不易冲突。
- **本地时间对齐**：小但必做，否则日志/证书时间错乱引发隐性 bug。

---
> 本文为技术点轴示范（对应 Handoff 2026-08-05）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合。每个 Handoff 都应有一篇对应技术点，与项目轴一一对应。
