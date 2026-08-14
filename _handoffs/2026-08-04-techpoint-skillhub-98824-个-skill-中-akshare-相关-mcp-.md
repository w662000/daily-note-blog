---
layout: default
title: 技术点 · skillhub 98824 个 skill 中「akshare 相关 MCP Skill」重筛清单
date: 2026-08-04 23:30:00 +0800
---

# 技术点 · skillhub 98824 个 skill 中「akshare 相关 MCP Skill」重筛清单

> 来源：交接文档《skillhub 98824 个 skill 中「akshare 相关 MCP Skill」重筛清单》（2026-08-04）

---

## 一、技术选型

本项目要解决的核心问题是：在 SkillHub 将近 10 万个 skill 里，快速、准确地找出真正与 akshare 相关的 MCP Skill，并给出可安装的优先级清单。

选型结论：
- **数据源**：`skillhub_all.json`（98,824 条 skill 元数据）作为全量检索池。
- **匹配引擎**：本地 Python 脚本做字段级文本匹配，不依赖外部 API，避免二次限流与费用。
- **匹配策略**：双口径——
  - **精确口径**：在 `name / slug / description / description_zh / tags / labels / category / source / upstream_url / homepage` 中大小写不敏感匹配 `akshare`，得到 102 个。
  - **宽口径**：用金融数据类关键词做同类能力扩展，得到 14,447 个（仅作主题分布参考）。
- **排序依据**：按 GitHub stars 降序，辅助安装量，得到 TOP 20 精选列表。

---

## 二、实施要点与关键技术

1. **字段全覆盖匹配**：不能只看 `name` 或 `description`，因为很多 skill 的 akshare 关联藏在 `upstream_url`、`homepage` 或 `tags` 里。
2. **大小写与符号归一化**：`akshare`、`AKShare`、`AkShare` 必须视为同一个词，避免漏检。
3. **去重与清洗**：`node_modules` 与重复目录要剔除；同名但不同路径的 skill 要标记重复来源。
4. **可信度分层**：输出必须标注 T0（官方/财报/公开课）/ T1（权威第三方）/ T2（媒体估算），不能把所有数字混为一谈。
5. **TOP 列表聚焦**：102 个结果仍太多，按 stars 取 TOP 20 并展开官方说明，便于读者直接决策安装哪一个。

---

## 三、模块职责划分

| 模块 | 职责 | 输出 |
|---|---|---|
| 数据加载层 | 读取 `skillhub_all.json` | 98,824 条结构化 skill 记录 |
| 匹配引擎层 | 多字段正则/子串匹配 | 精确命中 102 条 + 宽口径 14,447 条 |
| 排序与精选层 | 按 stars 降序、安装量辅助 | TOP 20 列表及官方说明 |
| 主题分布层 | 对宽口径结果做关键词聚合 | 选股/量化、A股/行情、美股等子主题命中数 |
| 报告输出层 | Markdown 表格 + 机器可读 JSON | `akshare_mcp_matches.json` + handoff 文档 |

---

## 四、如何选型（方法论）

面对「海量 skill 中找某一类能力」的通用问题，可按以下步骤执行：

1. **明确关键词**：不仅看核心库名（akshare），还要看同类能力关键词（量化、选股、A股行情等）。
2. **多字段扫描**：name、slug、description、tags、upstream_url、homepage 一个都不能少。
3. **双口径设计**：精确口径保证「确实是它」；宽口径保证「功能等价也不漏」。
4. **用 stars + installs 排序**：开源社区用脚投票，比官方描述更真实。
5. **输出双格式**：人看 Markdown，机器读 JSON，方便下游自动化安装或看板展示。
6. **标注可信度**：凡是数字都要标 T0/T1/T2，避免读者把估算当官方。

---

## 五、深化学习指引

| 方向 | 推荐来源 | 可信度 |
|---|---|---|
| SkillHub 官方 API 与数据格式 | SkillHub 官方文档 / api.skillhub.cn | T0 |
| akshare 库本身用法 | akshare 官方文档（akshare.akfamily.xyz） | T0 |
| 中文金融数据接口对比 | 「china-stock-data」skill 作者 @kekewater 的 MCP 实现 | T1 |
| 量化选股实践 | 《A股量化 AkShare》skill 官方说明 | T1 |
| MCP 协议基础 | modelcontextprotocol.io 官方规范 | T0 |

---

## 六、技术结合点（1+1>2）

- **本清单 + china-stock-data skill**：先在 SkillHub 找到合适的数据 skill，再通过 `china-stock-data` 做多源校验（通达信 + 腾讯财经 + AKShare + iWencai）。
- **本清单 + model-rate-limit-radar skill**：对筛选出的高 stars skill 做限流探测，确认免费档是否稳定可用。
- **本清单 + task-implement skill**：把「安装并实测某个 akshare skill」写成 `.task/` 契约，让 agent 自动执行验收。
- **本清单 + tri-agent-investigation skill**：对陌生 skill 的三方来源、版本、作者做快速安全审计后再安装。
