---
layout: default
title: 每日工作总结 · 2026-11-14
date: 2026-11-14 23:30:00 +0800
---

# 多 Agent 每日工作日志 · 2026-11-14

> 机器汇总（模型不可用，原文按 agent 分节保留，未做润色）

## 一、WB 国内版（wb-cn）
> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-14.md, D:\AI work\workbuddy\2026-11-13-20-41-08\.workbuddy\memory\2026-11-14.md


# 2026-11-14 工作日志

## towertop.kdns.fr 停在 10-12 排查 → 总根子修复（13:00-13:30）
- 站点解封三层修复，全部完成并线上实测：
  1. **Gridea 渲染+推送恢复**：手动跑 gridea_auto_sync.py（UTF-8 环境）两次成功 push（13:06、13:16、13:23），昨夜列车 step7 的 GBK emoji 崩溃已由 publish_train.py 的 PYTHONUTF8=1 环境修复（今晨列车虽 0/10 但原因见下）。
  2. **总根子：frontmatter 格式**。Gridea 渲染器只认 `date:` 字段；1837 篇稿件里 1800 篇用的是自动化写稿惯例的 `createdAt:`（自 2026-07-19 techpoint 起）→ 渲染器全程跳过，站点只出过 37 篇原生格式的旧稿。这是独立于 gh token 死亡的第二个平行根因。
  3. **修复**：repair_gridea_date.py 按文件名推日期补 `date:`（1795 篇，posts 目录整备份至 posts_backup_20261114_1314）；8 位数文件名(2026MMDD)被 6 位规则截断成错值的 6 篇由 fix_8digit_dates.py 修正；repair 脚本的 derive_date 规则顺序已改正（先 8 位再 6 位）。
- 线上终验（curl 实测标题）：`每日工作总结 · 2026-11-13` ✓、`2026-10-25` ✓ 均已上线。
- 源头堵漏：handoff_flow.py gen_gridea() 补 `date: 20YY-MM-DD`（yymmdd 推导，作用域已验证）；generate_daily_summary.py write_gridea() 补 `date:` + tags 列表格式。
- 今晨 10:20 列车 0/10 原因：step1/2/3 超时（751 篇 handoff 积压 × 每篇 40-60s，600/1800s 超时只够啃 10 篇）；step4-7 秒败原因未查（待查，可能与夜间残留进程/git 锁相关，锁现已不存在）。手动复现证明管道本身健康（90 秒发出 1.5 篇，Gridea/博客/phpBB 全通）。
- 遗留待办：① handoff 751 篇积压消化策略（需调大列车步超时 + schtasks 30 分钟执行上限，或单独长跑）；② bbs1org body>20000 字符限制导致部分长 handoff 永远发不上（需截断策略）；③ 750 篇积压全发是否造成论坛刷屏，待用户定调。
- 陷阱记录：Git Bash heredoc 会吃反斜杠，正则测试必须写成文件执行（昨天误判 re 模块损坏即为 heredoc 假象，re_health_check.py 实测托管 py 与 venv py 均健康）。

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

## 首页只到 10-24 排查（15:35-15:50）
- 用户反馈首页列表停在 10-24。三层新发现：
  1. 浓缩稿 frontmatter 内联 tags/createdAt 会让文章页渲染但不进列表（normalize_gridea_digest.py 规范化 93 篇为原生格式：id/title/date/published/tags 块式）；
  2. 文件名必须是 6 位 YYMMDD——8 位名（20261001工作总结.md）不被列表索引。根源是 backfill 用 8 位 ymd 查重导致重复件。rename_digest_yymmdd.py 统一改名 14 篇、去重隔离 15 篇（posts/_dup_8digit）；
  3. 手写 -c 里的 \n 被 bash 转成 /n 造成 tags 污染，normalize 已修复。
- 终验：本地渲染首页含 10-28/29/30/31

## 二、WB 国际版（wb-intl）
> 数据源：D:\workspace\workbuddyai\2026-11-13-21-01-54\.workbuddy-ai\memory\2026-11-14.md


# 2026-11-14 工作日志

## wb-orchestrator：免费模型降级链失效修复（CodeBuddy Hy4/Hy3）

### 背景
用户发现 WB 国际版免费模型只剩 Hy4/Hy3，担心调度器（wb-orchestrator）和多 agent teams
项目无法继续零成本运行。要求改成「优先 hy4free、失败降级 glm-5.3-flash」的多级 fallback。

### 关键实测（T0，`node orchestrator.mjs models --refresh`）
- CodeBuddy CLI catalog 共 **23 个模型**，`x0.00` 只有 **2 个**：`hy4free`、`hy3`
- **`deepseek-v4.1-flash` 和 `step-5-preview` 已从 catalog 移除**（只剩付费 `-sg` 版 x0.11）
- 因此旧链 `['deepseek-v4.1-flash','step-5-preview','hy3']` 前两项永久 absent，
  实际一直掉到最弱的 hy3；`hy4free` 从未进链
- 低倍率档位：`gpt-6-luna` x0.07、`glm-5.3-flash` x0.08、`minimax-m3.1-flash` x0.08
- `custom-local:GLM-5.3-Flash` / `custom-local:spark-x2.6` credits=null（走 wb-bridge 18901，不吃积分）

### `--fallback-model` 的结论（T0，`codebuddy --help`）
- 单值 `<model>`，**只能填 1 个**，不支持链式
- **only works with `--print`**；本项目走 `--serve` + ACP，该参数完全不生效
- 多级 fallback 只能在项目代码里实现（已有 `pickFreeModel`）

### 改动文件（6 个）
1. `lib/model-catalog.mjs`
   - `FREE_MODEL_PREFERENCE` → `['hy4free','hy3']`
   - 新增 `LOW_COST_FALLBACK_PREFERENCE = ['glm-5.3-flash','minimax-m3.1-flash','gpt-6-luna']`
   - 新增 `MAX_LOW_COST_CREDITS = 0.15`（硬上限，防误配 gpt-6-astra x6.67）
   - 新增 `creditNumber()`；`pickFreeModel()` 支持 `allowPaidFallback` 选项，
     返回新增 `billed` 字段；新增 `how` 值 `requested-lowcost` / `fallback-lowcost`
2. `lib/judge.mjs`
   - CliJudge 默认 model `deepseek-v4.1-flash` → `hy4free`，新增 `allowPaidFallback: false`
   - 调 `pickFreeModel` 时透传 `allowPaidFallback`；`billed` 时累计 `stats.billedPicks` + warning
3. `peers.json`
   - `codebuddy.autoStart.args` 的 `--model` → `hy4free`
   - `judge.model` → `hy4free`；更新 `_comment`
4. `tests/model-catalog.test.mjs` 全部重写（18 例，含 opt-in / ceiling 场景）
5. `README.md` / `SKILL.md` 文档同步

### 验证
- `node --test tests/*.test.mjs` → **78/78 通过**
- `node orchestrator.mjs models` → 服务按新配置启动正常，23 模型 / 2 free
- 备份：`D:/workspace/workbuddyai/wb-orchestrator_bak_20261114_1750`（diff 校验 byte-identical）

### 待复查
- **2026-11-15 23:59 官方限免到期**，需确认 `hy4free` 是否仍在 catalog、是否仍 x0.00
- 若 hy4free 下架：默认行为是**报错停跑**（严格免费）；需要继续跑则显式开
  `judge.allowPaidFallback=true` / `--allow-billed`

## 三、AutoClaw 1.15（autoclaw-115）

今日无机器日志记录。

## 四、ZCode（zcode）

今日无机器日志记录。

## 五、总计

- 当天有日志的 agent：2/4
- 日志总字符数：9343