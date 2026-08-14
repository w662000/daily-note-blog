---
layout: default
title: 技术点 · 用户级 Skill 清单 v1.5（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单 v1.5（~_.workbuddy_skills）

> 来源：交接文档《用户级 Skill 清单 v1.5（~/.workbuddy/skills）》（2026-08-14）

---

## 一、技术选型

v1.5 要解决：彻底消除财富自由系列 6 个 skill 的磁盘双份，使清单与磁盘都达到 name 去重后无重复。

选型结论：
- **删除顶层重复目录**：`fw01-wealth-freedom-definition`、`fw05-abandon-safety`、`fw13-investment-risk-aversion`、`p05-safety-is-shackle`、`p27-prediction-impossible`、`p45-execution-cognition` 的顶层独立副本。
- **保留内嵌副本**：`cangjie-skill/books/caifuziyouzhilu/` 内的副本继续保留。
- **结果**：磁盘目录由 50 → 44；name 重复由 6 → 0；独立 skill 为 44 个（23 个共建 + 21 个其余）。
- **备份**：整目录备份至 `~/.workbuddy/skills_trash/wealth-dup-top6_20260814_225311/`。

---

## 二、实施要点与关键技术

1. **连根拔起脏数据**：不仅清单里不显示重复，源文件也要删除，否则下次扫描又会冒出来。
2. **整目录备份**：6 个顶层目录一起移入 trash，便于一次性回滚。
3. **明确保留策略**：决定保留 `cangjie-skill` 内嵌副本，因为它们是书籍拆书体系的组成部分。
4. **重新统计口径**：磁盘目录数、独立 name 数、共建/其余数三者口径要一致。
5. **版本变更说明**：清晰写出 v1.4→v1.5 删除的是哪 6 个顶层目录。

---

## 三、模块职责划分

| 模块 | 职责 | 输出 |
|---|---|---|
| 重复定位模块 | 识别 6 个顶层重复目录 | 待删除路径列表 |
| 备份模块 | 整目录移入 skills_trash | 备份目录 |
| 删除模块 | 删除顶层 6 个目录 | 干净的 skills 目录 |
| 清单重生成器 | 重新扫描并输出无重复清单 | v1.5 Markdown |

---

## 四、如何选型（方法论）

1. **脏数据要连根拔**：只改展示层是绕过，必须删源 + 改采集器 + 堵兜底。
2. **先备份再删除**：批量删除目录前先整体归档。
3. **保留策略要说明**：为什么选择保留内嵌副本、删除顶层副本，要给理由。
4. **重跑扫描验证**：删除后必须重新扫描，确认 name 去重后无重复。

---

## 五、深化学习指引

| 方向 | 推荐来源 | 可信度 |
|---|---|---|
| cangjie-skill 拆书体系 | `cangjie-skill/books/caifuziyouzhilu/` 目录结构 | T0（一手） |
| WorkBuddy skill name 去重规则 | workbuddy-asar-inspect 分析结果 | T1 |
| 批量文件操作安全 | windows-launcher-safety skill | T0（用户级） |

---

## 六、技术结合点（1+1>2）

- **v1.5 + cangjie-skill skill**：保留内嵌副本后，继续用拆书体系维护财富自由系列。
- **v1.5 + workbuddy-asar-inspect skill**：验证删除顶层副本后，WorkBuddy 加载的 skill 列表是否正确。
- **v1.5 + tri-agent-investigation skill**：调查「为何最初会出现顶层与内嵌双份」的根因，防止再次产生。
- **v1.5 + task-implement skill**：把「扫描重复→备份→删除→验证」做成可复用自动化任务。
