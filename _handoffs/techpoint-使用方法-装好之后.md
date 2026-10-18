---
layout: default
title: 技术点 · 使用方法（装好之后）
date: 2026-10-18 23:30:00 +0800
---

# 技术点 · 使用方法（装好之后）

> 来源：261018_使用方法（装好之后）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
```bash
dsh --profile web        # 启动 web UI
```
然后用自然语言下令，例如：
> Use AgentTeams to review the commits after v0.5.3 from performance, security, and product perspectives. Return one consolidated report.

- 团队状态落盘在 `/.agent-teams/`，Web UI 右上角有实时活动面板
- 配置默认开箱即用；trusted profile 可覆盖 `stateDir / memberProvider / memberModel / memberMaxDepth`
- 边界：一个队长同时只带一个活跃团队；成员空闲时邮件持久化；并发进程编辑同一团队不协调

---

### 关键技术要点（自动抽取）
- ```
dsh --profile web        # 启动 web UI
```
- 配置默认开箱即用；trusted profile 可覆盖 `stateDir / memberProvider / memberModel / memberMaxDepth`
- 边界：一个队长同时只带一个活跃团队；成员空闲时邮件持久化；并发进程编辑同一团队不协调

## 三、关键产物与命令
- （见源文档）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
