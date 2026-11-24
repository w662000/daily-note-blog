---
layout: default
title: 交接文档 · DeepSeek 10 月双发（V4.1-Flash 更新 + 数学专用模型）· 调研稿（Q3）
date: 2026-10-22 12:00:00 +0800
---

# DeepSeek 10 月双发（V4.1-Flash 更新 + 数学专用模型）· 调研稿（Q3）

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\Q3_调研稿_20261023.md

> 检索方式：通过 `mcp__agent-teams__agent_teams_web_search`（SearXNG/Tavily）联网检索，检索日期 2026-10-23。
> 本题事件均发生在 2026-10-15~17，超出模型训练数据，以下结论均来自联网检索结果，非凭记忆作答。
> 来源标注：**官方一手** = DeepSeek 官方（API 文档更新日志、官网新闻、Hugging Face 官方模型卡）；**自媒体/新闻转述** = IT之家、财联社、QQ 新闻等媒体报道（已注明）。无一手来源支撑的说法标注「未核实」。

---

## Q1. 10 月 17 日左右 V4.1-Flash 更新到的版本号？官方定性哪四个字？价格变没变？

- **具体版本号**：**DeepSeek-V4.1-Flash-1017**（即 V4.1-Flash-1017）。官方网页端、APP 与 API 模型已同步更新；API 仍用 `deepseek-flash` 调用即可访问最新版。 — 来源 [1]（官方更新日志）、[2]（IT之家，转述官方）
- **官方定性（四字）**：官方表述为本次更新"在性能与成本之间实现了**帕累托改进**"（Pareto 改进）——即在不增加成本的前提下提升能力、缩短输出与耗时。 — 来源 [2]（IT之家引述"深度求索官方"原话）
  > 说明：官方原话是"性能–费用的帕累托改进"，核心定性词为"**帕累托改进**"（严格是五字术语，意为"帕累托改进/Pareto improvement"）。若按四字概括，即"帕累托改进"所表达的"性能↑、成本↓、互不牺牲"之意。
- **价格有没有变**：**没有变**。官方更新日志明确"API 调用方式与价格保持不变"。 — 来源 [1]
  > 区分提示：DeepSeek 在 V4.1 Flash **首发**时（非本次 1017 补丁）曾下调定价并采用峰谷定价（来源 [3]，官网新闻）；但针对 **2026-10-17 这次 1017 更新**，官方日志写明价格"保持不变"。所以本题"这次更新价格有没有变"的答案是：**没变**。

---

## Q2. 同月发布的数学专用大模型：名字？参数规模？MiniF2F 通过率？

检索到的、与"数学专用 + MiniF2F 通过率"最吻合且数据最一致的模型是：

- **模型名字**：**DeepSeek-Prover-V2-671B**（深度求索面向数学定理证明/形式化证明的开源专用大模型，基于 Lean 4）。
- **参数规模**：**671B（6710 亿）参数**。 — 来源 [4]（Hugging Face 官方模型卡）、[5]（多家媒体报道一致）
- **MiniF2F 通过率**：在 **MiniF2F-test** 上通过率 **88.9%**（pass ratio），并解出 PutnamBench 658 题中的 49 题。 — 来源 [4]（官方模型卡）、[5]

> ⚠️ **「未核实」：发布时间**。题面称该模型与 V4.1-Flash-1017"同一个月（2026 年 10 月）"发布。但本次检索结果中，DeepSeek-Prover-V2-671B 的发布时间**多指向 2025 年**（如 2025-05-01 的报道，来源 [5]），未能通过检索独立确认其在 **2026 年 10 月**单独发布。因此：**模型名称 / 参数 / MiniF2F 88.9% 均有来源**；唯独"2026 年 10 月同月发布"这一时间点标注为「未核实」（检索到的公开报道将其归在 2025 年）。

> **备选/相关模型（供参考，数据有冲突，未作为主答案）**：检索同时出现 **DeepSeek-Math-V2**（Hugging Face 模型卡，来源 [6]），报道称其基于 V3.2 实验架构、达 IMO 金牌水平，MiniF2F 形式化证明"解决率 over 90%"、参数有"6850 亿"（来源 [7]）与"236B 总参数 / 21B 活跃"（来源 [8]）两种说法。因其参数与 MiniF2F 数字来源不一致，本稿未将其作为主答案，仅列此备查。

---

## Q3. 那次更新前两天是不是出过宕机？大概什么时候？

**是的。** 在 1017 更新前两天（即 **2026 年 10 月 15 日**），DeepSeek 发生过一次较大规模服务中断。

- **时间**：**2026 年 10 月 15 日**，约 **北京时间 08:11 至 13:04**，持续约 **5 小时**。 — 来源 [9]（库币/ChainCatcher 转述：DeepSeek API 平台发布修复与补偿公告，写明 8:11–13:04 北京时间系统故障）；[10]（downforeveryoneorjustme：10 月 15 日，约 5 小时）
- **影响范围**：聊天服务（chat）与 **V4.1 Flash API** 均出现部分中断。 — 来源 [11]（knowflowhub：公司确认 chat 与 V4.1 Flash API 部分中断，原因已定位、修复进行中）
- **后续**：据媒体报道，DeepSeek API 平台就此次中断发布了恢复与全额补偿通知。 — 来源 [9]

> 来源性质：以上为**新闻/第三方监测转述**（knowflowhub、库币/ChainCatcher、downforeveryone 等）。报道中提及"DeepSeek 官方发布了恢复与补偿公告"，即存在官方一手公告，但本稿未直接取到该公告原文链接，故宕机事实以多家媒体/监测一致报道为准。

---

## 来源列表（每个数字 / 版本号 / 百分比对应链接）

- **[1] 官方·DeepSeek API 文档更新日志**（V4.1-Flash-1017、价格不变、"性能–费用的帕累托改进"）
  https://api-docs.deepseek.com/zh-cn/updates/
- **[2] 新闻转述·IT之家（2026-10-17）**（引述深度求索官方："性能与成本之间实现了帕累托改进"；价格保持不变）
  https://www.ithome.com/1/014/328.htm
- **[3] 官方·DeepSeek 官网新闻《Introducing DeepSeek-V4.1-Flash》**（首发时下调定价、峰谷定价，非 1017 补丁）
  https://www.deepseek.com/news/deepseek-v4-1-flash/
- **[4] 官方·Hugging Face 模型卡 deepseek-ai/DeepSeek-Prover-V2-671B**（671B、MiniF2F-test 88.9%）
  https://huggingface.co/deepseek-ai/DeepSeek-Prover-V2-671B
- **[5] 新闻转述·QQ 新闻 / 澎湃 / CSDN**（Prover-V2-671B：671B、MiniF2F 88.9%）
  https://news.qq.com/rain/a/20250501A02X0800  ·  https://m.thepaper.cn/newsDetail_forward_30757753
- **[6] 官方·Hugging Face 模型卡 deepseek-ai/DeepSeek-Math-V2**（IMO 金牌水平、MiniF2F over 90%，备选模型）
  https://huggingface.co/deepseek-ai/DeepSeek-Math-V2
- **[7] 新闻转述·aibase**（DeepSeek-Math-V2：6850 亿参数）
  https://www.aibase.com/zh/news/23185
- **[8] 新闻转述·财联社 / codefather**（DeepSeek-Math-V2：236B 总参 / 21B 活跃，11 月 27 日发布）
  https://www.cls.cn/detail/2213231
- **[9] 新闻转述·库币/ChainCatcher**（10-15 宕机 8:11–13:04 北京时间、约 5 小时、官方补偿公告）
  https://www.kucoin.com/news/flash/deepseek-api-service-outage-lasts-5-hours-full-compensation-promised
- **[10] 第三方监测·downforeveryoneorjustme**（10 月 15 日，约 5 小时）
  https://downforeveryoneorjustme.com/deepseek
- **[11] 新闻转述·knowflowhub**（10-15 宕机，chat 与 V4.1 Flash API 部分中断）
  https://www.knowflowhub.com/en/content/article/2026-10-15/deepseek-service-outage-october-2026

---

## 关键数字 / 版本号一览

| 问题 | 项目 | 数值 | 来源性质 | 链接 |
|------|------|------|----------|------|
| Q1 | 版本号 | **DeepSeek-V4.1-Flash-1017** | 官方 [1] | [1][2] |
| Q1 | 官方定性 | 帕累托改进（性能与成本的帕累托改进） | 官方口径 [2] | [2] |
| Q1 | 价格 | **保持不变**（未变） | 官方 [1] | [1] |
| Q2 | 模型名 | **DeepSeek-Prover-V2-671B** | 官方模型卡 [4] | [4][5] |
| Q2 | 参数规模 | **671B（6710 亿）** | 官方 [4] | [4][5] |
| Q2 | MiniF2F 通过率 | **88.9%**（MiniF2F-test） | 官方 [4] | [4][5] |
| Q2 | 发布时间(2026-10) | 「未核实」（检索多归 2025 年） | — | 见正文 |
| Q3 | 宕机日期 | **2026-10-15** | 新闻/监测 [9][10][11] | [9][10][11] |
| Q3 | 宕机时段 | **08:11–13:04 北京时间**（约 5 小时） | 新闻 [9] | [9] |
| Q3 | 影响范围 | 聊天服务 + V4.1 Flash API | 新闻 [11] | [11] |

> 官方来源：[1][3][4][6]；自媒体/新闻转述：[2][5][7][8][9][10][11]。无编造链接；凡检索无法确认之处（Q2 的 2026-10 发布时间）已明确标「未核实」。
