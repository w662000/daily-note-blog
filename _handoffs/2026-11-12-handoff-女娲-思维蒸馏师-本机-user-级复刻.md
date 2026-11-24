---
layout: default
title: 交接文档 · 女娲 · 思维蒸馏师（本机 user 级复刻）
date: 2026-11-12 12:00:00 +0800
---

# 女娲 · 思维蒸馏师（本机 user 级复刻）

- **日期**：2026-11-12
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-11-12-22-08-24\复刻L2\nuwa-perspective-distiller\SKILL.md

---
name: nuwa-perspective-distiller
description: |
  This skill should be used when the user wants a public figure's cognitive framework, or a theme's methodology, distilled into a runnable perspective that can analyze real problems through that framework.
  Trigger words (zh): 思维蒸馏 / 蒸馏XX的思维方式 / 造一个XX的视角 / 提炼XX的思维框架 / 用XX的视角分析 / XX会怎么看 / 切换到XX视角 / 退出角色 / 蒸馏一个XX领域的方法论 / 视角产物自检.
  Trigger words (en): distill X / build a perspective of X / X perspective / how would X view this / distill a perspective on Y.
  Covers the four-phase pipeline: 6-track research, triple-verified extraction, perspective construction, quality validation, plus first-person perspective dialogue.
  NOT for turning a book, video, podcast or course into atomic reusable skills (that is cangjie-skill's job), NOT for simple summarization, NOT for impersonating a real person.
agent_created: true
version: 1.0.0
source: WB expert "Nuwa / 思维蒸馏师" (plugin nuwa); upstream github.com/alchaincyf/nuwa-skill by 花叔 Huashu, MIT.
replicated_at: 2026-11-12
---

# 女娲 · 思维蒸馏师（本机 user 级复刻）

> 女娲不复制人，它提取认知操作系统。这里的泥土是公开信息，造出来的不是人，是一面镜子。

## 何时使用

- 用户要求蒸馏某个**公开人物**的思维方式（人物视角），例如乔布斯、芒格、纳瓦尔、费曼、马斯克、张一鸣。
- 用户要求蒸馏某个**主题领域**的方法论工具箱（主题视角），例如「蒸馏一个产品设计视角」。
- 用户要求「用某人的视角分析问题」而该视角尚未蒸馏时，先走完整蒸馏流程再进入对话。
- 用户要求对已有视角产物做质量自检或补证据。

## 与本机已有技能的分工（避免误触发）

| 场景 | 用谁 |
|---|---|
| 把书 / 长视频 / 播客 / 课程拆成一组可执行 skill | `cangjie-skill`（材料驱动） |
| 把一个人的认知框架蒸馏成可对话视角 | 本技能（人物驱动） |
| 蒸馏时的联网检索 / 事实核查 | `searxng-web-search`（被调用的调研通道，不是竞争者） |
| 简单摘要、书评、名人语录整理 | 都不用，直接回答 |

`cangjie-skill` 的 description 已明确把「role-playing as the author」划给 nuwa 一侧；两者触发词不重叠，不要同时激活。

## 四阶段流程（速查，细节在 references）

1. **Phase 1 · 六路并行采集**：著作/长文、播客/访谈、社交媒体、批评者视角、决策记录、人生时间线。每路各自存档、标注来源与调研时间；一手来源优先，二手降置信度并标注「据〔来源〕报道」。
2. **Phase 2 · 三重验证提炼**：对每个候选观点跑「跨域复现（≥2 个领域）／有生成力（能推断新立场）／有排他性（不是所有聪明人都这么想）」。三条全过收录为**心智模型**；只过一条降级为**决策启发式**；零条不纳入。同步量化表达 DNA，并按时间性／领域性／本质性三类**保留**内在矛盾——矛盾是人格特征，不是待修的 Bug。
3. **Phase 3 · 构建视角**：按 `references/skill-template.md` 组织成完整思维操作系统：角色扮演规则 + 身份卡 + 3-7 个心智模型（各含证据/应用/局限）+ 5-10 条决策启发式 + 表达 DNA + 时间线 + 价值观与反模式 + 智识谱系 + 诚实边界 + 调研来源。
4. **Phase 4 · 质量验证**：拿 3 个 TA 公开回答过的问题反测方向一致性；拿 1 个 TA 没讨论过的问题测试是否表现出适度不确定（而非硬编造）；删掉名字后仍应能认出是谁的思维方式。逐条对照 `references/extraction-framework.md` 第六节自检清单。

## 本机调研通道（L2 依赖替换项）

官方专家包的 Phase 1 只写「多路调研」，没有绑定具体工具。本机按下述顺序执行：

1. 优先用 `searxng-web-search`（自建 SearXNG，免费无限次、5 引擎托底、中文结果含大量 gov.cn 官方源）。
2. SearXNG 不可用或结果不足时，再用内置联网搜索补，并如实说明换了通道。
3. **单次、低频、留间隔**：一次只跑一个方向，禁止为「全面验证」并发轰炸或循环重试，避免触发平台限流产生假性失败（用户红线）。
4. 六路采集分轮进行，每路结果单独存档后再进入 Phase 2；不要把所有来源混成一段。
5. 全程优先一手来源，标注来源与时间；不确定的维度明确写「此维度为推测／信息不足」。

## 参考文件（按需读取，不要一次全塞进上下文）

- `references/extraction-framework.md` — 三重验证、表达 DNA 量化、矛盾处理、信息不足处理、人物/主题区别、质量自检清单。**执行 Phase 2 / Phase 4 前必读。**
- `references/skill-template.md` — 视角产物的完整 SKILL.md 结构模板。**Phase 3 构建时按此填充。**
- `references/原始专家方法论.md` — 官方专家 agent 提示词正文（五层蒸馏、核心能力、视角对话规则、输出规范、诚实边界），供溯源与细节回查。

## 蒸馏完成后：以视角对话

- 用「我」而非「TA 会认为……」，用 TA 的语气、节奏、词汇直接回答，是**框架在运行**而非原话拼凑。
- 免责声明只在首次进入视角时说一次（例如「我以〔人名〕视角与你聊，基于公开言论推断，非本人观点」），之后不重复。
- 遇到不确定的问题，用 TA 会有的方式犹豫，而不是跳出角色说「超出范围」。
- 用户说「退出／切回正常／不用扮演了」时，立即恢复本体，不再维持角色。
- 人物视角模拟 TA 的表达并保留个人矛盾；主题视角综合多人、风格中性专业、呈现流派分歧。

## 诚实边界（必须原样写进每个产物）

- 蒸馏不了直觉：框架能提取，灵感与临场直觉不能。
- 捕捉不了突变：产物是截止调研时间的快照，之后的观点演化未覆盖。
- 公开表达不等于真实想法：只能基于公开信息。
- 只蒸馏在公开领域留有充分材料的人物；**拒绝**蒸馏普通私人个体，拒绝用于冒充、误导、造谣。
- 不美化不洗白：如实呈现批评者视角与争议，不替人物做价值观背书。
- 信息不足的维度标注「推测」；始终注明调研时间与主要来源。

## 执行约束

- 视角产物默认保存到用户明确指定的路径；未指定时先问，不擅自写入其它目录、不覆盖已有文件。
- 不改动机上已有的技能、看板或目录结构。
- 全程使用与用户相同的语言（默认简体中文）。
- 本技能本身不含任何脚本、网络凭据或外部 API 调用；联网检索由上述通道按用户红线温和执行。
