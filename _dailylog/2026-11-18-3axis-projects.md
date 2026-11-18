---
layout: default
title: 项目流 · 2026-11-18
date: 2026-11-18 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-17-22-32-26\.workbuddy\memory\2026-11-18.md, D:\AI work\workbuddy\2026-11-18-14-41-01\.workbuddy\memory\2026-11-18.md

## 19:25 接口恢复检测 + 补发项目流/技术点（已执行写入）
- 单次 list 探测接口：1.5s rc=0 → 已恢复(守温和红线,未轰炸)。
- search 查重:工作日志 True(已存不动),项目流/技术点 None(抽风);改用 list 全量核实确认两篇确实缺失。
- 复用官方 publish_3axis_extra._save_youdao 补发成功:项目流 ID=121BDCFAFCD14DB3AE9DD67A5B6D2DB9 / 技术点 ID=8C53B507FC184ACD8EFF4F63FEB72792。
- G3熔断(expected2/实际2)、G4台账(handoff/youdao_backfill_ledger.json)、G5 list回查(项目表31→32,技术点1→2,ID一致无重复)全部通过。
- 提醒:全清重建仍未收尾(final_state 仍缺),去重未跑;本次只补11-18两篇。详情见 进度/进度_20261118_1925.md。

## 19:36 重大纠错 + 三轴全量重传（用户催办"别墨迹"）
- **纠错**:之前说"7.7万条要重传"是错的!inventory 77028 = 全删的垃圾重复副本清单,不该重传;真正要传的是本地干净素材 644 篇(归一化582唯一:工作日志141/项目表221/技术点220)。
- **真相**:全量 list 分页拉尽后,云端三目录几乎全空——工作日志仅1篇(今天step0c传的)、项目表32、技术点2。昨天quickfill传的596篇全没了(疑似11-17晚~18之间又被清一次)。缺约550篇,根本没补发完。
- **行动**:用户要求"去重先不跑,先全部上传"。备份陈旧断点(quickfill_result.json.bak-stale-20261118)后清空,启动 quick_fill.py 全量直传(4路温和并发,list_titles跳过云端已有的3篇不重复)。后台 task NeBamN,输出 Temp/quickfill_run_20261118.out。
- 待传完后核验三目录计数是否回到~582唯一。去重仍按用户要求暂缓。

## 20:38 全量重传完成 + 核验通过(收尾)
- quick_fill 19:45 跑完:611/611 成功,零失败(按轴 工作日志141/项目表233/技术点237)。
- 全量 list 分页拉尽核验:云端 工作日志142/项目表222/技术点221;本地唯一 141/221/220;三轴缺失全部=0。每轴云端+1是今天step0c单独传的3篇(标题格式略不同),正常。
- 熔断复核:无 .ALLOW_YD_DELETE 授权文件=删除默认禁止;删除日志末条仍是19:43 CIRCUIT-BREAK,无新删除动作。
- 至此"7月中旬至今三轴文档"全部补齐,delete BUG已熔断。去重仍按用户要求暂缓。YD_Rebuild_Logon任务本体仍在(无害,待用户决定是否删)。

## wb-intl（WB 国际版）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）