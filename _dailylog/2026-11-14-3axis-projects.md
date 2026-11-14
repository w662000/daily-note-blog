---
layout: default
title: 项目流 · 2026-11-14
date: 2026-11-14 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-14.md, D:\AI work\workbuddy\2026-11-13-20-41-08\.workbuddy\memory\2026-11-14.md

## 假 handoff 清理 + 日志 4 端补发（13:30-14:20，用户指令）
- 假货规模与来源：收件箱 751 篇中 630 篇假货 = ① 10-10 hermes-upgrade 源码文档树 147 篇（docusaurus/i18n docs）② 11-12 专家包审计 session 收割的 485 篇专家定义 md。根因：handoff_flow scan 的 tier-2「主题 markdown」递归收割项目内文档树。
- 清理（全部隔离备份不删除）：收件箱 630 篇→handoff/quarantine_20261114_1330；Gridea 草稿 1355 篇→posts_quarantine_20261114_1330；博客 _handoffs git rm 1208 篇并推送（8fdd46a，剩 535 篇）；techpoint 2 篇。论坛实测零污染（70 帖全是每日工作日志）。
- 护栏补丁（handoff_flow.py）：_walk_md_recursive 排除 专家包/website/src-*/youdao_tmp 等；tier-2 只认 session 根目录 md + 中文占比≥30%；SKIP_SECTION_RE 增加 交付物/当前状态/分工/关键文件/警告/^任务$/^进度$/注意事项。dry-run 验证：假货全挡、真货 120 篇已在收件箱（昆明收租/抖音运营/SearXNG 评审等，无需重新生成）。
- 日志审计（audit_daily_logs.py v2）：10-01→11-14 共 45 天，30 天有日志，9 天有日志缺总结（10-10,10-28,10-29,10-30,11-04,11-09,11-11,11-12,11-14）。注意：递归 glob 单次要 40s，须一次全量收集（v1 按日查询被超时假杀）。
- 批量补发 backfill_daily_4ends.py：45 天 ×（补总结→补 Gridea 浓缩稿→sync_logs 博客/语雀源→论坛发帖）。CF 免费档 neurons 一天只够 1-2 篇生成 → 批量切 --engine deepseek（deepseek-flash），日常单日生成仍用 CF 双模型。后台任务 VRnRcS 运行中。
- generate_daily_summary.py 新增 --digest-only 模式。
- 后续队列：补发完成 → Gridea 渲染推送 → handoff_flow publish 发 120 篇真货 4 端（约 2 小时，bbs1org 2 万字符上限会卡部分长文，需截断策略待定）。

## 为什么论坛没混假货 + 三脚本闸门落地（14:20-14:40，用户追问）
- 论坛干净的真相（三重运气而非防护）：①假货生成(10-10/11-12)到发布能力恢复(11-13)隔了一个月，期间论坛端从未跑过 handoff 发布；②bbs1org 2 万字符上限天然拦掉大部分长文档 handoff；③发布按文件名排序+每轮 600s 超时只啃 10 篇，假货 261010/261112 排在队尾还没轮到。Gridea/博客沦陷因为它们是每篇 handoff 的第一、二步且无任何校验；博客 push 失效期间假货堆进本地 git 历史，token 恢复后一次性冲上去。
- 第 5 端（有道云）也沦陷：upload_youdao 项目表/技术点轴直接从 blog/_handoffs 取材，11-13/11-14 镜像了假笔记到云端（项目表 100 条 + 技术点 2000+ 条中 892 条命中假标题，(13)/(14) 后缀即上传日）。
- 云端清理：youdao_fake_cleanup.py（游标分页 list → 标题规范化匹配假标题集 629 → delete 逐条 3s 间隔），后台 --kill 运行中。
- 本地 techpoint 二次清理：quarantine_techpoint_fakes.py 按 slug 反查隔离 121 篇（update 剩 21、bak 剩 139 全真）。
- 三脚本闸门（防复发）：handoff_flow.py `_is_bogus_handoff()`（来源指向文档树 / 中文占比<30% 拒发）；upload_youdao.py 项目表/技术点轴同款中文占比闸门；techpoint_flow 源=已净化收件箱（scan 护栏前置兜底）。

## 下午进度对账（15:30）
- 45 天日志 4 端补发：已完成（上一会话后台任务跑完）——Gridea 工作总结稿 54 篇（10-11 月全覆盖）、博客 _dailylog 32 篇、未推送 commit 0、论坛全发。Gridea 渲染推送 15:32 完成，线上实测「每日工作总结 · 2026-10-05」已上线。
- 有道云假笔记清理：昨晚会话中断只删约 87 篇；复扫发现云端规模此前被分页低估（项目表 1550 + 技术点 1500 = 3050 条，v1 只读到 100）。当前剩 805 篇假笔记，--kill 已重启后台（NEn3VD）。
- handoff 真货 120 篇 4 端发布：已启动后台长跑（U2HW09，无超时，约 2 小时）。

## 论坛碎片帖删除（16:45-17:00，用户指令）
- bbs1org#3 / phpBB#11 的 11-14「碎片标题」交接帖各 35 篇（共 70）已删，复核剩余 0。
- MCP tools/list 实测两端都没有 delete 工具 → 走 FTP 一次性 PHP 维护脚本（密钥+三重 GUARD：ID清单∩版块∩11-14标题），执行后立即删远端脚本。bbs1org 删 app_topics/replies/favorites/notifications；phpBB 删 posts/topics/watch/track + 重算版块计数。
- 踩坑：phpBB 禁用 $_GET（deactivated_super_global→General Error），须用 $request->variable()。
- 防复发：handoff_flow.py 新增 FRAG_TITLE_RE 碎片标题闸门，dry-run 验证碎片被拦、真项目放行。
- 新发现（未处理，待用户定夺）：分页拉全后 #3 有 400 帖、#11 至少 1000 帖（官方计数 5142 主题），含 10-23 448 + 10-25 323 篇早期外文文档帖（Hermes 文档树/专家包误收割，与已清假货同源）；70 篇碎片在博客/Gridea 也有同内容副本，是否一并清理待确认。
- 交付报告：会话目录「论坛碎片帖清理报告_20261114.md」；一次性脚本已移入 logs/。

## 全量清理（17:00-17:15，用户「全部一起清理」）
- 旧外文帖真实规模 1910 篇（此前分页只读到 771）：phpBB#11 服务器侧 SQL 全量扫描（交接文档·+10-23/25+中文占比<30% 或 8 个 Hermes 中文译名），先 dry 报数+样例、命中数 700-2000 才 go，删 posts/topics/watch/track 并重算版块计数；复用 dry 脚本复核 MATCH=0。bbs#3 无外文帖（26 篇中文，其中 12 碎片未动、14 真项目保留）。
- 70 篇碎片的本地副本：clean_frag_copies.py 按 frontmatter title 精确匹配（注意 CRLF 与 bash 反斜杠坑，须用脚本文件），博客 _handoffs 35 篇 + Gridea posts 35 篇移入隔离备份；博客推送 1520a47、Gridea 重渲染推送完成，首页碎片残留 0。
- 轻微代价：skillhub 重筛清单 10-23 旧副本因中文占比<30% 被删，11-14 正本仍在，内容未丢。
- 有道云删除任务会话中断（进度 75/739）后重启（Zl52PP）。
- 交付：会话目录「全量清理总账_20261114.md」。

## 后台任务进度对账（17:20）
- handoff 4 端发布实质完成：收件箱 120→8（6 退化+1 碎片被闸门拦+1 真项目「旧插件清理」待 23:15 列车发）；bak 1353→1385(+32)；博客 _handoffs 595、未推送 0；Gridea posts 557。
- Gridea 终渲染 17:15 推送完成，output/api/search.json 实测含新发项目（深度研究/昆明收租/SearXNG/Q6）。
- 有道云删除：16:36 中断在 75/739，17:12 重启（Zl52PP），瓶颈是每次重启都要游标分页全量盘点 3750+ 条云端笔记；已给 youdao_fake_cleanup.py 加断点续删（成功 ID 落盘 logs/youdao_deleted_ids.txt，重启跳过已删），当前进程用旧代码，下次中断即生效。
- 交付：会话目录「后台任务进度对账_20261114.md」。

## 4端发布升级·多agent 探查结论（17:30）
- 4 个 agent 日志源：wb-cn=D:/AI work\workbuddy\**\.workbuddy\memory\；wb-intl=D:/workspace/workbuddyai/**/.workbuddy-ai/memory/（10-14 归纳文件写明）；autoclaw-115=C:/Users/Administrator/.openclaw-autoclaw/workspace/memory/；zcode 无日志文件，只有 ~/.zcode/cli/db/db.sqlite（session 26 / message 1955），需按日聚合。
- 三轴既有实现：handoff/upload_youdao.py 的 collect_workbuddy_entries + collect_autoclaw_entries（工作日志/项目表/技术点），仅发有道云第5端。10-14 有三份 daily-summary-{wb-cn,wb-intl,autoclaw-115}.md 历史模板。
- 现有链：generate_daily_summary.py(单篇) → sync_logs_to_github.py(单文件→博客+语雀源) → publish_worklog_to_forums.py(单文件→#2/#10) → Gridea 浓缩稿；handoff_flow/techpoint_flow 只认 WB 国内版收件箱。
- 用户要求升级为「统计 4 agent 当天日志后再发布 工作日志/项目流/技术点 三轴到 4 端」，因涉及文章形态（产品可见），已用 AskUserQuestion 确认口径，待确认后实现。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-13-21-01-54\.workbuddy-ai\memory\2026-11-14.md

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）