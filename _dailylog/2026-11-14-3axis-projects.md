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

## 追加（21:12–21:20）· 按能力分重排主力模型 + 场景推荐

用户新名单：CF 5 个 + NIM 4 个作免费主力、`spark-x2.6` 主力、`deepseek` 收费 flash 作备用兜底；要求**按能力分排行**并做场景推荐。

### 核实结果（不瞎编）
- 活清单 `models.json`（94 条）里**没有 `deepseek-4.1-flash`**；DeepSeek 官方仅 `deepseek-v4-pro` 与 `deepseek-flash`（= [DeepSeek] DeepSeek-V4-Flash），url 均为 `api.deepseek.com`。10-13 综合分排行第 19 行出现过别名 `DeepSeek-V4.1-Flash[Loomy]`，但当前已不在活清单 → 本次按 `deepseek-flash` 处理并在报告里明写推断依据、请用户确认。
- `spark-x2.6` = `[xf] spark-x2.6`（vendor Xunfei），10-13 报告把 `spark-x` 列入「未取到公开分(主流类)」，08-02 干活榜无此模型 → **无任何能力分**，按 T0 可靠性（98.33% 成功、零 429）入选，能力分填 `—`。

### 能力分口径（重要，已补进 skill）
- 08-02 干活榜有两列：「**得分**」= 纯能力分不含速度（字面意义的"能力分"）；「**综合**」(榜A) = `0.7×速度分 + 0.3×得分`，含 70% 速度。用户说按能力分，用纯「得分」列做主排序；综合 A 与上一份"靠谱分"高度重叠，换维度没意义，只作对照列。
- T1 公开基准分（10-13 报告，OpenCompass/Vellum 均值）与 T2 量纲不同，单列展示、不混排。
- **同模型双分数冲突**：`nemotron-3-ultra-550b` 在 08-02 榜有 NIM 直连行「得分 84 / 综合 25.2」（当时 0% 可靠率 network 失败）与 OR 免费行「得分 78 / 综合 48.7」，必须并列标注，不能偷偷取一个。
- **跨通道引用**：`poolside/laguna-xs-2.1`、`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` 榜里只有 OpenRouter 免费版行，能力分标 `*`。
- **无分模型**：`nemotron-3.5-lightning-30b-a3b`、`spark-x2.6`、`deepseek-flash`（后者有 T1 62.7）一律填 `—` 排表尾，不编数字。

### 结论
- 能力分第 1 `nvidia/nemotron-3-ultra-550b-a55b` 84（OR 版 78）；CF 第 1 `@cf/google/gemma-4-26b-a4b-it` 80。
- 能力分 vs 综合A 排序差异大：`@cf/nvidia/nemotron-3-120b-a12b` 能力 73 第 4 → 综合A 43.9 第 8；`@cf/qwen/qwen3-30b-a3b-fp8` 能力 63 第 5 → 综合A 62.4 第 2。
- 11 个入选 = 9 免费主力（CF5+NIM4）+ 1 指定主力 spark + 1 收费兜底 deepseek-flash；4 个平台。
- 部署三件事：① CF 5 个仍在 `config.json` `skip_models`（额度让给发布链），要当主力须删 5 行 + 重启 8848/8849 daemon，且会与发布链抢免费额度；② CF 窗口小（11-13 日志 T1：qwen3-30b 32768 / qwq-32b 24000 vs WB agent 会话约 53974 token），只适合短请求，不能塞进 WB agent 会话；③ NIM 预览模型 180 个 untestable 轮次 / 219 次 model_gone，易下架。
- 场景推荐 8 个场景 + 免费优先组合链路（CF/NIM 免费主力 → spark 高可靠批处理 → deepseek-flash 收费兜底）。

### 产物
`主力模型能力分排行_2026-11-14.md`、`.csv`、`主力模型能力分看板_2026-11-14.html`、`能力分看板预览_2026-11-14.png`、`分析脚本/render_capability.py`、`进度/进度_20261114_2117_主力选型能力分.md`。

### 验证 / 踩坑
静态校验：11 行、9 免费主力、3 无分、能力分降序成立、T0 数值与上一轮聚合 JSON 完全一致、HTML 零外部依赖。浏览器实测：**8899 端口有上一轮残留的两个 LISTENING 进程导致 `ERR_EMPTY_RESPONSE`**，换 8901 后成功（11 行主表 + 8 场景卡片 + 筛选器全渲染），console 仅 favicon 404。以后临时服务用完要确认进程真的退出，别复用同一端口。

## 追加（21:32–21:45）· 本次结果以「项目流」发布到 4 端

用户指令「这次结果以项目流发布到4端」。查清「项目流」= 11-14 18:05 落地的多 Agent 三轴发布体系里的一轴（工作日志 / 项目流 / 技术点），文档 `2026-11-13-20-41-08/4端发布升级_多Agent三轴_20261114.md`，发布器 `publish_3axis_extra.py`。

### 用户确认口径（AskUserQuestion）
- 新增带后缀的一篇《项目流 · 2026-11-14 · 主力模型能力分选型》，**不覆盖** 18:05 已发的《项目流 · 2026-11-14》
- **只 4 端**（博客 / Gridea / bbs1org#3 / phpBB#11），不发第 5 端有道云

### 为什么不能直接跑原脚本
`publish_3axis_extra.py` 三轴一起发、标题固定 `项目流 · {date}`、内容从 4 agent 日志抽取、默认 5 端、论坛/云笔记按标题幂等。今天已实跑过 → 重跑只会覆盖博客/Gridea 同名稿、论坛跳过，等于没发还破坏已发内容。故新建独立发布器 `publish_projects_4ends.py`（不改原脚本）。

### 发布结果（4 端全部线上实测）
| 端 | 落地 | 证据 |
|---|---|---|
| 博客 | `_dailylog/2026-11-14-3axis-projects-models.md` 17,635 B | push OK；`https://w662000.github.io/daily-note-blog/` HTTP 200 含新标题 |
| Gridea | `posts/261114项目流-模型能力分选型.md` 17,679 B，id=`0izhjk` | 本地 + 线上 `api/search.json`（477,516 B）均含新标题 |
| bbs1org #3 | topic **2106** | `solve_waf()` cookie 复查 20 条标题含新标题 |
| phpBB #11 | topic **8950** | `solve_waf()` cookie 复查 50 条标题含新标题 |

旧稿两篇（8870/8900 B，mtime 17:58:55，title `项目流 · 2026-11-14`）未被覆盖；两个论坛版块新旧两篇同日标题并存。稿件 10,673 字符，论坛 18,000 上限未截断；对外文案已把 8 处对话口吻改成中立项目记录，数字与结论未动。

### 踩坑（已沉淀为 skill `publish-projects-axis`）
1. 三轴脚本标题固定 + 按标题幂等 → 同日第二篇必须换标题**且**换博客/Gridea 文件名。
2. Gridea 渲染日志出现 `curl 22 / 408 / send-pack unexpected disconnect`，脚本第 2 次 push 成功；不能只看脚本自报，要查 `output/api/search.json` 与线上 `api/search.json`。
3. 论坛复查用 `FALLBACK_COOKIE` 返回 0 条（WAF 未过），必须用发布时同款 `solve_waf() or FALLBACK_COOKIE`，否则误判「没发出去」。
4. Windows Git Bash 传中文 argv 会按 GBK 串码 → 标题/文件名/路径固化进脚本默认值，脚本用英文名，命令行只传开关。
5. 论坛验证只做只读 `list_topics` 各 1 次 + 3 秒间隔，未重复发帖（温和红线）。

### 产物
`项目流稿_主力模型能力分选型_2026-11-14.md`、`publish_projects_4ends.py`、`进度/进度_20261114_2145_项目流4端发布.md`。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-03-10-29-12\.workbuddy-ai\memory\2026-11-14.md, D:\workspace\workbuddyai\2026-11-13-15-38-12\.workbuddy-ai\memory\2026-11-14.md

## 星空图收录 clash-node-check skill（2026-11-14）
- 项目：`D:/workspace/workbuddyai/2026-10-29-16-13-56/`
- 备份：`2026-10-29-16-13-56_bak_20261114_1940/`（diff 校验一致后才动工）
- 改动：projects.json 新增节点 p111「clash-node-check 节点检查 skill」（星座 H 技能与知识沉淀，w=6，st=running，path 指向 `C:/Users/Administrator/.workbuddy-ai/skills/clash-node-check`），新增边 p111→p93(evolve)、p111→p94(same)；重建 星图预览.html（111 节点 / 125 边）
- 注意：星空图扫描器 ROOTS 不含 `~/.workbuddy-ai/skills`，skill 类项目以后要收录都得手动加节点（或改 ROOTS，会带出 28 个 skill 噪音）
- 坑：bash 双引号里 python -c 写反斜杠路径会被转义成四重斜杠，path 一律用正斜杠

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）