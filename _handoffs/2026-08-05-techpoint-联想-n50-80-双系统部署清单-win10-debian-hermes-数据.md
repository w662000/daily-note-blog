---
layout: default
title: 技术点 · 联想 N50-80 双系统部署清单（Win10 + Debian + Hermes 数据共享）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · 联想 N50-80 双系统部署清单（Win10 + Debian + Hermes 数据共享）

> 对应项目轴 Handoff：`2026-08-05-handoff-联想-n50-80-双系统部署清单-win10-debian-hermes-数据.md`
> 目的：把「老机器改造成常开 Agent 节点」这条链路里的**可复用技术资产**抽出来——老硬件选型、双系统分区与引导、跨系统共享数据时的代码/数据分离策略、以及 Windows 启动器与进程锁的工程坑。下次做「旧本子 / 双系统 / Agent 节点部署」可直接复用，不必重踩坑。

## 一、技术选型

| 选型项 | 选定 | 落选 | 依据 |
|---|---|---|---|
| 常开系统（跑 agent） | **Debian 12/13 minimal headless** | Ubuntu / Win 常开 | Debian minimal 缺省无 snapd，空载内存低 30~50%；Hermes Agent 以 Linux/WSL2 优先（T1） |
| 应急/兼容系统 | **Win10** | Win7 | Win7 扩展支持 2020 年结束，最高只到 Node16 / Python3.8，跑不了需 Node18+ / Py3.10+ 的 Hermes（T0 官方） |
| 共享盘格式 | **NTFS** | exFAT | 双系统原生读写；NTFS 有权限位（uid/gid）适配 Linux 用户体系，exFAT 无（T1） |
| 启动盘工具 | **Ventoy** | 反复格 U 盘 | 多 ISO 共存，免反复写盘（T1） |
| Agent 运行时数据 | **共享盘放数据真身 + 代码留各自系统盘** | 整根软链共享 | 直接软链整根会导致两边安装器互相覆盖 `hermes-agent/` 代码（T1 实测） |
| 启动器脚本编码 | **纯 ASCII / GBK(ANSI) + CRLF + 无 BOM** | UTF-8 无 BOM | cmd.exe 按 GBK 解读 .bat，UTF-8 无 BOM 会被当乱码在开头语法崩溃（T1 实测） |

## 二、实施要点与关键技术

1. **先做 EFI 扣减再定分区**。总盘 119GiB 先扣掉 EFI 512MB，再切：Win 60G / Debian 18G ext4 / 共享 40G NTFS。曾出现过「Win64/Deb20/共享43」未扣 EFI、导致 Debian 只剩 ~11.5G 偏紧的情况——**分区表先留 EFI 再算其余**（T1）。
2. **安装顺序硬规则：先 Win 后 Debian**。反了 Windows 会覆盖 grub 导致 Debian 不可引导，非建议（T1）。Debian 装到整盘 `/dev/sda`，自动识别 Win10 加进菜单；装时只勾「SSH server + 标准系统实用工具」，桌面环境取消（headless 最省）。
3. **共享盘 fstab 用 LABEL 不用设备名**：`/dev/disk/by-label/SHARED` 比 `/dev/sda4` 稳（设备名可能变）。挂载必须带 `uid=1000,gid=1000,umask=022,windows_names`，否则 Hermes 权限不足读不了配置（T1）。验证：`sudo umount /mnt/shared && sudo mount -a`，无报错即正确。
   ```
   /dev/disk/by-label/SHARED  /mnt/shared  ntfs-3g  defaults,uid=1000,gid=1000,umask=022,windows_names  0  0
   ```
4. **关 Windows 快速启动**：否则 Win 关机是休眠、NTFS 锁卷、Debian 只读，整套方案废（T1）。路径：电源选项 → 选择电源按钮功能 → 更改当前不可用的设置 → 取消「启用快速启动」。
5. **代码/数据分离共享**：Hermes 代码各留系统盘，只把数据子目录（`sessions`/`skills`/`memory`/`config` 等，以实际 `ls` 为准）真身放共享盘、两边软链（Debian 用 `ln -s`，Win 用 `mklink /J` junction）。**软链前必须先对齐两边子目录名**，否则对不上（T1）。
6. **本地时间对齐**：`timedatectl set-local-rtc 1 --adjust-system-clock` 让 Debian 用本地时间，避免和 Win 时间打架、引发证书/日志错乱（T1）。
7. **一次只启一个系统**：双系统同挂一个 Hermes SQLite 库会出现数据库锁。切换使用天然满足此约束，无需额外锁机制（T1）。
8. **Windows 启动器进程锁清理：按完整路径精确过滤**。`taskkill /IM Hermes.exe` 不区分大小写，会误杀 `hermes.exe` 网关进程。正确做法是用 `wmic` 按 `ExecutablePath like '%win-unpacked%Hermes.exe'` 过滤（cmd 原生，不受 PowerShell 执行策略拦截）（T1 实测）。
9. **Hermes 用户级 skill 落盘即生效**：放到 `~/.hermes/skills/<category>/<name>/SKILL.md` 即可，会话启动时递归扫描加载，不用改索引；但加载器有会话级缓存，装完要新开会话验证（T1）。

## 三、模块职责划分

- **Debian = 主用 Agent 节点**：Hermes 数据主真身所在；常开跑 API 型 agent（老硬件无法本地推理）。
- **Win10 = 应急/兼容层**：独立 Hermes 副本，处理只能在 Windows 干的事；不常开。
- **共享 NTFS 盘 = 数据总线**：只承载 Hermes 纯数据子目录，代码绝不进共享盘（避免分平台代码互相覆盖）。
- **EFI 分区 = 引导仲裁**：先装 Win 后装 Deb，grub 接管，EFI 由 Debian 安装器检测复用、不得格式化。
- **硬约束**：一次只启一个系统，避免双系统同挂一个 Hermes SQLite 库导致锁。

## 四、如何选型（可复用的决策方法论）

- **老机器系统选型先看硬件规格**：内存/CPU 代际 → 能本地推理就 Debian+轻量桌面，否则 Debian headless 跑远程 API。snapd 是 Ubuntu 劝退点，Debian minimal 缺省不带。
- **系统版本查官方生命周期 + 工具链最低要求**：别凭印象。Win7 可行是常见误判，实际 Node/Python 最低版本直接判死刑。
- **共享盘格式按场景选**：双系统优先 NTFS（权限位适配 Linux）；纯 Win/Mac 才考虑 exFAT。
- **代码 vs 数据先分离再共享**：任何「多系统共享同一应用」场景，先区分代码（分平台独立）和数据（可共享），否则安装器覆盖直接崩。
- **启动器脚本的编码是确定性坑**：在中文 Windows 上，.bat 一律纯 ASCII 或 GBK+无BOM，UTF-8 无 BOM 必崩。识别特征：bat 双击一闪而过且预期日志根本没生成——说明连第一行都没执行到。

## 五、深化学习指引

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Debian 安装 / 双系统 / grub | debian.org 官方安装指南 | 官方文档 | T0 |
| NTFS 在 Linux 挂载 / ntfs-3g / ntfs3 | linux.die.net / ntfs-3g 官网 | 官方+社区 | T1 |
| Hermes Agent 安装 / 目录结构 | hermes-agent.nousresearch.com/docs | 官方文档 | T0 |
| Ventoy 多 ISO 启动盘 | ventoy.net | 官方 | T0 |
| Windows 快速启动锁盘原理 | Microsoft 电源管理文档 | 官方 | T0 |
| 老机器跑 agent 的硬件边界 | 社区实测（CPU/内存代际 vs 本地推理） | 社区 | T1 |
| 双系统/grub 视频教程 | 待补具体 B站/YouTube UP主 | 待补 | T2 |
| Electron 单实例锁清理 | Electron 官方文档（app.requestSingleInstanceLock） | 官方 | T1（本项目按路径过滤为实测做法） |

## 六、技术结合点

- **顺序 + 引导**：先 Win 后 Deb 是 grub 能干净接管的前提——顺序错，后面全白搭。
- **快速启动 + fstab**：关快速启动解锁 NTFS，fstab 才能稳定读写共享盘；两者任一漏做，Hermes 数据互通就断。
- **代码分离 + 软链**：代码各留系统盘（避免覆盖），数据软链共享盘（实时同一份）——这是整套方案「既能双系统又能数据互通」的核心，比「各留副本再 rsync」省事且不易冲突。
- **EFI 复用 + 分区预留**：先扣 EFI 再切其余分区，Debian 安装器检测复用已有 EFI 而非格式化，保证双系统引导互不破坏。
- **本地时间对齐 + 进程锁精确清理**：小但必做——时间错乱引发隐性 bug；锁清理按路径过滤则避免误杀网关进程。两项都是「不做会间歇性发作」的隐藏项。

---
> 技术点轴文章（对应 Handoff 2026-08-05）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合点。
