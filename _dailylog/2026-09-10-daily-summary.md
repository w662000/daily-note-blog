---
title: "每日工作总结 · 2026-09-10"
date: 2026-09-10
category: daily-note
tags: [workbuddy, daily-log]
---

# 每日工作总结 · 2026-09-10

## 一、今日完成事项

- **Agnes 平台五端模型接入**：将 agnes-3.0-flash、agnes-2.5-pro-beta 等新增模型写入 WorkBuddy、DSH、Hermes、AutoClaw、有道龙虾共五个平台，更新配置文件并生成回滚备份。
- **DeepSeek flash 故障修复**：定位到模型 id 拼写错误（本地写的是 `deepseek-v4-flash-official`，官方实际叫 `deepseek-flash`），同步修复五个平台的配置，恢复 deepseek-flash 的正常对话/推理/工具调用能力。
- **SenseNova 平台可用性诊断**：基于两个雷达（测速 + 限流）30 轮历史数据，确认该平台限流率 16.7%（全平台第 2 高），但更严重的问题是 8 个模型中有 3 个每轮必挂（404），真正能用的只剩 glm-5.2。
- **SenseNova 模型清单整理**：通过官方 API 获取 8 个模型真实列表，识别出本地未配置的 kimi-k3 和 sensenova-u1.5-lite 为全新模型，实测 kimi-k3 支持对话 + 推理 + 工具调用。
- **本地可用模型优先调用指南**：综合两个雷达数据，输出 17 个平台 / 47 个模型的分级推荐表，第一梯队 5 个模型（deepseek-v4-pro、glm-4.1v-thinking-flash 等）日常连发都稳。
- **FAILOVER 巡检（目标日 09-09）**：核验发现主链未产出总结文件（09-09 无日志），Handoff/技术点轴合规为空，云笔记第 5 端 51 篇工作日志已同步至 09-06。

## 二、关键决策 / 注意事项

- **模型 id vs name 区分**：DeepSeek 官方 flash 的 id 是 `deepseek-flash`（不带 v4），改 id 会 400；撞名问题应改 name（UI 显示名），不动 id（API 请求用）。
- **雷达数据解读方法**：日常成功率 vs 连发成功率是两回事，同一模型可能日常 83% 但连发 3%（如 sensenova-6.8-flash-lite），误判风险高。
- **SenseNova 平台整体评级**：虽然 glm-5.2 可用，但限流 39% + 大量模型 404，整体不建议作为主力。
- **新模型接入规范**：写入五平台前先检查 id 是否撞名，生成 `.bak-<timestamp>` 备份文件便于回滚。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|-----------|------|------|
| 五平台接入报告 | `D:\AI work\workbuddy\2026-09-10-12-50-38\agnes_五平台接入报告_20260910.md` | Agnes 新增 5 模型写入记录与备份清单 |
| DeepSeek flash 故障分析 | `D:\AI work\workbuddy\2026-09-10-12-50-38\DeepSeek_flash故障分析与修复_20260910.md` | 根因定位 + 五处修复详情 |
| SenseNova 限流分析 | `D:\AI work\workbuddy\2026-09-10-12-50-38\sensenova_限流分析_20260910.md` | 双雷达数据诊断报告 |
| SenseNova 模型清单 | `D:\AI work\workbuddy\2026-09-10-12-50-38\sensenova_模型清单_20260910.md` | 官方 API 获取的 8 模型列表 + kimi-k3 实测 |
| Agnes 模型清单 | `D:\AI work\workbuddy\2026-09-10-12-50-38\agnes_models_20260910.md` | 平台 11 模型列表 + agnes-3.0-flash 实测 |
| 模型优先调用指南 | `D:\AI work\workbuddy\2026-09-10-12-50-38\模型优先调用指南_20260910.md` | 17 平台 47 模型分级推荐表 |
| 工作日志 | `D:\AI work\workbuddy\.workbuddy\memory\2026-09-10.md` | FAILOVER 巡检记录 |

## 四、待办 / 风险

- **P1 SenseNova glm-5.2 限流 39%**：日常一半时间在冷却，建议降低拨测频率或换用 GLM API 同档模型。
- **P2 DeepSeek 官方 flash 与 b.ai 同名**：已用 name 区分解决，但需定期检查其他平台是否有类似撞名。
- **P2 kimi-k3 未接入五平台**：实测可用（对话 + 推理 + 工具），下次有空时补充配置。
- **云笔记第 5 端**：不在本任务范围，由 23:07 主链 `upload_youdao.py` 独立处理。
