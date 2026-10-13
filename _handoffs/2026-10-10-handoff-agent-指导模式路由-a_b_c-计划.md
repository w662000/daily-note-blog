---
layout: default
title: 交接文档 · agent 指导模式路由（A_B_C 计划）
date: 2026-10-13 23:30:00 +0800
---

# agent 指导模式路由（A/B/C 计划）

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\autonomous-ai-agents\agent-plan-router\SKILL.md

---
name: agent-plan-router
description: "Use when the user says 'use plan A' / 'execute with A', 'plan B', 'plan C', or mentions 'PDCA' — route to the matching orchestration recipe. A = six thinking hats + RACI + parallel multi-agent; B = Cynefin sense-making + kanban WIP + MoSCoW; C = PDCA closed-loop (spine provided by multi-agent-pdca). When the plan is unspecified, ask the user which one to use — never default."
version: 1.0.0
author: WorkBuddy export (adapted for Hermes)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [plan-router, a-b-c, six-hats, raci, cynefin, moscow, pdca, orchestration]
    related_skills: [multi-agent-pdca, plan]
---

# agent 指导模式路由（A/B/C 计划）

> 把一套项目管理思维工具落成三套可点名的 agent 工作法。
> **调用方式**：用户说「用A计划执行 / 用A执行」→ 按 A；「用B计划执行 / 用B执行」→ 按 B；「用C计划执行 / 用C执行」→ 按 C。
> 用户未点名时，先向用户澄清采用哪套，不擅自默认。

## Overview

三套方案共享同一个底层能力底座（Hermes 落地映射）：
- 多 agent 派活：用 `delegate_task` 并行 / 串行派子 agent 承担调查、规划、挑刺、执行等角色。
- 任务清单 / 看板：用 `todo` 建卡、指派 owner、标状态、限 WIP。
- 联网检索 / 读官方文档：`web_search` / `web_extract` / `read_file` / `search_files`，先搜再判。
- 对话澄清：用六何（Who/What/When/Where/Why/How）追问模糊需求；必要时向用户澄清。
- 落盘记忆 / 文件：`write_file` 把过程与结论写入本地文件 / 记忆，作验证证据与交接。
- 结果呈现：结构化一页报告或文件交付。
- 定时自动化：固定节奏任务设为定时自动执行（Hermes cron）。

---

## A 方案 — 多角色并行（六顶思考帽 + RACI + 多 Agent）

核心：把任务当平行思维会议，角色从同一角度集中贡献再归纳。
- 白帽(事实/调查)=调查员：联网检索、读官方文档、摸清机制与坑位。
- 绿帽+黄帽(方案/价值)=规划员：出可执行方案、评估价值与可行性。
- 黑帽(谨慎/风险/挑刺)=挑刺员：动手前专找 plan 漏洞、排风险矩阵。
- 蓝帽(控流程/meta)=主 agent：定流程、终决、汇总。
- RACI：每子任务标 R(执行 agent)/A(主 agent,唯一)/C(挑刺员)/I(用户)。

流程：蓝帽定题 → 白帽查事实(并行) → 绿帽出方案 → 黑帽挑刺 → 蓝帽定夺 → 执行(单变量小步) → A3 交付。
适用：成规模 / 多步骤 / 陌生领域任务（= multi-agent-pdca 骨架，但更强调多角色平行视角）。
优点：视角全、挑刺前置、责任清。缺点：开销大，小任务杀鸡用牛刀。

---

## B 方案 — 情境路由（Cynefin + 看板 + MoSCoW）

核心：先判这是哪类事，再选最轻路径，拒绝一刀切套重流程。
Cynefin 五域 → 路径：
- Clear(已知已知,有最佳实践)：直接执行，套现有脚本 / 流程（如每日自动发布）。
- Complicated(已知未知,需专家分析)：派调查 / 规划类子 agent 查清机制再干。
- Complex(未知未知,要试错)：探索-感知-响应，小循环(OODA)低成本试错（如微信改版抓取失败）。
- Chaotic(不可知,先止血)：行动-感知-响应，先停手止损再找因（如灌库报错数据丢了）。
- Confusion：先拆分再归类，不急着动手。

辅助：看板(WIP)限制同时跑的 agent / 任务数（如 ≤2）防并发撞限流；MoSCoW 在频率预算 / 时间受限时排 Must/Should/Could/Won't。

流程：收任务 → Cynefin 判域 → 选路径(直接/专家/试错/止血) → 看板排 WIP → MoSCoW 排优先级 → 执行 → 落盘验证。
适用：日常混合任务流、频率 / 额度受限场景（限流、免费层）。优点：最省资源、自适应、天然防限流。缺点：依赖主 agent 判域准，缺强制挑刺。

---

## C 方案 — 闭环验证（PDCA + SMART + 5W1H + 风险矩阵 + 5 Whys + A3）

核心：一切以可验证闭环为中心。
- PDCA 为唯一主循环：Plan(目标/拆解/风险) → Do(单变量小步、温和测试) → Check(落盘证据对照标准) → Act(固化/沉淀)。
- SMART：每 Do 子任务必须有 Measurable + Time-bound 验收线。
- 5W1H：接任务澄清六何。
- 风险矩阵：Plan 阶段排风险（黑帽思维内嵌）。
- 5 Whys：Check 不符预期连问五层根因，禁凭印象归因。
- A3：交付 / 交接一页纸，写全现状与根因（契合"不折叠长输出"纪律）。

**实现**：C 的 PDCA 脊由 `multi-agent-pdca` 技能提供——选中 C 时**通过 related_skills / `skill_manage`(`skill_view`) 加载 `multi-agent-pdca`** 获取完整 PDCA 编排（调查员 / 规划员 / 挑刺员 / 执行员 + 四阶段模板），再叠加本方案的 SMART/5W1H/风险矩阵/5Whys/A3 包装。

流程：5W1H 澄清 → SMART 定标 → 风险矩阵 → Plan → Do(单变量) → Check(落盘证伪) → 不符则 5Whys 回 Plan → 符合则 Act 固化 → A3 交付。
适用：工程改进、需稳定可复现任务（每日采集、发布修复、脚本回归）。优点：强制验证、失败可控、根因清、交付不折叠。缺点：节奏偏慢。

---

## 路由决策（主 agent 收到任务后）
1. 扫描用户原话是否含「用A/用B/用C」+「计划执行/执行/计划」；或含「PDCA」字样（如「用PDCA执行」「PDCA思路」「PDCA计划执行」）视同 C（PDCA 即 C 的脊）。
2. 命中 → 加载本 skill（即此次）并按对应方案编排；命中 C 时再加载 `multi-agent-pdca`。
3. 未命中 → 向用户澄清用哪套（A/B/C），不擅自默认。
4. 三方案共享底层纪律：先搜再判、温和测试(不连跑触发限流)、不折叠长消息。

## 来源
- 项目管理思维工具全景回顾（六顶思考帽 / RACI / Cynefin / MoSCoW / PDCA / SMART / 5W1H / 风险矩阵 / 5Whys / A3）。
- C 方案的 PDCA 脊由 `multi-agent-pdca` 提供。

## Common Pitfalls
1. **未点名就默认 A**：用户没说用哪套时，必须澄清，不擅自选最重的 A。
2. **C 忘了加载 multi-agent-pdca**：C 的 PDCA 编排在 `multi-agent-pdca` 里，选中 C 必须一并加载，否则缺调查/挑刺骨架。
3. **B 判域错误**：把 Chaotic 当 Clear 直接套脚本，或把 Complicated 当 Clear 不派调查员 → 先 Cynefin 判域再选路。
4. **A 省掉挑刺员**：黑帽挑刺是强制环节，不能因为"视角全"就跳过。
5. **验证不可证伪 / 输出折叠**：C 的 Check 必须落盘证伪；A3 交付须写全，不压缩成结论短句。

## Verification Checklist
- [ ] 已识别用户点名的方案（A/B/C 或 PDCA）；未点名则已向用户澄清。
- [ ] A：白/绿/黑/蓝四帽角色齐，RACI 标注，黑帽挑刺在 Do 前完成。
- [ ] B：已做 Cynefin 判域并选最轻路径，看板 WIP 与 MoSCoW 已排。
- [ ] C：已加载 `multi-agent-pdca`，含 SMART 定标 + 风险矩阵 + 5Whys + A3 交付。
- [ ] 三方案均遵守：先搜再判、温和测试不连跑、长输出不折叠。
- [ ] 交付物为结构化一页报告 / 文件，结论与证据完整。
