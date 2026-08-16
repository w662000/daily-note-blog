---
layout: default
title: 交接文档 · Auto Dark Mode（自动深色模式）恢复说明
date: 2026-08-16 23:30:00 +0800
---

> 来源：2026-08-15-20-54-11\ADM恢复说明_20260815.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# Auto Dark Mode（自动深色模式）恢复说明
日期：2026-08-15

## 你装的软件是什么
- 名称：**Auto Dark Mode（自动深色模式）** v10.1.0.10
- 安装时间：2026-08-03
- 安装路径：`C:\Program Files (x86)\AutoDarkMode\`
- 作用：按时间/规则自动把 Windows 桌面在「浅色 / 深色」之间切换（也就是你说的"强制桌面浅色还是深色"）

## 结论：它其实一直在跑，已经恢复了
排查后发现核心功能没坏，而且现在就是正常运行状态：

| 组件 | 状态 | 说明 |
|------|------|------|
| 后台引擎 AutoDarkModeSvc.exe | ✅ 运行中 | 今天 10:47 启动，一直在自动切换主题 |
| 登录自启任务 ADM Logon | ✅ Ready（已启用） | 之前丢失过，软件自己重建了 |
| GUI 托盘 AutoDarkModeApp.exe | ✅ 运行中 | 当前进程稳定在线 |
| 注册表 Run 自启项 | ⚠️ 空 | 被软件自管清理，改用登录任务（不影响启动） |

## 你为什么会觉得"不启动了"
1. 有一段时间 `ADM Logon` 登录启动任务丢了 → 开机没自动拉起后台；
2. GUI 托盘程序有**间歇性崩溃**（见下），你看到没图标/打不开就以为全挂了。
实际后台引擎一直在干活，深浅色切换没停。

## 唯一残留的小毛病：GUI 托盘偶发崩溃
- 事件日志（Application，EventID 1000）记录 3 次崩溃：08-03、08-04、08-15，**异常码都是 0xe0434352，崩在同一个地址 KERNELBASE 0x2cb69**。
- 说明是某个固定的代码路径（启动或某个定时操作）抛 .NET 异常，不是偶发硬件问题。
- 但托盘进程能存活一段时间，且**换肤功能不依赖 GUI**，所以不影响"强制深浅色"本身。

## 建议的彻底修复（需你点头）
要根治 GUI 崩溃，最靠谱的是**升级到 11.0.0.54**（软件自己之前也提示过有新版本）：
- 同版本（10.1.0.10）重装大概率还崩（这是版本/环境层面的坑，不是文件损坏）；
- 升级到 11.x 很可能修掉这个崩溃，配置会保留。
- 需要我联网下载安装包并升级吗？还是你只想保持现状（后台换肤已经在自动跑）？

## 排查用到的命令（备查）
- 安装软件清单 / 自启项：`Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"` 及 Run 键
- 计划任务：`Get-ScheduledTask -TaskName "ADM Logon"`
- 进程：`Get-Process -Name "AutoDarkMode*"`
- 崩溃日志：`Get-EventLog -LogName Application -Source "Application Error"`（筛选 AutoDarkModeApp.exe）
- 软件自身日志：`C:\Users\Administrator\AppData\Roaming\AutoDarkMode\service.log`