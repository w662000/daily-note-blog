---
layout: default
title: 交接文档 · 复盘：au（autoclaw）的 handoff 生成流程与效果
date: 2026-08-16 23:30:00 +0800
---

# 复盘：au（autoclaw）的 handoff 生成流程与效果

- **日期**：2026-08-16
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-16-10-57-55\复盘_au_handoff流程_20260816.md

> 来源：`C:\Users\Administrator\.openclaw-autoclaw\workspace\reports\20260816_日志读取与handoff生成流程报告.html`
> 核实方式：亲自盘磁盘 + 读实际产出文件（非仅信报告）。
> 日期：2026-08-16

## 一、au 流程（6 阶段，已核实）

1. **日志源定位**：`os.walk`+`glob` 扫两时代日志——OpenClaw 8/7+ 的 `memory/YYYY-MM-DD.md`、WorkBuddy 8/4-8/6 的 `D:\AI work\workbuddy\2026-08-0X\*.md`。⚠️ **但路径扫了 ≠ 真纳入**：au 在"项目识别聚合"阶段仍以 OpenClaw 8/7 启动为界做了减法，实际**减掉了 8/4-8/6（WB 时代）**的产出（见第七节，用户已纠正）。
2. **编码探测读取**：`read_any()` 依次 utf-8→gbk→gb18030 取无 `\ufffd` 者；**不经 shell 重定向**（PowerShell `>` = UTF-16）；复杂逻辑写 `.py` 不写 `python -c`。脚本真在 `.openclaw/tmp/`（报告路径笔误写成 `.openclaw-tmp`）。
3. **项目识别聚合**：判定标准 ✅完结（交付物+验证闭环）/🟡阶段完结 /🔴不写（挂起·被证伪）；同主线跨天合并、同主题小项合并。
4. **模板批量生成**：9 字段模板 + `dict列表→TEMPLATE.format`；命名 `YYMMDD_项目名_handoff.md`（兼容 `^\d{6}_.+_handoff\.md$`）。
5. **校验+索引**：列目录核对 + 生成 `readme.md` 按日期分组导航。
6. **交付**：覆盖表 + 领域分组 + 索引链接。

## 二、效果核实（trust-but-verify 结论）

- **实际产出**：`C:\Users\Administrator\.openclaw-autoclaw\workspace\handoff\` 下 **16 份** `*_handoff.md` + 1 份 `readme.md` + 1 份 HTML 修复报告（共 18 文件）。
- **报告虚高**：HTML 报告称"33 份 handoff + 1 索引"，README 自己写"共 16 个"。**以磁盘和 README 为准 = 16 份**。报告 metric 不可信，视为预期值/笔误。
- **质量抽查**（TradingAgents-CN 那份）：9 字段齐全、绝对路径完整（含 `.bak`、看门狗脚本）、"后续/风险"写了 systemd 周期重启不影响 + IP 变重跑脚本——是真能交接的 handoff，非流水账。

## 三、值得我（WorkBuddy）学的 4 点

1. **handoff 目录加 README 索引**（我最大 gap）：我的 `D:\AI work\workbuddy\handoff\` 有 34+ 份但无索引，应补「日期分组+链接+一句话」。
2. **编码探测 `read_any()`**：读 WB 旧日志（8/4-8/6）前先探测编码，别赌 UTF-8。
3. **聚合判定标准**（完结/阶段完结/不写）：做历史回填时显式用，别只跟着 automation 走。
4. **9 字段模板**（尤其"来源"+"关键产物绝对路径"+"后续/风险含过期时间/重打方法"）：我那份总表 handoff 只写了"来源"头，未完整 9 字段。

## 四、要警惕的 2 点

1. **报告数量必须盘磁盘核实**：au 报告 33 与实际 16 矛盾，自嗨式总结会误导下游。
2. **目录隔离**：au 的 handoff 在 `.openclaw-autoclaw/workspace/handoff/`，WB 的 scan automation 扫不到，**不冲突**；但若 au 往 WB 的 `D:\AI work\workbuddy\handoff\` 写，会与"幂等防重复发布"逻辑打架。

## 五、我的独特贡献（au 未覆盖）

今天往 handoff 收件箱放总表时解决了 **scan 每晚自动再生成一份→发两次** 的幂等问题：用"精确同名文件名让 scan 检测到已存在即跳过"。au 报告无此逻辑（其 handoff 是独立管线、不担心重复发布）。该技巧 WB 特有，已固化在本次会话。

## 六、可信度

- 流程/脚本存在/README/16 份质量：**T1**（亲自盘磁盘+读文件）。
- "33 份/11 日志源"：**不可信**（与磁盘 16 份及 README 自述矛盾）。
- 报告本身来源：au 自述复盘（T3 内部文档），关键项已交叉核实。

## 七、🚨 用户纠正：handoff 统计「参与优先」原则（2026-08-16 补，等同红线）

- **事实**：au 的 16 份 handoff 全部是 8/7 之后（收件箱无 `0804/0805/0806` 开头），**WB 8/4-8/6 被减掉**。盘磁盘确认 WB 那三天 daily log 真实存在且有实质项目：限流雷达四迭代 / Groq·Hermes skill / 75 模型工具调用实测 / 笔记本选型+handoff / Hermes Desktop 五轮攻坚 / Gridea 竞态修复 / Debian 装机等。
- **根因**：au 误用"日期/工具优先"——以 OpenClaw 8/7 启动为界，把之前 WB 时代当"旧时代"在聚合阶段砍掉。其报告里 `2026-08-04`/`WorkBuddy` 等字样只是"读到了源"，聚合阶段仍按客户端启动日切。
- **用户红线**：**handoff/工作总结的统计范围 = 用户参与过的所有项目，不论工具（WB 还是 au/OpenClaw），不以启动日期/工具切换为界做减法。** 8/4-8/6 是用户在 WB 亲自参与的项目，必须统计进来。
- **我的连带失误**：本节第一版写"✅ 合理，避免漏读"——判断过于乐观，已改为"路径扫了 ≠ 真纳入"。trust-but-verify 必须在「产出」层验，不能只看"源定位"阶段。
- **固化**：已写入 `~/.workbuddy/MEMORY.md` 的 au 借鉴点段，作为跨项目红线。
