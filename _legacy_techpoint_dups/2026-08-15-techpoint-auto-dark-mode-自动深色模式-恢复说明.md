---
layout: default
title: 技术点 · Auto Dark Mode（自动深色模式）恢复说明
date: 2026-08-15 23:30:00 +0800
---

# 技术点 · Auto Dark Mode（自动深色模式）恢复说明

> 来源：handoff《Auto Dark Mode（自动深色模式）恢复说明》（2026-08-15）

## 一、技术选型

- **软件**：Auto Dark Mode（ADM）v10.1.0.10，开源 Windows 主题自动切换工具。
- **安装路径**：`C:\Program Files (x86)\AutoDarkMode\`
- **核心组件**：
  - `AutoDarkModeSvc.exe`：后台服务，实际执行浅色/深色切换；
  - `AutoDarkModeApp.exe`：GUI 托盘程序，用于配置和状态展示；
  - `ADM Logon`：计划任务，登录时自启后台服务。
- **自启机制**：软件优先使用「登录计划任务」而非注册表 Run 键。

## 二、实施要点与关键技术

1. **判断「是否真坏了」要先看后台服务**：GUI 托盘可能崩溃，但只要 `AutoDarkModeSvc.exe` 在跑，主题切换就正常。
2. **排查三步走**：
   - 进程：`Get-Process -Name "AutoDarkMode*"`；
   - 计划任务：`Get-ScheduledTask -TaskName "ADM Logon"`；
   - 崩溃日志：`Get-EventLog -LogName Application -Source "Application Error"`。
3. **崩溃特征识别**：本次崩溃码 `0xe0434352`、崩在 `KERNELBASE.dll` 同一地址，说明是 .NET 运行时异常，不是随机硬件问题。
4. **升级优先于重装**：同版本重装大概率复现崩溃；升级到 11.x 通常能修复已知 .NET 异常，且配置可保留。

## 三、模块职责划分

| 组件 | 职责 | 故障影响 |
|---|---|---|
| AutoDarkModeSvc.exe | 实际切换主题 | 若未运行，主题完全不切换 |
| ADM Logon 计划任务 | 登录时拉起后台服务 | 丢失则开机不自动启动 |
| AutoDarkModeApp.exe | 提供 GUI 托盘和设置界面 | 崩溃不影响主题切换 |
| 注册表 Run 键 | 旧版自启方式 | 被软件清理后改用计划任务 |

## 四、如何选型（方法论）

- 如果只需要「按时间自动切换深浅色」：ADM 后台服务足够，不必纠结 GUI 托盘。
- 如果需要频繁手动改设置/看状态：建议升级到 11.x 修掉 GUI 崩溃。
- 替代方案评估：
  - Windows 自带「自动切换主题」：功能弱，只能按日落到日出；
  - NightOwl / Windows 10 自带：功能单一；
  - ADM 仍是 Windows 下最灵活的主题调度器。

## 五、深化学习指引

- **Auto Dark Mode 官方仓库/GitHub Releases**：https://github.com/AutoDarkMode/Windows-Auto-Night-Mode（T0，一手来源）
- **崩溃码 0xe0434352 解读**：.NET 托管异常通用码，可在 Event Viewer 查看详细堆栈（T1，Windows 官方文档/社区）
- **计划任务管理**：`Get-ScheduledTask` / `schtasks` 官方文档（T1）
- **推荐 UP/博主**：搜索「Auto Dark Mode 设置教程」「Windows 自动深色模式」，注意版本号，优先 2025 年后内容。

## 六、技术结合点（1+1>2）

- **ADM + PowerShell 自动化**：用 `Set-ItemProperty` 改注册表主题键，配合 ADM 的时间规则做更复杂的场景切换。
- **ADM + 屏幕色温工具（如 f.lux、Windows 夜间模式）**：晚上自动切深色 + 降蓝光，白天自动切浅色 + 高亮。
- **ADM + 工作流自动化**：深浅色切换可作为触发器，联动壁纸、IDE 主题、浏览器扩展主题切换。
- **故障排查 SOP 可复用**：「进程→计划任务→事件日志」三板斧适用于任何 Windows 自启软件异常。
