---
layout: default
title: 交接文档 · 用户级 Skill 清单 v1.2（~_.workbuddy_skills）
date: 2026-08-16 23:30:00 +0800
---

# 用户级 Skill 清单 v1.2（~_.workbuddy_skills）

- **日期**：2026-08-14
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260814_用户级 Skill 清单 v1.2（~_.workbuddy_skills）_handoff.md（编码探测：utf-8）

> 来源：2026-08-14-13-34-35\用户级skill清单_20260814_v1.2.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。


> 扫描时间：2026-08-14 ｜ 共 **51** 个用户级 skill（已剔除 node_modules 依赖）
> 其中 **★ 我参与制定 24 个** = 自动检测(agent_created=true) **15** 个 + 手动补进(用户确认) **9** 个
> 相对 v1.1：新增 `cf-58-scraper-replicate`、`forum-handoff-publisher`、`glm-41v-visual-transcribe`、`skillhub-daily`、`todolist`、`wechat-mp-crawler-cookie-fix` 6 个手动补进「我参与制定」(用户指出其余表 3/5/12/27/31/33 行)。

## ★ 我参与制定的 skill（24 个）

| # | Skill ID | 版本 | 来源 | 用途说明 |
|---|---|---|---|---|
| 1 | `agent-plan-router` | 1.0.0 | 手动补进 | A/B/C 计划路由(A=六顶思考帽+RACI+多Agent；B=情境路由；C=PDCA) |
| 2 | `agent-reach` | 1.0.0 | 自动 | 无需API的跨平台调研与素材采集 |
| 3 | `agnes-media-gen` | — | 自动 | Agnes AI 文生图 / 图生视频生成 |
| 4 | `cf-58-scraper-replicate` | — | 手动补进 | Cloudflare 全栈 58同城爬虫复刻(Worker+D1+KV+Pages 看板) |
| 5 | `favicon-picker` | — | 自动 | 为网页/看板生成 favicon 多候选方案 |
| 6 | `forum-handoff-publisher` | — | 手动补进 | 本地 handoff/markdown 批量发布到 bbs1org 论坛与免费主机 |
| 7 | `gentle-ratelimit-test` | 1.0.0 | 自动 | 温和验证模型/API 限流(429/503)，单次低频不轰炸 |
| 8 | `glm-41v-visual-transcribe` | — | 手动补进 | 视觉模型转述模式(先文字描述图片再作答，历史可继承) |
| 9 | `model-rate-limit-radar` | 2.0.0 | 自动 | 对活清单全模型按平台并发探测限流，本地看板(8849) |
| 10 | `multi-agent-pdca` | 1.0.0 | 手动补进 | 通用 PDCA 多 agent 协作骨架(调查员+规划+红队+执行) |
| 11 | `port-list` | — | 手动补进 | 本机开放端口清单看板(netstat 扫描+项目标注+本地 http 展示) |
| 12 | `skillhub-daily` | 6.2.0 | 手动补进 | 每日扫描 SkillHub 全站 Top100+7分类 Top20 推荐 |
| 13 | `todolist` | — | 手动补进 | 通用任务清单/待办系统 |
| 14 | `tri-agent-investigation` | — | 自动 | 陌生API/错误码三方调查法(调查员+规划+红队) |
| 15 | `txt2img-vector-overlay` | 1.0.0 | 自动 | 文生图 + 矢量叠加做海报/壁纸 |
| 16 | `visual-ui-align` | — | 自动 | UI/网站/主题视觉对齐 |
| 17 | `wechat-mp-crawler-cookie-fix` | 2.0.0 | 手动补进 | 微信公众平台爬虫静默0条故障排障(含2026-07-30接口关停) |
| 18 | `win-py-daemon-launcher` | 1.0.0 | 自动 | Windows 下 .bat 一键启 Python 服务避坑 |
| 19 | `windows-launcher-safety` | 2.0.0 | 自动 | 写 .bat/.cmd/.lnk 前的避坑自查清单 |
| 20 | `wispbyte-vps-gost-proxy` | — | 自动 | wispbyte VPS gost 代理 |
| 21 | `workbuddy-asar-inspect` | 1.0.0 | 自动 | 解析 WorkBuddy app.asar 查模型调用行为 |
| 22 | `workbuddy-disable-update-toast` | 1.0.0 | 自动 | 禁用 WB 自动更新 toast(字节补丁) |
| 23 | `workbuddy-window-width-patch` | — | 自动 | 修改 WB 主窗口最小宽度(字节补丁) |
| 24 | `zlib-book-downloader` | — | 自动 | zlib 电子书下载 |

## 其余用户级 skill（未标记为我参与制定，27 个）

| # | Skill ID | 版本 | 来源 | 用途说明 |
|---|---|---|---|---|
| 1 | `browser-use` | 2.0.7 | 其他 | 浏览器自动化（导航、点击、截图、数据提取、多会话、云浏览器） |
| 2 | `cangjie-skill` | 1.0.3 | 其他 | 将书籍、长视频、播客或课程蒸馏为一组可执行技能。适用于拆书、蒸馏、把XX做成skill等场景，通过RIA阅读法提取框架、原则、思维模型和方法论，生成原子化可复用… |
| 3 | `china-stock-data` | 2.0.0 | 其他 | 中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWe… |
| 4 | `fw01-wealth-freedom-definition` | — | 其他 | | |
| 5 | `fw01-wealth-freedom-definition` | — | 其他 | | |
| 6 | `fw05-abandon-safety` | — | 其他 | | |
| 7 | `fw05-abandon-safety` | — | 其他 | | |
| 8 | `fw13-investment-risk-aversion` | — | 其他 | | |
| 9 | `fw13-investment-risk-aversion` | — | 其他 | | |
| 10 | `html-ppt` | — | 其他 | HTML PPT Studio — author professional static HTML presentations in many styles, … |
| 11 | `humanizer` | 2.1.1 | 其他 | 去除文本中的 AI 写作痕迹 |
| 12 | `impeccable` | 2.0.0 | 其他 | 高品质 UI/UX 设计工具集：帮助生成独特、生产级的前端界面，涵盖视觉风格、布局排版、动效交互、质量保障、设计系统等全方位设计能力，避免泛 AI 审美 |
| 13 | `notebooklm-studio` | 2.1.3 | 其他 | NotebookLM 学习工作室：导入多种来源，生成播客、测验、抽认卡、思维导图等学习产物 |
| 14 | `p05-safety-is-shackle` | — | 其他 | | |
| 15 | `p05-safety-is-shackle` | — | 其他 | | |
| 16 | `p27-prediction-impossible` | — | 其他 | | |
| 17 | `p27-prediction-impossible` | — | 其他 | | |
| 18 | `p45-execution-cognition` | — | 其他 | | |
| 19 | `p45-execution-cognition` | — | 其他 | | |
| 20 | `plan-tracker` | 1.0.0 | 其他 | 目标拆解与打卡助手——SMART/OKR/ABC 三档拆解 + 打卡积累成就 + 智能预警纠偏 |
| 21 | `playwright-browser-automation` | 2.0.0 | 其他 | 直接调用 Playwright API 实现浏览器自动化（无需 MCP） |
| 22 | `publish-to-4ends` | — | 其他 | 把本地一个文件（通常是交互式 HTML 看板/报告）按"分裂格式"一键发布到 4 端——博客(Jekyll `_handoffs/`, |
| 23 | `skill-creator` | 0.2.0 | 其他 | 创建和维护自定义技能的指南 |
| 24 | `study-planner` | — | 其他 | 学习规划师——输入目标+截止日+每日时长，输出每天可执行的学习计划 |
| 25 | `task-alignment` | — | 其他 | 把模糊想法对齐成可独立交付的任务契约 |
| 26 | `task-implement` | — | 其他 | 作为用户代理自主执行任务并独立验收交付 |
| 27 | `web-access` | 2.5.3 | 其他 | CDP 直连本地 Chrome，智能调度联网工具，支持登录态、并行批量操作 |

## 说明

- **“我参与制定”判定**：自动检测 15 个（frontmatter 含 `agent_created: true`）；手动补进 9 个（你确认参与制定，v1.1 补 3 个、v1.2 再补 6 个）。
- **其余 27 个来源**统一标「其他」(预装/市场/第三方作者)；用途说明均取自各自 SKILL.md 的 description 字段。
- `node_modules` 内的 Playwright 依赖不计入。
