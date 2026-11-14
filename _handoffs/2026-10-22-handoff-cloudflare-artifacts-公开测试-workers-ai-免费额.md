---
layout: default
title: 交接文档 · Cloudflare Artifacts 公开测试 + Workers AI 免费额度 + 增值税起征点 · 调研稿
date: 2026-11-14 23:30:00 +0800
---

# Cloudflare Artifacts 公开测试 + Workers AI 免费额度 + 增值税起征点 · 调研稿

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\Q1_调研稿_20261023.md

> 检索方式：通过 `mcp__agent-teams__agent_teams_web_search`（SearXNG/Tavily）联网检索，检索日期 2026-10-23。
> 本题所有事件均发生在 2026 年 10 月，超出模型训练数据，以下结论**均来自联网检索结果，非凭记忆作答**。
> 来源标注规则：**官方一手** = Cloudflare / 国家税务总局 / 财政部官方页面；**自媒体/第三方转述** = 媒体或聚合站点。无一手来源支撑的说法标注「未核实」。

---

## Q1. Artifacts 是什么？公开测试大概在哪一天？

### 是什么
Cloudflare **Artifacts** 是一个**兼容 Git 的、版本化的分布式存储/文件系统**，定位为面向 AI Agent 与代码平台的"Git for Agents"（为 Agent 打造的版本控制基础设施）。

- **官方一手**（Cloudflare Changelog，2026-10-01）：*"Artifacts is now in open beta with Workers Builds integration, programmable repository workflows, event subscriptions, data localization, and metrics."* — 来源 [1]
- **自媒体/第三方转述**（Forkast，2026-10-07）：*"a distributed, versioned filesystem that speaks Git, marking the first time a major cloud provider has built version control specifically for [agents]"* — 来源 [4]
- **第三方**（aiidelist）：*"a Git-compatible versioned storage service designed for developers building AI agents, coding platforms, and automated software workflows"* — 来源 [5]

### 公开测试日期
官方 Changelog 显示 Artifacts 于 **2026 年 10 月 1 日（2026-10-01）** 进入 open beta（公开测试）。— 来源 [1]

> ⚠️ **与题面差异说明**：题面称"2026 年 10 月中旬公开测试"，但官方 changelog 落款为 **10 月 1 日（月初）**。与"10 月中旬"相关的两个真实节点是：
> - 配套竞赛 *"build the next Git platform on Cloudflare"* 的投稿截止日 = **2026-10-14** — 来源 [2]
> - Cloudflare 对 Artifacts 开始计费日 = **2026-10-14** — 来源 [3]
>
> 因此"公开测试"本身实际始于 **2026-10-01**，而非中旬；中旬（10-14）是竞赛截止与计费启动日。

---

## Q2. 它提供哪些能力（至少列出三项）？

依据官方 Changelog 2026-10-01 条目，Artifacts 开放测试期提供的核心能力（≥3 项，均来自官方一手来源 [1]）：

1. **Workers Builds 集成**（Workers Builds integration）
2. **可编程的仓库工作流**（programmable repository workflows）
3. **事件订阅**（event subscriptions）
4. **数据本地化**（data localization）
5. **用量指标**（metrics）

（第三方转述还称其提供"兼容 Git 的版本化存储"，见来源 [4][5]；官方 changelog 已明确列出前 5 项。）

官方来源：[1] `https://developers.cloudflare.com/changelog/post/2026-10-01-artifacts-open-beta/`

---

## Q3. Cloudflare Workers AI 的免费额度是多少（按什么单位计）？

第三方聚合站点 **pricepertoken.com** 给出的口径（**非 Cloudflare 官方一手来源**，见来源 [6]）：

- **免费额度：每个账户每天 10,000 个「Neurons」**（Cloudflare 的归一化算力单位），在 **Workers Free 套餐**下提供，**每日 00:00 UTC 重置**。
- 超出免费额度后，按 **$0.011 / 1,000 Neurons** 计费（同一第三方来源）。
- **计费单位 = Neurons**（Cloudflare 自有的标准化算力计量单位，不是 token、也不是"次"）。

> ⚠️ **未核实（官方口径）**：本次检索未能直接命中 Cloudflare 官方文档页面对"10,000 Neurons/天"这一数字的逐字确认（官方 plan/pricing 页仅返回泛化结果）。该数字**仅来自第三方来源 [6]**，已明确标注。建议以官方 `developers.cloudflare.com` 的 Workers AI 限额/定价页为准。

来源：[6] `https://pricepertoken.com/endpoints/cloudflare/free`（第三方/聚合站点）

---

## Q4. 小规模纳税人按月计税的增值税起征点是多少？

**以一个月为一个计税期间的，增值税起征点标准为：月销售额 10 万元（人民币 100,000 元）。**

- **官方一手**（国家税务总局，上海税务转发解读，2026-02）：*"10号公告第一条规定，以一个月为一个计税期间的，起征点标准为月销售额10万元。"* — 来源 [7]
- **官方一手**（国家税务总局 2026 年《关于起征点标准等增值税征管事项的公告》解读）：自然人通常按次纳税（起征点每次/日 **1,000 元**）；特定情形下参照按期纳税，直接适用**月销售额 10 万元**标准。— 来源 [8]
- **立法层面**（财政部《中华人民共和国增值税法》第二十三条）：小规模纳税人销售额未达到起征点的免征增值税；具体起征点标准由 10 号公告明确为月销售额 10 万元。— 来源 [9]

> 注：历史上曾有"月销售额 15 万元"的阶段性免税政策（2021 年，发改委文稿提及"从月销售额10万元提高到15万元"，来源 [10]），但**当前常态化执行的起征点标准为月销售额 10 万元**（依据 2026 年现行 10 号公告）。来源 [10] 为历史政策，不代表现行口径。

---

## 来源列表（每个数字 / 日期对应链接）

- **[1] 官方·Cloudflare Changelog — Artifacts open beta（2026-10-01）**
  https://developers.cloudflare.com/changelog/post/2026-10-01-artifacts-open-beta/
- **[2] 官方·Cloudflare Blog — build the next Git platform（投稿截止 2026-10-14）**
  https://blog.cloudflare.com/next-git-platform-on-cloudflare/
- **[3] 官方·Cloudflare Artifacts Changelog（计费起始 2026-10-14）**
  https://developers.cloudflare.com/changelog/product/artifacts/
- **[4] 自媒体/第三方·Forkast（2026-10-07）**
  https://forkast.news/cloudflare-ships-git-for-agents-artifacts-turns-version-control-into-infrastructure/
- **[5] 第三方·aiidelist**
  https://aiidelist.com/blog/cloudflare-artifacts
- **[6] 第三方·pricepertoken.com（Workers AI 免费额度）**
  https://pricepertoken.com/endpoints/cloudflare/free
- **[7] 官方·国家税务总局（上海税务）— 起征点解读（2026-02）**
  https://shanghai.chinatax.gov.cn/zcfw/zcjd/202602/t479287.html
- **[8] 官方·国家税务总局 — 起征点征管公告解读**
  https://www.chinatax.gov.cn/chinatax/n810219/n810724/c5247478/content.html
- **[9] 官方·财政部 — 中华人民共和国增值税法（第二十三条）**
  https://m.mof.gov.cn/czxw/202412/t20241225_3950494.htm
- **[10] 历史政策·发改委（2021，"月销售额15万元"阶段性政策）**
  https://www.ndrc.gov.cn/xwdt/ztzl/jdstjjqycb/zccs/202110/t20211029_1337331.html

---

## 官方 vs 自媒体 标注汇总

| 问题 | 数字/日期 | 数值 | 来源性质 | 链接 |
|------|-----------|------|----------|------|
| Q1 | 公开测试日 | 2026-10-01 | 官方一手 [1] | [1] |
| Q1 | 竞赛截止/计费日 | 2026-10-14 | 官方一手 [2][3] | [2][3] |
| Q2 | 能力清单（5 项） | Workers Builds 集成 / 可编程工作流 / 事件订阅 / 数据本地化 / 指标 | 官方一手 [1] | [1] |
| Q3 | 免费额度 | 10,000 Neurons/天（每日 00:00 UTC 重置） | 第三方 [6] | [6] |
| Q3 | 超出计费 | $0.011 / 1,000 Neurons | 第三方 [6] | [6] |
| Q3 | 计费单位 | Neurons（Cloudflare 归一化算力单位） | 第三方 [6] | [6] |
| Q4 | 按月起征点 | 月销售额 10 万元 | 官方一手 [7][8][9] | [7][8][9] |
| Q4 | 按次起征点 | 每次/日 1,000 元 | 官方一手 [8] | [8] |

**未核实项**：Q3 中"10,000 Neurons/天"缺乏 Cloudflare 官方一手页面直接确认，仅由第三方 [6] 提供，已在文中明确标注。
