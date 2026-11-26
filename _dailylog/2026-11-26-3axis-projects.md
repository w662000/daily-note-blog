---
layout: default
title: 项目流 · 2026-11-26
date: 2026-11-26 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-26-10-42-34\.workbuddy\memory\2026-11-26.md, D:\AI work\workbuddy\2026-11-26-21-10-26\.workbuddy\memory\2026-11-26.md

（该 Agent 当天日志中未检出此类段落）

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-26-10-38-56\.workbuddy-ai\memory\2026-11-26.md, D:\workspace\workbuddyai\2026-11-26-12-43-58\.workbuddy-ai\memory\2026-11-26.md

## 12:47-12:56 两张星图 HTML 补自动同步（已完成 ✅）

- 查明：原项目星图定时任务只在工作区重生成 `星图预览.html`，不会同步到 skill 自带 HTML（skill 副本是人工复制的）；技能星图 skill 的 `skill_map.json` 还停留在 75 节点，HTML 已是 277 节点。
- 改造前已完整备份：`D:\workspace\workbuddyai\2026-10-29-16-13-56_bak_20261126_1252`（项目目录 diff 一致；另存 24 份 HTML/JSON + 16 份 SKILL.md 八端副本）。
- 新增 `D:\workspace\workbuddyai\2026-10-29-16-13-56\sync_skill_starmap.py`：
  - `--project-only` 把工作区新 HTML 原子同步到 8 端 project-star-map skill；
  - `--skill-only` 扫 8 端 skill 目录（以 SKILL.md 为准），保留原星级/星座/来源，按实测刷新覆盖、追加新 skill（新节点 1 星/F 星座，source 按 `agent_created` 判定），重建 HTML DATA + 标题节点数，并从 HTML 重建 skill_map.json，原子写 8 端；日志 `扫描日志/skill_starmap_sync.log`。
- `run_daily_star_scan.py` 升 v1.2：扫描后追加 `html_sync` 步骤（项目 HTML 同步），已 dry-run 验证 scan/memory/merge/html_sync/smoke 全 0。
- 首次实跑：技能星图 277→287 节点（新增 10，其中 skill-star-map 自身识别为 user），133 条覆盖变化；8 端 HTML/JSON/SKILL.md 哈希各自一致；`find_skill.py --id s01` 正常。再 dry-run 显示 0 变更，幂等。
- 定时任务：Windows `ProjectStarMap-DailyScan`（11:00/23:00，原）与新建 `SkillStarMap-DailyScan`（11:10/23:10，pythonw 静默、无黑窗）；WorkBuddy 自动化 `9585354d`（项目星图汇报，22:45，已修正 22:30 陈旧口径并加 HTML 哈希核验）与新建 `fb9851f4`（技能星图 23:20 核验/兜底补跑）。
- 两份 SKILL.md 数据更新章节已改写并同步 8 端；技能星图旧写死的 277/14 个共有等静态数字改为「随每日同步变化」。

## 13:59-14:04 Nodaroo 流程交接 + skill + 项目星图新节点（已完成 ✅）

- 用户要求三件套：handoff 文档、生成 skill、收录项目星图新节点（au / 2026-11-24 / 路径指向 au workspace）。
- 动工前备份：`D:\workspace\workbuddyai\nodaroo_handoff_bak_20261126_1359`（项目星图工程 + 八端 project/skill-star-map 共 16 份 skill 目录）。
- 交付1 handoff：`C:\Users\Administrator\.openclaw-autoclaw\workspace\handoff\20261124_Nodaroo免费容器部署XrayREALITY节点_handoff.md`（5.3KB，含环境参数/完成内容/产物/后续风险；**凭证不写文档**，只指向服务端 vless-url.txt）。
- 交付2 skill：`ptero-container-xray-node` v1.0.0，复用 2026-11-24 已验证资产（workflow.md 分阶段流程 + app.py 12.7KB + client-test.json），新建 SKILL.md；已分发八端，app.py 编译通过、client JSON 有效。
- 交付3 项目星图：权威 star_map.json 加 `p173`（p=autoclaw，s/e=2026-11-24，path=au workspace，handoff/cred/next 齐全），发现层 projects.json 加 `p182` 同名同 path；**必须同步 8 端 star_map.json**——否则 merge 基准（au-intl 副本）没有 p173，会把 scanner:p182 重复追加成 p173。同步后 `merge_to_starmap.py --dry-run` 新增0/更新0。
- 重建 HTML：`build_starmap.py` 生成后源 HTML 是 CRLF、同步器写 LF，导致哈希不一致；把源规范成 LF 后 9 份项目 HTML 哈希统一 `a58da2fc8840`。
- **踩坑修复**：8 端 project-star-map 的 HTML 原本都是只读 0444，`os.replace` 报 WinError 5——之前"同步一致"其实从没真正写过。`sync_skill_starmap.py` 的 `write_if_changed` 已加自动解除只读位，以后定时任务不会再卡。
- 技能星图自动发现新 skill，节点 287→288（ptero-container-xray-node，user 1星 8平台），9 份 HTML 哈希一致。

## 14:06-14:13 漏扫根因诊断与修复（P0，已完成 ✅）

- 用户问「很多项目做了但定时任务扫不到」。T0 实证：今天有产出却没进星图的 4 个单元（`D:\AI work\workbuddy\2026-11-17-01-21-22` 39产物/今天8改、`2026-11-26-11-30-34` 6改、`lobsterai\project\选股` 108产物/3改、`2026-11-12-23-22-49` 1改）。
- 根因（读码+实证）：①`known_units` 目录差集——目录一旦进基线永久不再检查，长会话里后长出的新项目全漏；②`INFRA_DIRS` 硬排除 `handoff/`，nodaroo 交接文档扫不到；③`discover_from_memory.py` 把 `*_bak_*` 备份目录 memory 也扫进来（6 个变化文件里 3 个来自备份）；④`--full` 只重置文件时间，单元差集仍看 known_units，补不回来。技能星图发现链路本身干净（磁盘 287↔星图 287 双向 0 差异）。
- 修复：备份 `2026-10-29-16-13-56_bak_20261126_1408` 后改造——
  - `scan_projects.py`：新增 `unit_signals()` 指纹通道（handoff/SKILL.md/项目报告/README/部署说明的 相对路径+大小+mtime分钟 签名），基线内单元指纹变化也进候选；`handoff/` 移出 INFRA_DIRS（空目录/youdao_tmp 仍排除）；summary 加「指纹补获(基线内新产物)」；state 写 `unit_signals`；**带 handoff 字段的人工节点跳过日期回填**（防 p173 Nodaroo 的 2026-11-24 被 mtime 冲成 11-26）。
  - `discover_from_memory.py`：collect_files 排除 `_bak_`/backup 目录（190→182 文件，备份残留 0）。
  - `sync_skill_starmap.py`：加技能星图双向核验日志（磁盘有SKILL.md但星图无 / 星图有但磁盘全无）；项目 HTML 源按二进制检测 CRLF 并规范化（文本模式会自动转换导致判断失效）。
- 验证：造临时 handoff 测试指纹通道立刻识别；真跑扫描新增 p183/p184；编译全过；编排器 dry-run scan/memory/merge/html_sync/smoke 全 0；双向核验 N=0 M=0；项目/技能各 9 份 HTML 哈希一致。
- 定时任务口径更新：项目星图自动化 `9585354d` 加指纹补获/漏扫告警/unit_signals 检查；技能星图自动化 `fb9851f4` 加双向核验 N/M 必须汇报。

## 14:21-14:25 指纹通道修复与长会话项目发现闭环（P0，已完成 ✅）

- 用户追问「没落 handoff、只在长会话里完成的几个新老项目能被发现吗」。实证：上一版强信号对 4 个今天有产出的单元全为空（`2026-11-17-01-21-22` 8改、`2026-11-26-11-30-34` 6改、lobsterai选股 3改、`2026-11-12-23-22-49` 1改）——强信号通道不够。
- 二次改造：`unit_signals()` 拆强/弱双通道。强信号=handoff/SKILL.md/项目报告/README/部署说明，自动入图；弱信号=任意 md/html 产物变化，只进「待确认候选」不自动建节点，防噪音灌爆星图。state 的 `unit_signals` 从 list 改为 `{"strong":[...],"weak":[...]}`。
- **关键 bug（本次核心）**：指纹循环条件写反——注释说查「已在基线里的单元」，代码却是 `if k in prev_units: continue`，把要查的单元全跳过，强弱信号通道从未真正运行（所以之前弱信号一直显示 0）。备份 `..._bak_20261126_1421` 后改为 `if k not in prev_units or k in picked_keys: continue`。
- 验证闭环（测试文件名必须**不含** handoff 字样，否则会被判强信号）：纯文件 `长会话新项目验证_纯文件_20261126.md` → dry-run 显示 `指纹弱信号(待确认)=1` 并列名；`handoff_验证强信号_20261126.md` → `指纹强信号(可入图)=1` 且自动建节点。测试文件已清理。
- 真实跑完整编排器：scan/memory/merge/html_sync/smoke 全 0。merge 新增 p182/p183（raccoon 的 xray 两项目）。**踩坑**：`p182 raccoon · _t` 名字被临时目录 `_t` 误占——`guess_title` 按「产物最多的子目录」命名，`_t` 有 4 个 json 胜过根目录 SKILL.md。备份 `..._bak_20261126_1423` 后修 `GENERIC_DIRS` 加 `_t/_tmp/tmp/temp/cache/node_modules/__pycache__`，并让 `guess_title` 也读 SKILL.md 标题且跳过 YAML frontmatter。新标题验证为「Xray 跨主机部署（判型 → 场景 → 验证）」。
- 纠正已写入的错误名：projects.json p185 与 8 端 star_map.json p182 全部改新名（改前单文件备份在 `..._bak_20261126_1423`）；重建 HTML 源哈希 `27f1e77ee962850f`，8 端一致。
- 定时任务口径二次更新：项目星图自动化 `9585354d` 第3/4步改为分别汇报「指纹强信号(可入图)」「指纹弱信号(待确认)」，弱信号必须列单元名+文件名等我确认；要求核对 unit_signals 为 dict 格式。技能星图自动化无需改。
- 遗留：`build_starmap.py` 提示 p173 Nodaroo 为孤立节点（无连线）；projects.json 现 186 节点、权威 183（发现层比权威多 3 属正常差集）。

## 14:28-14:31 给 Nodaroo 补 Xray/建站连线（已完成 ✅）

- 用户要求把 p173 Nodaroo 连上 Xray 相关、建站相关节点。备份 `..._bak_20261126_1428`。
- **编号错位注意**：用户看到的 HTML 由发现层 `projects.json` 生成，那里 Nodaroo 是 **p182**（p173 被「微信小程序调研」占用）；权威库 `star_map.json` 里 Nodaroo 是 **p173**。`merge_to_starmap.py` 按 name/path 翻译 scmap，所以在发现层加边即可自动映射到权威库正确编号。
- 在发现层加 5 条 same 边：p182→p185（Xray判型）、p182→p186（Xray SOP 套件）、p182→p61（SnapDeploy 免费容器）、p182→p62（Void.cloud 建站枢纽）、p182→p60（免费 VPS 与代理线）。
- 重建 HTML（186 节点/204 边，哈希 `1cf620adcd7d`）同步 8 端；跑 merge 后权威库新增 7 条边（5 条本次 + 2 条历史漏补 p79→p182 / p53→p183）。核验：权威库 p173 度数 5、8 端 JSON 边数一致、8 端 HTML 哈希一致。


# 2026-11-26 工作日志

## 15:22-15:35 第四轮：两端每栏加本栏张数 + 云端部署（已完成 ✅）

- 备份 `C:\Users\Administrator\lobsterai\project_bak_20261126_1522`（本地两文件 + cf_worker/dashboard.html + 线上 Worker 包 `live_worker_pre_count.bin`）。
- 本地 `scan_realtime.py` / `选股\涨停回调候选股.htm`：持仓 hCnt、严选突破 hitCnt、观察 watchCnt、宽池 brokeCnt、全量 mAllCnt 均按当前实际显示张数赋值；云端 `cf_worker/dashboard.html`：posCnt/hitCnt/watchCnt/brokeCnt/allCnt/evCnt（事件按条），并补 `.allCnt` 样式。
- 云端部署踩坑：Python `wrangler` 是坏包；手搓 multipart 调 CF API 一律 10021 unexpected EOF（probe 最小请求也失败）；最终用 `npx wrangler@3.60.0 deploy --config <wrangler.toml>` + 代理 + XDG_CONFIG_HOME 指向 `AppData/Roaming/xdg.config` 成功。部署 ID `0f8ae596-966a-4035-924a-34a3059d948e`，cron 保持 `*/3 1-3,5-8 * * 1-5`。
- 密钥保留：部署后 bindings 仍为 AUTH_TOKEN/MAIL_PASS/MAIL_TO/MAIL_USER/STATE；线上 worker.js 由 wrangler 从本地源码重新编译（历史线上包 26KB 是编译产物，本地源码 29KB 正常）。
- 验证：py_compile / 两端 JS node --check 通过；本地服务端 5 个计数 ID、云端原始 HTML 6 个计数 ID 全在；WebFetch 云端页面显示严选0/观察0/宽池0/全量37。用户需 F5 加载本地新版。

## 接管 WB 国内版定时任务到国际版（已完成 ✅）

- 背景：用户要求接管国内版所有定时任务，由国际版（本 agent）调度运行。
- 关键事实：国内版与国际版是两套独立 db + 独立调度器。
  - 国内版：`C:\Users\Administrator\.workbuddy\workbuddy.db`（48 条记录，14 条 ACTIVE 且未软删）
  - 国际版：`C:\Users\Administrator\.workbuddy-ai\workbuddy.db`（原有 7 条）
- 用户确认方案：迁移 + 停国内版；只接 14 条有效的；模型接受统一换 `hy4flash-free`。
- 动工前已备份两个 db（在线 backup API，完整性校验一致）：
  - `C:\Users\Administrator\.workbuddy\workbuddy.db.bak_20261126_104206`
  - `C:\Users\Administrator\.workbuddy-ai\workbuddy.db.bak_20261126_104206`
- 依赖检查：14 条任务引用的本机脚本/skill/专家包路径全部存在。
- 已在**国际版创建 14 条任务，全部 PAUSED**（防止与仍在跑的国内版双跑），prompt/rrule/cwds 原样保留。
  - 新任务 ID：01ee7602 / a05963c0 / 6920caf0 / 175aa6da / d86ae6bf / 17760812 / ca752509 / e4856d53 / c501ca7f / 3c9b8058 / d0464243 / bc5e4b1f / 83cd6987 / 14cc5427
- 用户已在国内版暂停全部 14 条（我这边只读复核国内版 db：未删 14 条全部 PAUSED，ACTIVE 残留 0）。
- 国际版 14 条已全部改回 ACTIVE，核验 `MIGRATED_ACTIVE=14`，next_run_at 均已计算（最近的是今天 11:00 签到/巡检、11:30 两个雷达/看板、11:45 老王、12:00 虚拟商品、12:45 看门狗）。接管完成。
- 注意冲突点：国际版原有「天气站城市目录月度维护+增量部署」（alwaysdata 版）与新迁移的「天气站城市目录月度维护（CF 部署）」时间都是每月 15 日 10:00，但目标不同，用户知情保留。


# 2026-11-26 工作日志

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）