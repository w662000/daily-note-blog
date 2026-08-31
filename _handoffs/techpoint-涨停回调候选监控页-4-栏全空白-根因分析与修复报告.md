---
layout: default
title: 技术点 · 涨停回调候选监控页「4 栏全空白」根因分析与修复报告
date: 2026-08-31 23:30:00 +0800
---

# 技术点 · 涨停回调候选监控页「4 栏全空白」根因分析与修复报告

> 来源：260831_涨停回调候选监控页「4 栏全空白」根因分析与修复报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：2026-08-31-21-55-16\涨停回调页空白_根因修复报告.md
- 报告方：WorkBuddy（本机排查 + 浏览器实测验证）
- 交付对象：lobsterai（请在**生成器源码**层面修复，见第 2 节）
- 不是数据问题，也不是行情接口问题。是**生成出来的 HTML 里的 JavaScript 有 3 个 bug**，其中 1 个是致命的：`render()` 函数在第 358 行对一个用 `const` 声明的变量重新赋值，抛出 `TypeError` 中断执行，导致后面给 4 个栏位填内容的语句一行都没跑到。持仓面板因为走独立定时器，所以照常显示。
- ```
C:\Users\Administrator\lobsterai\project\scan_realtime.py
```
- ```
// 593 行：用 const 声明
const card='<div class="stk '+cls+'">'
  + fbTag
  + '<div class="top">…'
  + '</div>';

// 606 行：给同一个 const 重新赋值 → 抛异常
card=card.replace(/<\/div>$/, '<button class="latbtn" onclick="quickLatent(\''+it.sym+'\',…)</button></div>');
```
- **浏览器实测报错**：
- ```
TypeError: Assignment to constant variable.
    at render (涨停回调候选股.htm:358:11)
```
- ```
tick(); restartTimer();                        // 拉行情 → render() → 画 4 栏（崩在这条）
renderHold(); setInterval(renderHold, 10000);  // 持仓，独立定时器，不受影响
```
- ```
// 第 540 行附近
const srcs=[[loadTencent,''],[loadEast,'https://push2.eastmoney.com'],[loadEast,'https://push2delay.eastmoney.com']];
fn(codes, host, ok=>{ … });   // ← 传 3 个参数
```
- ```
function loadTencent(codes, done){   // ← 只有 2 个
    …
    done(ok && qsSymOk(codes));      // done 实际收到的是 host（空字符串 ''）
}
```
- ```
TypeError: done is not a function
    at s.onload (涨停回调候选股.htm:248:5)
```

## 三、关键产物与命令
- `C:\Users\Administrator\lobsterai\project\选股\涨停回调候选股.htm`（产物行号：229 / 329 / 345 / 358）
- `C:\Users\Administrator\lobsterai\project\选股\涨停回调候选股_fix.htm`（同上，行号一致）

这两个文件我已直接改好并验证通过，同时留了备份：
- `涨停回调候选股_20260831_220354.bak`
- `涨停回调候选股_fix_20260831_220354.bak`

> ⚠️ **重要**：产物是静态生成的（`CANDS`/`ALLPOOL` 是写死在 HTML 里的常量）。**改完 `scan_realtime.py` 后必须重新生成一次产物**，否则下次自动重跑会用旧模板覆盖掉我临时打的补丁，问题原样复现。

---

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
