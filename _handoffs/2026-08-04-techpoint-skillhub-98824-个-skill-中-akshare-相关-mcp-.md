---
layout: default
title: 技术点 · skillhub 98824 个 skill 中「akshare 相关 MCP Skill」重筛清单
date: 2026-08-04 23:30:00 +0800
---

# 技术点 · skillhub 98824 个 skill 中「akshare 相关 MCP Skill」重筛清单

> 来源：handoff《skillhub 98824 个 skill 中「akshare 相关 MCP Skill」重筛清单》（2026-08-04）

## 一、技术选型

- **数据来源**：SkillHub 全站 skill 元数据（`skillhub_all.json`，98,824 条）。
- **匹配策略**：对 `name / slug / description / description_zh / tags / labels / category / source / upstream_url / homepage` 做大小写不敏感匹配，命中 `akshare` 即计入。
- **输出口径**：
  - 精确命中 `akshare`：102 个；
  - 宽口径金融数据类（akshare 同类能力）：14,447 个，其中仅命中宽口径的 3,656 个。
- **筛选工具链**：Python + JSON 批量处理 + 正则/子串匹配，结果落盘为 `akshare_mcp_matches.json`。

## 二、实施要点与关键技术

1. **多字段联合匹配**：不能只看 `name`，很多 skill 在 `description` 或 `upstream_url` 里才暴露 akshare 依赖。
2. **去重与分级**：
   - 严格匹配（strict_akshare）才是可直接替代/对接 akshare 的 skill；
   - 宽口径只能作为「同类能力」参考池，不能等同 akshare。
3. **TOP 排序**：按 `stars` 降序取前 20 做展开说明，避免 102 条平铺无法阅读。
4. **可信度标注**：所有数据来自 SkillHub API 元数据（一手来源），未做运行时验证；安装量、认证状态以元数据为准。

## 三、模块职责划分

| 模块 | 职责 |
|---|---|
| 数据采集 | 导出/获取 `skillhub_all.json` |
| 匹配引擎 | 多字段子串匹配，输出 strict / broad 两类 |
| 精选展示 | 按 stars 排序，TOP 20 提取官方 description |
| 分布统计 | 宽口径按主题分类计数 |
| 产物输出 | `akshare_mcp_matches.json` + 人类可读 Markdown 清单 |

## 四、如何选型（方法论）

- 若目标是「直接用 akshare 能力」：只从严匹配 102 个里挑，优先看 `akshare-stock`（235 stars，13,337 安装）。
- 若目标是「金融数据能力全覆盖」：把 14,447 个宽口径结果当候选池，再按 stars/安装量/认证状态二次过滤。
- 若做量化选股/回测：重点关注 `quant-backtest-strategy`、`a-stock-multi-factor-screener`、`quant-stock-selector`。
- 若做每日复盘/资金流：关注 `csm-20260430`、`china-etf-flow-premarket`、`china-margin-financing-premarket-akshare`。

## 五、深化学习指引

- **akshare 官方文档**：https://www.akshare.xyz/（T0，一手来源）
- **SkillHub 技能广场**：https://skillhub.cn/（T0，数据来源）
- **量化相关 UP/博主**：B站/知乎搜索「akshare 量化」「AKShare 教程」，注意甄别是否用最新版（akshare 接口变动频繁，优先看 2025–2026 年内容）。
- **回测框架对比**：Backtrader、VeighNa、Qlib 与 skill 中宣称的 OneQuant/米筐/聚宽接口需实测匹配度。

## 六、技术结合点（1+1>2）

- **akshare + 通达信/同花顺**：用 akshare 拉盘后数据，通达信做公式选股，实现「数据获取—策略筛选—可视化」闭环。
- **akshare skill + WorkBuddy MCP**：把筛选出的 MCP skill 接入 WorkBuddy，直接在对话中查行情/财报/资金流。
- **重筛方法可复用**：把 `akshare` 关键词替换成 `tushare`、`jqdata`、`akshare`、`eastmoney`，即可批量筛选其他金融数据源 skill。
- **榜单固化**：把 TOP 20 写成「全球AI排行榜」类文章，每日/每周自动更新，成为可沉淀的内容资产。
