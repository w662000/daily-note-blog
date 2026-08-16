---
layout: default
title: 技术点 · slg-resume-plan（AutoClaw 项目表）— 交接文档
date: 2026-08-12 23:30:00 +0800
---

# 技术点 · slg-resume-plan（AutoClaw 项目表）— 交接文档

> 来源：260812_autoclaw-slg-resume-plan_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260812_autoclaw-slg-resume-plan_handoff.md（编码探测：utf-8）
- > 背景：2026-08-09 实测确认微信对"新浏览器环境"做了环境级风控（任何新 profile 窗口 2 秒内"请重新登录"，即使正常扫码）。同日已停止全部自动化并清理。
- 原理：把用户真实 Edge profile（含登录态、指纹、历史）完整复制到非默认目录，Playwright 用它启动——微信看到的是"熟悉的浏览器环境 + 已有登录态"，理论上不触发环境风控，且**无需扫码**。
- 2. 运行克隆脚本（约 1-3 分钟）：
- ```
   powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\edge-profile-clone.ps1
```
- 3. 修改抓取脚本 profile 路径（把 `D:\edge-pw-profile` 写入）：
- ```
   # 复制 tmp 下的脚本到 workspace 正式位置，改 PROFILE 变量
   Copy-Item C:\Users\Administrator\.openclaw-autoclaw\workspace\.openclaw\tmp\pw_repost2.py C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\slg_repost_grab.py
```
- ```
   python slg_repost_grab.py 九牧手游助手
```
- ```
   python slg_repost_grab.py 九牧配将君; sleep 30; python slg_repost_grab.py 九牧手游攻略站; ...
```
- 抓取脚本固定用 `D:\edge-pw-profile`；微信 cookie 2-3 天过期 → 每 2 天重新克隆一次 profile（覆盖复制）刷新登录态；或接受每周重克隆
- 方案设计：`D:\AI work\workbuddy\2026-08-02-18-41-45\wewe-rss-test\SLG_A方案_wewe-rss_实测与多方案设计_2026-08-02.md`
- 主机部署：`SLG_A方案_主机决策_Wispbyte_2026-08-02.md`（7 步命令齐全）

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
- ❌ 反复新建浏览器实例弹登录页（触发环境风控的直接原因）
- ❌ 向新实例注入 cookie（被识别为自动化）
- ❌ 风控期连续重试（加深标记；每次失败后至少停 24h）
- ✅ 只在"用户真实环境"（真实 profile 或复制品）里操作
- ✅ 每号每天 1 次搜索、间隔 ≥30 秒、count ≤10
