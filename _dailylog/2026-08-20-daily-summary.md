---
layout: default
title: 每日工作总结 · 2026-08-20
date: 2026-08-20 23:30:00 +0800
---

# 每日工作总结 · 2026-08-20

> 来源：本机机器日志 `2026-08-20-11-25-37/.workbuddy/memory/2026-08-20.md`（全天主线）+ 根 `.workbuddy/memory/2026-08-20.md`（仅 10:00 离线兜底 checkpoint，补发 08-19）。当天无纯日期文件夹，用承载主线的会话目录 11-25-37。

## 一、今日完成事项（分点，通俗语言）

1. **通达信「由绿翻红」分时预警公式重述**：用户要求把 8/13 写过的「股价由绿翻红」分时预警公式重新整理交付。经 `conversation_search` + 回读 8/13 会话日志找回核心逻辑后，重新交付两套公式（方案 A 主图叠加 / 方案 B 条件预警）+ 严格版 `CROSS(C, DYNAINFO(3))`。核心机制不变：分时线颜色以昨收 `DYNAINFO(3)` 为界，翻红＝分时价上穿昨收。

2. **NVIDIA NIM 模型批量测速**：用户发来小金鱼「白嫖 NVIDIA 大模型」速度榜截图（17 个模型），要求拉清单＋实测＋做表。从 NVIDIA API 拉到完整 **102 个模型**列表，对比截图找出 **12 个缺失模型**；写温和测速脚本（间隔 3s／超时 15s／串行）实测 15 个模型，分级结果：
   - S 级（<500ms）6 个：gpt-oss-20b(177ms)、gpt-oss-120b(199ms)、poolside/laguna-xs-2.1(257ms)、nemotron-3-nano-30b(275ms)、nemotron-3-super-120b(322ms)、minimax-m3(352ms)
   - A 级（500–1000ms）3 个：nemotron-nano-9b-v2(394ms)、nemotron-3-ultra-550b(557ms)、inkling(588ms)
   - B 级（>5s）3 个：llama-3.3-nemotron-49b(6.5s)、gemma-4-31b(7.6s)、step-3.7-flash(10.3s)
   - 超时 3 个：mistral-nemotron / deepseek-v4-flash(NV) / glm-5.2(NV)（疑似下线或限流）

3. **6 个 NVIDIA 快模型批量写入全平台**：用户确认将测速 S/A 级的 6 个模型写入所有平台。6 个模型：`openai/gpt-oss-20b`(NVIDIA版·177ms)、`poolside/laguna-xs-2.1`(257ms)、`nvidia/nemotron-3-nano-30b-a3b`(275ms)、`minimaxai/minimax-m3`(352ms)、`nvidia/nvidia-nemotron-nano-9b-v2`(394ms)、`nvidia/nemotron-3-ultra-550b-a55b`(557ms)。已落地 **5 个平台**：
   - `~/.workbuddy/models.json`（DSH 活清单）— 新增 6 条，gpt-oss-20b 用 `:nvidia` 后缀区分 Groq 版
   - `~/.hermes/config.yaml`（Hermes AI Gateway）— nvidia-nim custom_providers 从 3→9 个
   - `~/.hermes-web-ui/config.json`（WebUI/Studio）— custom:nvidia-nim 从 3→9 个
   - `AppData/Roaming/autoclaw/settings.json`（AutoClaw）— 新增 3 个
   - `AppData/Roaming/LobsterAI/openclaw/state/openclaw.json`（LobsterAI）— custom_4 从 4→10 个 + agents 注册 6 个

4. **活清单综合评分表（性能 85% + 速度 15%）**：把活清单（`models.json` 共 36 个模型）按「性能分×0.85 + 速度分×0.15」打分做表。
   - 性能分 P：取自 8/2 活清单性能评分汇总（0–100 综合指数），已评估 26 个／同源参考 7 个／同系估计 3 个／未评估 3 个
   - 速度分 S：基于实测 TTFT 分段映射（数据源＝测速雷达 `data/latest.json` 30 个模型均值 ＋ 今天新加 6 个 NVIDIA 实测）
   - **关键发现**：36 个里 22 个有完整综合分、14 个 N/A（11 个速度未实测因本机网络不可达、3 个性能未评估）
   - 综合分 Top5：GLM-5.2(SenseNova)87.8 / DeepSeek-V4-Pro(官方)87.3 / WeChat Deepseek-v4-flash 85.4 / Nemotron-3-Ultra-550B(NVIDIA)84.9 / Inkling(NVIDIA)83.2
   - 已生成可视化 HTML 评分表

5. **（10:00 离线兜底 checkpoint）补发 08-19 总结**：当晚 23:30 自动总结未生成（本机大概率关机）。基于会话目录 `2026-08-19-12-55-37` 真实提炼新建 `2026-08-19_每日工作总结.md`，语雀源 `summaries/` 与博客源 `daily-note-blog/_dailylog/2026-08-19-daily-summary.md` 双推 git push ✅，云端 Action 发布语雀 workflow 已触发（幂等）。

## 二、关键决策 / 注意事项

- **速度缺口是真实不可达，未编造**：14 个 N/A 中 11 个速度未实测，根因是测速雷达 round 141 对 Gemini / DeepSeek 官方 / b.ai / WeChat / SenseNova / Groq / BazaarLink 等渠道连续 7 次全失败，温和补测仍不可达——属本机网络环境限制，非脚本故障，已在评分表里如实标注「N/A」而非填假数。
- **撞名规避**：`gpt-oss-20b` 用 `:nvidia` 后缀区分 Groq 版，避免两渠道同 id 冲突。
- **性能分来源可靠**：性能分取自 8/2 已沉淀的 `model_scores_merged.json` 综合指数，速度分来自雷达 7 次采样均值，两层数据均有出处，非拍脑袋。
- **6 个 NVIDIA 模型写入全平台需用户重启各网关生效**：Hermes/WebUI/Studio/AutoClaw/LobsterAI 多数需重启进程才会加载新 provider，本次只改配置未重启。

## 三、生成的有用文件（表格：文件/目录 | 路径 | 用途）

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| nvidia_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_test.py` | NVIDIA NIM 温和测速脚本（间隔 3s／超时 15s／串行），实测 15 个模型 TTFT |
| nvidia_speed_test.json | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_test.json` | 15 个模型实测 TTFT 原始数据 |
| nvidia_speed_table.html | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_table.html` | NVIDIA 速度榜可视化（S/A/B/超时分级） |
| supplement_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\supplement_speed_test.py` | 速度补测脚本（针对雷达不可达渠道温和重试） |
| supplement_speed.json | `D:\AI work\workbuddy\2026-08-20-11-25-37\supplement_speed.json` | 补测结果数据 |
| build_score_table.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\build_score_table.py` | 活清单综合评分表生成脚本（性能×0.85＋速度×0.15） |
| 活清单综合评分表.html | `D:\AI work\workbuddy\2026-08-20-11-25-37\活清单综合评分表.html` | 36 个模型综合评分可视化表（含 Top5 与 14 个 N/A 标注） |
| 2026-08-19_每日工作总结.md | `D:\AI work\workbuddy\2026-08-19_每日工作总结.md` | 10:00 离线兜底补发的 08-19 总结（语雀源＋博客源双推成功） |

## 四、待办 / 风险

- **P1**：6 个 NVIDIA 模型写入全平台后需用户重启 DSH(3080)/Hermes gateway(5324)/WebUI(8787)/Studio(8648)/AutoClaw/LobsterAI 各进程，配置才会真正生效；Hermes 默认模型仍待切换。
- **P1**：14 个 N/A 模型（尤其 Gemini/DeepSeek 官方/WeChat/SenseNova/Groq/BazaarLink 渠道）速度缺口源于本机网络不可达，若日后网络恢复需补测补全评分表。
- **P2**：12 个截图缺失模型未进一步追查来源（是否私有/已下线），仅标注缺失，待用户决定是否深挖。
- **P2**：通达信翻红预警公式重述版尚未在本地通达信客户端实盘验证触发效果，待用户回测。
