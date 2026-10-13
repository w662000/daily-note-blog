---
layout: default
title: 交接文档 · MSYS _ Windows 路径与工具速查
date: 2026-10-13 23:30:00 +0800
---

# MSYS / Windows 路径与工具速查

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\productivity\disk-audit-clean\references\msys-path-tricks.md

## 路径映射

| Windows 原生 | MSYS / bash | 说明 |
|---|---|---|
| `C:\Users\Administrator` | `/c/Users/Administrator` | 必须带 `/c/` 前缀 |
| `C:\Windows\Temp` | `/c/Windows/Temp` | 同上 |
| `D:\AI work\workbuddy` | `/d/AI work/workbuddy` | 盘符转 `/盘符字母/` |
| `C:\Users\Administrator\Desktop` | `/c/Users/Administrator/Desktop` | |

## 工具用法（MSYS 下）

| 操作 | 命令 | 说明 |
|---|---|---|
| 列出目录大小 | `du --max-depth=1 -h <path> \| sort -rh` | 注意 `--max-depth` 不是 `-d` |
| 递归总大小 | `du -sh <path>` | |
| 数文件 | `find <path> -type f \| wc -l` | |
| 搜目录 | `find <path> -type d -name "__pycache__"` | |
| 列文件 | `ls -lh <path>` | 带人类可读大小 |
| 跨目录找 | `find /c/Users -name "Crashpad" -type d` | |

## 常见错误

- `ls: cannot access '/Users/...'` → 忘了 `/c/` 前缀
- `du: invalid option -- 'd'` → MSYS 用 `--max-depth` 不是 `-d`
- `bash: -c: unexpected EOF` → 用 heredoc 写 HTML 时 `>` 被当作重定向
- ACL 拒绝 → 某些系统目录 `find` 进不去，降级用 `ls` 探

## Python 落盘

```python
from pathlib import Path
Path(r"C:\Users\Administrator\Desktop\report.html").write_text(html, encoding="utf-8")
```

execute_code 的 `/tmp` 是沙箱隔离的，无法从 terminal 访问。要落盘到 Windows 用绝对路径。
