---
layout: default
title: 技术点 · 用户级 Skill 清单 v1.4（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单 v1.4（~_.workbuddy_skills）

> 来源：260814_用户级 Skill 清单 v1.4（~_.workbuddy_skills）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260814_用户级 Skill 清单 v1.4（~_.workbuddy_skills）_handoff.md（编码探测：utf-8）
- | 1 | `agent-plan-router` | 1.0.0 | 我参与制定 | A/B/C 计划路由(A=六顶思考帽+RACI+多Agent；B=情境路由；C=PDCA) | 用A计划执行/用A执行 |
- | 4 | `favicon-picker` | — | 我参与制定 | 为网页/看板生成 favicon 多候选方案 | （无显式触发词；按需求描述语义触发） |
- | 6 | `gentle-ratelimit-test` | 1.0.0 | 我参与制定 | 温和验证模型/API 限流(429/503)，单次低频不轰炸 | 测限流 |
- | 8 | `model-rate-limit-radar` | 2.0.0 | 我参与制定 | 对活清单全模型按平台并发探测限流，本地看板(8849) | 模型测限流雷达 |
- | 10 | `port-list` | — | 我参与制定 | 本机开放端口清单看板(netstat 扫描+项目标注+本地 http 展示) | 端口清单、扫描端口、端口列表、哪些端口开着、开放端口、本机端口、netstat 查端口、命令行查端口。 |
- | 13 | `tri-agent-investigation` | — | 我参与制定 | 陌生API/错误码三方调查法(调查员+规划+红队) | （无显式触发词；按需求描述语义触发） |
- | 16 | `wechat-mp-crawler-cookie-fix` | 2.0.0 | 我参与制定 | 微信公众平台爬虫静默0条故障排障(含2026-07-30接口关停) | （无显式触发词；按需求描述语义触发） |
- | 17 | `win-py-daemon-launcher` | 1.0.0 | 我参与制定 | Windows 下 .bat 一键启 Python 服务避坑 | （无显式触发词；按需求描述语义触发） |
- | 19 | `wispbyte-vps-gost-proxy` | — | 我参与制定 | wispbyte VPS gost 代理 | （无显式触发词；按需求描述语义触发） |
- | 21 | `playwright-browser-automation` | 2.0.0 | 其他 | Direct Playwright API for browser automation without MCP complexity. Navigate websites, in | （无显式触发词；按需求描述语义触发） |
- `node_modules` 内的 Playwright 依赖不计入。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
