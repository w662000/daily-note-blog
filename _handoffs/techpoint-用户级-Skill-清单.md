---
layout: default
title: 技术点 · 用户级 Skill 清单
date: 2026-08-05 23:30:00 +0800
---

# 技术点 · 用户级 Skill 清单

> 来源：260805_用户级 Skill 清单_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260805_用户级 Skill 清单_handoff.md（编码探测：utf-8）
- | 1 | `@kekewater\china-stock-data` | china-stock-data | 中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWencai问财搜索、JQData聚宽量化、Tushare Pro公告、RiceQuant米筐。8大来源自动降级。 | 启用 |
- | 2 | `agent-plan-router` | agent-plan-router | agent 指导模式路由：当用户说「用A计划执行/用A执行」「用B计划执行/用B执行」「用C计划执行/用C执行」「用PDCA执行/PDCA计划执行」时，按对应的 A 多角色并行 / B 情境路由 / C 闭环验证(PDCA) 方案来编排 agent 工作。A=六顶思考帽+RACI+多 Agent；B=Cynefin 判域+看板WIP+MoSCoW；C=PDCA+SMART+5W1H+风险矩阵+5Whys+A3（其 PDCA 脊由现有 multi-agent-pdca 技能提供）。用于把《项目管理思维工具全景回顾》的思维工具落成可点名的 agent 工作法。 | 启用 |
- | 3 | `agent-reach` | agent-reach | Cross-platform research and material gathering without any API
- keys. Use when the user wants to research a topic, collect information from
- and WebFetch — no API setup, no keys required. Produces a structured, cited
- | 4 | `agnes-media-gen` | agnes-media-gen | Generate images and videos with Agnes AI's two generation models (agnes-image-2.1-flash for images, agnes-video-v2.0 for video). Use this skill when the user says 用agnes生视频, 用agnes生图, 准备生视频, 准备生图, or asks to generate an image or video via Agnes models. It encodes the verified endpoint, the async polling loop, and the correct result-fetch endpoint (GET /agnesapi?video_id= with Bearer API key) so the agent does not wrongly conclude a console cookie is needed. Also covers the key footguns: response_format must be inside extra_body for images, and num_frames must be 8n+1 and 441 or less for video. | AI自建 |
- 当用户纠结"我是不是财富自由了"、"财富自由到底是什么意思"、"有钱了是不是就自由了"、"时间自主权 vs 资产多少"、"如何判断自己离财富自由还有多远"、"个人商业模式升级的目标"时使用。给出作者对财富自由的精确定义，帮助用户澄清概念、判断当前状态、规划升级路径。不适用于具体投资标的推荐或短期理财建议。 | 已禁用 |
- 当用户意识到自己"不敢改变/不敢行动/不敢尝试"、"在舒适区待了很久但很痛苦"、"追求完美计划/完美时机"、"害怕不确定性"、"安全感 vs 成长冲突"、"想等准备好再开始"时使用。给出"安全感是人生最重的枷锁"这一原则，帮助用户识别安全感陷阱、理解其代价、找到突破路径。不适用于金融投资风险评估（见 fw13-investment-risk-aversion）。 | 已禁用 |
- | 12 | `cf-58-scraper-replicate` | cf-58-scraper-replicate | 把一套已验证的 Cloudflare 全栈 58同城爬虫（Worker + D1 + KV + Pages 看板，本地爬虫→落盘→wrangler 直连 D1）复刻到新城市 / 新房租通道。当用户说"参考上次的 58 爬虫再做一个 XX 城市/买房/租房项目""复刻 yunnan-housing 工作流到 XX"时使用。核心是用 token 替换生成器批量产出项目，并严格核对「城市名所有形态」避免泄漏。 | 启用 |
- 嵌套响应解析、phpBB 限流与 iFastNet 偶发 SSL 错误重试、发前去重。 | 已禁用 |
- 当用户纠结"我是不是财富自由了"、"财富自由到底是什么意思"、"有钱了是不是就自由了"、"时间自主权 vs 资产多少"、"如何判断自己离财富自由还有多远"、"个人商业模式升级的目标"时使用。给出作者对财富自由的精确定义，帮助用户澄清概念、判断当前状态、规划升级路径。不适用于具体投资标的推荐或短期理财建议。 | 启用 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
