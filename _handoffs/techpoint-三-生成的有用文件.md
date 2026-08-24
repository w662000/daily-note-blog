---
layout: default
title: 技术点 · 三、生成的有用文件
date: 2026-08-21 23:30:00 +0800
---

# 技术点 · 三、生成的有用文件

> 来源：260821_三、生成的有用文件_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| download.py | `D:\AI work\workbuddy\涨停回调回测\download.py` | 新浪源批量落盘日线（幂等/重试/限速） |
| backtest.py | `D:\AI work\workbuddy\涨停回调回测\backtest.py` | 首板/2连板涨停回调回测核心 |
| backtest_ma.py | `D:\AI work\workbuddy\涨停回调回测\backtest_ma.py` | 6均线×3放量 36组合入场对比 |
| backtest_ma_sqlite.py | `D:\AI work\workbuddy\涨停回调回测\backtest_ma_sqlite.py` | 改用 lobsterai stocks.db 重跑 |
| backtest_by_day.py | `D:\AI work\workbuddy\涨停回调回测\backtest_by_day.py` | 板后第几天买点胜率分析 |
| 通达信选股公式.txt / 通达信选股公式_EMA7放量版.txt | `D:\AI work\workbuddy\涨停回调回测\` | 通达信选股公式（2连板右侧放量突破） |
| data/ | `D:\AI work\workbuddy\涨停回调回测\data\` | 4561 只日线 CSV（约 508M） |
| 回测报告.html + 明细 csv | `D:\AI work\workbuddy\涨停回调回测\results_sqlite\` | 最终回测结果与明细 |
| 板后第几天买入胜率分析.html | `D:\AI work\workbuddy\涨停回调回测\results_sqlite\` | 按板后天数分组胜率分析 |
| Gridea 自动同步·独立兜底 | automation-1787285013065（每日 23:15） | Gridea render+push 兜底，根除单点脆弱 |

### 关键技术要点（自动抽取）
- | 文件 / 目录 | 路径 | 用途 |
- | download.py | `D:\AI work\workbuddy\涨停回调回测\download.py` | 新浪源批量落盘日线（幂等/重试/限速） |
- | Gridea 自动同步·独立兜底 | automation-1787285013065（每日 23:15） | Gridea render+push 兜底，根除单点脆弱 |

## 三、关键产物与命令
- | download.py | `D:\AI work\workbuddy\涨停回调回测\download.py` | 新浪源批量落盘日线（幂等/重试/限速） |
- | backtest.py | `D:\AI work\workbuddy\涨停回调回测\backtest.py` | 首板/2连板涨停回调回测核心 |
- | backtest_ma.py | `D:\AI work\workbuddy\涨停回调回测\backtest_ma.py` | 6均线×3放量 36组合入场对比 |
- | backtest_ma_sqlite.py | `D:\AI work\workbuddy\涨停回调回测\backtest_ma_sqlite.py` | 改用 lobsterai stocks.db 重跑 |
- | backtest_by_day.py | `D:\AI work\workbuddy\涨停回调回测\backtest_by_day.py` | 板后第几天买点胜率分析 |

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
