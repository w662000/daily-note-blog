---
layout: default
title: 技术点 · 2026-11-26
date: 2026-11-26 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-26-10-42-34\.workbuddy\memory\2026-11-26.md, D:\AI work\workbuddy\2026-11-26-21-10-26\.workbuddy\memory\2026-11-26.md

## 21:15 skill 清单 + 加模型 handoff 汇总（纯检索，无配置改动）
- 用户要求：列出 skill 目录里跟"新增模型/给其他agent装模型"相关的 skill，并分别写出最近成功加模型的 handoff。
- 锁定 4 个加模型 skill：`custom-model-onboarding`（总入口五端）、`autoclaw-add-model`（au 1.x/2.0/国际版）、`lobsterai-batch-model-import`（龙虾）、`zcode-batch-model-import`（ZCode）。辨析排除 `cross-agent-skill-install`（装 skill 非装模型）。
- 各 skill 最近成功案例（均本地 T1 记录）：onboarding=11-25 SenseNova 五端同步；autoclaw=11-24 au 国际版 +11；lobsterai=11-25 custom_2 换 6 模型（+9-23 对齐68）；zcode=11-16 WB 41 条 DECODE_OK。
- 产物：`加模型skill清单与最近成功handoff_20261126.md`；进度备份 `进度/进度_20261126_2115_加模型skill清单与handoff.md`。
- 未重启任何 agent、未改任何配置。会话ID：3c322604-5c56-4804-bec5-79b6075b55a7


# 2026-11-26 工作日志

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-26-10-38-56\.workbuddy-ai\memory\2026-11-26.md, D:\workspace\workbuddyai\2026-11-26-12-43-58\.workbuddy-ai\memory\2026-11-26.md

## 13:07-13:09 共有标记口径纠错（用户质疑 43 → 查因并修回 17）

- 根因（T0）：旧 HTML 的 32 个 `cover=6` 节点**全部缺 wb-intl 和 au-intl 两端**（生成时漏扫这两端），我的新脚本补全 8 端后 cover 6→8，又用 `shared = (cover==8)` 自动推导，把旧 HTML 实际 17 个共有误膨胀到 43。用户记忆的 14 来自 SKILL.md 旧列表（漏写 memory / skill-creator / skill-vetter 三个）。
- 被误标 26 个：17 个原本 cover=6 的已标节点被改 cover=8 后连带标 shared；9 个是今天新发现的节点（autocli-skill、last30days、skill-star-map、qiaomu-opencli-* 5 个、qiaomu-smart-search）。
- 修复：`sync_skill_starmap.py` 的 `rebuild_data` 改为 **shared 保留旧值、新节点 shared=False**；cover 仍按磁盘实测刷新（8/8 是对的）。从备份恢复权威 HTML 的 17 个标记后重新同步 8 端。
- 核验：HTML/JSON 287 节点、shared **17**、cover=8 **43**（两者不再混为一谈）；8 端 HTML/JSON/SKILL.md 哈希各一致；dry-run 0 变更。
- SKILL.md 共有列表补齐 17 个，并写明 shared 是人工语义标记、不按 cover 自动推导。

## 13:23 溯源技能星图 HTML「本体」（只读调查）

- 全盘共 18 份 `skill星空图*.html`。用户给的 `AutoClaw...\projects\Default\skill星空图-全量.html` 是 **11:56 旧版**：277 节点、65,453B、sha `e0a4597a1b45`、标题「全量 277 Skill」，与备份中 8 份旧版逐字节一致——它是当时的生成落点/过期快照，**不在当前同步链里**。
- 当前唯一权威源 = `C:\Users\Administrator\.workbuddy-ai\skills\skill-star-map\data\skill星空图-全量.html`（13:08，287 节点，69,110B，sha `0cddd79dc8cc`），`sync_skill_starmap.py` 的 `AUTHORITY_HTML` 指向它；8 端副本哈希一致。
- 「14 个共有」的数字来源找到：11:14 的 `projects\Default\skill星空图.html`（**75 节点版**，shared=14、cover=8 有 29），不是全量版的数字。另有 10:31 附件目录一份 SVG 版 75 节点图。277 版 shared=17。
- 用户决定「纳入同步」。已从备份目录留底旧版（`au-intl-projects-default__skill星空图-全量.html`，sha `e0a4597a1b45`），再改 `sync_skill_starmap.py` 增 `VIEW_HTML_AU_INTL` 常量（从 au-intl skill 根上溯三级到 `projects/Default`），`sync_skill_html` 在八端之外多写 1 份查看副本。
- 13:31 实跑：查看副本由 277 节点旧版更新为 287 节点（sha `0cddd79dc8cc`），**9 份 HTML 哈希全一致**；dry-run 显示 9 份 0 更新，幂等。
- 顺手修正 SKILL.md 里「刷新 shared」的错误描述（实际是保留 shared、只刷新 p/cover），并写明共 9 份 HTML，同步八端。

## 13:35-13:39 修复技能星图标签显示（已完成 ✅）

- 用户反馈：平台下载类节点只有粉色星星、没有名称。数据侧排查：212 个平台类节点 name/c/r/p 全完整，c 全在 CL 内；非 DATA 部分与备份逐字一致（不是同步脚本改坏的）。
- 根因：原标签渲染按星级降序 + 严格防重叠；75 个自建类多为 3-5 星先占满位置，187 个 2 星平台类几乎全被 skip。项目星图同样逻辑但节点权重分布不同，没暴露。
- 修复：改权威 HTML 的标签块——低星（1-2 星）用 9.4px 小字号 + 收紧碰撞盒（只避让高星标签、同档允许适度靠近），平台类名称改用浅粉色 `lighten(PLATFORM_COLOR,0.46)` 与星星配色一致；高星保持 12.2px 和原逻辑。补 JS 括号平衡检查通过。
- 备份：`..._bak_20261126_1252\skill_data_backup\pre_label_fix__skill星空图-全量.html`（修复前 sha `0cddd79dc8cc9f2f`）。
- 13:38 同步：9 份 HTML 全部更新，哈希 `28569e87b109` 一致；因同步器以权威 HTML 为模板，后续定时重建会保留此修复，不会回退。
- 环境无 playwright，未能截图自动验证，已用 present_files 打开预览供用户目视确认。

## 15:00-15:05 涨停回调看板：本地/云端严选池报警差异查因与修复（已完成 ✅）

- 项目星图：p43「涨停回调候选股站点 zt-site」（autoclaw，星图 path 指向 `.openclaw-autoclaw/workspace/.openclaw-attachments`，实际线上文件不在此）。
- 真实路径：本地页 `C:\Users\Administrator\lobsterai\project\选股\涨停回调候选股.htm`（8844 由 `hold_sync_server.py` 托管，WEB_ROOT=选股）；云端 Worker 源码 `C:\Users\Administrator\lobsterai\project\cf_worker\worker.js`，页面读 `https://zt.780.de5.net/pool.json`。
- 结论：报警差异不是算法/数据源不同，是**本地浏览器旧标签页**。两份最新池子（11-26 10:25:22）严选子集都为空。
- 证据：本地当前 HTML `const CANDS = []`，候选_20261126.json 无 001226/600408；云端 pool.json 37 只、严选 0。截图两票参数与 `涨停回调候选股261120.htm` 内嵌值逐字一致（板日 2026-11-10、gap 7、拓山 ey=41.023/pc=39.53/dc=5.5，安泰 ey=3.54/pc=3.41/dc=6.6）；其最后出现在 11-18/11-20 扫描，11-26 已剔除。
- 根因（T0）：本地模板页脚写「每1分钟整页重载以更新候选池」，但模板与历史页面里**从未有 location.reload**，只刷行情不换池子；云端每轮 fetch `/pool.json`（no-store）自动换池。
- 修复：先整目录备份 `C:\Users\Administrator\lobsterai\project_bak_20261126_1500`（diff 校验一致）。在 `scan_realtime.py` 模板 + 当前生成 HTML 增加每分钟 HEAD 检查 `Last-Modified`，服务端文件更新则自动 `location.reload()`，并修正页脚文案。py_compile 通过；服务端页面已含自愈逻辑；编译产生的 .pyc 已从备份还原。最终差异仅 scan_realtime.py 与 选股/涨停回调候选股.htm（cloud_daily.log 由后台任务自行变化）。
- 用户侧动作：旧标签页会在 1 分钟内自愈；按 F5 可立即对齐。

## 15:05-15:10 第二轮：宽候选池数量 5 vs 7 查因与对齐（已完成 ✅）

- 用户刷新后严选池已对齐（两边均 0），但本地「已突破EMA7·候选池」5 张 vs 云端「宽候选池·已突破EMA7」7 张。
- 根因（T0）：本地 `broke_js` 由 `scan_realtime.py` 在 10:25 扫描时快照生成（`现价>EMA7 且 gap>=3`），盘中后来突破的票不会进列表；云端每轮用全部 37 只实时重算同条件，多出小熊电器(002959)、泰嘉股份(002843)。另本地徽标用「真上穿」(昨收≤EMA7×1.02) 而云端宽池用 plainBroke(站上即算)，导致本地 5 张全显示「未上穿/回踩」。
- 修复：二次备份 `C:\Users\Administrator\lobsterai\project_bak_20261126_1505`（仅两文件）。把本地模板和当前 HTML 的中部栏改为遍历 ALLPOOL 全池实时重算（`plainBroke && g>=3`），徽标统一为突破✅并额外标「真上穿」，语音与新宽池集合同步；栏目标题改为与云端一致。
- 验证：py_compile 通过；抽取脚本 node --check 通过；用同一腾讯行情源复算 WIDE_NOW=7，与云端截图 7 只逐只一致（000521/002959/002843/600410/000530/002199/603004）；服务端页面已含新逻辑。用户侧需再 F5 一次加载新页面。

## 15:10-15:15 第三轮：底部全量池数量与灰色卡片口径（已完成 ✅）

- 用户反馈本地底部「候选池·10日2板（37只）」而云端看起来更多、且卡片发灰。
- T0 核对：本地 ALLPOOL 37 只、云端 KV pool.json 37 只，`SAME_SET=True`，两边代码集合完全一致；云端视觉上更多是因为它还有宽池 7 只独立面板（本地第二轮已补齐）。
- 灰色含义：云端 `card()` 在 `!pr.price`（无实时行情）时返回 `.stk.far`（opacity .5 + saturate .55）+「无行情」标签；不是被淘汰、也不是信号，只表示行情没拿到。本地 CSS 本来就有 `.stk.far`，但底部栏从没用过，而是显示缓存价/`…`。
- 修复：三次备份 `C:\Users\Administrator\lobsterai\project_bak_20261126_1512`。本地模板+当前 HTML 底部全量栏改为：无实时行情即灰卡+「无行情」，不再用缓存价冒充实时；页脚加「灰色卡片=无行情（与云端同口径）」。py_compile 与 node --check 通过，服务端页面已更新。

## 15:42-15:50 新建 zt-dashboard-deploy skill 并分发六端（已完成 ✅）

- 新建 skill：源在 WB 国内版 `C:\Users\Administrator\.workbuddy\skills\zt-dashboard-deploy\`，含 `SKILL.md`、`references/deployment.md`、`scripts/deploy_cloud.py`（刷新 token + wrangler@3.60.0 部署，支持 --dry-run，静默无窗）。记录本地生成/publish_site、云端部署、对齐清单、KV 额度与踩坑（API 手搓 multipart 10021、wrangler Python 坏包）。
- 校验：skill-creator quick_validate 通过；脚本 py_compile 通过；实跑 `--dry-run` 成功（Total Upload 52.76 KiB，绑定正常）。
- 分发：`sync_skill.py zt-dashboard-deploy --to wb-intl au au-intl loomy raccoon`，五端均新装成功；加源端共 6 端。脚本内置绿灯闸按 8 端检查，因按要求未装 zcode/lobsterai 报 RED（预期），改用 SHA256 手工验收：6 端三文件哈希全一致。
- 注意：新 skill 需各 agent 新开会话才会加载。

## 16:04-16:10 新增 SLG WordPress 发布端（技术点链，已完成 ✅）

- 用户要求在原 4 端/5 物理落点基础上新增 `https://slg.de5.net/`（WordPress blog）。项目星图 p57/p154 指向旧 SLG 攻略中心，实际凭证与发布脚本在 `D:/workspace/autoclaw_zai/wp-kb/config.json`（site/user/app_password/notes），只读探测确认 `wp-json/wp/v2` 可达：全站 765 篇；分类 id：工作日志 3（151篇）、项目流 4（270篇）、技术点 5（344篇）。`kb_publish.py` 说明必须发送 HTML（Ultimate Markdown 不会渲染 API 送入的 MD）。
- 先整目录备份 `D:/AI work/workbuddy/handoff_bak_20261126_160419`（101MB，diff 校验一致），并把 automation `6920caf0-aa43-46fd-9bbb-0791b687c8fa` 原 prompt/配置备份为 `automation_6920caf0_before_slg.json`。
- 新建 `D:/AI work/workbuddy/handoff/slg_blog_publish.py`：按 external-write-idempotency-gate G1~G5 实现——G1 全量分页+X-WP-Total 对账+最小 700 篇断言；G2 站点历史同名组证明不能靠重复 POST 报错兜底；G3 单次默认最多 20 写；G4 JSONL 台账 `slg_blog_ledger.jsonl`；G5 `audit` 只读报告落 `slg_blog_reports/`。凭证只从配置读入内存，日志/报告不输出敏感值。
- 修改 `techpoint_flow.py`：技术点 publish 从 4 通道扩为 5 通道/6 物理落点，新增调用 `publish_slg_blog_techpoint()`（`sync --axis techpoint --source-dir UPDATE_DIR --trigger techpoint_flow`）。更新 automation 名称与 prompt 为「5通道/6落点核验」，加入 SLG 只读 audit 与幂等补发命令，禁止自行放大写入熔断。
- 验证：只读 API 探测成功；脚本 AST/语法检查通过；`sync --dry-run` 不写远端；`audit --axis techpoint --since 2026-11-01` 全量 765、目标 3、台账缺失 0、同名组 0；用 `_handoffs` 历史源 dry-run（since 2026-08-01）显示 300 候选、290 已存在、**10 篇未发布**（未擅自补发，待用户确认）；敏感值泄漏检查 False。
- 编译产生的 pyc 已清理/从备份还原，最终差异仅 `slg_blog_publish.py`、`techpoint_flow.py`、`slg_blog_reports/` 与备份目录中的 automation 备份。


# 2026-11-26 工作日志

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）