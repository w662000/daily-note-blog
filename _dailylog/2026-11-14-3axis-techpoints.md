---
layout: default
title: 技术点 · 2026-11-14
date: 2026-11-14 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-14.md, D:\AI work\workbuddy\2026-11-13-20-41-08\.workbuddy\memory\2026-11-14.md

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

## 首页只到 10-24 排查（15:35-15:50）
- 用户反馈首页列表停在 10-24。三层新发现：
  1. 浓缩稿 frontmatter 内联 tags/createdAt 会让文章页渲染但不进列表（normalize_gridea_digest.py 规范化 93 篇为原生格式：id/title/date/published/tags 块式）；
  2. 文件名必须是 6 位 YYMMDD——8 位名（20261001工作总结.md）不被列表索引。根源是 backfill 用 8 位 ymd 查重导致重复件。rename_digest_yymmdd.py 统一改名 14 篇、去重隔离 15 篇（posts/_dup_8digit）；
  3. 手写 -c 里的 \n 被 bash 转成 /n 造成 tags 污染，normalize 已修复。
- 终验：本地渲染首页含 10-28/29/30/31/11-01/11-13；线上 curl 实测同 ✓。全清单覆盖 260718→261113（11-02~11-12 无日志无总结属正常空档）。
- 教训沉淀：Gridea 稿件命名铁律 = YYMMDD 前缀 + 原生四字段 frontmatter；generate_daily_summary write_gridea 需同步改 6 位命名（待办）。

## 续跑收尾（16:20-16:35）
- 收件箱剩 59 → 分类：真项目 34 / 日志碎片 19 / 退化命名 6 / 超长 1。19 篇碎片已隔离；handoff_flow 论坛正文加 18000 字截断（bbs1org 2 万上限）。
- 闸门误伤修正：中文占比 <30% 拦截了真项目（Cloudflare 调研/SearXNG/8850 端口等英文代码多）→ 放宽到 <8%（假货由「来源字段」判定兜住）；upload_youdao 同步放宽。
- 论坛核查口径更正：handoff 发在 bbs1org#3 / phpBB#11（工作日志在 #2/#10）；精确匹配假标题集后 #3/#11 均 0 命中假货（此前结论是口径错但结论不变）。
- 有道云全量分页真实规模 3750 条 / 假笔记 875 篇（此前分页低估）；--kill 重启（w52rkn），进度落盘 logs/youdao_cleanup_progress.log。
- handoff 发布重启（syqKuM），此前已发约 61 篇；博客残留 commit 已推（0 未推送）。
- 待后台结束后：gridea_auto_sync 终渲染 + 全端复核 + 最终对账。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-13-21-01-54\.workbuddy-ai\memory\2026-11-14.md

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

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）