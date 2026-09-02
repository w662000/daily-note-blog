---
layout: default
title: 技术点 · 三、生成的有用文件（表格：文件/目录 | 路径 | 用途）
date: 2026-08-20 23:30:00 +0800
---

# 技术点 · 三、生成的有用文件（表格：文件/目录 | 路径 | 用途）

> 来源：260820_三、生成的有用文件（表格：文件_目录 _ 路径 _ 用途）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
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

### 关键技术要点（自动抽取）
- | 文件/目录 | 路径 | 用途 |
- | nvidia_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_test.py` | NVIDIA NIM 温和测速脚本（间隔 3s／超时 15s／串行），
- | nvidia_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_test.py` | NVIDIA NIM 温和测速脚本（间隔 3s／超时 15s／串行），实测 15 个模型 TTFT |
- | supplement_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\supplement_speed_test.py` | 速度补测脚本（针对雷达不可达渠道温和重试） |
- | build_score_table.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\build_score_table.py` | 活清单综合评分表生成脚本（性能×0.85＋速度×0.15） |

## 三、关键产物与命令
- | nvidia_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_test.py` | NVIDIA NIM 温和测速脚本（间隔 3s／超时 15s／串行），实测 15 个模型 TTFT |
- | nvidia_speed_test.json | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_test.json` | 15 个模型实测 TTFT 原始数据 |
- | nvidia_speed_table.html | `D:\AI work\workbuddy\2026-08-20-11-25-37\nvidia_speed_table.html` | NVIDIA 速度榜可视化（S/A/B/超时分级） |
- | supplement_speed_test.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\supplement_speed_test.py` | 速度补测脚本（针对雷达不可达渠道温和重试） |
- | supplement_speed.json | `D:\AI work\workbuddy\2026-08-20-11-25-37\supplement_speed.json` | 补测结果数据 |
- | build_score_table.py | `D:\AI work\workbuddy\2026-08-20-11-25-37\build_score_table.py` | 活清单综合评分表生成脚本（性能×0.85＋速度×0.15） |
- | 活清单综合评分表.html | `D:\AI work\workbuddy\2026-08-20-11-25-37\活清单综合评分表.html` | 36 个模型综合评分可视化表（含 Top5 与 14 个 N/A 标注） |
- | 2026-08-19_每日工作总结.md | `D:\AI work\workbuddy\2026-08-19_每日工作总结.md` | 10:00 离线兜底补发的 08-19 总结（语雀源＋博客源双推成功） |

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
