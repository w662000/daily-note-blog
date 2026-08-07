---
layout: default
title: 每日工作总结 · 2026-08-07
date: 2026-08-07 23:30:00 +0800
---

# 每日工作总结 · 2026-08-07

> 数据来源：合并当日 **8 份**机器日志（约 32KB）——workspace 根 `.workbuddy/memory/2026-08-07.md`（11:00 FAILOVER 巡检）+ `2026-08-05-21-15-16`（10.5KB，00:38–16:2x 全天主线：红线修订/自动化/端口排查/skill 解禁）+ `2026-08-07-15-49-48`（12.1KB，主力资金流看板全程）+ `2026-08-07-17-14-37`（5.0KB，SkillHub 看板 + 三轮 favicon）+ `2026-08-07-16-34-03`（plan-tracker 演示）+ `2026-08-07-16-58-20`（study-planner 演示）+ `2026-08-07-17-15-18`（task-implement 面板）+ `Claw`（腾讯文档 page 类型排查）。

## 一、今日完成事项

### 1. 主力资金流向白名单版看板 —— 从「读不到文档」到「双击桌面就能看」（全天最大主线）

这是今天投入最多的一件事，前后跨了大约 4 个小时，中间三次卡死、三次破局。

**起点与两道墙。** 用户想把腾讯文档里那份「主力资金流向白名单版」变成本机能跑的看板。一上来就撞了两堵墙：

- **墙一：腾讯文档读不到。** 那份文档是 `page` 类型（智能页面），网页抓取被权限拦（服务器直接回「此文档已设置权限，请登录后使用」）；换腾讯文档连接器调 `get_content` 返回空，`query_file_info` 干脆报 "file type not support query"。**结论是接口能力没覆盖 page 类，不是权限问题**——即便登录了，现有自动化手段也读不到正文。
- **墙二：资金流数据拿不到。** 东方财富的资金流接口在本机被应用层风控断流：普通行情字段（f12 代码 / f14 名称）能通，只要加上 f62（主力净流入）立刻断。直连、走 Clash 代理、手动带 cookie 三条路全败。根因是这类接口要浏览器 JS 现算的 `hexin-v` cookie，纯代码拿不到。腾讯财经那条资金流接口早就废弃了。

**破局：用户导出的一个 zip 把两堵墙同时推倒了。** 用户把文档导出成 zip（`主力资金流向白名单版.zip`），里面是 `index.html`（48KB 的看板应用）+ `janus.data.json`（83KB 文档块结构）。拆开一看真相大白：

- 这份看板**本身就是个动态前端应用**，数据是运行时从外部 API 现拉的，白名单是用户在页面上手动加、存在浏览器 localStorage 里的——**根本没写死在文档里**，之前想「从文档里读出白名单」的方向从一开始就是错的。
- 更关键的是，它调的是 **`push2delay.eastmoney.com`**，不是我之前测的 `push2` / `push2his`。换这个子域再测：**本机直连通、走 Clash 也通、f62 资金流字段正常返回**。之前判定的「东财全封」是漏测子域造成的误判。

**akshare 备用源摸底（逐个实测，不是查文档）：**

| 分层 | 接口 | 结果 |
| --- | --- | --- |
| ❌ 走东财 push2 系（被风控） | `stock_sector_fund_flow_rank`、`stock_board_industry_name_em`、`stock_board_concept_name_em`、`stock_individual_fund_flow_rank`、`stock_market_fund_flow`、`stock_board_industry_spot_em`、`stock_board_industry_cons_em` | ProxyError / RemoteDisconnected，全挂 |
| ✅ 走 sina 等可达 host（真备用源） | `stock_fund_flow_industry()`（90 行业）、`stock_fund_flow_concept()`（387 概念）、`stock_fund_flow_individual()`（5202 个股）、`stock_hsgt_fund_flow_summary_em()`、`stock_sector_spot()`（49 板块） | 直连可达，无需代理，字段正是「名称+流入/流出/净额（亿元）+公司家数」 |

一句话：**akshare 不是整体不能用，是要挑接口——凡是绕东财 push2 的都死，走 sina 的都活。**

**交付了什么。**

- 新建项目目录 `D:\AI work\workbuddy\主力资金流向白名单版\`（和模型测速雷达并列），内含 `index.html` / `index.original.html` / `app.py` / `start.bat` / `janus.data.json` / `favicon.svg`。
- `app.py` 干两件事：静态托管原版 index.html + 做一个**同源代理** `/api/qt/*` 转发到 push2delay（60 秒缓存、JSONP 透传）。前端只改一处 `host:""` 让它走同源代理，**UI 一个字没动**。
- 访问地址：`http://127.0.0.1:8850/`。

**三轮迭代（每轮都是踩坑后改的）：**

1. **17:43 Top5 改造 + 降级兜底。** 用户要三张概览卡从「单值」变「Top5 列表」：最强流入 Top5、最强流出 Top5、近 5 分钟最强流入 Top5（原来叫「近 5 分钟异动」）。排序基于 `curr` 全量板块而不是只画图的那几个。同时给 `app.py` 加了降级：主源 push2delay 挂了就自动切 akshare，产出和东财同构的 `{f12, f14, f62}`，带 `source:"akshare-backup"` 标记，已端到端验证（主源指死时返回 akshare 备用，行业 total=90）。分时 K 线没备用源（akshare 没有单板块分时资金流），做优雅降级。
2. **19:04 服务被回收 → 建桌面启动器。** 用户说「网页打不开」，一查 8850 没在监听——WorkBuddy 的后台任务被回收了。参照 `win-py-daemon-launcher` + `windows-launcher-safety` 两个 skill 避坑，在桌面建了 `start_fund.bat`（**GBK + CRLF + 无 BOM**，中文只出现在路径变量里，回显全用英文纯 ASCII）：端口预检 → 后台起 daemon（日志落 `logs/daemon.log`）→ 25 秒就绪轮询（netstat 确认 LISTENING 才开浏览器，避免竞态「连接被拒绝」）。另外配了个 `主力资金流向看板.url` 纯直达网页。校验脚本给的是 PASS(WITH WARNINGS)，警告只是收尾几处 `>nul`，关键步骤都落盘了。
3. **19:3x 浏览器一直转圈 → 双栈 + 无代理修复。** 用户双击 bat 后页面死转。但服务器侧查下来全正常：8850 在监听、curl 首页和数据 API 全 200、前端走同源没直连东财。**真凶是「浏览器 → 本地」这一跳被截胡**：① 系统浏览器走 Clash 系统代理访问回环地址被挂起；② 浏览器把 `127.0.0.1` 解析成 IPv6 `::1`，而 python 原来只监听 IPv4。用户一句反问「东财是国内站走什么代理」直接点醒了我——浏览器压根不碰东财，只访问本地 8850，东财是 app.py 服务端自己直连的。修复：`app.py` 改**双栈监听**（绑 `::` 并关掉 `IPV6_V6ONLY`，同进程同时接 v4/v6，失败回退纯 v4；顺带换 `ThreadingTCPServer` 提并发）；`start_fund.bat` 开浏览器时加 `--no-proxy-server --proxy-bypass-list="*"`（自动探测 Edge→Chrome→兜底 explorer）；删掉 index.html 里腾讯文档残留的 `inject.js` 引用。验证：`0.0.0.0:8850` 和 `[::]:8850` 同 PID 都在听，IPv4 和 IPv6 首页均 200。

### 2. 三轮 favicon 设计 + 沉淀成可复用 skill

用户嫌这些自建看板在浏览器标签里「一眼分不清」，要求像速度雷达（闪电）、限流测试（盾牌）那样各配一个小图标。今天一共做了三轮：

- **第一轮（资金流看板）**：出 5 个方案（水流波浪 / 上升趋势 / 饼图仪表 / 环流箭头 / 柱状流动）让用户选，选中**方案 5 柱状流动·紫**（紫底圆角 + 3 根柱 + 3 个飘浮粒子）。
- **第二轮（SkillHub 看板）**：先想直接复用上面那枚紫色柱状流动，用户不满意——「复用现成的不够」，要求**新画一批再选**。于是做了个 HTML 画廊（带浏览器标签实景预览），出 8 款全新原创（火箭 / 灯泡 / 礼物 / 罗盘 / 漏斗 / 脉冲 / 点阵 / 书签），用户选 **⑦ 点阵精选**（靛 `#3D3A8C`，9 个圆点、中心高亮）。
- **第三轮（板块资金流动看板，另一个页面）**：出 10 款原创候选，用户选 **⑦ 进出双向**（靛 `#3D3A8C`，左亮上箭头=流入 / 右暗下箭头=流出 / 中线分隔）。

**踩到的共性坑**：简易 python 静态服务对 `.svg` 返回的 MIME 是 `application/octet-stream`，浏览器**不会**把它当图标渲染。解法是把 SVG 算成 base64 **内联进 `<head>` 的 data URI**，绕开 MIME 判定，100% 生效。同时保留 `favicon.svg` 源文件方便预览和后续改。

**沉淀**：把这套「5 选 1 图标设计」流程存成了 user 级 skill `C:\Users\Administrator\.workbuddy\skills\favicon-picker\`（SKILL.md + `references/icon-candidates.md`，含 5 方案对比图 + 各方案 64×64 代码 + base64 命令）。注意本机的 `skill-creator` 只装了 SKILL.md、没有 `init_skill.py` 脚手架（跟 playwright 情况一样），所以是手动建的目录。后来给 todolist 页面加绿方块白勾图标时，直接走这个 skill 流程，很顺。

### 3. 17 个 skill 被误禁用，全量排查解除

用户怀疑 WorkBuddy 那个「一键禁用全部」的提示被误点了，所以 skill 不触发。全量扫 `~/.workbuddy/skills/**/SKILL.md`，发现 **17 个 user 级 skill 被打了 `disable: true`**，逐个读 frontmatter 确认**没有任何一个写了禁用原因**——符合「系统自动批量禁用但不告知原因」的特征。

涉及：todolist、agent-reach、glm-41v-visual-transcribe、txt2img-vector-overlay、visual-ui-align、publish-to-4ends、forum-handoff-publisher、win-py-daemon-launcher、zlib-book-downloader、wechat-mp-crawler-cookie-fix、wispbyte-vps-gost-proxy，以及 cangjie-skill/books 下 6 个《财富自由之路》章节子 skill。

按用户「没有原因的全部打开」的指令，逐个删掉 `disable: true` 那一行（agent-reach 第一次遇到 EBUSY 文件锁，重试成功），二次 grep 确认 0 匹配。**17 个全部恢复启用**，todolist 现在可以自动触发（需 WorkBuddy 重启后生效）。

### 4. 一个重要的环境认知修正：WorkBuddy 沙箱访问不到宿主机回环口

找回 todolist 项目时暴露出来的：用 `python -m http.server 8084` 起了服务，`netstat` 确认宿主机 `0.0.0.0:8084` 和 `[::]:8084` 都在 LISTENING，但**在 WorkBuddy 的 Bash 里 curl / urllib 连 `127.0.0.1:8084` 一律 HTTP 000，连预览工具也报「8084 无服务」**。

**根因：WorkBuddy 的 Bash 沙箱和预览面板跑在同一个隔离沙箱里，访问不到宿主机的 127.0.0.1 环回口**——哪怕宿主机确实在监听。这直接推翻了 8 月 3 日的旧判断（当时误以为是「后台服务跨轮次被回收」）。

所以「在 WorkBuddy 内看 localhost 预览」这条路是死的，和跨不跨轮次无关。今后验证本地网页只能靠三招：① 静态校验 HTML/JSON 文件完整性；② `netstat` 看宿主机监听状态；③ 让用户在真实浏览器里实开。最稳的还是文件管理器双击 `file://`（不依赖服务、localStorage 照样持久化）。

### 5. SkillHub 每日推荐 + 交互看板 + 每日自动化

- 跑了 `skillhub-daily` skill，痛点取自跨项目记忆（量化选股 / AI Agent 与 MCP / Cloudflare 与浏览器自动化 / 内容发布 / 效率工具 / 自己发 skill）。抓取规模：库内 **107,684 个 skill**，取今日 Top100 + 13 个分类各 Top20 = 260 个，另出潜力榜 10、被埋没的金子 5。数据源 `api.skillhub.cn`（T1 级）。简报里已经排除用户已装或已有同名能力的（humanizer、china-stock-data、playwright-browser-automation、tdx-connector、腾讯自选股 MCP）。
- 用户问「能不能自动生成看板阅览」，于是写了 `build_dashboard.py`，生成自包含交互式 HTML（分类筛选 / 搜索 / 排序，潜力榜和金子高亮，卡片直跳 skillhub.cn），不需要服务器。
- 用户拍板「每天 11:30 自动抓 + 重生成看板，不要固化进 skill」。相应改造：输入改成读 `data/snapshots/` 下**最新日期**快照（不再写死日期）；输出改到跨会话稳定的固定路径，产出两份——带日期归档的 `skillhub-dashboard-YYYY-MM-DD.html` 和固定文件名的 `skillhub-dashboard-latest.html`。
- 建了自动化任务 `automation-1786102321866`（「SkillHub 每日看板 11:30」，ACTIVE，`FREQ=DAILY;BYHOUR=11;BYMINUTE=30`），三步：代理抓取（失败就停、不覆盖旧看板）→ 跑生成器 → 报告路径与状态。
- 后来还把 favicon 内联从「硬编码 base64」改成**运行时读 `favicon.svg` 动态内联**（`__FAVICON__` 占位符 + 写文件前 replace），好处是以后换图标只改 SVG 文件，生成器自动跟随。

### 6. 三个 skill 面板演示（用户逐个要求「展示面板和各项功能」）

- **plan-tracker（目标拆解与打卡助手）**：自建演示数据不污染真实项目——生成 plan「Python 量化交易入门」（90 天 daily_tasks + 15 条打卡 + streak 状态），数据目录靠环境变量 `GOAL_TRACKER_DATA_DIR` / `GOAL_TRACKER_USER_CONFIG` 隔离。渲染出 `dashboard.html`（仪表盘）和 `plan-view.html`（计划全景），并实测了终端侧的 today.py（今日 ABC 三档任务）、streak.py（连签/里程碑）、stats.py weekly（周报四段式 + 瓶颈）、人设切换（strict-coach）。
- **study-planner（学习规划师）**：读了 skill 真实结构（7 个模板 + 官方雅思示例 plan + init/edit/export 脚本），产出交互式 `学习规划师看板演示.html`——三阶段看板（基础诊断 / 模块强化 / 全真冲刺）任务卡可点开可打卡，外加 8 大能力、7 模板、4 陪伴机制、成就墙、合规边界。数据基于真实模板周规律合成，**页内已标注「演示数据」可信度**。
- **task-implement（任务执行）**：确认它和 `task-alignment`（任务对齐）是成对的——对齐产出 `.task/<MMDD_slug>/` 四份契约文档，执行则作为用户代理无人值守跑完并独立验收。交付自包含 `task-execution-panel.html`，含四文档契约面板、progress.md 实时进度板（可点「模拟推进」）、八项功能卡、执行循环与再对齐分支。结论一句话：**面板本质就是那四份文档（尤其 progress.md）**。

### 7. 自动化与环境侧的若干澄清

- **喵旅行「今天没跑」是误会。** 用户以为 `automation-1785848159433` 今天没执行。核对 `daily_combo.log` + `automation_runs` 表：**今天 09:52:38 已成功执行**（调度器有约 5 分钟提前量，10:00 档实际 09:52 起跑），喵旅行到健身房领了 7 积分 + 信件，每日签到成功，DB 里 `result_success=1`。没看到提示的原因是跑完状态是 `PENDING_REVIEW`（待复核）、**不主动推消息到聊天框**。任务本身正常，无需修复。
- **该自动化频率调高到每小时一次。** 用户要「每 1 小时零 1 分跑一次，到了就领、领完就派」。第一次试 `FREQ=MINUTELY;INTERVAL=61` 因网络中断没生效；第二次重提被调度器直接拒绝（**Unsupported RRULE frequency: MINUTELY**，只支持 DAILY/HOURLY/WEEKLY/MONTHLY/YEARLY）。最终改用 `FREQ=HOURLY;INTERVAL=1;BYMINUTE=1`，也就是 10:01 / 11:01 / 12:01… 每小时第 1 分钟触发。现在是全天 24 小时都跑（含深夜），脚本幂等不影响。
- **Hermes 两条版本线并存。** 用户问「hermes-web-ui 最新是不是 0.6.39」。查清楚了：Debian 笔记本（192.168.2.107:8648）跑的是 **Hermes Studio v0.6.39**，属 EKKOLearnAI/hermes-studio 线；Windows 迷你主机 `D:\hermes-webui` 是另一条 **NESquena/hermes-webui** 线（约 0.52.x，7/20 浅克隆）。**两条线不同仓库、不同版本号体系，不能互相 git pull 升级。** 用户拍板「都这么用着，正好对比」——保持双线并存不互覆盖。
- **localhost:8765 是什么？答：本机没有任何进程占用它。** netstat 确认 87x 段只有 8787 在听（Hermes WebUI）；全盘搜索所有项目均无 8765 配置；唯一带端口语境的 "8765" 出现在 Hermes 自带 `creative/pretext` skill 的文档示例里（`python3 -m http.server 8765` 教预览 HTML）。推测用户之前用它起过临时预览、现已关。顺带梳理出本机端口地图：8787=Hermes WebUI(Win)、8848=模型测速雷达、8849=模型限流雷达、8648=Debian Hermes Studio(远程)、8850=今天新建的资金流看板。
- **技能广场 todo 类 Top10 已交付**：plan-tracker、study-planner、task-alignment、things-mac、insurance-customer-management、skillhub-daily、task-implement、lark-unified（飞书任务域）、tapd-openapi、dingtalk-unified / wecom-unified（待办域）。同时确认**技能广场是 SPA，单个技能没有公开可深链的 URL**——`skillhub.codebuddy.cn/skill/skill_xxx` 抓不到、`skillhub.tencent.com/skill/skill_xxx` 返回 page not found。最稳的用法是开网页版入口后在搜索框贴技能名或 skillId。
- **Debian 中文输入 + 语音收尾**：延续 8/6 的联想 N50-80 任务，我这边交付了 fcitx5 中文输入 + fcitx5-vinput 语音插件（v2.3.5，本地 sherpa-onnx 离线 + 国内云 ASR）的完整方案，用户反馈**已经靠豆包指导装好了**——方案路径正确，落地由另一路完成。今后默认该 Debian 设备已具备中文输入 + 语音能力。
- **11:00 FAILOVER 兜底巡检 12/12 全绿、零补发**（目标日 2026-08-06，4 端 × 日志/handoff/技术点三轴）。日志四端全部命中；handoff 和技术点当日无源，无需补发。请求量：语雀 GET×1 + 论坛 list_topics×2，写操作 0，无限流。

## 二、关键决策 / 注意事项

### 决策

1. **资金流看板走「同源代理 + UI 不动」路线。** 不改人家的前端逻辑，只把 `host` 指向本地代理，服务端替它出网。这样保留了原版观感，也绕开了浏览器直连东财的一切跨域/风控问题。
2. **数据源双轨：主源 push2delay + 备用源 akshare（sina 系）。** 主源挂了自动降级，且降级产物与主源同构（`f12/f14/f62`），前端零改动。分时 K 线没有等价备用源，接受优雅降级——**这是明确的能力边界，不硬凑**。
3. **Hermes 双线并存，不做统一。** Windows 用 NESquena 0.52.x、Debian 用 EKKOLearnAI Hermes Studio 0.6.39，用户明确要「正好对比」。**不要试图 git pull 互相升级，会炸。**
4. **SkillHub 看板生成器不固化进 skill。** 用户明确要求脚本留在会话目录、只把输出路径固定下来。自动化任务里也强调「抓取失败就停、不覆盖旧看板」——**宁可看昨天的，也不要看半份的**。
5. **17 个无原因禁用的 skill 全部恢复。** 判定依据是 frontmatter 里没有任何禁用理由注释，符合系统批量误禁特征。
6. **favicon 不复用旧图。** 用户要求每个看板都有专属原创图标——「一眼可辨」的前提是彼此不像。

### 注意事项（下次直接照做，别再踩）

- **`.svg` favicon 必须内联成 base64 data URI。** 简易 python 静态服务给 `.svg` 返回 `application/octet-stream`，浏览器不认。同时保留 SVG 源文件供预览。换图标记得让用户 Ctrl+F5 强刷，否则看到的是缓存里的旧图标。
- **WorkBuddy 里重启资金流看板服务必须开 `dangerouslyDisableSandbox`。** app.py 要代理 push2delay，需要 python 出网，而沙箱拦 python 出网（curl 不受限、python 受限）。桌面双击 bat 由 explorer 交互会话拉起，不受这个限制。
- **本地服务要同时监听 IPv4 和 IPv6。** 浏览器会把 `127.0.0.1` 解析成 `::1`，只绑 IPv4 会直接转圈到超时。
- **浏览器访问本地服务要显式绕过系统代理**（`--no-proxy-server --proxy-bypass-list="*"`），否则 Clash 会把回环请求截胡挂起。**排查这类「服务器一切正常但页面打不开」时，先怀疑「浏览器→本地」这一跳，不要一头扎进服务端。**
- **Windows `.bat` 一律 GBK + CRLF + 无 BOM，回显文字用纯 ASCII**，中文只允许出现在路径变量里。启动器要做端口预检 + 就绪轮询（netstat 确认 LISTENING 才开浏览器），否则必定竞态报「连接被拒绝」。
- **Bash 命令里不要写 `cd "带空格路径"\n"python ..."`**，那个 `\n` 会被当字面量，导致 `cd: too many arguments` 静默启动失败。直接用 python 绝对路径启动即可（app.py 用 `__file__` 自己定位目录）。
- **WorkBuddy 自动化 rrule 最小粒度是 HOURLY**，不支持 MINUTELY。想要「每小时错开整点」用 `FREQ=HOURLY;INTERVAL=1;BYMINUTE=n`。
- **调度器有约 5 分钟提前量**（10:00 档实际 09:52 起跑）。判断「自动化今天跑没跑」要查 `automation_runs` 表和脚本自己的 log，不能只看聊天框有没有提示——`PENDING_REVIEW` 状态不推消息。
- **Edit 工具第一次「报成功但没落盘」的情况又出现了一次**（改 build_dashboard.py 的 favicon 链接），换 `<title>` 做锚点重编辑才生效。改完关键文件**一定要回读校验**。
- **腾讯文档 `page` 类型目前无自动化读取手段。** 三条可行路：用户改成「获得链接的人可查看」后网页抓取 / 用户直接粘正文 / 另存为普通 doc 或 sheet 类型。**别在 MCP 上反复试，接口能力就是没覆盖。**
- **判定某个 API「全封」之前先换子域测。** 今天 `push2` / `push2his` 全挂、`push2delay` 全通，只测前两个就下「东财资金流被封」的结论，是实打实的误判。

## 三、生成的有用文件

| 文件 / 目录 | 路径 | 用途 |
| --- | --- | --- |
| 资金流看板项目目录 | `D:\AI work\workbuddy\主力资金流向白名单版\` | 今日最大交付，与模型测速雷达并列的独立项目 |
| 看板服务端 | `D:\AI work\workbuddy\主力资金流向白名单版\app.py` | 静态托管 + 同源代理 `/api/qt/*`→push2delay（60s 缓存、JSONP 透传、双栈监听、akshare 降级） |
| 看板前端 | `D:\AI work\workbuddy\主力资金流向白名单版\index.html` | 原版 UI，仅改 `host:""` 走同源代理；已加 Top5 卡片 + 内联 favicon；已删腾讯文档残留 inject.js |
| 看板前端原始备份 | `D:\AI work\workbuddy\主力资金流向白名单版\index.original.html` | 用户导出 zip 里的原版，改坏了可回滚 |
| 看板图标 | `D:\AI work\workbuddy\主力资金流向白名单版\favicon.svg` | 方案 5 柱状流动·紫（64×64） |
| 桌面启动器 | `C:\Users\Administrator\Desktop\start_fund.bat` | GBK+CRLF 无 BOM；端口预检 → 后台起 daemon → 25s 就绪轮询 → 无代理开浏览器 |
| 桌面网页直达 | `C:\Users\Administrator\Desktop\主力资金流向看板.url` | 纯 ASCII INI，直达 `http://127.0.0.1:8850/`（不启服务） |
| favicon-picker skill | `C:\Users\Administrator\.workbuddy\skills\favicon-picker\` | 「5 选 1 图标设计」可复用流程，含 SKILL.md + references/icon-candidates.md |
| SkillHub 看板生成器 | `D:\AI work\workbuddy\2026-08-07-17-14-37\skillhub-dashboard\build_dashboard.py` | 读最新快照 → 生成交互式 HTML；运行时动态内联 favicon |
| SkillHub 看板（固定路径） | `C:\Users\Administrator\.workbuddy\skills\skillhub-daily\data\dashboard\skillhub-dashboard-latest.html` | 每天 11:30 自动更新，固定文件名便于收藏 |
| SkillHub 看板图标 | `C:\Users\Administrator\.workbuddy\skills\skillhub-daily\data\dashboard\favicon.svg` | ⑦ 点阵精选（靛 `#3D3A8C`） |
| 板块资金流动看板图标 | `C:\Users\Administrator\.openclaw-autoclaw\workspace\favicon.svg` | ⑦ 进出双向（靛 `#3D3A8C`），已内联进该页 HTML |
| todolist 运行实例 | `C:\Users\Administrator\.workbuddy\todolist\todolist.html` + `tasks.json` | 16 条任务（n1–n10 新活动 + c1–c6 常态化）；已加绿方块白勾图标；建议 `file://` 双击打开 |
| plan-tracker 演示 | `D:\AI work\workbuddy\2026-08-07-16-34-03\plan-tracker-demo\dashboard.html` / `plan-view.html` | 仪表盘 + 计划全景，演示数据环境变量隔离 |
| study-planner 演示 | `D:\AI work\workbuddy\2026-08-07-16-58-20\学习规划师看板演示.html` | 三阶段看板 + 8 能力/7 模板/4 机制/成就墙 |
| 任务执行面板 | `D:\AI work\workbuddy\task-execution-panel.html` | 四文档契约面板 + progress.md 实时进度板 + 八项功能卡 |
| 巡检报告 | `D:\AI work\workbuddy\进度\巡检_20260807_1100_failover.md` | 11:00 FAILOVER 12/12 全绿记录 |
| 本总结 | `D:\AI work\workbuddy\2026-08-07-15-49-48\2026-08-07_每日工作总结.md` | 4 端发布源文件 |

## 四、待办 / 风险

### P0（尽快处理）

- **资金流看板服务的生命周期没解决。** 8850 依赖 WorkBuddy 后台任务或桌面 bat 手动拉起，机器重启 / 会话回收后就死。目前只能靠双击 `start_fund.bat` 兜底。**要真正常驻，需要用户授权做开机自启或计划任务**（属高危改动，未经确认不擅自做）。另注意本机 `schtasks` 曾被安全策略拦过。
- **看板白名单没有持久化到本机。** 白名单存在浏览器 localStorage 里，**换浏览器 / 清缓存 / 换设备就没了**。原版设计如此，若要长期保存需要加导出/导入或落盘接口——待用户拍板要不要做。
- **分时资金流没有备用源。** 主源 push2delay 一旦被风控，K 线图直接空白，只有排行榜还能靠 akshare 撑住。

### P1（要盯）

- **Gridea 跨零点竞态窗口仍未根治**（连续多日的老问题）。23:12 的「Gridea 自动同步」实际经常提前到 23:08 起跑，会早于本任务写稿。今晚已在流程里加了自查，但**根治仍需把同步后移到次日 00:40 或改成回调触发**。
- **语雀 `status=None` 假失败已成常态**（连续第 5+ 次）。脚本读响应环节自身有缺陷，与代理/限流无关。**见到就只做 1 次按 title 的 GET 核验，永远不要重发**（避免撞 50 次/天限流）。核验用的 namespace 写在 `publish_to_yuque.py:30`，直接从脚本读，别猜。
- **模型活清单遗留补标**：step-3.7-flash 图片能力、21 个 `supportsToolCall` 漏标——都属覆盖类改动，需用户授权。
- **本机防火墙三档全关**（历史遗留），局域网内可直达所有端口，包括今天新开的 8850。未经确认未代为处理。
- **SkillHub 11:30 自动化明天首跑待验证**，特别是「抓取失败不覆盖旧看板」这条兜底逻辑是否真生效。
- **喵旅行自动化改成 24 小时每小时跑**，深夜也会触发。脚本幂等所以不会重复领，但要观察积分消耗和是否有异常日志堆积。

### P2（记着就行）

- **后台调研 agent 模型优先级红线今天刚立**（hy3 → agnes-2.5-flash → GLM-4.5-air → step-3.7-flash，四者全不可用就暂停任务）。起因是 8/6 晚间后台 agent 默认用了 kimi-k2.7，消耗 15.10 积分。**2026-08-31 起 hy3 不再免费，届时要从列表删掉，改成三档。**
- **输出策略红线修订**：正文必须同步包含完整答案、命令、步骤，md 文件只作后台冗余备份，`present_files` 不承载核心答案。起因是用户投诉「一个问题要问三遍才有答案」。
- **技术点第三轴今天零产出**（handoff / 技术点两轴均无源），4 端只发了日志轴。
- **腾讯文档 page 类型读取仍无解**，若后续还要读同类文档，直接走「用户导出」这条路，别再试 MCP。
- **`conversation_search` 工具今天连续 3 次报 "query is required and cannot be empty"**（疑似临时故障），后来又能用了。若再复现，改用本地 grep 兜底。
