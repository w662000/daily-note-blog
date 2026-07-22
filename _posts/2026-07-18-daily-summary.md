---
layout: default
title: 每日工作总结 · 2026-07-18
date: 2026-07-18 23:30:00 +0800
---

# 每日工作总结 · 2026-07-18

## 一、今日完成事项
- **彻底关闭 Windows 10 强制更新**（用户环境：Win10 专业版 22H2 19045，管理员账户）。
- 采用三层防护，全部执行并验证通过：
  1. **服务层**：禁用 wuauserv / UsoSvc / bits / **WaaSMedicSvc**（更新医生服务，受 SYSTEM 保护，靠夺取注册表所有权 + 改 Start=4 才搞定）。
  2. **注册表策略**：NoAutoUpdate=1、锁定版本 TargetReleaseVersionInfo=22H2、禁用驱动更新等组策略级键值。
  3. **计划任务**：禁用 WindowsUpdate / UpdateOrchestrator / WaaSMedic 三个目录下共 15 项任务（受保护任务靠夺取 `C:\Windows\System32\Tasks` 文件所有权后禁用）。
- 附带清理开始菜单"更新并关机"黄点（清理 DataStore + 刷新状态），用户重启后确认黄点消失。

## 二、关键决策 / 注意事项
- **核心突破**：只禁用 wuauserv 没用，WaaSMedicSvc 会自动恢复更新服务——必须先制服它。
- **大版本升级已锁**：TargetReleaseVersion 阻止 22H2→23H2 等功能更新。
- **受保护对象处置套路**（可复用）：服务报"拒绝访问"→ 夺取 `HKLM:\SYSTEM\CurrentControlSet\Services\<svc>` 注册表所有权改 Start=4；计划任务报拒绝访问 → takeown + icacls 夺 `Tasks\...` 文件所有权再 Disable。

## 三、生成的有用文件
| 文件 | 路径 | 用途 |
|---|---|---|
| 恢复更新脚本 | `D:\AI work\workbuddy\2026-07-18-19-00-53\恢复更新-restore-update.ps1` | 一键重新开启 Windows 更新（将来需要时） |

## 四、待办 / 风险
- 无未决项。若将来需重开更新，运行上面的 ps1 即可。
