---
layout: default
title: 技术点 · loomy2api 网关双开修复（2026-10-13 21:40）
date: 2026-10-12 23:30:00 +0800
---

# 技术点 · loomy2api 网关双开修复（2026-10-13 21:40）

> 来源：261012_loomy2api 网关双开修复（2026-10-13 21_40）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：2026-10-12-11-05-04\loomy2api\进度_20261013_2140_网关双开修复.md
- 21:20 模型测速时, 全部 [Loomy] 路由模型报 `Remote end closed`；本次排查发现 17890 上有 **两个** `pythonw.exe` 同时 LISTENING（PID 6492/11708）。
- `/health` 实测连发 5 次全 `curl exit 52 Empty reply`（TCP 能连, 但服务器零字节回）→ 网关对客户端等于「假死/没启动」。
- `server.py` 的 `main()` 直接 `ThreadingHTTPServer((host,port),Handler).serve_forever()`, **无单实例/端口锁**。
- 这正是 10-12 修复文档(1155)自己警告过的「Windows SO_REUSEADDR 会让旧进程占端口」。
- 触发双开的原因: 启动文件夹 `loomy2api-AutoStart.vbs`(登录自启) 与某次手动启动叠加。启动链: Startup\loomy2api-AutoStart.vbs → start_silent.vbs → `pythonw server.py`（不经过 .bat）。
- pidfile 锁 `.loomy2api.pid`：已存在且 PID 存活→视为已有实例, `sys.exit(0)`；PID 已死→清理陈旧 pidfile。
- 端口探测：若 `host:port` 已能连通→视为已有实例在跑, 主动退出, 不再重复 bind。
- 2. **start_silent.bat 改幂等**：启动前 `netstat | findstr :17890`, 已监听则跳过, 防手动双开。
- 3. 启动链 `.vbs` 不经过 `.bat`, 故核心防线在 server.py（覆盖所有启动路径）。
- `taskkill /F /PID 6492 /PID 11708` 杀掉两个僵死实例 → 端口释放。
- 干净起一个实例: 本 agent 会话内以 `python.exe` 后台任务(PID 14112)托管（因本环境下 `start pythonw` 会被沙箱回收, run_in_background 才能存活）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
