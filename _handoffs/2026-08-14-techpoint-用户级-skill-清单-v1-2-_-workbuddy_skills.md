---
layout: default
title: 技术点 · 用户级 Skill 清单 v1.2（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单 v1.2（~_.workbuddy_skills）

> 来源：交接文档《用户级 Skill 清单 v1.2（~/.workbuddy/skills）》（2026-08-14）

---

## 一、技术选型

v1.2 要解决：v1.1 只补了 3 个手动 skill，用户进一步指出还有 6 个共建 skill 未纳入。

选型结论：
- **手动补进扩展 6 个**：`cf-58-scraper-replicate`、`forum-handoff-publisher`、`glm-41v-visual-transcribe`、`skillhub-daily`、`todolist`、`wechat-mp-crawler-cookie-fix`。
- **我参与制定总数**：由 18 个增至 24 个。
- **其余 skill 数**：由 33 个减至 27 个。
- **判定规则不变**：仍以 `agent_created=true` 自动 + 用户手动确认。

---

## 二、实施要点与关键技术

1. **逐行核对**：按用户指出的行号（3/5/12/27/31/33 行）逐一确认并补进。
2. **触发词提取**：为补进的 skill 从各自 `SKILL.md` 提取用途说明，保持表格结构一致。
3. **去重意识**：部分 skill 在不同路径有双份存在，清单按磁盘目录列出，但需标注重复来源。
4. **版本差异透明**：明确列出 v1.1→v1.2 新增的 6 个 skill。

---

## 三、模块职责划分

| 模块 | 职责 | 输出 |
|---|---|---|
| 用户反馈接收 | 记录用户指出的遗漏行号 | 待补进列表 |
| skill 信息补全 | 读取对应 SKILL.md 的 description | 6 条补进记录 |
| 分类重算 | 重新统计「我参与制定」与「其余」 | 24 + 27 两张表 |
| 差异说明 | 输出版本变更日志 | v1.1→v1.2 差异 |

---

## 四、如何选型（方法论）

1. **建立反馈闭环**：用户说漏了哪行，立刻核对、确认、补进。
2. **保留行号索引**：在核对阶段引用原表行号，避免找错。
3. **信息来源真实**：补进的用途说明必须取自对应 SKILL.md，不编造。
4. **提前识别重复**：扫描阶段就要发现同名不同路径的 skill，避免统计口径混乱。

---

## 五、深化学习指引

| 方向 | 推荐来源 | 可信度 |
|---|---|---|
| 各补进 skill 的 SKILL.md | `cf-58-scraper-replicate` 等 6 个目录 | T0 |
| 用户反馈驱动的清单维护 | 本次 handoff 的迭代记录 | T0（一手） |
| SkillHub 市场安装记录 | `~/.workbuddy/skills/` 磁盘状态 | T0 |

---

## 六、技术结合点（1+1>2）

- **v1.2 + forum-handoff-publisher skill**：本清单的发布流程正是用该 skill 把 handoff 批量发到论坛。
- **v1.2 + skillhub-daily skill**：该 skill 每日扫描 SkillHub，可作为清单增量来源。
- **v1.2 + wechat-mp-crawler-cookie-fix skill**：如清单需补充公众号文章类 skill，可复用其排障经验。
- **v1.2 + tri-agent-investigation skill**：对补进来源做快速三方核验，确保不是误把市场 skill 当共建。
