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

## 4端发布升级·多Agent三轴（18:05，详见 cwd 报告）
- 新脚本：multi_agent_sources.py / publish_3axis_extra.py；generate_daily_summary.py --multi（CF 双模型+纯拼接兜底）；publish_train.py 加 step0c_3axis_publish、step4 改只补历史。
- 4 agent 源：wb-cn=D:/AI work\workbuddy\**\.workbuddy\memory；wb-intl=D:/workspace/workbuddyai/**/.workbuddy-ai/memory；autoclaw-115=~/.openclaw-autoclaw/workspace/memory；zcode=~/.zcode/cli/db/db.sqlite 按日聚合（只读）。
- 当天实跑：博客3页/Gridea渲染/论坛6帖/有道云3笔记全部成功；CF 429 时纯拼接兜底不漏发。


# 2026-11-14 工作日志（本会话）

## 近 10 天双雷达「最靠谱模型 TOP20」分析（19:50–20:05）

用户要求：读测速雷达 + 限速雷达报告，总结最近 10 天约 20 个最靠谱模型，出数据分析表格，至少覆盖 3–5 个 API 提供平台（活清单有十几个平台）。

### 数据源与规模（T0，纯本地只读，全程未发 API 请求）
- 测速雷达：`D:/AI work/workbuddy/model-speed-radar/data/history.jsonl`（57 轮 / 5,219 条）、`latest.json`（round 717, 11-14 18:28）
- 限速雷达：`C:/Users/Administrator/.cache/rate-limit-radar/data/history.jsonl`（16 轮 / 1,462 条 / 18,645 次 15 连发）、`latest.json`（round 189, 11-14 19:47）
- 窗口 2026-11-05 00:00 ~ 11-14 19:47；**历史全集 92 模型 / 14 平台**，最新快照 87 模型 / 13 平台

### 口径与踩坑（重要，下次直接复用）
1. 限速雷达 `untestable=True` = 整轮不可测（鉴权/网络/模型下架），`rate_limited/success_rate` 为 None，**必须剔除而非记 0 分成功**，否则把通道故障错判成限流。源码 `ratelimit_daemon.py:400-405`。
2. 测速雷达 `skipped=True` = 慢模型当天冷却，剔除出分母。
3. **Python falsy 陷阱**：`x or 100` 会把 `429率=0.0` 当成缺省值，导致所有零限流模型被门槛排除。必须写 `x if x is not None else 100`。
4. **模型全集必须取「窗口内历史出现过的所有 id」，不能用 `latest.json`**：11-14 有 5 个 `@cf/*` 被停测，只用 latest 会漏掉 CF 全部模型（而它们正是 11-13 榜的 T1 主力）。
5. **Cloudflare 真实状态**：5 个 `@cf/*` **仍在 `C:/Users/Administrator/.workbuddy/models.json`（94 条）**，是 `model-speed-radar/config.json` 的 `skip_models` 排除出雷达轮询；配置注释 `_comment_cf_skip`：「2026-11-14 用户指令：@cf 系列排除出雷达轮询，额度让给发布链（直连生成+雷达互抢免费额度）」。不是模型删除、不是模型坏了。
6. **每日趋势跳变**：11-05/11-06 整体成功率 6.7%/7.25%，11-07 跳到 31.52%。查 `err_kind` 确认是**本机网络出口故障**（测速雷达 314 / 256 次 `network` 错误），11-07 恢复后错误转为稳定的 `http_4xx` / `model_gone`。该曲线不能读作平台质量趋势。

### 公式
`靠谱分 = 100 × (0.50×限速10天成功率 + 0.30×测速10天成功率 + 0.20×速度分) ÷ 权重和`；速度分 = TTFT 中位数对数归一（300ms→1.0，5000ms→0.0）。入榜门槛：限速≥60 次可测调用、测速≥10 有效轮、429率≤10%。**能力分（T1 10-13 公开基准 / T2 08-02 干活榜）只展示、不参与加权**（量纲不同且非近 10 天实测）。

### 结论
- 前 5：`glm-4.1v-thinking-flash` 93.39 / `deepseek-flash` 91.76 / `glm-z1-flash` 91.02 / `glm-4-flash-250414` 90.18 / `deepseek-v4-pro` 89.61
- `deepseek-flash` 是唯一 240/240 全成功、零限流的通用模型；DeepSeek 官方平台近 10 天 99.79% 成功、0% 429
- TOP20 覆盖 5 个平台（GLM API / DeepSeek / NVIDIA NIM / Cloudflare / Xunfei）；平台汇总覆盖全部 14 个
- 不可用：Agnes-AI 429率 92%、SenseNova 83%、WeChat 100%、OurFreeModel 24 个模型 0 成功（全是 `other_errors` 而非限流）
- 与 11-13 单晚 TOP20 榜的差异来自：10 天聚合 vs 单晚快照、能力分不计入、CF 停测；两边共同确认的稳模型一致

### 产物（均在本会话目录）
`最近10天最靠谱模型TOP20_2026-11-14.md`（11 章完整报告）、`近10天模型可靠性明细_2026-11-14.csv`（92×26）、`近10天平台可靠性汇总_2026-11-14.csv`（14×10）、`近10天模型可靠性看板_2026-11-14.html`（零外部依赖交互看板）、`分析脚本/radar_analyze.py` + `radar_render.py`（可复现）、`进度/进度_20261114_2003_双雷达TOP20分析.md`

### 验证
Playwright MCP 打开本地 8899 静态服务实测看板渲染正常（92 行明细 / 14 平台表 / 10 天趋势 / 筛选器齐全），唯一 console error 是 `favicon.ico` 404，与页面脚本无关。静态校验：分母恒等式 `ok+429+other=18645` 成立、HTML 内嵌 JSON 合法、MD 与 HTML 的 TOP20 完

## 21:12 进度核查
- 有道云删除任务 17:31:34 后停滞 3h40m（wmic 查无 youdao_fake_cleanup 进程，判定会话切换杀掉），21:12 用断点续删版重启（OnQb9R），处于全量盘点阶段；断点文件 youdao_deleted_ids.txt 尚未产生属正常。
- 各端实测：博客未推送 0、三轴 3 文件在；Gridea posts 560、18:02 渲染推送；论坛三轴 6 帖全存活；收件箱 8 / bak 1385；4 脚本语法 OK、列车含 step0c 与 --multi。
- schtasks：\WB_publish_train_2315 今晚 23:15 就绪（升级后首次自动跑）、\WB_publish_train_retry_1020 次日 10:20 就绪。
- 交付：会话目录「进度/进度_20261114_2112.md」。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-03-10-29-12\.workbuddy-ai\memory\2026-11-14.md, D:\workspace\workbuddyai\2026-11-13-15-38-12\.workbuddy-ai\memory\2026-11-14.md

## 审计「4端发布升级_多Agent三轴」并修复 BUG（19:31-20:0x）

项目根目录：`D:\AI work\workbuddy`；升级报告：`D:\AI work\workbuddy\2026-11-13-20-41-08\4端发布升级_多Agent三轴_20261114.md`

**备份（改动前，逐字节校验通过）**：`D:\AI work\workbuddy_bak_20261114_1941`，含 5 个待改 .py。

**改动文件（5 个）**
- `multi_agent_sources.py`：修 `_read` 编码 fallback 失效（errors=ignore 让 utf-8 永远成功，GBK 中文被吞）；`merged_for_llm` 改为按 agent 均分预算，保证 4 节都在、去 HTML 注释。
- `generate_daily_summary.py`：兜底日报去掉每 agent 硬截 4000 字符（实测 wb-cn 8266 只发 4000）；新增 `_plain_digest`；浓缩稿改为「非首次生成/模型已挂 → 纯文本截取，零 LLM 调用」，`--digest-only`/`--force` 保留原语义。
- `publish_3axis_extra.py`：`extract_axis` 放得下就不截，超限才按 agent 均分并注明截断；`build_articles` 改用真正的 fallback（原来 `hasattr(mas,...)` 是死代码）；`--dry` 前置不落盘；Gridea 保留原 id；WAF cookie 回落 `FALLBACK_COOKIE`；有道云 save 对齐 `run_save`（3 次重试 + 检查输出 error + UTF-8 env）；新增失败汇总 + 非零退出；所有子进程 `CREATE_NO_WINDOW`。
- `publish_train.py`：子进程静默；docstring 同步 step4 日期口径。
- `handoff/upload_youdao.py`：daily 轴排除 `-3axis-*.md`（原来 3 个三轴文件全被当成「工作日志」镜像，每天多 2 篇错目录重复笔记）；子进程静默。

**查证结论（实测，非推测）**
- ZCode `db.sqlite` 表 `message.time_created` 是毫秒，北京时间分日 SQL 正确；10-25 回测返回 5 会话 / 423 条。库内最新 10-25，今天无记录属真实空档。
- 发布出去的内容无 `
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


# 2026-11-14 工作日志

## 17:57 复查 KV 用量，验证修复生效

- 用户问「今天 KV 额度用了多少、起作用没有」。用 Cloudflare GraphQL Analytics（T0 官方接口）拿到按天/按命名空间/按 actionType 的真实计数。
- **今天（UTC 11-14 00:00–10:30，即北京 08:00–18:30）**：写 **20** 次（全部 youdao-brief-store）、读 **34** 次（youdao 32 + webmon 1 + 探测）、list/delete 0。webmon 周六不跑，写 0。
- 对比（GraphQL 口径，只统计 HTTP 200 成功的请求；429 失败的不计入，且官方明确分析数据 ≠ 账单精确计数）：
  - 11-12（告警日）：write 989（youdao 770 + webmon 219）、read 4683 → 正好撞 1000 写/天上限。
  - 11-13（修复日）：write 413 成功、read 584、list 7；08:15Z 之后写入失败（429）不计入统计 → fs_state 停在 08:15Z、last_tick 停在 11-12T08:58Z。
  - 11-14：write 20。
- 起作用的三条硬证据：① fs_state `last_run=2026-11-14T09:00:35Z`（整点轮，写成功=额度没爆）；② 周六 webmon 0 写；③ 按新频率全天预计 25–30 写（周六）/ 200–280 写（工作日），远低于 1000。
- **GraphQL 数据集复用要点**（下次直接查额度）：
  - 顶层 `viewer { accounts(filter: { accountTag: "<account_id>" }) { kvOperationsAdaptiveGroups(limit, filter: {datetime_geq/leq}) { dimensions { actionType namespaceId date responseStatusCode } sum { requests } } } }`
  - 类型 `AccountKvOperationsAdaptiveGroups`；actionType 值实测 read/write/list；responseStatusCode 200/404。
  - 坑：filter 参数名必须是 `accountTag`（不是 accountID）；数据集名是 `kvOperationsAdaptiveGroups`（不是 worker*）；`__type` introspection 对通用名返回 null，但 `__schema { types { name } }` 能列出全部 2186 个类型名。
  - 脚本：`cf_kv_count.py`（当日）、`cf_kv_compare.py`（多日对比）、`cf_gql_kv.py`（字段 introspect）。
- 未做任何写操作，纯只读复查。

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）