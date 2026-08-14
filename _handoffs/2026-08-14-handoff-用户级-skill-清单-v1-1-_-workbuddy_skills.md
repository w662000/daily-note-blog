---
layout: default
title: 交接文档 · 用户级 Skill 清单 v1.1（~_.workbuddy_skills）
date: 2026-08-14 23:30:00 +0800
---

> 来源：2026-08-14-13-34-35\用户级skill清单_20260814_v1.1.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# 用户级 Skill 清单 v1.1（~/.workbuddy/skills）

> 扫描时间：2026-08-14 ｜ 共 **51** 个用户级 skill（已剔除 node_modules 依赖）
> 其中 **★ 我参与制定 18 个** = 自动检测(agent_created=true) **15** 个 + 手动补进(用户确认) **3** 个
> 两张表列结构一致：Skill ID / 版本 / 来源 / 用途说明；其余 33 个的用途说明均取自各自 SKILL.md frontmatter。

## ★ 我参与制定的 skill（18 个）

| # | Skill ID | 版本 | 来源 | 用途说明 |
|---|---|---|---|---|
| 1 | `agent-plan-router` | 1.0.0 | 手动补进 | A/B/C 计划路由(A=六顶思考帽+RACI+多Agent；B=情境路由；C=PDCA) |
| 2 | `agent-reach` | 1.0.0 | 自动 | 无需API的跨平台调研与素材采集 |
| 3 | `agnes-media-gen` | — | 自动 | Agnes AI 文生图 / 图生视频生成 |
| 4 | `favicon-picker` | — | 自动 | 为网页/看板生成 favicon 多候选方案 |
| 5 | `gentle-ratelimit-test` | 1.0.0 | 自动 | 温和验证模型/API 限流(429/503)，单次低频不轰炸 |
| 6 | `model-rate-limit-radar` | 2.0.0 | 自动 | 对活清单全模型按平台并发探测限流，本地看板(8849) |
| 7 | `multi-agent-pdca` | 1.0.0 | 手动补进 | 通用 PDCA 多 agent 协作骨架(调查员+规划+红队+执行) |
| 8 | `port-list` | — | 手动补进 | 本机开放端口清单看板(netstat 扫描+项目标注+本地 http 展示) |
| 9 | `tri-agent-investigation` | — | 自动 | 陌生API/错误码三方调查法(调查员+规划+红队) |
| 10 | `txt2img-vector-overlay` | 1.0.0 | 自动 | 文生图 + 矢量叠加做海报/壁纸 |
| 11 | `visual-ui-align` | — | 自动 | UI/网站/主题视觉对齐 |
| 12 | `win-py-daemon-launcher` | 1.0.0 | 自动 | Windows 下 .bat 一键启 Python 服务避坑 |
| 13 | `windows-launcher-safety` | 2.0.0 | 自动 | 写 .bat/.cmd/.lnk 前的避坑自查清单 |
| 14 | `wispbyte-vps-gost-proxy` | — | 自动 | wispbyte VPS gost 代理 |
| 15 | `workbuddy-asar-inspect` | 1.0.0 | 自动 | 解析 WorkBuddy app.asar 查模型调用行为 |
| 16 | `workbuddy-disable-update-toast` | 1.0.0 | 自动 | 禁用 WB 自动更新 toast(字节补丁) |
| 17 | `workbuddy-window-width-patch` | — | 自动 | 修改 WB 主窗口最小宽度(字节补丁) |
| 18 | `zlib-book-downloader` | — | 自动 | zlib 电子书下载 |

## 其余用户级 skill（未标记为我参与制定，33 个）

| # | Skill ID | 版本 | 来源 | 用途说明 |
|---|---|---|---|---|
| 1 | `browser-use` | 2.0.7 | 其他 | 浏览器自动化（导航、点击、截图、数据提取、多会话、云浏览器） |
| 2 | `cangjie-skill` | 1.0.3 | 其他 | 将书籍、长视频、播客或课程蒸馏为一组可执行技能。适用于拆书、蒸馏、把XX做成skill等场景，通过RIA阅读法提取框架、原则、思维模型和方法论，生成原子化可复用… |
| 3 | `cf-58-scraper-replicate` | — | 其他 | 把一套已验证的 Cloudflare 全栈 58同城爬虫（Worker + D1 + KV + Pages 看板，本地爬虫→落盘→wrangler 直连 D1）… |
| 4 | `china-stock-data` | 2.0.0 | 其他 | 中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWe… |
| 5 | `forum-handoff-publisher` | — | 其他 | 把本地 handoff / markdown 文档批量发布到 my-place.us 免费主机上的 bbs1org 极简论坛与 |
| 6 | `fw01-wealth-freedom-definition` | — | 其他 | | |
| 7 | `fw01-wealth-freedom-definition` | — | 其他 | | |
| 8 | `fw05-abandon-safety` | — | 其他 | | |
| 9 | `fw05-abandon-safety` | — | 其他 | | |
| 10 | `fw13-investment-risk-aversion` | — | 其他 | | |
| 11 | `fw13-investment-risk-aversion` | — | 其他 | | |
| 12 | `glm-41v-visual-transcribe` | — | 其他 | 切到视觉模型后说"转述"即激活：让模型先文字描述图片再作答，文字留历史、切其他模型可继承。4.1V 有 overthink |
| 13 | `html-ppt` | — | 其他 | HTML PPT Studio — author professional static HTML presentations in many styles, … |
| 14 | `humanizer` | 2.1.1 | 其他 | 去除文本中的 AI 写作痕迹 |
| 15 | `impeccable` | 2.0.0 | 其他 | 高品质 UI/UX 设计工具集：帮助生成独特、生产级的前端界面，涵盖视觉风格、布局排版、动效交互、质量保障、设计系统等全方位设计能力，避免泛 AI 审美 |
| 16 | `notebooklm-studio` | 2.1.3 | 其他 | NotebookLM 学习工作室：导入多种来源，生成播客、测验、抽认卡、思维导图等学习产物 |
| 17 | `p05-safety-is-shackle` | — | 其他 | | |
| 18 | `p05-safety-is-shackle` | — | 其他 | | |
| 19 | `p27-prediction-impossible` | — | 其他 | | |
| 20 | `p27-prediction-impossible` | — | 其他 | | |
| 21 | `p45-execution-cognition` | — | 其他 | | |
| 22 | `p45-execution-cognition` | — | 其他 | | |
| 23 | `plan-tracker` | 1.0.0 | 其他 | 目标拆解与打卡助手——SMART/OKR/ABC 三档拆解 + 打卡积累成就 + 智能预警纠偏 |
| 24 | `playwright-browser-automation` | 2.0.0 | 其他 | 直接调用 Playwright API 实现浏览器自动化（无需 MCP） |
| 25 | `publish-to-4ends` | — | 其他 | 把本地一个文件（通常是交互式 HTML 看板/报告）按"分裂格式"一键发布到 4 端——博客(Jekyll `_handoffs/`, |
| 26 | `skill-creator` | 0.2.0 | 其他 | 创建和维护自定义技能的指南 |
| 27 | `skillhub-daily` | 6.2.0 | 其他 | 基于 SkillHub (skillhub.cn) 全站数据，每日扫描 Top100 热门 Skill 与 7 大分类各 Top20（共 240 个），结合用户… |
| 28 | `study-planner` | — | 其他 | 学习规划师——输入目标+截止日+每日时长，输出每天可执行的学习计划 |
| 29 | `task-alignment` | — | 其他 | 把模糊想法对齐成可独立交付的任务契约 |
| 30 | `task-implement` | — | 其他 | 作为用户代理自主执行任务并独立验收交付 |
| 31 | `todolist` | — | 其他 | 通用任务清单 / 待办系统。当用户说「打开 todolist / 显示待办 / |
| 32 | `web-access` | 2.5.3 | 其他 | CDP 直连本地 Chrome，智能调度联网工具，支持登录态、并行批量操作 |
| 33 | `wechat-mp-crawler-cookie-fix` | 2.0.0 | 其他 | 微信公众平台爬虫静默 0 条故障排障（含 2026-07-30 接口关停） |

## 说明

- **“我参与制定”判定**：自动检测 15 个（frontmatter 含 `agent_created: true`）；手动补进 3 个（`agent-plan-router`、`multi-agent-pdca`、`port-list`，你确认参与制定，v1.1 标注）。
- **其余 33 个来源**统一标「其他」(预装/市场/第三方作者)，其精确出处未逐一核验；用途说明全部取自各自 SKILL.md 的 description 字段。
- `node_modules` 内的 Playwright 依赖不计入。