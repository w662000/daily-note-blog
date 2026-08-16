---
layout: default
title: 交接文档 · Hermes 接入模型评分表（纯 5 站榜单视角 · MoA 选型）
date: 2026-08-16 23:30:00 +0800
---

# Hermes 接入模型评分表（纯 5 站榜单视角 · MoA 选型）

- **日期**：2026-08-08
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260808_Hermes 接入模型评分表（纯 5 站榜单视角 · MoA 选型）_handoff.md（编码探测：utf-8）

> 来源：项目文档 `2026-08-08-10-56-22\HANDOFF_Hermes模型评分表MoA选型.md`
> 由 handoff_flow.py（scan 阶段）自动收集，标题取自文档 H1（即主要干的活），待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。


> 生成日期：2026-08-08 ｜ 接入清单来源：`C:/Users/Administrator/.hermes/provider_models_cache.json`（Hermes 实测缓存，T0 可信）
> 用途：为 Hermes 开启 MoA（多模型聚合）模式挑主力/助手模型

## 一、评分方法（可信度说明）
- **5 个数据源（用户指定）**：LMArena / Artificial Analysis / LiveBench / Chatbot Arena / SuperCLUE
- **评分方式**：表格列 5 站原始分；**5 站综合 = 5 站各自归一化到 0–100 后的算术平均**（不去重）。不含速度/成本/中文加权。
- **量纲差异（重要）**：LMArena / AA / Chatbot Arena 用 **Elo 分（~1150–1500）**；LiveBench / SuperCLUE 用 **百分制（0–100）**。表内「5 站原始分」按真实量纲展示，综合分先归一化再平均。
- **Chatbot Arena 2024 已更名 LMArena，同源**——表内仍并列两列忠实呈现；介意重复计权可只看 LMArena。
- **沙箱预置未来型号**（gpt-5.6 / claude-opus-4.8 / gemini-3.x / deepseek-v4 等）在真实公开榜单**无数据** → 5 站全标 `N/A`，综合 `N/A`，排表末，**不瞎编数字**。

## 二、评分总表（节选，去重后独立模型 64 个；Hermes 各 provider 原始接入 75 条）
| 排名 | 模型 | Provider | 5站综合 | MoA角色 | 可信度 |
|---|---|---|---|---|---|
| 1 | `anthropic/claude-sonnet-5` | copilot+openrouter | **90.3** | 主力候选 | T1 |
| 2 | `claude-sonnet-4` | copilot | **85.1** | 主力候选 | T1 |
| 3 | `gemini-2.5-pro` | copilot+gemini | **82.4** | 主力候选 | T1 |
| 4 | `gemini-2.5-flash` | gemini | **78.0** | 助手(快/省) | T1 |
| 5 | `z-ai/glm-5.2` | openrouter+zai | **74.4** | 可用 | T2 |
| 6 | `tencent/hy3` | openrouter | **71.6** | 助手(快/省) | T1(免费至8.31) |
| 7 | `glm-5` | zai | **70.8** | 可用 | T2 |
| 10 | `stepfun/step-3.7-flash` | openrouter | **65.7** | 助手(快/省) | T1(本机StepFun) |
| 19 | `glm-4.5-air` | zai | **53.0** | 助手(快/省) | T2 |

> 完整 64 行表见源文档 `model_score_table.md`。

## 三、MoA 推荐配置
**主力模型（5站综合≥80 且现实存在 + 代际 S/A）**：
- `anthropic/claude-sonnet-5`（90.3，中文 4/5）
- `claude-sonnet-4`（85.1）
- `gemini-2.5-pro`（82.4）

**助手模型（现实存在 + 快/省，适合 MoA fan-out / 校验层）**：
- `gemini-2.5-flash`（78.0，速度5/5 成本4/5）
- `tencent/hy3`（71.6，中文5/5，腾讯官方免费延长至 **2026-08-31** → 强烈建议做主力之一）
- `gemini-2.5-flash-lite`（68.3）、`stepfun/step-3.7-flash`（65.7，本机极速中文强）、`glm-5-turbo`（63.5）等

## 四、特别注意
- **hy3**：OpenRouter 的 `tencent/hy3` 路由已下架，走 Z.ai/直连或 WorkBuddy 内置入口。
- **step-3.7-flash**：本机 StepFun，免费/极速/中文强 → 优秀助手层。
- 沙箱预置的 gpt-5.6 / claude-opus-4.8 / gemini-3.x 等代际高但**5 站均无公开榜单数据（综合 N/A）**，实际可用性需先在 Hermes 试连通性再纳入主力。
