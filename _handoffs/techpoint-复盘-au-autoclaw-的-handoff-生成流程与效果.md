---
layout: default
title: 技术点 · 复盘：au（autoclaw）的 handoff 生成流程与效果
date: 2026-08-16 23:30:00 +0800
---

# 技术点 · 复盘：au（autoclaw）的 handoff 生成流程与效果

> 来源：260816_复盘：au（autoclaw）的 handoff 生成流程与效果_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 1. **日志源定位**：`os.walk`+`glob` 扫两时代日志——OpenClaw 8/7+ 的 `memory/YYYY-MM-DD.md`、WorkBuddy 8/4-8/6 的 `D:\AI work\workbuddy\2026-08-0X\*.md`。⚠️ **但路径扫了 ≠ 真纳入**：au 在"项目识别聚合"阶段仍以 OpenClaw 8/7 启动为界做了减法，实际**减掉了 8/4-8/6（WB 时代）**的产出（见第七节，用户已纠正）。
- 2. **编码探测读取**：`read_any()` 依次 utf-8→gbk→gb18030 取无 `\ufffd` 者；**不经 shell 重定向**（PowerShell `>` = UTF-16）；复杂逻辑写 `.py` 不写 `python -c`。脚本真在 `.openclaw/tmp/`（报告路径笔误写成 `.openclaw-tmp`）。
- **实际产出**：`C:\Users\Administrator\.openclaw-autoclaw\workspace\handoff\` 下 **16 份** `*_handoff.md` + 1 份 `readme.md` + 1 份 HTML 修复报告（共 18 文件）。
- **质量抽查**（TradingAgents-CN 那份）：9 字段齐全、绝对路径完整（含 `.bak`、看门狗脚本）、"后续/风险"写了 systemd 周期重启不影响 + IP 变重跑脚本——是真能交接的 handoff，非流水账。
- 2. **编码探测 `read_any()`**：读 WB 旧日志（8/4-8/6）前先探测编码，别赌 UTF-8。
- 4. **9 字段模板**（尤其"来源"+"关键产物绝对路径"+"后续/风险含过期时间/重打方法"）：我那份总表 handoff 只写了"来源"头，未完整 9 字段。
- 2. **目录隔离**：au 的 handoff 在 `.openclaw-autoclaw/workspace/handoff/`，WB 的 scan automation 扫不到，**不冲突**；但若 au 往 WB 的 `D:\AI work\workbuddy\handoff\` 写，会与"幂等防重复发布"逻辑打架。
- 今天往 handoff 收件箱放总表时解决了 **scan 每晚自动再生成一份→发两次** 的幂等问题：用"精确同名文件名让 scan 检测到已存在即跳过"。au 报告无此逻辑（其 handoff 是独立管线、不担心重复发布）。该技巧 WB 特有，已固化在本次会话。
- 流程/脚本存在/README/16 份质量：**T1**（亲自盘磁盘+读文件）。
- **事实**：au 的 16 份 handoff 全部是 8/7 之后（收件箱无 `0804/0805/0806` 开头），**WB 8/4-8/6 被减掉**。盘磁盘确认 WB 那三天 daily log 真实存在且有实质项目：限流雷达四迭代 / Groq·Hermes skill / 75 模型工具调用实测 / 笔记本选型+handoff / Hermes Desktop 五轮攻坚 / Gridea 竞态修复 / Debian 装机等。
- **根因**：au 误用"日期/工具优先"——以 OpenClaw 8/7 启动为界，把之前 WB 时代当"旧时代"在聚合阶段砍掉。其报告里 `2026-08-04`/`WorkBuddy` 等字样只是"读到了源"，聚合阶段仍按客户端启动日切。
- **我的连带失误**：本节第一版写"✅ 合理，避免漏读"——判断过于乐观，已改为"路径扫了 ≠ 真纳入"。trust-but-verify 必须在「产出」层验，不能只看"源定位"阶段。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
