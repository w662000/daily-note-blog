---
layout: default
title: 项目流 · 2026-11-16
date: 2026-11-16 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-16.md, D:\AI work\workbuddy\2026-11-16-11-32-53\.workbuddy\memory\2026-11-16.md

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

## 11:31-11:40 继续完成未闭环三项
- ①有道云全清重传（核心，后台 YD_Rebuild 自动跑）：进度 worklog 收完 14986 / projects 收完 40042 / techpoints 收集到 40页2000篇仍在翻页；三目录总量约 5.5 万条（远超之前估的 2 万）。WMI 确认 pythonw+youdaonote 进程存活正常，日志每 10 页落盘。删→传→复核待跑。
- ②0c 的 _save_youdao 查重补修：`publish_3axis_extra.py` 第 285 行旧单次 list 查重后加 `yd.run_search_exists()` 兜底（复用 upload_youdao 已修好的全库 search），查询失败 None 时宁漏勿重跳过。备份 `backup/publish_3axis_extra.py.bak-0csearch-20261116`，语法通过。
- ③G5 周期对账落地：新建 `D:\AI work\workbuddy\youdao_g5_reconcile.py`（只读/只碰三目录/全 subprocess 带 CREATE_NO_WINDOW/重建未完成自动跳过/搜近7天三轴标题查副本+目录首副本占比>5%告警），产出 logs/youdao_g5_YYYY-MM-DD.json。注册 automation `automation-1794800083381`（每周一09:00·ACTIVE）。撞车保护实测通过。
- 至此自查自纠方案的 0c 尾巴 + G5 落地全部闭环；仅剩重建任务跑完验收 + 删 YD_Rebuild 一次性任务。

## 13:10-13:13 GLM 免费模型补全(T1 官方文档核实)
- WebSearch T1(docs.bigmodel.cn/pricing+model-overview)核实免费清单：文本 glm-4.7-flash(200K主力)/glm-4-flash-250414/glm-4.5-flash(即将下线)；视觉 glm-4.6v-flash(128K)/glm-4.1v-thinking-flash/glm-4v-flash；生成类 CogView-3-Flash/CogVideoX-Flash 不进文本清单。**用户记的 GLM-4.6V-Flash 属实；不带flash的 GLM-4.6V 收费(1~2元/M)**。
- 探针3枪全过：glm-4.7-flash 854ms、glm-4.6v-flash 10.6s(慢)、glm-4v-flash 662ms(纯文本输入会幻觉描述图片，已标注视觉)。
- 写入3个→models.json 41条；GLM API 平台现役6个全免费零删除(z1-flash 历来免费但T1清单未列,标注)。注意 glm-5.2=SenseNova、z-ai/glm-5.3-flash=NIM,是别家平台的GLM权重,不属智谱收费体系。
- 45秒客户端重写但内容一致。GLM 目录接口 /models 只返回12个不含免费系,补全要靠官方文档+直接探针。

## 夜秣git副业雷达 首跑
- 用户要求用刚装的 skill「yemo-git-radar」（夜秣git副业雷达，作者夜秣）跑一轮看效果。
- 技能目录：C:\Users\Administrator\.workbuddy\skills\yemo-git-radar；Python 用 managed 3.13.12。
- 无 GitHub token → 自动走轻量通路（抓网页+raw，不耗 API 额度，慢 1-2 分钟）。doctor 体检通过。
- 完整流程：doctor → run → translate --todo → 手写 data/translate.json（8 条精修）→ translate --apply → translate 体检(100%) → render。
- 产物：data/reports/Git副业雷达_2026-11-16.html，另拷一份到本项目 outputs/Git副业雷达_2026-11-16.html。
- 今日入选 8 个，前三：aerial-tv(S/97)、daily_stock_analysis(S/91，今日涨4548)、rea-video(S/80)。榜首推荐 aerial-tv。
- 首次跑完按技能契约询问定时；用户要「每天11:30」→ 建 automation id `automation-1794800521709`（RRULE FREQ=DAILY;BYHOUR=11;BYMINUTE=30），并跑 sched --done 收尾。
- 坑：手写译文 JSON 时中文正文里嵌套英文双引号会破坏 JSON，改用中文「」才通过。已在 automation prompt 里写明提醒。
- 进度备查：进度/进度_20261116_1138.md。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-13-15-32-52\.workbuddy-ai\memory\2026-11-16.md, D:\workspace\workbuddyai\2026-11-15-22-54-25\.workbuddy-ai\memory\2026-11-16.md

## 同日早前：项目星图扫描器 A+B+C+D 全修复
- 详见扫描日志与星图项目目录；星图 111→122 节点，扫描器 discovery-v2 口径。

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-16.md

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）