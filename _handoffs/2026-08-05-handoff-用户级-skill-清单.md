---
layout: default
title: 用户级 Skill 清单 · 交接文档
date: 2026-08-10 23:30:00 +0800
---

> 来源：2026-08-05-10-41-07\用户级skill清单.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# 用户级 Skill 清单

> 扫描目录：`C:\Users\Administrator\.workbuddy\skills`
> 共发现 **39** 个 SKILL.md（用户级；含子命名空间与嵌套子技能）
> 说明字段优先取 `description`，缺失时取 `summary`；状态列标注 `disable:true`(已禁用) 与 `agent_created`(AI 自建)
> 生成时间：2026-08-05 18:44

| # | 目录 | 名称 | 说明 | 状态 |
|---|------|------|------|------|
| 1 | `@kekewater\china-stock-data` | china-stock-data | 中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWencai问财搜索、JQData聚宽量化、Tushare Pro公告、RiceQuant米筐。8大来源自动降级。 | 启用 |
| 2 | `agent-plan-router` | agent-plan-router | agent 指导模式路由：当用户说「用A计划执行/用A执行」「用B计划执行/用B执行」「用C计划执行/用C执行」「用PDCA执行/PDCA计划执行」时，按对应的 A 多角色并行 / B 情境路由 / C 闭环验证(PDCA) 方案来编排 agent 工作。A=六顶思考帽+RACI+多 Agent；B=Cynefin 判域+看板WIP+MoSCoW；C=PDCA+SMART+5W1H+风险矩阵+5Whys+A3（其 PDCA 脊由现有 multi-agent-pdca 技能提供）。用于把《项目管理思维工具全景回顾》的思维工具落成可点名的 agent 工作法。 | 启用 |
| 3 | `agent-reach` | agent-reach | Cross-platform research and material gathering without any API
keys. Use when the user wants to research a topic, collect information from
multiple sources/platforms (web, academic, news, developer communities,
forums, video, social), or asks to 'search across platforms' / 'gather sources
on X' / '跨平台搜一下' / '帮我找关于 X 的资料，要覆盖多个来源'. Relies solely on built-in WebSearch
and WebFetch — no API setup, no keys required. Produces a structured, cited
synthesis with a source-diversity check. | 已禁用 / AI自建 |
| 4 | `agnes-media-gen` | agnes-media-gen | Generate images and videos with Agnes AI's two generation models (agnes-image-2.1-flash for images, agnes-video-v2.0 for video). Use this skill when the user says 用agnes生视频, 用agnes生图, 准备生视频, 准备生图, or asks to generate an image or video via Agnes models. It encodes the verified endpoint, the async polling loop, and the correct result-fetch endpoint (GET /agnesapi?video_id= with Bearer API key) so the agent does not wrongly conclude a console cookie is needed. Also covers the key footguns: response_format must be inside extra_body for images, and num_frames must be 8n+1 and 441 or less for video. | AI自建 |
| 5 | `cangjie-skill` | cangjie-skill | Distill a book, long-video transcript, podcast, course, or interview into a coherent set of executable skills. Use when the user asks to "拆书" / "蒸馏一本书" / "把 XX 书做成 skill" / "把这个视频/播客/课程蒸馏成 skill" / "turn a book or video into skills" — i.e. wants the frameworks, principles, and methodologies in long-form content extracted into atomic, reusable Claude skills that an agent can invoke in real-world situations. NOT for simple summarization, book reviews, or role-playing as the author (that is nuwa-skill's job). | 启用 |
| 6 | `cangjie-skill\books\caifuziyouzhilu\fw01-wealth-freedom-definition` | fw01-wealth-freedom-definition | |
当用户纠结"我是不是财富自由了"、"财富自由到底是什么意思"、"有钱了是不是就自由了"、"时间自主权 vs 资产多少"、"如何判断自己离财富自由还有多远"、"个人商业模式升级的目标"时使用。给出作者对财富自由的精确定义，帮助用户澄清概念、判断当前状态、规划升级路径。不适用于具体投资标的推荐或短期理财建议。 | 已禁用 |
| 7 | `cangjie-skill\books\caifuziyouzhilu\fw05-abandon-safety` | fw05-abandon-safety | |
当用户陷入"不敢辞职/不敢创业/不敢表白/不敢改变"、"追求完美计划/完美时机"、"想等准备好再开始"、"怕出错/怕丢脸/怕不稳定"、"在舒适区待了很久但不敢动"、"安全感 vs 成长"冲突时使用。给出"放弃部分安全感是成长的前提"这一框架，帮助用户识别安全感陷阱、计算安全感溢价、做出行动决策。不适用于需要风险评估的金融投资决策（见 fw13-investment-risk-aversion）。 | 已禁用 |
| 8 | `cangjie-skill\books\caifuziyouzhilu\fw13-investment-risk-aversion` | fw13-investment-risk-aversion | |
当用户讨论投资决策、仓位管理、杠杆使用、all-in 风险、"富贵险中求"、避险 vs 冒险、"不买也是冒险"、投资刚需、风控策略、市场下跌时的应对时使用。给出"投资的刚需是避险，而不是冒险"框架，帮助用户建立风险优先的投资决策逻辑。不适用于心理层面的"安全感陷阱"（见 fw05-abandon-safety）或财富自由的定义澄清（见 fw01-wealth-freedom-definition）。 | 已禁用 |
| 9 | `cangjie-skill\books\caifuziyouzhilu\p05-safety-is-shackle` | p05-safety-is-shackle | |
当用户意识到自己"不敢改变/不敢行动/不敢尝试"、"在舒适区待了很久但很痛苦"、"追求完美计划/完美时机"、"害怕不确定性"、"安全感 vs 成长冲突"、"想等准备好再开始"时使用。给出"安全感是人生最重的枷锁"这一原则，帮助用户识别安全感陷阱、理解其代价、找到突破路径。不适用于金融投资风险评估（见 fw13-investment-risk-aversion）。 | 已禁用 |
| 10 | `cangjie-skill\books\caifuziyouzhilu\p27-prediction-impossible` | p27-prediction-impossible | |
当用户纠结"如何预测市场/股票/趋势/未来"、"明天会涨吗"、"我该不该现在买"、"预测 vs 策略"、"如何应对不确定性"、"趋势判断 vs 预测"时使用。给出"预测不可能，策略才可靠"这一原则，帮助用户从预测思维转向策略思维，建立可执行的决策系统。不适用于需要具体预测的场景（如天气预报），也不适用于投资中的"听消息做决策"（见 ce07-listen-to-news）。 | 已禁用 |
| 11 | `cangjie-skill\books\caifuziyouzhilu\p45-execution-cognition` | p45-execution-cognition | |
当用户说"听了很多道理但过不好"、"知道却做不到"、"学习了很多但没用上"、"执行力差"、"为什么同样听课有人改变有人没改变"、"认知升级"、"知行合一"、"从知道到做到"、"践行"时使用。给出"践行是认知升级的唯一工具"这一原则，帮助用户建立"行动优先"的学习和成长策略。不适用于技能教学本身（如"如何编程"），而是解决"为什么学了很多却没用"的问题。 | 已禁用 |
| 12 | `cf-58-scraper-replicate` | cf-58-scraper-replicate | 把一套已验证的 Cloudflare 全栈 58同城爬虫（Worker + D1 + KV + Pages 看板，本地爬虫→落盘→wrangler 直连 D1）复刻到新城市 / 新房租通道。当用户说"参考上次的 58 爬虫再做一个 XX 城市/买房/租房项目""复刻 yunnan-housing 工作流到 XX"时使用。核心是用 token 替换生成器批量产出项目，并严格核对「城市名所有形态」避免泄漏。 | 启用 |
| 13 | `forum-handoff-publisher` | forum-handoff-publisher | 把本地 handoff / markdown 文档批量发布到 my-place.us 免费主机上的 bbs1org 极简论坛与
phpBB 论坛（经 MCP）。当用户说"把 handoff 发到论坛""发布到 bbs1org 知识库""把文档发到 AI项目组版块""批量发帖到
my-place.us 两个论坛"时使用。核心是 JSON-RPC over HTTP 穿透 iFastNet，处理 WAF cookie、MCP
嵌套响应解析、phpBB 限流与 iFastNet 偶发 SSL 错误重试、发前去重。 | 已禁用 |
| 14 | `fw01-wealth-freedom-definition` | fw01-wealth-freedom-definition | |
当用户纠结"我是不是财富自由了"、"财富自由到底是什么意思"、"有钱了是不是就自由了"、"时间自主权 vs 资产多少"、"如何判断自己离财富自由还有多远"、"个人商业模式升级的目标"时使用。给出作者对财富自由的精确定义，帮助用户澄清概念、判断当前状态、规划升级路径。不适用于具体投资标的推荐或短期理财建议。 | 启用 |
| 15 | `fw05-abandon-safety` | fw05-abandon-safety | |
当用户陷入"不敢辞职/不敢创业/不敢表白/不敢改变"、"追求完美计划/完美时机"、"想等准备好再开始"、"怕出错/怕丢脸/怕不稳定"、"在舒适区待了很久但不敢动"、"安全感 vs 成长"冲突时使用。给出"放弃部分安全感是成长的前提"这一框架，帮助用户识别安全感陷阱、计算安全感溢价、做出行动决策。不适用于需要风险评估的金融投资决策（见 fw13-investment-risk-aversion）。 | 启用 |
| 16 | `fw13-investment-risk-aversion` | fw13-investment-risk-aversion | |
当用户讨论投资决策、仓位管理、杠杆使用、all-in 风险、"富贵险中求"、避险 vs 冒险、"不买也是冒险"、投资刚需、风控策略、市场下跌时的应对时使用。给出"投资的刚需是避险，而不是冒险"框架，帮助用户建立风险优先的投资决策逻辑。不适用于心理层面的"安全感陷阱"（见 fw05-abandon-safety）或财富自由的定义澄清（见 fw01-wealth-freedom-definition）。 | 启用 |
| 17 | `gentle-ratelimit-test` | gentle-ratelimit-test | 温和地验证某模型/API 的限流行为（是否出现 429/503）。当用户说「测限流」「测试限流」「测一下 X 模型限流」「看看会不会 429」「XXX 会不会被限流」「连续对话会限流吗」时调用。特点：单次、低频、轮间停顿 5 秒、不循环轰炸、绝不触发平台自身限流（避免假性 503/429 污染结论）。从 WorkBuddy models.json 自动读取模型的 endpoint 与 apiKey（不硬编码、不在对话里复述）。纯标准库 urllib，零依赖。 | AI自建 |
| 18 | `glm-41v-visual-transcribe` | glm-41v-visual-transcribe | 切到视觉模型后说"转述"即激活：让模型先文字描述图片再作答，文字留历史、切其他模型可继承。4.1V 有 overthink
bug、65K 上下文上限，遇问题切 GLM-4.6V-Flash(免费视觉)。 | 已禁用 |
| 19 | `humanizer` | humanizer | Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Detects and fixes patterns including: inflated symbolism, promotional language, superficial analyses, vague attributions, em dash overuse, rule of three, AI vocabulary words, negative parallelisms, and excessive conjunctive phrases. | 启用 |
| 20 | `impeccable` | impeccable | |
Create distinctive, production-grade frontend interfaces with high design quality.
Use this skill when the user asks to build web components, pages, artifacts, posters, or applications
(examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when
styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic
AI aesthetics.

Trigger scenarios — use when the user mentions any of:
- UI design, frontend design, web design, interface design, 界面设计, 前端设计
- responsive layout, mobile adaptation, breakpoints, 响应式, 自适应, 适配
- animation, motion, micro-interaction, transitions, 动画, 动效, 微交互
- UX copy, microcopy, error messages, labels, UX 文案, 文案优化
- performance optimization, bundle size, rendering, 性能优化, 渲染, 加载速度
- accessibility audit, a11y, WCAG, 无障碍, 可访问性
- design review, design critique, UX evaluation, 设计评审, 设计审查
- typography, fonts, type hierarchy, 字体, 排版, 字号
- color palette, color scheme, theming, 配色, 色彩, 主题
- layout, spacing, visual rhythm, grid, 布局, 间距, 视觉节奏
- simplify UI, declutter, reduce noise, 精简, 简化, 去噪
- design system, components, tokens, 设计系统, 组件库, token
- edge cases, error handling, i18n, overflow, 边缘情况, 容错, 国际化
- onboarding, empty state, first-run experience, 引导, 空状态, 新手体验
- visual impact, make it bold, more personality, 视觉冲击, 更大胆, 更有个性
- tone down, calmer, less aggressive, 降噪, 更柔和, 更克制
- polish, finishing touches, pre-launch QA, 打磨, 最终检查
- extraordinary effects, shaders, scroll-driven, 炫酷效果, 非凡视觉
- normalize, consistency, design drift, 规范化, 一致性
- extract components, refactor patterns, 提取组件, 复用模式 | 启用 |
| 21 | `model-rate-limit-radar` | model-rate-limit-radar | 对 WorkBuddy 活清单(models.json)里的全部模型，按「平台(vendor)」分组后并发探测：每个平台起一个 worker、平台内串行每模型做 15 轮温和限流测试（轮间停顿 5 秒），统计 429 与失败，产出健康度排行榜，并内置本地 HTTP 看板（默认端口 8849）。毫无限流(429=0)且零其它错误的模型排第一，随后按 429 升序、其它错误升序、平均耗时升序「以此类推」。每天只自动跑一轮。当用户说「模型测限流雷达」「测限流雷达」「限流看板」「哪些模型会被限流」「开限流雷达」时使用。 | AI自建 |
| 22 | `model-speed-radar` | model-speed-radar | 查看或启动本地「模型测速雷达」——一个常驻守护进程，每小时对 models.json 里全部模型做一次温和的流式拨测，测 TTFT 首包延迟，产出排行榜并在 http://127.0.0.1:8848 提供实时看板页面（含上次测速时间、历史快照、排名变化）。当用户问「现在哪个模型最快」「模型速度排行」「测速」「测速雷达」「模型看板」「该切哪个模型」「哪些模型没额度了」，或想启动/停止/立即触发一轮测速时使用本技能。 | AI自建 |
| 23 | `multi-agent-pdca` | multi-agent-pdca | 通用思维骨架：用户发出成规模/多步骤/涉及陌生领域的任务时，按 PDCA 原则派 3~5 个 agent 分工——至少 1 个调查员摸清领域机制与坑位（如微信风控），1 个规划员出方案，1 个红队挑刺员专找 plan 漏洞，再派执行员分工落地。先查清底细、先暴露方案缺陷，再正式执行，杜绝一头扎下去猛干。 | 启用 |
| 24 | `notebooklm-studio` | notebooklm-studio | Import sources (URLs, YouTube, files, text) into Google NotebookLM and generate artifacts: podcasts, videos, reports, quizzes, flashcards, mind maps, slide decks, infographics, data tables. Use when users want to study from web content, create learning materials from URLs or documents, generate quizzes from articles, or produce study aids. | 启用 |
| 25 | `p05-safety-is-shackle` | p05-safety-is-shackle | |
当用户意识到自己"不敢改变/不敢行动/不敢尝试"、"在舒适区待了很久但很痛苦"、"追求完美计划/完美时机"、"害怕不确定性"、"安全感 vs 成长冲突"、"想等准备好再开始"时使用。给出"安全感是人生最重的枷锁"这一原则，帮助用户识别安全感陷阱、理解其代价、找到突破路径。不适用于金融投资风险评估（见 fw13-investment-risk-aversion）。 | 启用 |
| 26 | `p27-prediction-impossible` | p27-prediction-impossible | |
当用户纠结"如何预测市场/股票/趋势/未来"、"明天会涨吗"、"我该不该现在买"、"预测 vs 策略"、"如何应对不确定性"、"趋势判断 vs 预测"时使用。给出"预测不可能，策略才可靠"这一原则，帮助用户从预测思维转向策略思维，建立可执行的决策系统。不适用于需要具体预测的场景（如天气预报），也不适用于投资中的"听消息做决策"（见 ce07-listen-to-news）。 | 启用 |
| 27 | `p45-execution-cognition` | p45-execution-cognition | |
当用户说"听了很多道理但过不好"、"知道却做不到"、"学习了很多但没用上"、"执行力差"、"为什么同样听课有人改变有人没改变"、"认知升级"、"知行合一"、"从知道到做到"、"践行"时使用。给出"践行是认知升级的唯一工具"这一原则，帮助用户建立"行动优先"的学习和成长策略。不适用于技能教学本身（如"如何编程"），而是解决"为什么学了很多却没用"的问题。 | 启用 |
| 28 | `playwright-browser-automation` | playwright-browser-automation | Direct Playwright API for browser automation without MCP complexity. Navigate websites, interact with elements, extract data, take screenshots, generate PDFs, record videos. More reliable than MCP-based approaches. Requires: node, npx, playwright. | 启用 |
| 29 | `port-list` | port-list | 本机开放端口清单看板。当用户说「打开端口清单 / 扫描端口 / 端口列表 / 看看哪些端口开着 / 开放端口 / netstat 查端口 / 命令行查端口」时，自动扫描本机所有 LISTENING 端口（或给出 netstat 命令行快速查询），标注每个端口运行的项目（如 8848=模型测速雷达、8084=todolist、8787/8642=Hermes、18999=codingplan-proxy），拉起本地 http server 展示。触发词：端口清单、扫描端口、端口列表、哪些端口开着、开放端口、本机端口、netstat 查端口、命令行查端口。 | 启用 |
| 30 | `publish-to-4ends` | publish-to-4ends | 把本地一个文件（通常是交互式 HTML 看板/报告）按"分裂格式"一键发布到 4 端——博客(Jekyll `_handoffs/`,
完整交互 HTML, layout:none) + Gridea(内嵌 HTML, published:true)
走富格式；语雀(w662000/ylv5l7) + 论坛(bbs1org forum3 + phpBB forum11) 走纯文本
MD。当用户说"把某个文件直接发布到4端""发布到4端""4端发布""把看板发到博客/语雀/论坛"时触发。注意：与 handoff_flow.py
的单源广播不同，本 skill 是分裂格式（HTML→博客/Gridea，MD→语雀/论坛），且标题统一由用户指定。 | 已禁用 |
| 31 | `skill-creator` | skill-creator | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends CodeBuddy's capabilities with specialized knowledge, workflows, or tool integrations. | 启用 |
| 32 | `todolist` | todolist | 通用任务清单 / 待办系统。当用户说「打开 todolist / 显示待办 /
我的清单」时自动打开固定位置的清单页面；支持从活动页面、文本、URL
导入任务，手动增删任务，勾选状态持久化（关闭后仍保存，下次打开正常）。触发词：todolist、待办、任务清单、把 XX 加入清单、导入清单、打开我的清单。 | 已禁用 |
| 33 | `txt2img-vector-overlay` | txt2img-vector-overlay | Workflow for producing crisp, controllable poster / wallpaper /
background art by combining an AI text-to-image generated atmospheric
background with a precise vector overlay drawn in code (PIL). Use when the
user wants AI-generated artwork that must carry legible text, an exact element
count, accurate shapes (constellations, icons, maps), or wallpaper-grade
sharpness — all of which pure text-to-image models garble or fail to count.
This skill owns the proven 'background = diffusion, structure = vectors' split
architecture. | 已禁用 / AI自建 |
| 34 | `visual-ui-align` | visual-ui-align | Use this skill when a user asks to make a UI, website, theme, or
component "match", "unify with", "copy the style of", "align to", "be
consistent with", or "add the same dark/light theme as" another site or design
(e.g. "add a dark/light toggle like w662000.github.io", "make the blog
consistent with my homepage", "use X's color scheme / theme"). It prevents the
recurring failure where the theme framework (CSS variables, toggle button, JS)
is copied correctly but individual visible elements end up with mismatched
colors — because the agent re-decides element styling in its own
newly-authored layer instead of copying the target's ACTUAL rendered colors
element-by-element. | 已禁用 / AI自建 |
| 35 | `wechat-mp-crawler-cookie-fix` | wechat-mp-crawler-cookie-fix | Diagnose silent 0-result failures in WeChat Official Account
(mp.weixin.qq.com) crawlers using cgi-bin appmsg/searchbiz. CRITICAL
2026-07-30 UPDATE: WeChat permanently shut down third-party article-list
reading; a persistent ret=200013 that outlasts normal cooldown means the API
is DEAD, not rate-limited - check this FIRST before blaming cookies or
frequency. Also covers: half-baked cookie trap (missing data_ticket), Windows
wrangler/npx FileNotFoundError, freq control (ret=200013) from high-frequency
testing, and the false-success chain where exit code 0 masks a total failure. | 已禁用 |
| 36 | `win-py-daemon-launcher` | win-py-daemon-launcher | Windows 下用 .bat 一键启动 Python HTTP 服务/看板/网页时，常出现「双击后页面打不开、连接被拒绝、cmd
一闪而过」。本 skill 提供经实战验证的稳健启动模板：pythonw 无窗口常驻 + 端口预检防重复 + 就绪轮询防竞态 + explorer 拉浏览器
+ 日志。当用户要做「双击 bat 启动 Python 服务但页面打不开」的启动器、或排查 Windows 下 Python 守护进程自启脚本时使用。 | 已禁用 / AI自建 |
| 37 | `wispbyte-vps-gost-proxy` | wispbyte-vps-gost-proxy | 在 Wispbyte/Pterodactyl 免费 VPS 上部署 gost SOCKS5 代理，并配置 Clash 客户端加速 GitHub 等开发资源 | 已禁用 / AI自建 |
| 38 | `workbuddy-asar-inspect` | workbuddy-asar-inspect | 解析 WorkBuddy 安装包 app.asar（注意其比标准 asar 多一层头部），查模型调用行为（流式 stream 是否默认开、某参数/配置是否生效、某功能如何实现）。触发词：扒workbuddy / workbuddy-asar-inspect。ReadOnly 分析，绝不修改安装文件。 | AI自建 |
| 39 | `zlib-book-downloader` | zlib-book-downloader | 根据书名自动从 z-library (zlib) 下载 EPUB/TXT 到 D:/HDDownload（不下载 PDF，便于直接抽文本给
cangjie 蒸馏）。支持用用户提供的或联网搜到的 T0/T1 级镜像，使用用户 cookie 登录下载。 | 已禁用 / AI自建 |