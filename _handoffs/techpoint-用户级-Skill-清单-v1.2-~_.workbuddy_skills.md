---
layout: default
title: 技术点 · 用户级 Skill 清单 v1.2（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单 v1.2（~_.workbuddy_skills）

> 来源：260814_用户级 Skill 清单 v1.2（~_.workbuddy_skills）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260814_用户级 Skill 清单 v1.2（~_.workbuddy_skills）_handoff.md（编码探测：utf-8）
- > 扫描时间：2026-08-14 ｜ 共 **51** 个用户级 skill（已剔除 node_modules 依赖）
- | 1 | `agent-plan-router` | 1.0.0 | 手动补进 | A/B/C 计划路由(A=六顶思考帽+RACI+多Agent；B=情境路由；C=PDCA) |
- | 2 | `agent-reach` | 1.0.0 | 自动 | 无需API的跨平台调研与素材采集 |
- | 5 | `favicon-picker` | — | 自动 | 为网页/看板生成 favicon 多候选方案 |
- | 7 | `gentle-ratelimit-test` | 1.0.0 | 自动 | 温和验证模型/API 限流(429/503)，单次低频不轰炸 |
- | 9 | `model-rate-limit-radar` | 2.0.0 | 自动 | 对活清单全模型按平台并发探测限流，本地看板(8849) |
- | 11 | `port-list` | — | 手动补进 | 本机开放端口清单看板(netstat 扫描+项目标注+本地 http 展示) |
- | 14 | `tri-agent-investigation` | — | 自动 | 陌生API/错误码三方调查法(调查员+规划+红队) |
- | 17 | `wechat-mp-crawler-cookie-fix` | 2.0.0 | 手动补进 | 微信公众平台爬虫静默0条故障排障(含2026-07-30接口关停) |
- | 18 | `win-py-daemon-launcher` | 1.0.0 | 自动 | Windows 下 .bat 一键启 Python 服务避坑 |
- | 20 | `wispbyte-vps-gost-proxy` | — | 自动 | wispbyte VPS gost 代理 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
