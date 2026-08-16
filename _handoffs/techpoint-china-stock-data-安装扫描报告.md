---
layout: default
title: 技术点 · china-stock-data 安装扫描报告
date: 2026-08-04 23:30:00 +0800
---

# 技术点 · china-stock-data 安装扫描报告

> 来源：260804_china-stock-data 安装扫描报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260804_china-stock-data 安装扫描报告_handoff.md（编码探测：utf-8）
- ```
china-stock-data/
├── _meta.json          (135 B)  版本元数据
├── SKILL.md            (13.9 KB) 技能说明（frontmatter 含 version）
├── requirements.txt    (565 B)  依赖清单
├── scripts/                      5 个 Python 脚本
│   ├── china_stock.py     (28.4 KB) 主 CLI（16 个子命令）
│   ├── news_aggregator.py (9.4 KB)  新闻聚合（daily/headlines/indices）
│   ├── daily_briefing_image.py (9.8 KB) 每日简报图生成
│   ├── stock_monitor.py   (3.8 KB)  价格监控（check/watchlist）
│   └── sec_edgar.py       (4.3 KB)  美股 SEC Edgar 数据
└── references/                   6 篇 API 参考笔记
    ├── cninfo-api.md                巨潮资讯 API
    ├── cninfo-pdf-extraction.md     CNINFO PDF 提取
    ├── eastmoney-limitations.md     东方财富限流备忘
    ├── tdx-protocol-notes.md        通达信 TDX 协议笔记
    ├── tdx-rate-limiting.md         TDX 限速/反封指南
    └── tonghuashun-headlines-api.md 同花顺快讯 API
```
- **本机现状**：上一轮已装核心 6 项（含 pytdx）+ pandas/openpyxl；**akshare 尚未装**（report/moneyflow 依赖）。
- | 命令 | 用途 | 数据源 | 前置 |
- | `quote <code>` | 智能行情（TDX→腾讯→iFinD 自动降级） | 多源 | 免 Key |
- | `announce <code> [n]` | 公告查询(CNINFO→Tushare→AKShare降级) | 多源 | akshare/tushare |
- | `search <query>` | 问财语义搜索 | iWencai | `WENCAI_TOKEN` |
- 辅助脚本命令：
- `sec_edgar.py`：美股 SEC 数据（具体子命令见其 usage）
- ```
TUSHARE_PRO = ts.pro_api('c8dbb3833192a3e47991b1975ad02d95a6567988826e519ba76b0ef5')
```
- 一个 **Tushare Pro token 被明文写死在脚本里**，随 skill 一起分发——任何装这个 skill 的人都能拿到这个 token。
- 与 skill 自身设计不一致：问财/聚宽/米筐/同花顺都走环境变量或配置文件，唯独 Tushare 硬编码。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
