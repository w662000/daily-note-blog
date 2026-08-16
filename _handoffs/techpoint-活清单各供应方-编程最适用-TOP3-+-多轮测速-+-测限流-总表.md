---
layout: default
title: 技术点 · 活清单各供应方「编程最适用」TOP3 + 多轮测速 + 测限流 总表
date: 2026-08-16 23:30:00 +0800
---

# 技术点 · 活清单各供应方「编程最适用」TOP3 + 多轮测速 + 测限流 总表

> 来源：260816_活清单各供应方「编程最适用」TOP3 + 多轮测速 + 测限流 总表_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- > 来源：2026-08-16-10-57-55\各供应方编程TOP3_测速_限流_总表_20260816.md
- > 生成：2026-08-16。数据源：①编程能力 `model-speed-radar/model_scores_merged.json`(74模型)；②多轮测速 `model-speed-radar/data/history.jsonl`(**102轮**, 轮2–102)；③测限流 `C:/Users/Administrator/.cache/rate-limit-radar/data/history.jsonl`(**12轮×每轮15测=180次/模型**, 08-05→08-15)。
- **可信度**：编程分来自 Google 模型卡/Artificial Analysis/madebyagents/benched.ai/IBM 等（活清单逐条标 src）；Q3/Q4 为项目真跑代码跑基准用例；测速/限流为真实轮次记录。凡活清单缺字段的，表中标「—」不推断。
- | 供应方 | # | 模型 | 编程代表分(基准·层) | 综合/可信 | 测速TTFT中位·均值·成功率 | 测速等级 | 限流被限次数(轮) | 限流成功率 | 限流avg_ms |
- | GLM API | 1 | `glm-4.7` | 84.9(LiveCodeBench·T1) | 80/高 | 3659·3676·16% | A:1/B:9/C:85/S:1 | 1(1轮) | 50% | 6251 |
- | GLM API | 2 | `glm-5` | 77.8(SWE-bench V·T1) | 87/高 | 3518·3477·9% | B:9/C:87 | 0(0轮) | 55% | 4207 |
- | GLM API | 3 | `glm-4.5-air` | 68.4(LiveCodeBench·T1) | 62/高 | 755·1054·82% | A:4/B:3/C:20/S:69 | 0(0轮) | 91% | 893 |
- **#1 `glm-4.7`** — [GLM API] GLM-4.7
- 测限流(11轮×15测=165次)：被限流 **1 次**（涉及 1 轮）｜ 其他错误 82 次 ｜ 成功率 49.7% ｜ avg_ms 6251 ｜ 末轮等级 A
- **#2 `glm-5`** — [GLM API] GLM-5
- 测限流(11轮×15测=165次)：被限流 **0 次**（涉及 0 轮）｜ 其他错误 75 次 ｜ 成功率 54.5% ｜ avg_ms 4207 ｜ 末轮等级 A
- **#3 `glm-4.5-air`** — [GLM API] GLM-4.5-Air (赠送)

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. **GLM API 的 TOP3 有真实第三方基准（此前我误判为「全系缺」，已更正）**：`glm-4.7` 有 LiveCodeBench v6=84.9% + SWE-bench V=73.8%（z.ai 官方）、`glm-5` 有 SWE-bench V=77.8%（NYU rits）、`glm-4.5-air` 有 LiveCodeBench=68.4%（easy-benchmarks）。真正缺代码生成基准的是免费/视觉系小模型（glm-4.7-flash、glm-z1-flash、glm-4.x-vision 系列），它们不进 TOP3，不影响结论。
2. **Gemini 的 gemini-flash-latest 靠 Tau-bench 95.3 拉分**：Tau-bench 测的是 agentic 工具调用，非纯代码生成，已降入 Tier3，故排在 LCB 72 的 gemini-3.1-flash-lite 之后。若要的是「写代码」而非「调工具」，flash-latest 不一定是首选。
3. **Cloudflare 的 granite-4.0-h-micro 只有 HumanEval 81**（旧基准·易），无 LiveCodeBench，已正确排在 gemma/qwen3 之后；别被 HumanEval 数字骗去当编程主力。
4. **OpenRouter / HF / Agnes-AI 是路由/转售层**（非原厂）：它们复用了 NVIDIA/Cohere/Google/Qwen/Kimi 等原厂权重，编程能力本质来自上游模型；列为供应方是忠实于活清单标签，但评「原厂编程最强」应看 NVIDIA NIM / Cloudflare / GLM API / StepFun / SenseNova / Gemini 这些。
5. **限流结果 12 轮 ×15 测为温和探测**（轮间 5s，符合你定的「不触发平台限流」红线），被限次数低≠永远不限——高峰期密集调用仍可能触发，gemma-4-26b 在测速里就出现过 cooldown。
6. **`glm-5.2` 在活清单里被标了两次**：`[SenseNova] SenseNova GLM-5.2` 与 `[NVIDIA NIM] GLM-5.2 ⚡(Z.ai旗舰)`，是同一个 Z.ai 模型。故它既出现在 SenseNova 组的 TOP2（SWE-bench Pro 62.1%），也出现在 NVIDIA NIM 组的 TOP3（FrontierSWE 74.4%，官方/AA 双源）。评「原厂编程」时它就是同一模型，跨组去重看即可。

---
原始脚本：`_build_final_table.py`；中间文件：`_provider_top3.json`。
