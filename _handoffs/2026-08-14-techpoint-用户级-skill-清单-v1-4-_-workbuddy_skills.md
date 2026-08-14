---
layout: default
title: 技术点 · 用户级 Skill 清单 v1.4（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单 v1.4（~_.workbuddy_skills）

> 来源：交接文档《用户级 Skill 清单 v1.4（~/.workbuddy/skills）》（2026-08-14）

---

## 一、技术选型

v1.4 要解决：`agent-reach` skill 目录已被删除，清单仍将其列为「我参与制定」，造成脏数据；同时 `cangjie-skill` 财富自由系列存在磁盘双份，需标记重复。

选型结论：
- **删除失效 skill**：移除 `agent-reach`，我参与制定由 24 减为 23，用户级总数由 51 减为 50。
- **重复标记**：对 `cangjie-skill` 内嵌与顶层双份存在的 6 个财富自由系列 skill，在「其余」表标注「⚠重复」。
- **目录真实状态**：按磁盘实际目录列出 50 行，其中 6 行重复。
- **备份**：`agent-reach` 已移至 `~/.workbuddy/skills_trash/agent-reach_20260814_2235/`。

---

## 二、实施要点与关键技术

1. **扫描前校验目录存在性**：不能只看 name，必须确认目录是否仍在磁盘上。
2. **trash 机制**：删除 skill 目录前先移动到 skills_trash，而不是直接 rm -rf。
3. **重复检测**：按 `name` 聚合，发现同名多路径即标注重复。
4. **去重前透明披露**：在清单中明确说明重复是磁盘真实状态，不是清单 bug。
5. **版本差异清晰**：列出 v1.3→v1.4 的删除项与重复项。

---

## 三、模块职责划分

| 模块 | 职责 | 输出 |
|---|---|---|
| 目录存在性校验 | 过滤已删除 skill | 有效目录列表 |
| 重复检测器 | 按 name 聚合多路径 | 重复标记表 |
| trash 归档模块 | 把删除目录移入 skills_trash | 可回滚备份 |
| 清单重生成器 | 输出 50 行含重复标记的表 | v1.4 Markdown |

---

## 四、如何选型（方法论）

1. **清单必须与磁盘一致**：不能列出已删除的 skill，否则就是脏数据。
2. **删除先归档**：个人文件操作先移 trash，给用户二次确认机会。
3. **重复不能自动合并**：需先披露，由用户决定保留哪一份。
4. **总数口径说明**：磁盘目录数、name 去重后独立数要分开说明。

---

## 五、深化学习指引

| 方向 | 推荐来源 | 可信度 |
|---|---|---|
| WorkBuddy skill 加载规则 | 官方文档 / workbuddy-asar-inspect 分析 | T0/T1 |
| 文件删除安全实践 | windows-launcher-safety skill 自查清单 | T0（用户级） |
| 去重算法实现 | Python collections.defaultdict / pandas | T1 |

---

## 六、技术结合点（1+1>2）

- **v1.4 + workbuddy-asar-inspect skill**：分析 WorkBuddy 加载 skill 时是否按 name 去重，验证「独立 skill 为 44 个」的结论。
- **v1.4 + gentle-ratelimit-test skill**：如批量调用 SkillHub API 校验 skill 状态，需温和测试避免限流。
- **v1.4 + tri-agent-investigation skill**：对「name 重复时 WorkBuddy 保留哪一份」做三方调查。
- **v1.4 + todolist skill**：把「删除顶层重复 6 个 skill」加入待办，等待用户确认后执行。
