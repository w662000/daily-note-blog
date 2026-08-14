---
layout: default
title: 技术点 · 用户级 Skill 清单 v1.3（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单 v1.3（~_.workbuddy_skills）

> 来源：交接文档《用户级 Skill 清单 v1.3（~/.workbuddy/skills）》（2026-08-14）

---

## 一、技术选型

v1.3 要解决：把手动补进的 9 个 skill 永久化，并增加触发词信息，让清单真正反映 skill 的调用入口。

选型结论：
- **永久化 agent_created**：把 9 个手动补进 skill 的 `SKILL.md` 写入 `agent_created: true`。
- **新增「触发词」列**：从各 SKILL.md 提取真实触发词或语义触发说明。
- **备份机制**：修改前均备份为 `SKILL.md.bak-agent_created-20260814_223000`。
- **结果**：24 个「我参与制定」skill 全部有客观标记。

---

## 二、实施要点与关键技术

1. **frontmatter 修改**：在不破坏原有 YAML 结构的前提下追加 `agent_created: true`。
2. **触发词提取规则**：
   - 优先取 frontmatter 的 `triggers:` 列表；
   - 其次取 description 中「触发词：」子串；
   - 再次取「当用户说「X」」引号内容；
   - 最后取「当用户…时」整句；
   - 都没有则标注「按需求描述语义触发」。
3. **安全备份**：修改前先复制 `.bak` 文件，支持回滚。
4. **内容真实性**：所有触发词均取自文件真实内容，未编造。

---

## 三、模块职责划分

| 模块 | 职责 | 输出 |
|---|---|---|
| frontmatter 写入器 | 为 9 个 skill 追加 agent_created | 修改后的 SKILL.md |
| 备份模块 | 修改前生成 .bak | 9 个备份文件 |
| 触发词提取器 | 按优先级规则从 SKILL.md 提取触发词 | 触发词列 |
| 清单重生成器 | 重新输出带触发词的完整表 | v1.3 Markdown |

---

## 四、如何选型（方法论）

1. **临时手动→永久标记**：手动补进只是过渡，最终要落到 skill 文件的客观字段上。
2. **先备份再修改**：任何批量改动 skill 文件的操作都必须有回滚点。
3. **触发词提取要分层**：有显式取显式，无显式取语义，避免为空或编造。
4. **修改后重跑清单**：确保 frontmatter 写入生效且表格显示一致。

---

## 五、深化学习指引

| 方向 | 推荐来源 | 可信度 |
|---|---|---|
| YAML frontmatter 编辑 | python-frontmatter / ruamel.yaml 文档 | T1 |
| WorkBuddy skill 触发机制 | SkillManage 源码 / 官方示例 | T0 |
| 触发词设计最佳实践 | 各 SKILL.md 真实 frontmatter | T0（一手） |

---

## 六、技术结合点（1+1>2）

- **v1.3 + windows-launcher-safety skill**：批量修改 skill 文件前可用其自查清单确认备份、编码、路径等风险。
- **v1.3 + workbuddy-asar-inspect skill**：确认 WorkBuddy 读取 skill frontmatter 的实际逻辑，验证 `agent_created` 是否被识别。
- **v1.3 + tri-agent-investigation skill**：对触发词提取规则的边界情况做红队审查。
- **v1.3 + task-implement skill**：把「扫描→提取触发词→写 frontmatter→备份」做成可复用任务流。
