---
layout: default
title: 交接文档 · 进度_20261116 — Gridea 老浓缩稿重复 + wb-cn 空日志 bug 修复
date: 2026-11-17 23:30:00 +0800
---

# 进度_20261116 — Gridea 老浓缩稿重复 + wb-cn 空日志 bug 修复

- **日期**：2026-11-15
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-11-15-10-21-36\进度_20261116_Gridea浓缩稿修复.md

## 用户报告
线上 https://towertop.kdns.fr/post/261115工作总结/ 写着「每日工作总结 · 2026-11-15 / WB国内版（wb-cn）今日无机器日志记录」，但当天实际有大量日志。用户指出：①已有多Agent工作日志在总结，这个浓缩稿重复；②即使重复，15号 wb-cn 不可能没日志。

## 根因（两条，证据链）
1. **老浓缩稿是独立 automation 在每天无条件重写**：`automation-1787577004866`「Gridea 浓缩版补发·qwen垫底（10:10）」每天 10:10 触发，prompt 第 2c 步明写"Gridea 浓缩版已存在则仍安全重写（保留 id）"——它无条件覆盖 YYMMDD工作总结.md。10:20:41 写入时间戳与它吻合。这条是"还有老脚本在写"的元凶。
2. **空日志定稿**：wb-cn 当天日志 `D:\AI work\workbuddy\.workbuddy\memory\2026-11-15.md` 创建时间 10:35:16，而 step0 10:20:01 就跑了（列车日志：日志仅 195 字符），那一刻 wb-cn 日志不存在 → LLM 按 prompt 写"今日无机器日志记录"。且 `generate_daily_summary.py` 幂等（总结文件已存在则跳过）导致空档永久定稿，后续 11:xx 用真实日志重生成的三轴没回写进 Gridea 浓缩稿。

## 修复（用户拍板：停掉老浓缩稿 + step0 改总结昨天）
| 改动 | 文件/对象 | 内容 |
|---|---|---|
| 1 | `generate_daily_summary.py` | 加 `--with-gridea` 开关，默认不写 Gridea 浓缩稿；列车不传该参数 → 自动停写。备份 `backup/generate_daily_summary.py.bak-gridea-20261116` |
| 2 | `publish_train.py` | 加 `SUMMARY_DATE`（当前 hour<12→昨天，hour≥12→当天），step0 用它。两个列车任务 Command/Arguments 完全相同，故用时间判断，不改计划任务（规避 schtasks 编码坑）。备份 `backup/publish_train.py.bak-gridea-20261116` |
| 3 | automation | 暂停 `automation-1787577004866`（Gridea 浓缩版补发 10:10）——根上的修复 |
| 保留 | automation | `automation-1784739275903`（补总结+博客源+语雀，不写Gridea）、`automation-1787285013065`（Gridea 渲染推送，不生成内容） |

## 验证
- py_compile 两脚本通过。
- 日期判断纯计算验证：早班 hour=10 → 2026-11-15（昨天）；晚班 hour=23 → 2026-11-16（当天）。
- 未实跑列车（带外部发布副作用，不能当测试）。
- 排查确认：仅 `generate_daily_summary.py` 一个活跃脚本写浓缩稿；计划任务只有两个列车任务（都走 publish_train.py）；automation 命中的其他都是历史文档。

## 遗留 / 注意
- 线上那篇错误稿（11-15 浓缩版）按用户选择**未补正**（用户选"停掉"而非"停掉+补正"）。如需补正，用真实总结重写 `C:\Users\Administrator\Documents\Gridea Pro\posts\261115工作总结.md` 再跑 gridea_auto_sync.py。
- 10:20 列车当前进程是改代码前启动的旧实例（用旧代码），下次触发（今晚 23:15 / 明早 10:20）才用新逻辑。
- 现有 Gridea 历史浓缩稿不删（用户决策）。
