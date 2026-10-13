---
layout: default
title: 交接文档 · 批量落盘护栏（Safe Bulk Write Guardrail）
date: 2026-10-13 23:30:00 +0800
---

# 批量落盘护栏（Safe Bulk Write Guardrail）

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\safe-bulk-write-guardrail\SKILL.md

---
name: safe-bulk-write-guardrail
description: 批量落盘护栏。任何会写大量文件/临时目录的脚本任务都应加载本技能并走 safe_write 护栏，防静默产垃圾文件。
agent_created: true
---

# 批量落盘护栏（Safe Bulk Write Guardrail）

## Overview

把「静默产垃圾文件」在代码层面变成不可能。任何会写大量文件、写临时/隐藏目录的
脚本，都应走 `scripts/safe_write.py` 的护栏，而不是随手 `open/write`。
等价于把「垃圾文件罚款」写进代码：生成前就中止，而非事后审计。

## 何时加载本技能

- 要写脚本**批量生成**文件（handoff、文档、缓存、导出、拆分产物等）
- 脚本会产生**临时目录 / 中间产物**（翻译、转换、爬取暂存）
- 过去出现过「某 agent 静默往磁盘 dump 几百个文件用户毫不知情」类事故
- 给用户任何会落盘的任务收尾时，需要默认带「📁 落盘清单」

**不要做的事**：只写一个独立「磁盘体检脚本」去事后数垃圾——那是审计，不改行为。
护栏要写进产垃圾的代码路径本身。

## 护栏五原则（guarded_bulk_write 强制执行）

1. **隐藏目录拒绝**：输出路径任意段以 `.` 开头（`.archive_*` / `.bad_v1`）→ 直接拒绝落盘
2. **数量硬上限**：handoff 类 `HANDOFF_CEILING=72`，其它 `DEFAULT_CEILING=200`；
   超过且无 `force=True` → `sys.exit` 中止并报「粒度/数量爆炸防护」
3. **落盘前确认**：默认需交互 `y` / 环境变量 `SAFE_WRITE_YES=1` / 命令行 `--yes`
4. **临时目录自清理**：`SelfCleaningTemp` 上下文管理器，`with` 退出即 `rmtree`
5. **落盘后明细**：打印新建数 + 跳过数 + 绝对路径

## Quick Start

把 `scripts/safe_write.py` 放到脚本同目录或 `PYTHONPATH`，导入使用：

```python
import sys
sys.path.insert(0, r"技能目录/scripts")
from safe_write import guarded_bulk_write, SelfCleaningTemp, HANDOFF_CEILING

# 1) 批量写 handoff（带 72 硬上限 + 隐藏目录拒绝）
guarded_bulk_write(
    docs, out_dir,
    ceiling=HANDOFF_CEILING,
    name_fn=lambda d: f"{d[0]}_{safe_name(d[1])}_handoff",
    content_fn=lambda d: d[2],
    label="handoff",
)

# 2) 临时目录自清理（翻译/转换中间产物走这里，跑完即删）
with SelfCleaningTemp() as tmp:
    write_temp(tmp, "x.body.md", body)
# 退出 with 后 tmp 自动删除并打印清理明细
```

阈值（`HANDOFF_CEILING` / `DEFAULT_CEILING`）按各项目红线调整，不要写死成全局大数。
`guarded_bulk_write(..., force=True)` 仅在确属必要时显式放行（仍打印明细）。

## 真实事故与修复（必读，给学习 agent）

详见 `references/real_fixes.md`：记录 2026-08-16 一次静默产 **2497 个文件**
（682 篇 handoff + 1752 个翻译中间产物 + 62 个坏版本）的真实根因与用本护栏的修复方式。
核心教训：**根因不是「生成错了」，而是「只干不说 + 无结构护栏」**——检查脚本治标，
把护栏写进产垃圾的代码路径才治本。

## 配套行为红线（落到 agent 本人，非代码）

代码护栏管「脚本路径」，以下管「agent 随手写文件」路径，两道一起才封死：

- 批量落盘（≥20 文件 / 生成中间产物目录 / 往隐藏或散落位置 dump）**先报计划征得确认**
- 写完**打印精确清单**（绝对路径 + 数量），用户不派 agent 也能看见动了磁盘哪
- 临时文件集中到单一 `tmp/` 并收尾清理
- 删脏数据「连根拔」，个人文件不得自动 `-rf`

## Resources

### scripts/
- `safe_write.py` — 核心护栏库（纯标准库，无外部依赖）。含 `guarded_bulk_write`、
  `SelfCleaningTemp`、`HANDOFF_CEILING`、`DEFAULT_CEILING`、`is_hidden`。
  自带 `__main__` 自测：模拟 100>72 应被拦截。

### references/
- `real_fixes.md` — 真实事故（2497 文件）根因 + 三处修复 before/after + 配套红线。
