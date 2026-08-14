---
layout: default
title: 交接文档 · 用户级 Skill 清单 v1.3（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

> 来源：2026-08-14-13-34-35\用户级skill清单_20260814_v1.3.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# 用户级 Skill 清单 v1.3（~/.workbuddy/skills）

> 扫描时间：2026-08-14 ｜ 共 **51** 个用户级 skill（已剔除 node_modules 依赖）
> **★ 我参与制定 24 个**（全部已写入 `agent_created: true`，含本次永久化的 9 个）｜ 其余 27 个
> v1.3 相对 v1.2 变化：① 9 个手动补进 skill 已永久化（SKILL.md 写入 `agent_created: true`，备份见各目录 `SKILL.md.bak-agent_created-20260814_223000`）；② 两表均新增「触发词」列，取自各 SKILL.md 真实内容。

## ★ 我参与制定的 skill（24 个）

| # | Skill ID | 版本 | 来源 | 用途说明 | 触发词 |
|---|---|---|---|---|---|
| 1 | `agent-plan-router` | 1.0.0 | 我参与制定 | A/B/C 计划路由(A=六顶思考帽+RACI+多Agent；B=情境路由；C=PDCA) | 用A计划执行/用A执行 |
| 2 | `agent-reach` | 1.0.0 | 我参与制定 | 无需API的跨平台调研与素材采集 | 跨平台搜一下 / 帮我找关于X的资料 / 搜索多个平台 |
| 3 | `agnes-media-gen` | — | 我参与制定 | Agnes AI 文生图 / 图生视频生成 | （无显式触发词；按需求描述语义触发） |
| 4 | `cf-58-scraper-replicate` | — | 我参与制定 | Cloudflare 全栈 58同城爬虫复刻(Worker+D1+KV+Pages 看板) | 参考上次的 58 爬虫再做一个 XX 城市/买房/租房项目 |
| 5 | `favicon-picker` | — | 我参与制定 | 为网页/看板生成 favicon 多候选方案 | （无显式触发词；按需求描述语义触发） |
| 6 | `forum-handoff-publisher` | — | 我参与制定 | 本地 handoff/markdown 批量发布到 bbs1org 论坛与免费主机 | 把 handoff 发到论坛 |
| 7 | `gentle-ratelimit-test` | 1.0.0 | 我参与制定 | 温和验证模型/API 限流(429/503)，单次低频不轰炸 | 测限流 |
| 8 | `glm-41v-visual-transcribe` | — | 我参与制定 | 视觉模型转述模式(先文字描述图片再作答，历史可继承) | （无显式触发词；按需求描述语义触发） |
| 9 | `model-rate-limit-radar` | 2.0.0 | 我参与制定 | 对活清单全模型按平台并发探测限流，本地看板(8849) | 模型测限流雷达 |
| 10 | `multi-agent-pdca` | 1.0.0 | 我参与制定 | 通用 PDCA 多 agent 协作骨架(调查员+规划+红队+执行) | （无显式触发词；按需求描述语义触发） |
| 11 | `port-list` | — | 我参与制定 | 本机开放端口清单看板(netstat 扫描+项目标注+本地 http 展示) | 端口清单、扫描端口、端口列表、哪些端口开着、开放端口、本机端口、netstat 查端口、命令行查端口。 |
| 12 | `skillhub-daily` | 6.2.0 | 我参与制定 | 每日扫描 SkillHub 全站 Top100+7分类 Top20 推荐 | 每日推荐、SkillHub 日报、潜力Skill、帮我推荐技能。 |
| 13 | `todolist` | — | 我参与制定 | 通用任务清单/待办系统 | todolist、待办、任务清单、把 XX 加入清单、导入清单、打开我的清单。 |
| 14 | `tri-agent-investigation` | — | 我参与制定 | 陌生API/错误码三方调查法(调查员+规划+红队) | （无显式触发词；按需求描述语义触发） |
| 15 | `txt2img-vector-overlay` | 1.0.0 | 我参与制定 | 文生图 + 矢量叠加做海报/壁纸 | （无显式触发词；按需求描述语义触发） |
| 16 | `visual-ui-align` | — | 我参与制定 | UI/网站/主题视觉对齐 | （无显式触发词；按需求描述语义触发） |
| 17 | `wechat-mp-crawler-cookie-fix` | 2.0.0 | 我参与制定 | 微信公众平台爬虫静默0条故障排障(含2026-07-30接口关停) | （无显式触发词；按需求描述语义触发） |
| 18 | `win-py-daemon-launcher` | 1.0.0 | 我参与制定 | Windows 下 .bat 一键启 Python 服务避坑 | （无显式触发词；按需求描述语义触发） |
| 19 | `windows-launcher-safety` | 2.0.0 | 我参与制定 | 写 .bat/.cmd/.lnk 前的避坑自查清单 | 写个 bat |
| 20 | `wispbyte-vps-gost-proxy` | — | 我参与制定 | wispbyte VPS gost 代理 | （无显式触发词；按需求描述语义触发） |
| 21 | `workbuddy-asar-inspect` | 1.0.0 | 我参与制定 | 解析 WorkBuddy app.asar 查模型调用行为 | 扒workbuddy / 解析 app.asar（只读，不改安装文件） |
| 22 | `workbuddy-disable-update-toast` | 1.0.0 | 我参与制定 | 禁用 WB 自动更新 toast(字节补丁) | workbuddy 更新提醒 / workbuddy 更新提示 / 关掉 workbuddy 更新 / 关闭 workbuddy 自动更新 / workbuddy 新版本就绪 |
| 23 | `workbuddy-window-width-patch` | — | 我参与制定 | 修改 WB 主窗口最小宽度(字节补丁) | （无显式触发词；按需求描述语义触发） |
| 24 | `zlib-book-downloader` | — | 我参与制定 | zlib 电子书下载 | （无显式触发词；按需求描述语义触发） |

## 其余用户级 skill（27 个）

| # | Skill ID | 版本 | 来源 | 用途说明 | 触发词 |
|---|---|---|---|---|---|
| 1 | `browser-use` | 2.0.7 | 其他 | Automates browser interactions for web testing, form filling, screenshots, and data extrac | （无显式触发词；按需求描述语义触发） |
| 2 | `cangjie-skill` | 1.0.3 | 其他 | Distill a book, long-video transcript, podcast, course, or interview into a coherent set o | 拆书 |
| 3 | `china-stock-data` | 2.0.0 | 其他 | 中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWencai问财搜索、J | （无显式触发词；按需求描述语义触发） |
| 4 | `fw01-wealth-freedom-definition` | — | 其他 | 当用户纠结"我是不是财富自由了"、"财富自由到底是什么意思"、"有钱了是不是就自由了"、"时间自主权 vs 资产多少"、"如何判断自己离财富自由还有多远"、"个人商业模式升级的目标 | （无显式触发词；按需求描述语义触发） |
| 5 | `fw01-wealth-freedom-definition` | — | 其他 | 当用户纠结"我是不是财富自由了"、"财富自由到底是什么意思"、"有钱了是不是就自由了"、"时间自主权 vs 资产多少"、"如何判断自己离财富自由还有多远"、"个人商业模式升级的目标 | （无显式触发词；按需求描述语义触发） |
| 6 | `fw05-abandon-safety` | — | 其他 | 当用户陷入"不敢辞职/不敢创业/不敢表白/不敢改变"、"追求完美计划/完美时机"、"想等准备好再开始"、"怕出错/怕丢脸/怕不稳定"、"在舒适区待了很久但不敢动"、"安全感 vs  | 当用户陷入"不敢辞职/不敢创业/不敢表白/不敢改变"、"追求完美计划/完美时 |
| 7 | `fw05-abandon-safety` | — | 其他 | 当用户陷入"不敢辞职/不敢创业/不敢表白/不敢改变"、"追求完美计划/完美时机"、"想等准备好再开始"、"怕出错/怕丢脸/怕不稳定"、"在舒适区待了很久但不敢动"、"安全感 vs  | 当用户陷入"不敢辞职/不敢创业/不敢表白/不敢改变"、"追求完美计划/完美时 |
| 8 | `fw13-investment-risk-aversion` | — | 其他 | 当用户讨论投资决策、仓位管理、杠杆使用、all-in 风险、"富贵险中求"、避险 vs 冒险、"不买也是冒险"、投资刚需、风控策略、市场下跌时的应对时使用。给出"投资的刚需是避险， | （无显式触发词；按需求描述语义触发） |
| 9 | `fw13-investment-risk-aversion` | — | 其他 | 当用户讨论投资决策、仓位管理、杠杆使用、all-in 风险、"富贵险中求"、避险 vs 冒险、"不买也是冒险"、投资刚需、风控策略、市场下跌时的应对时使用。给出"投资的刚需是避险， | （无显式触发词；按需求描述语义触发） |
| 10 | `html-ppt` | — | 其他 | HTML PPT Studio — author professional static HTML presentations in many styles, layouts, a | （无显式触发词；按需求描述语义触发） |
| 11 | `humanizer` | 2.1.1 | 其他 | Remove signs of AI-generated writing from text. Use when editing or reviewing text to make | （无显式触发词；按需求描述语义触发） |
| 12 | `impeccable` | 2.0.0 | 其他 | Create distinctive, production-grade frontend interfaces with high design quality. Use thi | （无显式触发词；按需求描述语义触发） |
| 13 | `notebooklm-studio` | 2.1.3 | 其他 | Import sources (URLs, YouTube, files, text) into Google NotebookLM and generate artifacts: | （无显式触发词；按需求描述语义触发） |
| 14 | `p05-safety-is-shackle` | — | 其他 | 当用户意识到自己"不敢改变/不敢行动/不敢尝试"、"在舒适区待了很久但很痛苦"、"追求完美计划/完美时机"、"害怕不确定性"、"安全感 vs 成长冲突"、"想等准备好再开始"时使用 | （无显式触发词；按需求描述语义触发） |
| 15 | `p05-safety-is-shackle` | — | 其他 | 当用户意识到自己"不敢改变/不敢行动/不敢尝试"、"在舒适区待了很久但很痛苦"、"追求完美计划/完美时机"、"害怕不确定性"、"安全感 vs 成长冲突"、"想等准备好再开始"时使用 | （无显式触发词；按需求描述语义触发） |
| 16 | `p27-prediction-impossible` | — | 其他 | 当用户纠结"如何预测市场/股票/趋势/未来"、"明天会涨吗"、"我该不该现在买"、"预测 vs 策略"、"如何应对不确定性"、"趋势判断 vs 预测"时使用。给出"预测不可能，策略 | （无显式触发词；按需求描述语义触发） |
| 17 | `p27-prediction-impossible` | — | 其他 | 当用户纠结"如何预测市场/股票/趋势/未来"、"明天会涨吗"、"我该不该现在买"、"预测 vs 策略"、"如何应对不确定性"、"趋势判断 vs 预测"时使用。给出"预测不可能，策略 | （无显式触发词；按需求描述语义触发） |
| 18 | `p45-execution-cognition` | — | 其他 | 当用户说"听了很多道理但过不好"、"知道却做不到"、"学习了很多但没用上"、"执行力差"、"为什么同样听课有人改变有人没改变"、"认知升级"、"知行合一"、"从知道到做到"、"践行 | 听了很多道理但过不好 |
| 19 | `p45-execution-cognition` | — | 其他 | 当用户说"听了很多道理但过不好"、"知道却做不到"、"学习了很多但没用上"、"执行力差"、"为什么同样听课有人改变有人没改变"、"认知升级"、"知行合一"、"从知道到做到"、"践行 | 听了很多道理但过不好 |
| 20 | `plan-tracker` | 1.0.0 | 其他 | 当用户需要目标拆解、每日打卡、连续签到、学习热力图、进度预警时使用。支持 SMART 澄清 + OKR 月周拆解 + ABC 三档每日任务（A 完美 / B 基础 / C ≤15m | 当用户需要目标拆解、每日打卡、连续签到、学习热力图、进度预警时 |
| 21 | `playwright-browser-automation` | 2.0.0 | 其他 | Direct Playwright API for browser automation without MCP complexity. Navigate websites, in | （无显式触发词；按需求描述语义触发） |
| 22 | `publish-to-4ends` | — | 其他 | 把本地一个文件（通常是交互式 HTML 看板/报告）按"分裂格式"一键发布到 4 端——博客(Jekyll `_handoffs/`, | 把某个文件直接发布到4端 |
| 23 | `skill-creator` | 0.2.0 | 其他 | Guide for creating effective skills. This skill should be used when users want to create a | （无显式触发词；按需求描述语义触发） |
| 24 | `study-planner` | — | 其他 | 当用户需要制定学习计划、备考计划、拆解复习目标时使用。输入目标+截止日+每日时长，输出每天可执行的学习计划，支持雅思/考研/期末复习等场景。 | 当用户需要制定学习计划、备考计划、拆解复习目标时 |
| 25 | `task-alignment` | — | 其他 | Alignment conversation starting from a user's rough idea. Co-decides with the user whether | （无显式触发词；按需求描述语义触发） |
| 26 | `task-implement` | — | 其他 | Autonomous task execution driven by documents under `.task/<MMDD_slug>/` (produced by /tas | （无显式触发词；按需求描述语义触发） |
| 27 | `web-access` | 2.5.3 | 其他 | 所有联网操作必须通过此 skill 处理，包括：搜索、网页抓取、登录后操作、网络交互等。 触发场景：用户要求搜索信息、查看网页内容、访问需要登录的网站、操作网页界面、抓取社交媒体内 | （无显式触发词；按需求描述语义触发） |

## 说明

- **「我参与制定」判定**：各 SKILL.md 的 frontmatter 含 `agent_created: true`。v1.3 已将此标记**永久化**写入全部 24 个（含 agent-plan-router、multi-agent-pdca、port-list、cf-58-scraper-replicate、forum-handoff-publisher、glm-41v-visual-transcribe、skillhub-daily、todolist、wechat-mp-crawler-cookie-fix 这 9 个，改前均备份为 `SKILL.md.bak-agent_created-20260814_223000`）。
- **触发词来源**：优先取 frontmatter 的 `triggers:` 列表；其次 description 中的「触发词：」子串；再次「当用户说「X」」引号内容；最后「当用户…时」整句。均未显式列出者，标注「按需求描述语义触发」（WorkBuddy 按 description 语义匹配，无硬触发词）。**全部取自文件真实内容，未编造**。
- `node_modules` 内的 Playwright 依赖不计入。