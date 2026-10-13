---
layout: default
title: 交接文档 · 磁盘体检与清理（Disk Audit & Clean）
date: 2026-10-13 23:30:00 +0800
---

# 磁盘体检与清理（Disk Audit & Clean）

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\productivity\disk-audit-clean\SKILL.md

---
name: disk-audit-clean
description: 全盘扫描/体检 C 盘或工作区，按 🟢安全 🟡谨慎 🔴不可清 三档分级，产出 HTML 体检报告到桌面，再经用户确认执行清理。适用于"磁盘体检"、"垃圾文件扫描"、"清理 C 盘/Downloads/AppData 缓存"、"只读审计后再删"等任务。触发：用户要求扫盘、清理空间、给磁盘体检报告、"自己清掉垃圾"。
agent_created: true
---

# 磁盘体检与清理（Disk Audit & Clean）

## Overview

按三档分级只读审计整个 C 盘或工作区，产出 HTML 报告到桌面，再经用户确认执行清理。
核心规矩：**只读扫描 → 分级 → 报告 → 用户确认 → 执行 → 打印落盘清单**。
未确认前，任何一个文件都不许动。

## 用户规矩（来自 real-world 对话）

- **读前必问：这不是我创建的文件能删吗？** 原则：
  - ❌ 不动：用户的个人数据（Downloads/Documents/Pictures/项目代码/.workbuddy 核心 / .hermes / 各 AI 助手目录）
  - ❌ 不动：系统文件（.sys / INF / 驱动 / pagefile / swapfile / Windows 核心）
  - ✅ 可清：系统/工具**自行管理的运行时缓存**（npm-cache / pip-cache / Temp / panther / WebCache / Crashpad / 浏览器子缓存 / WebCache / panther）。这些不是"你的文件"，是系统自己 dump 又会自动重生的缓存，删除等价 Windows 磁盘清理。
  - ⚠️ 谨慎：会破坏依赖的（ms-playwright / 浏览器主 Default 会话），需先问用户是否仍使用
- **用户确认方式**：给出三档清单后，用户回数字序号（如"1"）确认要执行那一档
- **HTML 报告**：存 `C:/Users/Administrator/Desktop/盘体检报告.html`，三档分色（🟢=绿 #3fb950，🟡=黄 #d29922，🔴=红 #f85149）

## 工作流程

### 阶段 1：只读扫描

用 MSYS 工具（**不是 PowerShell**），分块并行扫：

```bash
WS=/c/Users/Administrator   # 注意 /c/ 前缀
du --max-depth=1 -h $WS 2>/dev/null | sort -rh | head -30
du --max-depth=1 -h /c/Windows/Temp /c/Windows/Logs /c/Windows/panther /c/Windows/INF 2>/dev/null
find $WS -maxdepth 1 -name ".*" -type d 2>/dev/null | while read d; do
  sz=$(du -sh "$d" 2>/dev/null | cut -f1)
  echo "  $sz  $d"
done | sort -rh
```

**必扫目录（Windows 常见垃圾区）：**
- `C:\Users\<user>\AppData\Local\Temp` — 用户临时，最大垃圾源
- `C:\Users\<user>\AppData\Local\npm-cache` — npm 缓存（可 npm cache clean）
- `C:\Users\<user>\AppData\Local\Pip\cache` — pip 缓存
- `C:\Users\<user>\.cache` — 各工具缓存（selenium/cargo/...）
- `C:\Windows\Temp` / `C:\Windows\panther` / `C:\Windows\Logs` / `C:\Windows\INF`
- 各浏览器 `Cache` / `GPUCache` / `GrShaderCache` / `Crashpad`
- 各应用的 `Crashpad`（崩溃转储）
- 工作区旧日志（按日期目录，保留近 7 天）

### 阶段 2：三档分类

| 档位 | 含义 | 例子 |
|---|---|---|
| 🟢 安全可清 | 删除后自动重生，无功能损失 | npm/pip/Temp/panther/浏览器子缓存/Crashpad/旧日志 |
| 🟡 谨慎可清 | 删了依赖失效，需用户判断是否仍使用 | ms-playwright、浏览器主 Default、工作区 traces/blobs |
| 🔴 不可清 | 用户数据/程序本体/系统文件 | Downloads、.hermes、各 AI 助手目录、pagefile.sys |

### 阶段 3：产出 HTML 报告

- 存 `C:/Users/Administrator/Desktop/盘体检报告.html`
- 用 `execute_code` + `Path.write_text(...)`（**不要用 bash heredoc 写 HTML**，`>` 会触发 bash 语法错误）
- 三档分色表格，每档一个小计行
- 顶部四张卡片：总占用 / 🟢 / 🟡 / 🔴 数字
- 报告底部：规矩回顾 tip

### 阶段 4：用户确认 → 执行

- 等用户回数字序号（如"1"= 只清 🟢）
- 执行前打印精确待删清单（路径 + 大小 + 文件数）
- 执行时跳过明显敏感目录（如 mise 管理的 Python 解释器内部）
- 执行后打印落盘清单（删除 X 个文件，释放 Y MB）

### 阶段 5：落盘清单

每次删除操作后必须打印：绝对路径 + 数量 + 大小 + 跳过项说明。

## 关键陷阱（real-world 已踩）

### 1. MSYS 路径是 `/c/Users/...`，不是 `/Users/...`
```bash
# ✅ 正确
WS=/c/Users/Administrator
# ❌ 错误
WS=/Users/Administrator   # No such file or directory
```

### 2. `du` 用 `--max-depth`，不用 `-d`（MSYS GNU coreutils 用法）
```bash
du --max-depth=1 -h /c/Users/Administrator
```

### 3. bash heredoc 不能写 HTML
HTML 里的 `>` 会被 bash 当成重定向。改用 `execute_code` + `Path.write_text()`。

### 4. Python 三引号 raw string 不能含 `\U` 字符
HTML 里如果出现 `\U` 会被 Python 当成 unicode escape。用 `r"""..."""` 前缀。

### 5. /tmp 在 execute_code 沙箱里，与终端隔离
沙箱写的 /tmp 文件无法被 terminal 访问。要落盘到桌面用 `Path(r"C:\Users\Administrator\Desktop\...")`。

### 6. ACL 限制：某些系统目录 `ls` 能进、`find` 进不去
用 `ls -la` 探目录、`find` 数文件；如果 `find` 报错就降级用 `ls` 逐层数。

## 配套技能

- `safe-bulk-write-guardrail` — 代码级护栏，防止脚本静默产垃圾。本技能管"事后清理"，那个管"事前防呆"，两道一起封死。

## References

- `references/msys-path-tricks.md` — MSYS/Windows 路径与工具使用速查
