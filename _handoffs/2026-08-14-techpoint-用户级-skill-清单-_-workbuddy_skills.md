---
layout: default
title: 技术点 · 用户级 Skill 清单（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单（~_.workbuddy_skills）

> 来源：交接文档《用户级 Skill 清单（~/.workbuddy/skills）》（2026-08-14，v1.0 基线版）

---

## 一、技术选型

本项目要解决：清晰盘点 `~/.workbuddy/skills` 目录下到底有多少个用户级 skill，其中哪些是模型与用户共建的，哪些来自市场/预装/第三方。

选型结论：
- **扫描对象**：`~/.workbuddy/skills/` 下所有 skill 目录（剔除 `node_modules` 依赖）。
- **判定标准**：以 `SKILL.md` frontmatter 中的 `agent_created: true` 作为「我参与制定」的客观依据。
- **输出形式**：Markdown 表格，分「我参与制定」与「其余」两张表。
- **基线结果**：共 51 个用户级 skill，其中 15 个 agent_created=true。

---

## 二、实施要点与关键技术

1. **目录扫描**：递归遍历 skills 目录，识别有效的 skill 根目录。
2. **node_modules 剔除**：Playwright 等依赖目录会被误识别，必须过滤。
3. **frontmatter 解析**：读取 `SKILL.md` 头部 YAML，提取 `agent_created` 标记。
4. **版本与说明提取**：从 frontmatter 读取 `version` 和 `description`。
5. **客观判定**：不凭印象，只看 `agent_created` 标记，避免把市场安装的 skill 误归为共建。

---

## 三、模块职责划分

| 模块 | 职责 | 输出 |
|---|---|---|
| 目录扫描器 | 遍历 skills 目录，定位 SKILL.md | 候选 skill 路径列表 |
| frontmatter 解析器 | 读取 agent_created、version、description | 结构化元数据 |
| 分类器 | 按 agent_created 分成两类 | 两张 Markdown 表 |
| 报告生成器 | 汇总统计并写入 handoff | Markdown 清单文档 |

---

## 四、如何选型（方法论）

1. **盘点前先定规则**：什么是「我的」、什么是「别人的」，必须有客观字段，不能靠感觉。
2. **用 frontmatter 说话**：`agent_created: true` 是 WorkBuddy SkillManage 的规范标记，可信度最高。
3. **过滤依赖噪音**：`node_modules` 里的同名目录必须排除。
4. **保留原始路径**：对于嵌套 skill（如 cangjie 书籍子 skill），按磁盘真实路径列出，便于后续去重。
5. **版本化迭代**：基线清单出来后再逐步补进用户确认的遗漏项。

---

## 五、深化学习指引

| 方向 | 推荐来源 | 可信度 |
|---|---|---|
| WorkBuddy Skill 管理规范 | SkillManage / skill-creator skill 文档 | T0 |
| SKILL.md frontmatter 字段 | WorkBuddy 官方 skill 规范 | T0 |
| Python frontmatter 解析 | python-frontmatter 库官方文档 | T1 |
| SkillHub 市场技能来源 | SkillHub 官方 API / 作者页 | T1 |

---

## 六、技术结合点（1+1>2）

- **本清单 + skillhub-daily skill**：每日扫描 SkillHub 新 skill，与本清单对比，发现值得安装或研究的增量。
- **本清单 + workbuddy-asar-inspect skill**：对内置 skill 的加载机制做逆向分析，确认用户级 skill 的优先级与覆盖规则。
- **本清单 + tri-agent-investigation skill**：对来源不明的第三方 skill 做安全审计后再启用。
- **本清单 + cangjie-skill skill**：对「拆书」类子 skill 做系统化整理与版本归档。
