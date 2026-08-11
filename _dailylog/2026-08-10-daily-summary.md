---
layout: default
title: 每日工作总结 · 2026-08-10
date: 2026-08-10 23:30:00 +0800
---

# 每日工作总结 · 2026-08-10

> 本篇由 2026-08-11 09:13 的补跑任务生成。08-10 当晚 23:00 的定时任务因本机关机未起跑（`last_run_at` 停在 08-09 23:07:24），四端均缺 08-10 这一篇，本次补齐。
> 数据来源：`2026-08-09-16-44-16/.workbuddy/memory/2026-08-10.md`（10,031 字节机器日志，跨零点会话，当天无纯日期文件夹）。

今天是**「handoff 断更问题的总攻日」**。从早到晚一条主线：先修进程、再查为什么 handoff 五天没发、再把漏掉的补回来、最后把规则本身改掉，让这个问题不会再犯。中间顺带解决了 Gridea 浓缩版"本地有、线上没有"的时间窗口 bug。

---

## 一、今日完成事项（分点，通俗语言）

### 1. Hermes 网关 + 18800 内存看板重启拉起（延续 8-9 会话）

用户要求重启 Hermes 网关，并把 18800 端口的 Hermes Memory Viewer 拉起来，看看 MemOS 配置到底生效没有。

- **先精确定位进程**，不猜：
  - Hermes 网关 = **PID 11692**（`gateway.pid` 里记着，命令行是 `D:\hermes-agent\venv\Scripts\hermes.exe gateway run --replace --accept-hooks`）
  - 18800 内存看板 = **PID 12752**（`node ...\.hermes\memos-plugin\dist\bridge.cjs --agent=hermes --daemon`）
  - 作为对照，OpenClaw 那边是 gateway=2748（18789 端口）、bridge=14036（18799 端口）
- **今天挖到一个很有复用价值的发现**：AutoClaw 的看门狗**只自动重启 OpenClaw 的 gateway（18789）**——8-9 那天杀掉 15580 之后它自己拉起了 2748，这是实证。但 **Hermes 这一侧的两个进程（网关 11692、bridge 12752）被杀之后不会自动复活，必须手动拉**。以后排障别再等它自愈了。
- **重启结果**：Hermes 网关拿到新 PID **13704**；18800 拿到新 PID **13476**，端口正常 LISTENING，curl 根路径能返回 MemOS Local Memory Viewer 的 HTML（API 那层要 token 登录才能看）。
- **一个容易误判的点**：Hermes 侧的 memos 配置写在 `~/.hermes/config.yaml` 第 112–119 行，是 `memory: enabled=true / provider=memtensor`，**不是** OpenClaw 那边的 `memos-local-plugin` 插件 id。所以 18800 看板上显示的是 memtensor provider 的状态，**不会**字面出现 "memos-local-plugin" 这个词——只要看到 memos/memtensor 处于激活态就算成功，别因为搜不到那个字符串就判定失败。

### 2. 查清「handoff 从 8.5 到 8.10 一篇都没发」的真正原因

用户直接质问：为什么从 8.5 到今天，handoff 一个新文档都没有发布？

**结论：是源头断供，不是自动化坏了。**

- 每晚 23:05 的 scan 任务（id `1785476214373`）只收集各 session 目录里的 `HANDOFF*.md` 文件——这是 8.2 定下的护栏，原话是"绝不读日志凑数"，本意是防止拿日志充数发垃圾。
- 但从 **8.6 开始，8 月所有 session 目录里再没出现过一个 `HANDOFF*.md`**（全量 Glob 搜索证实）。于是 scan 每天照常跑、照常 exit 0，但产出是 0 → 收件箱是空的 → publish 自然没内容可发。
- 三条实证链：`handoff/bak/` 里最后归档的是 8.5 的两篇；scan 的运行历史逐条都写着"0 个 session 含 HANDOFF*.md"；publish 的历史都是"探测无 HANDOFF.md 直接结束"。
- 顺带澄清一个误会：任务状态 `status=PENDING_REVIEW` 是"已生成待审阅对话"的**正常状态**（`result_success=1`），不是卡死了。
- **行为变化的根源**：8.6 之后项目文档大多写成了 `进度_*.md` 或各种分析 md（这是被"每次回复附 md 进度文件"那条红线带出来的习惯），没有用 HANDOFF 命名，所以全被漏扫了。

当时给了三个恢复方案：A = 把值得交接的活写成 `HANDOFF_*.md` 放进对应 session（当时推荐）；B = 放宽 scan 的匹配规则（违反 8.2 护栏，需要用户同意）；C = 如果确实没项目，不发布才是对的。

### 3. 真读 8.6–8.9 日志核实 + 当晚 handoff 补发

用户原话："看过这几天日志了吗？确实没啥可发吗？没有就发今晚的。"

**认真读完日志后的结论：8.6–8.9 确实有实质项目，但全都写成了每日工作总结 / 分析文档，没有一篇是 `HANDOFF*.md`。** 所以 scan 的守护栏跳过它们在逻辑上是对的，问题不是"没活儿干"。具体清点：

| 日期 | 实际有的项目 |
|---|---|
| 8.7 | 主力资金流向看板（新建项目 + `app.py` 同源代理 + 启动器 + `favicon-picker` skill） |
| 8.8 | 看板 v1.4 + Hermes MoA 评分表（`model_score_table.md`）+ WB 自动更新路径排查 |
| 8.9 | cua-driver 安全核查与卸载 + WB 自动化代理依赖诊断修复（Clash / ProxyOverride） |

**当晚的补发动作**：写了 `HANDOFF_MemOS_Hermes_部署排障.md`，标题为「MemOS 接入 AutoClaw/Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要/进化选型」，覆盖了 Studio 看板空白的根因、Node v24 升级、MemOS 部署、网关 slots 被重置的根因（缺 `plugins.installs` 注册导致 normalize 重置为 none）及修复、智谱 v4 的协议坑（实测 404）、技能进化模型选型（DeepSeek-V4-Flash 直连实测返回 200 + `reasoning_content`）、Hermes profile worker 崩溃待续、以及 handoff 断更诊断本身。

执行链路：`handoff_flow.py scan --days 5` 生成 `handoff/260809_MemOS 接入 AutoClaw_Hermes 排障..._handoff.md` → `handoff_flow.py publish` → Gridea ✅、博客 git push ✅、语雀 ✅、bbs1org ✅、phpBB 🔄（后台任务进行中）。本次沙箱 python 出网没被拦，四端都通。

另外确认了兜底机制：发布自动化 `1784951947030` 每天 23:07 跑一次，手动 publish 如果因网络失败，次日 23:07 会自动从收件箱补发（幂等，不会重复发）。

### 4. 补发 8.7 / 8.8 两篇 handoff，并修掉 handoff_flow.py 的文档缺陷

用户追问："上面两个怎么没发？是不是脚本偷懒？"

**先澄清（源码实证，不是猜）：脚本既没崩也没偷懒**，它每天都在正常 scan + publish——今晚那篇就是它发出去的。8.7/8.8 没发的真实原因是：那两个项目当初写成了主题 markdown（`8850-datasource-plan.md` = 主力资金看板方案、`model_score_table.md` = Hermes MoA 评分表），**文件名不是 `HANDOFF*.md`**，scan 按 8.2 护栏"整个 session 没有 HANDOFF*.md 就跳过"，就漏了。

**但确实揪出了一个真实缺陷——文档和代码对不上**：`handoff_flow.py` 顶部的 docstring（第 11–13 行、195–197 行）白纸黑字承诺了"结合模式"——即没有 `HANDOFF*.md` 时会回退去收集主题 markdown；但**代码（213–220 行）从来没实现过这个回退**，直接 `continue` 跳过了。这属于文档过度承诺，不影响运行但会误导人。已把这两处 docstring 改成 HANDOFF-only 的真实行为（纯文档修正，运行逻辑一个字没动）。

**补发执行（方案 A，用户拍板）**：
- 写 `2026-08-07-17-14-37/HANDOFF_主力资金流向看板数据源改造方案.md`（含降级链、腾讯 gtimg 是个股级的诚实修正、改法 A 推荐；状态标为"方案待确认"）
- 写 `2026-08-08-10-56-22/HANDOFF_Hermes模型评分表MoA选型.md`（含量纲差异说明、64 行表节选、MoA 推荐配置、hy3 免费到 8.31 的时限提醒）
- `scan --days 5` → 生成 `handoff/260807_主力资金流向看板..._handoff.md` + `handoff/260808_Hermes 接入模型评分表..._handoff.md`（今晚那篇 MemOS 幂等跳过，没重复）
- `publish` 后台执行：Gridea ✅、博客 git push ✅、语雀 OK、论坛去重中

### 5. 🚨 新规落地：handoff 查漏补缺改由 AI 负责，8.2 护栏正式废除

用户原话：**「一定要天天扫描每日工作日志并及时把完成的项目发到 handoff 收件箱，别让我来给你查漏补缺！」**

用户选了"放宽 8.2 护栏、天天扫日志"这条路，**并且明确纠正了我上一轮的说法**——我当时说"项目收尾你要记得用 HANDOFF 命名"，用户指出**那是 AI 的职责，不是用户的任务**。这个纠正很关键。

**`handoff_flow.py` 的实际改造（`collect_project_docs` 三级回退）**：

1. **第一级**：优先取 session 根目录的 `HANDOFF*.md`（显式项目文档）
2. **第二级**：没有的话，取同目录的主题 markdown（排除日志、排除 README、正文 ≥200 字）——这一级专门用来捕获 `8850-datasource-plan.md`、`model_score_table.md` 这类文件
3. **第三级**：前两级都没有，就调 `extract_from_daily_log()` 去解析每日工作日志，按 `##` 切出"已完成项目"的小节（自动跳过「今日完成事项」「待办」「问题记录」「小结」「复盘」这些管理性小节），提炼成 handoff

新增的代码元素：`THEME_MIN_CHARS=200`、`SKIP_SECTION_RE`、`extract_from_daily_log()`、`_build_handoff()`；`cmd_scan` 改为消费 `(yymmdd, title, content)` 三元组；顶部 docstring 和 argparse help 同步更新。**selftest 全过。**

**每日 scan 自动化 `1785476214373` 同步更新**：语义改为"三级回退 + 读日志"、`--days 5` 改成 `--days 7`、名称改为"三级回退：HANDOFF→主题md→日志提炼"，**23:05 的时序铁律保持不变**。

**跨项目记忆同步**：① 在 `MEMORY.md` 加了红线条目"handoff 查漏补缺由 AI 负责"；② 明确标记 8.2 那条"scan 绝不读日志 / 无 HANDOFF 即跳过"的护栏**已废除**，今后任何会话都不得改回 HANDOFF-only。

**补跑捞回漏发**：`scan --days 7` 实跑 → 收件箱新增 **10 篇**（8.4 五篇、8.5 三篇、8.7 两篇，均为日志提炼；已发过的 MemOS / 8.7 / 8.8 三篇幂等跳过）；`publish` 后台执行，首篇已完成四端发布并移入 `bak/`，其余陆续进行。

**诚实边界说明**：日志提炼是拿 `##` 小节标题当项目名的，所以会出现像 8.7 的「三、生成的有用文件」「二、关键决策」这种**日志小节名而非干净项目名**的条目。这些内容属于"完成的工作"范畴，用户可以自己审阅取舍——这是新规下"宁可多捞、不可漏发"的主动取舍，不是 bug。

### 6. Gridea 浓缩版 handoff 补发闭环（09:07 用户问「进度」）

用户追问："Gridea 浓缩版的 handoff 文档怎么没有补发？"

**根因有两类**：
1. **5 篇老文档**（260725、260729 两篇、260731 两篇）根本不在 `Gridea Pro/posts/` 目录里——之前被幂等逻辑或清理动作弄丢了，但 `bak/` 里的标记显示"已发布"，所以对不上账。
2. **260804–260809 这批重发**写进 `posts/` 的时间是**凌晨 01:30**，晚于每日 **23:45** 的同步窗口 → 结果就是本地有、线上没有。

**修复**：用 `handoff_flow.gen_gridea()` 把 5 篇补回来 → 手动跑 `gridea_auto_sync.py` 渲染 + git push。

**验证（09:07 实测）**：git 最后一次提交时间 `01:41:43` 已推送（master 分支无未推送提交）；`output/post/` 下 **75 篇**全部 mtime 为 `01:41`，包含补回的 5 篇和重发的全批。Gridea 浓缩版与 `bak/` 已对齐，没有缺口。

**防复发**：把时序改成 23:05 scan → 23:07 publish 写 posts → 23:12 sync 自动推送，三步顺接，不会再卡在同步窗口外面。

---

## 二、关键决策 / 注意事项

| # | 事项 | 结论与理由 |
|---|---|---|
| 1 | **AutoClaw 看门狗的覆盖范围** | 只自动重启 **OpenClaw gateway（18789）**；Hermes 网关和 Hermes bridge（18800）**杀了不会复活，必须手动拉**。排障时别干等自愈。 |
| 2 | **handoff 断更的定性** | **源断供，不是自动化故障**。有源码 + 运行历史 + `bak/` 归档三方证据链。不要一看到"没发布"就归因到脚本坏了。 |
| 3 | **废除 8.2 护栏** | 用户明确拍板：不许让用户来查漏补缺。8.2 那条"绝不读日志"的护栏**永久作废**，今后任何会话不得改回 HANDOFF-only。 |
| 4 | **职责边界纠正** | "项目收尾要用 HANDOFF 命名"**是 AI 的职责，不是用户的任务**。这是用户当场纠正的，写进红线了。 |
| 5 | **三级回退的取舍** | 宁可多捞不漏。代价是日志提炼出来的项目名可能不干净（会出现"二、关键决策"这类小节名），这是**已知取舍**，不是缺陷。 |
| 6 | **文档过度承诺是真缺陷** | docstring 承诺了代码从未实现的"结合模式"回退。虽不影响运行，但会严重误导后来人排障，必须修。已改为如实描述。 |
| 7 | **Gridea 时间窗口铁律** | 写稿时间必须早于同步窗口，否则本地有线上无。已固化为 23:05 → 23:07 → 23:12 顺接。 |
| 8 | **环境坑（复记）** | ① Bash 工具内调 PowerShell 被安全策略误拦（报 "Invoke PowerShell from Bash"）；② PowerShell 工具的 stdout 会被终端标题行污染，**必须 `Out-File` 写文件再用 Read 读回**才可靠。 |
| 9 | **MemOS 配置判定标准** | Hermes 用的是 `provider=memtensor`，**不是** OpenClaw 的 `memos-local-plugin`。18800 看板不会显示后者字符串，看到 memos/memtensor 激活即成功。 |

---

## 三、生成的有用文件

| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| 08-10 机器日志 | `D:\AI work\workbuddy\2026-08-09-16-44-16\.workbuddy\memory\2026-08-10.md` | 本总结的原始数据源（10,031 字节） |
| MemOS/Hermes 排障交接 | `D:\AI work\workbuddy\2026-08-09-16-44-16\HANDOFF_MemOS_Hermes_部署排障.md` | 当晚补发的 handoff 主文档，覆盖看板空白、slots 重置、智谱 v4 坑、模型选型 |
| 主力资金看板交接 | `D:\AI work\workbuddy\2026-08-07-17-14-37\HANDOFF_主力资金流向看板数据源改造方案.md` | 补发 8.7 项目；含降级链与改法 A 推荐（状态：方案待确认） |
| Hermes MoA 选型交接 | `D:\AI work\workbuddy\2026-08-08-10-56-22\HANDOFF_Hermes模型评分表MoA选型.md` | 补发 8.8 项目；含量纲差异说明、64 行表节选、MoA 推荐配置 |
| 进度·Hermes 重启 | `D:\AI work\workbuddy\2026-08-09-16-44-16\进度_20260810_0012_hermes重启18800拉起.md` | 进程定位与手动拉起命令全记录 |
| 进度·handoff 未发布诊断 | `D:\AI work\workbuddy\2026-08-09-16-44-16\进度_handoff未发布诊断_20260810.md` | 断更根因的完整证据链 |
| 进度·新规落地 | `D:\AI work\workbuddy\2026-08-09-16-44-16\进度_20260810_0124_handoff扫日志新规落地.md` | 三级回退改造的实施记录 |
| 进度·Gridea 补发闭环 | `D:\AI work\workbuddy\2026-08-09-16-44-16\进度_20260810_0907_Gridea浓缩版补发闭环.md` | Gridea 缺口修复与 09:07 验证结果 |
| handoff 主脚本（已改） | `D:\AI work\workbuddy\handoff\handoff_flow.py` | 新增 `extract_from_daily_log()`、`_build_handoff()`、`THEME_MIN_CHARS`、`SKIP_SECTION_RE`；三级回退落地 |
| handoff 收件箱 | `D:\AI work\workbuddy\handoff\` | 补跑 `scan --days 7` 后新增 10 篇待发 |
| handoff 归档区 | `D:\AI work\workbuddy\handoff\bak\` | 已完成四端发布的 handoff 归档，用于对账 |
| Gridea 稿件目录 | `C:\Users\Administrator\Documents\Gridea Pro\posts\` | 补回 5 篇老文档，与 `bak/` 已对齐 |
| Gridea 渲染输出 | `C:\Users\Administrator\Documents\Gridea Pro\output\post\` | 75 篇全部 mtime `01:41`，已 git push |
| Hermes 配置 | `C:\Users\Administrator\.hermes\config.yaml` | 第 112–119 行 `memory: enabled=true / provider=memtensor` |

---

## 四、待办 / 风险

### P0（优先处理）

- **18800 看板需用户亲自确认**：浏览器打开 `http://127.0.0.1:18800` 登录后，查看 slots / memory 是否真的激活。API 层需要 token，我这边只能确认端口 LISTENING 和根路径返回 HTML，**激活状态无法代为核实**。
- **Hermes 两个进程不受看门狗保护**：网关（现 PID 13704）和 bridge（现 PID 13476）一旦挂掉不会自动复活，重启机器后也需要手动拉。**长期看应该给 Hermes 侧也配一个看门狗**，否则每次都要人工介入。
- **收件箱 10 篇补捞件的发布状态未最终对账**：`publish` 是后台跑的，08-10 当晚只确认了首篇完成四端并移入 `bak/`，**其余 9 篇的最终落地情况没有逐条核验**。需要对一次 `handoff/` 与 `handoff/bak/` 的差集。

### P1（需要留意）

- **日志提炼出的项目名不干净**：会出现「二、关键决策」「三、生成的有用文件」这类日志小节名混进 handoff 标题。这是"宁可多捞"的主动取舍，但**已经发到四端的这些条目，标题在公开渠道上是不好看的**，需要用户审阅决定是否清理。
- **Hermes profile worker 崩溃问题待续**：在 MemOS handoff 里记了一笔，但当天没有解决。
- **智谱 v4 协议坑**：实测 404，未找到可用调用方式，暂时搁置。
- **8.7 看板改造方案仍是"待确认"状态**：HANDOFF 里写了改法 A 推荐，但用户尚未拍板，项目处于挂起态。
- **三级回退的第二级可能误捞**：主题 markdown 的判定条件只有"非日志、非 README、正文 ≥200 字"，比较宽松，**有可能把纯分析文档、调研笔记当成项目交接件发出去**。需要观察几天看误报率。

### P2（观察项）

- **`--days 7` 扫描窗口带来的重复风险**：窗口从 5 天拉到 7 天，靠幂等跳过来防重复。目前幂等是有效的（本次 MemOS/8.7/8.8 三篇正确跳过），但窗口越大，幂等逻辑的压力越大。
- **Gridea 那 5 篇老文档为什么会丢**：只知道"被幂等或清理弄丢了"，**具体是哪个环节丢的没查清**。已经补回来了，但根因不明就有再次发生的可能。
- **本篇迟发说明**：08-10 的四端发布因本机 08-10 夜间关机而全部缺失，由 08-11 09:13 的补跑任务补齐。**08-11 当天的总结仍由今晚 23:00 的常规任务生成**，不受本次补跑影响。
