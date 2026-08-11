---
layout: default
title: 交接文档 · china-stock-data 安装扫描报告
date: 2026-08-10 23:30:00 +0800
---

> 来源：2026-08-04-20-35-31\china-stock-data-扫描报告.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# china-stock-data 安装扫描报告

> 扫描时间：2026-08-04 20:56（GMT+8）
> 安装位置：`C:\Users\Administrator\.workbuddy\skills\@kekewater\china-stock-data`
> 来源：SkillHub CLI `skillhub install china-stock-data --namespace kekewater`

## 一、整体结构

```
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

## 二、版本号不一致（小瑕疵）

| 文件 | version 字段 | 值 |
|---|---|---|
| `SKILL.md` frontmatter | `version:` | **2.0.0** |
| `_meta.json` | `version` | **1.7.0** |

两个版本号对不上，建议以 `_meta.json` 的 1.7.0 为准（发布平台元数据更权威）。不影响使用，仅信息不一致。

## 三、依赖清单（requirements.txt）

- **核心（必装）**：requests / beautifulsoup4 / lxml / pandas(≥2.0) / openpyxl / pytdx / **akshare(≥1.14.0)**
- **可选（注释掉，需各自账号）**：wencai / jqdatasdk / rqdatac / tushare
- **本机现状**：上一轮已装核心 6 项（含 pytdx）+ pandas/openpyxl；**akshare 尚未装**（report/moneyflow 依赖）。

## 四、子命令清单（china_stock.py，共 16 个）

| 命令 | 用途 | 数据源 | 前置 |
|---|---|---|---|
| `quote <code>` | 智能行情（TDX→腾讯→iFinD 自动降级） | 多源 | 免 Key |
| `tdx-quote <code>` | 通达信实时+5档盘口 | TDX | pytdx |
| `tdx-kline <code> [period]` | TDX K线(日/周/月/60min) | TDX | pytdx |
| `tencent-quote <code>` | 腾讯财经(PE/PB/市值/换手) | 腾讯 | requests |
| `tencent-batch <c1,c2>` | 腾讯批量行情 | 腾讯 | requests |
| `ifind-quote <code>` | 同花顺iFinD专业行情 | iFinD | ifind_config.json |
| `report <code> [n]` | 研报查询 | AKShare | akshare |
| `announce <code> [n]` | 公告查询(CNINFO→Tushare→AKShare降级) | 多源 | akshare/tushare |
| `moneyflow <code> [n]` | 资金流向 | AKShare | akshare |
| `sector` | 板块排行 | 同花顺 | requests |
| `themes` | 热点题材(行业+概念) | 同花顺 | requests |
| `search <query>` | 问财语义搜索 | iWencai | `WENCAI_TOKEN` |
| `tushare-ann <code>` | 公告查询(Tushare Pro) | Tushare | 见下★ |
| `jq-financial <code>` | 财报数据 | JQData | `JQ_USER`/`JQ_PASS` |
| `jq-macro` | 宏观数据 | JQData | `JQ_USER`/`JQ_PASS` |
| `status` | 数据源状态总览 | - | - |

辅助脚本命令：
- `news_aggregator.py`：`daily` / `headlines` / `indices`
- `stock_monitor.py`：`check` / `watchlist`
- `sec_edgar.py`：美股 SEC 数据（具体子命令见其 usage）
- `daily_briefing_image.py`：直接运行生成简报图

## 五、🔴 安全发现：脚本内硬编码 Tushare token

`scripts/china_stock.py` **第 512 行**：

```python
TUSHARE_PRO = ts.pro_api('c8dbb3833192a3e47991b1975ad02d95a6567988826e519ba76b0ef5')
```

- 一个 **Tushare Pro token 被明文写死在脚本里**，随 skill 一起分发——任何装这个 skill 的人都能拿到这个 token。
- 与 skill 自身设计不一致：问财/聚宽/米筐/同花顺都走环境变量或配置文件，唯独 Tushare 硬编码。
- 风险：该 token 可能被原作者在 Tushare 后台限流/作废；且属他人密钥，不应随包扩散。
- 建议：改为从环境变量 `TUSHARE_TOKEN` 读取（保留向后兼容），删除明文 token。

> 此改动属于对安装产物的修改，需你确认后再动（避免擅自改写你的 skill）。是否要我把它改成读 `TUSHARE_TOKEN` 并清掉明文？

## 六、需配置的密钥/账号汇总

| 来源 | 配置方式 | 状态（本机） |
|---|---|---|
| 通达信 TDX | 免 Key（需 pytdx） | ✅ 已装（沙箱出网拦截） |
| 腾讯财经 | 免 Key | ✅ 可用 |
| 同花顺 iFinD | `ifind_config.json`(access/refresh token) | ⚠️ 未配 |
| AKShare | 仅 `pip install akshare` | ❌ 未装 |
| iWencai 问财 | `WENCAI_TOKEN` 环境变量 | ⚠️ 未配 |
| JQData 聚宽 | `JQ_USER`/`JQ_PASS` | ⚠️ 未配 |
| Tushare Pro | **硬编码 token（见上★）** / 或 `TUSHARE_TOKEN` | ⚠️ 硬编码 |
| RiceQuant 米筐 | `RQ_USER`/`RQ_PASS` | ⚠️ 未配 |

## 七、与下午 akshare 筛选清单的关联

本 skill 的 slug `china-stock-data` 正是下午（19:44 会话）akshare 筛选清单里的 **第 24 行**（`kekewater/china-stock-data`，3⭐）。它本身依赖 akshare，属"含 akshare 家族"。