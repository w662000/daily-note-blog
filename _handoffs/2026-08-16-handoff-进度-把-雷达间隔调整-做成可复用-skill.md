---
layout: default
title: 交接文档 · 进度 · 把「雷达间隔调整」做成可复用 skill
date: 2026-08-16 23:30:00 +0800
---

# 进度 · 把「雷达间隔调整」做成可复用 skill

- **日期**：2026-08-16
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-16-10-57-55\进度_20260816_1920_雷达skill.md

> 生成时间：2026-08-16 19:20 ｜ 状态：✅ 已完成并端到端实测通过

## 交付物

| 项 | 路径 |
|---|---|
| skill 目录 | `C:\Users\Administrator\.workbuddy\skills\radar-interval-tune\` |
| 说明 | `SKILL.md`（含触发词 description、两雷达硬事实表、坑清单） |
| 核心脚本 | `scripts\set_radar_interval.py` |
| 打包产物 | `C:\Users\Administrator\.workbuddy\skills\dist\radar-interval-tune.zip` |
| 校验 | `package_skill.py` → ✅ Skill is valid |

## 触发词（说出即自动加载）

- 中文：雷达间隔 / 改雷达间隔 / 雷达调频 / 测速间隔 / 测限流间隔 / 雷达多久跑一次 / 雷达状态 / 雷达没跑 / 重启雷达 / 雷达 daemon / 雷达工作目录
- 英文：radar interval / restart radar / radar status

## 命令速查

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
S="C:/Users/Administrator/.workbuddy/skills/radar-interval-tune/scripts/set_radar_interval.py"

"$PY" "$S" --status                          # 只读查状态（配置值+PID+日志实证）
"$PY" "$S" --radar speed --hours 1            # 测速改1小时（改+重启+验证）
"$PY" "$S" --radar ratelimit --hours 2        # 测限流改2小时
"$PY" "$S" --radar both --hours 1 2           # 两个一起改
"$PY" "$S" --radar speed --hours 6 --no-restart   # 只改配置不重启
"$PY" "$S" --radar speed --seconds 300 --force     # 越过安全下限（有限流风险）
```

## 两雷达硬事实（脚本内置）

| | 测速雷达 speed | 测限流雷达 ratelimit |
|---|---|---|
| 目录 | `D:\AI work\workbuddy\model-speed-radar` | `D:\AI work\workbuddy\model-rate-limit-radar` |
| 端口 | 8848 | 8849 |
| daemon | speed_daemon.py | ratelimit_daemon.py |
| daemon.log | 项目目录 `logs\daemon.log` | **`~\.cache\rate-limit-radar\logs\daemon.log`** |
| 日志关键字 | 测速间隔 | 扫描间隔 |
| 安全下限 | 600 秒 | 1800 秒 |
| 当前值 | 3600（1h） | 7200（2h） |

## 端到端实测记录

1. `--status` ✅ 正确读出两雷达配置值、PID（8848/2860、8849/9288）、日志实证行。
2. `--radar speed --hours 1`（值保持不变，仅验重启链路）✅
   - 停旧 PID 4396 → 端口释放 → 起新 PID 2860 → 端口监听
   - 日志实证 `[2026-08-16 19:19:45]   测速间隔 : 3600 秒（1.0 小时）`
3. 安全下限拒绝 `--seconds 300` ✅
   - 打印拒绝原因、退出码 1、**config 仍 3600 未被篡改、8848 进程未被误杀**
4. 全程未触碰测限流雷达（PID 9288 保持运行）。

## 设计要点（三个已实测坑，改脚本时勿破坏）

1. **Bash 不能调 `cmd.exe`**（WB 安全策略拦截）→ `start.bat`/`stop.bat` 走不通，改用 Python 管进程。
2. **PowerShell `Start-Process -ArgumentList` 不给含空格路径加引号** → `D:/AI work/...` 被截成 `D:/AI`，pythonw 报 SyntaxError（上一轮真实翻车，daemon 被杀却拉不起来）。Python `subprocess.Popen([py, script])` 列表传参天然安全。
3. **测限流雷达 daemon.log 不在项目目录**（`LOG_DIR = ~/.cache/rate-limit-radar/logs`）→ 去项目 `logs/` 找间隔行会误判"没生效"。

附：PowerShell 工具本机常不回显 stdout，故验证一律用「Python 自打印 + netstat 端口 + 读 daemon.log」三件套。

## 记忆固化

- user 级 `~/.workbuddy/MEMORY.md`：两个雷达条目均补「调间隔一律用 radar-interval-tune skill」+ 补测限流 daemon.log 真实位置。
- 项目日志 `2026-08-16.md`：追加「19:20 固化雷达间隔 skill」一节。
