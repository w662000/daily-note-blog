---
layout: default
title: 项目流 · 2026-11-16
date: 2026-11-16 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-16.md

## 00:38-00:42 有道云全清重传：暂停待明早开机续跑（用户要关机）
- 已暂停三个旧 agent 型 automation（与 23:15 列车并发冲突实锤，昨晚 23:15 轮因此 4 步 FAIL）：
  automation-1784700756809（23:00 五端发布）/ 1785476214373（23:05 scan）/ 1784951947030（23:07 主链）→ 全部 PAUSED。
- YD_Rebuild 改为 **/sc onlogon 计划任务**（pythonw 无窗口跑 collect_delete_rebuild_v2.py）：用户明天开机登录后**自动续跑**。当前运行实例已终止、残留 CLI 进程已清（youdaonote.exe 0 个）。
- 脚本状态：PHASE 1 收集会全量重扫（三目录约 1.5~2 万条，40~60 分钟）→ 15 路并发删除（DELRESULT 断点续删）→ 修好的 upload_youdao 重传 → 三目录复核计数。
- 预计明早登录后 2~3 小时完成；进度 = 会话目录 youdao_rebuild_progress.log；产物 = youdao_full_inventory.json / youdao_delete_all_result.json / youdao_reupload.log / youdao_final_state.json。
- ⚠️ 注意：若明天开机时间在 10:00-10:30，晨检 automation（有道云补发 10:15 等）与重传的 upload_youdao 可能并发互踩——重传的删除阶段不受影响，重传阶段若撞上，错峰手动 `schtasks /run /tn YD_Rebuild` 即可。
- 验收点：①三目录 final counts 合理（约 80~100 篇干净快照）；②`youdao_reupload.log` 无 FAIL；③归一化标题无 (n) 副本。
- 待办：跑完验收后 `schtasks /delete /tn YD_Rebuild /f` 删掉一次性任务；11:00 failover 巡检会核对 4 端。

## 10:18 事故自查自纠方案 + skill 固化
- 交付 `自查自纠方案_有道云重复事故_20261116.md`（会话目录）：S 级定性、五层根因链（①查重只读第一页 ②list 显示延迟 ③CLI 静默改名副本 ④高频调度放大 ⑤零对账监控）、AI 操作层追责（禁止全量同步当调试手段）、G1~G5 写入门禁（数据源完备性 planted-count / 静默失败探针 / 写入规模熔断 / 台账 / 周期对账）、SOP 六步、回归验证清单。
- 固化用户级 skill `~/.workbuddy/skills/external-write-idempotency-gate/SKILL.md`：以后任何"向外部存储写入 + 自称幂等"的项目强制过 G1~G5 闸门。与 safe-bulk-write-guardrail（磁盘落盘）互补。
- 未闭环：0c 的 _save_youdao 换 search 兜底（等重传完成后做，planted-count 测试）；G5 周期对账任务待注册。

## wb-intl（WB 国际版）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）