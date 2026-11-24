---
layout: default
title: 交接文档 · Render 免费档三个数字 + Cloudflare Workers 免费额度 · 调研稿（Q6）
date: 2026-10-22 12:00:00 +0800
---

# Render 免费档三个数字 + Cloudflare Workers 免费额度 · 调研稿（Q6）

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\Q6_调研稿_20261023.md

> 检索方式：`mcp__agent-teams__agent_teams_web_search`，检索日期 2026-10-23。
> 来源标注：**官方** = render.com 官方博客/文档/官方文章、developers.cloudflare.com；**第三方** = 教程站、对比站、媒体（已注明）。
> 单位纪律：**请求数（次/天）、Neurons（个/天）、小时（实例小时/月）、分钟（闲置时长）四个单位互不换算、互不混用。**

---

## 结论速览

| # | 说法 | 判定 | 正确表述 |
|---|------|------|----------|
| 1 | Render 免费档内存 **512MB** | **对** | 512 MB RAM，同时只有 **0.1 CPU** |
| 2 | 闲置 **15 分钟**自动休眠 | **对** | 无入站流量（inactivity）15 分钟后 spin down，下次请求冷启动约 **1 分钟** |
| 3 | 账号每月 **750 小时**额度 | **对（口径需精确）** | **每个 workspace 每月 750 实例小时**（免费服务**共享**该额度，不是每个服务各 750 小时） |
| 4 | Cloudflare Workers 免费额度 **每天 10 万次请求** | **对** | **100,000 requests/day**（UTC 零点重置，超限返回 Error 1027） |

> 四个数字**全部正确**，但第 3 条的单位/归属需要收紧（per workspace、共享池），第 2 条应写「无活动/无入站流量」而不是「闲置」。

---

## 一、Render 免费档内存 512MB —— **对**

官方文章（render.com 域内）原文：
> **Memory allocation: 512MB RAM for web services**
> **CPU allocation: 0.1 CPU**
- https://render.com/articles/from-side-project-to-production-scaling-your-first-app

第三方交叉印证（同口径）：
- https://livemy.app/blog/render-pricing —— "free compute instance with **512 MB RAM and 0.1 CPU**"
- https://www.codecapsules.io/blog/best-render-alternatives-in-2026-where-to-go-when-render-falls-short —— "free instances get **512 MB RAM and 0.1 CPU**"
- https://www.srvrlss.io/provider/render —— "free web service instance has **512 MB RAM**"

**补充（容易漏的点）**：内存 512MB 是**上限**，同时 CPU 只有 **0.1 核**。跑 SearXNG 这类要起 Python 进程 + 聚合多个搜索引擎的服务，512MB 属于「能跑但紧」，CPU 0.1 核才是更常见的瓶颈。

---

## 二、闲置 15 分钟自动休眠 —— **对**

官方文章原文：
> **Free web services spin down after 15 minutes of inactivity** and restart on the next request, with spin-up taking about on[e minute]
- https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026

官方另一篇（同一域）：
> **Service instances spin down after 15 minutes of inactivity**
> **Cold start occurs when spinning up from idle state, taking about one minute** before the service serves traffic again
- https://render.com/articles/from-side-project-to-production-scaling-your-first-app

第三方印证：
- https://www.codecapsules.io/blog/best-render-alternatives-in-2026-where-to-go-when-render-falls-short —— "free web services sleep after **15 minutes without inbound traffic** and take about a minute to wake up"
- https://www.srvrlss.io/provider/render —— 同口径

**措辞修正建议**：官方口径是 **inactivity / 无入站流量**，不是「闲置」这种模糊说法。另外要点是**冷启动约 1 分钟**——对 SearXNG 意味着休眠后第一次搜索会明显卡顿。

**第三方补充（未经官方页面直接确认，标「未核实」）**：有第三方称「自 2026 年 2 月起，WebSocket 流量也算作活动」（https://www.codecapsules.io/blog/best-render-alternatives-in-2026-where-to-go-when-render-falls-short ）。该条我未在 render.com 官方页面取到原文，**不作为结论**。

---

## 三、账号每月 750 小时 —— **对，但口径要精确**

官方博客原文：
> Render's free instance type for web services gives every user **750 hours of compute time every month** to run as many free services as you'd like.
- https://render.com/blog/free-tier

官方文章原文（更精确）：
> **Free instance hours: 750 hours per workspace per month**
- https://render.com/articles/from-side-project-to-production-scaling-your-first-app

官方文档页（对应小节标题为「Monthly usage limits → Free instance hours」）：
- https://render.com/docs/free

第三方印证（强调「共享池」）：
- https://livemy.app/blog/render-pricing —— "free services **share 750 instance hours a month across the workspace**"
- https://www.codecapsules.io/blog/best-render-alternatives-in-2026-where-to-go-when-render-falls-short —— "**750 free instance hours per workspace per month**. Go over and all your free services ar[e suspended]"

**三处必须说清楚的口径**：
1. 单位是 **实例小时（instance hours）**，不是「运行时长」「请求数」或「CPU 秒」。
2. 归属是 **每个 workspace 每月**，不是每个服务各 750 小时；同一 workspace 下所有免费服务**共享**这 750 小时。
3. 算术：750 ÷ 730（一个月约 730 小时）≈ **1.03**，即这额度基本只够**一个免费服务 7×24 常驻**。想同时挂两个常驻免费服务会超额。超过额度后免费服务会被暂停（第三方口径，官方页面未逐字确认具体处置方式，标「未核实」）。

---

## 四、Cloudflare Workers「每天 10 万次请求」—— **对**

官方文档（Limits）原文：
> Accounts on the Workers Free plan have a **daily request limit of 100,000 requests**, resetting at midnight UTC. When a Worker exceeds this limit, Cloudflare returns **Error 1027**.
- https://developers.cloudflare.com/workers/platform/limits

官方文档（Pricing）原文：
> | | Free plan | Paid plan |
> | Requests | **100,000 / day** | 1 million / month, + $0.15/million |
> | Duration | 13,000 GB-s / day | 400,000 GB-s / month |
- https://developers.cloudflare.com/workers/platform/pricing

第三方印证：
- https://buildoto.com/en/blog/cloudflare-workers-pricing-real-costs —— "Workers: **100,000 requests/day**, 10 ms of CPU per invocation"

**要点**：
- 单位是 **请求数（requests）/ 天**，重置点是 **UTC 零点**，不是北京时间零点。
- 免费档同时还有 **每次调用 10ms CPU** 与 **13,000 GB-s/天** 的 Duration 限制（官方 limits/pricing 页），这三者是**并列的三种限额**，不能互相换算。
- ⚠️ **不要和 Workers AI 的额度混淆**：Workers AI 是 **10,000 Neurons/天**（单位是 Neurons，算力单位），与 Workers 的 **100,000 requests/天**（单位是请求数）是**两套完全不同的额度**，数量级差 10 倍，单位也不同。

---

## 五、单位对照表（本题最容易混的地方）

| 平台/产品 | 数字 | 单位 | 周期 | 官方出处 |
|---|---|---|---|---|
| Render 免费 Web 服务 | 512 | **MB（内存）** | 常驻上限 | render.com/articles/…scaling-your-first-app |
| Render 免费 Web 服务 | 0.1 | **CPU 核** | 常驻上限 | 同上 |
| Render 免费服务休眠 | 15 | **分钟（无入站流量）** | 每次触发 | render.com/articles/platforms-with-a-real-free-tier… |
| Render 免费实例额度 | 750 | **实例小时（instance hours）** | 每 workspace 每月 | render.com/blog/free-tier + render.com/docs/free |
| Cloudflare Workers Free | 100,000 | **请求数（requests）** | 每天（UTC 重置） | developers.cloudflare.com/workers/platform/limits |
| Cloudflare Workers Free | 13,000 | **GB-s（Duration）** | 每天 | developers.cloudflare.com/workers/platform/pricing |
| （对照）Cloudflare Workers AI Free | 10,000 | **Neurons（算力单位）** | 每天 | developers.cloudflare.com/workers-ai/platform/pricing |

---

## 六、给「在 Render 免费档跑 SearXNG」的实务提醒

以下为**基于上述官方限制的推断/建议**，不是官方原文，已单独标注：

1. **内存**：512MB 对 SearXNG（Python + 多引擎并发抓取）偏紧，建议限制 worker 数、关掉重型引擎（如需要浏览器渲染的引擎）。
2. **冷启动**：15 分钟无流量即休眠，下一次请求要等约 1 分钟，交互式搜索体验会明显受损。**推断**：可用外部定时任务每 10 分钟打一次请求保活，但这会消耗 750 实例小时（本来就是常驻消耗，不额外增加，因为保活=保持运行）。
3. **额度**：750 小时/workspace/月 ≈ 只够一个服务常驻；如果还要在同一 workspace 挂别的免费服务，会互相抢额度。
4. **持久化**：官方文档明确「Free web services 不能挂持久磁盘」（https://render.com/docs/free ），SearXNG 的配置需走环境变量或每次重建，**不要指望本地文件持久化**。
5. **免费 Postgres**：1GB、创建 30 天后过期（官方文章 https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026 ），SearXNG 本身不需要数据库，可忽略。

---

## 七、未核实项（如实标注）

| 项目 | 状态 | 说明 |
|------|------|------|
| 「2026 年 2 月起 WebSocket 流量算作活动」 | **未核实** | 仅第三方一处提及，未在 render.com 官方页取到原文 |
| 超出 750 小时后免费服务的具体处置（暂停/收费） | **未核实** | 第三方称「all your free services are suspended」，官方页未逐字确认 |
| Render 免费档未来是否调价/调额 | **不适用** | 本文只对 2026-10-23 检索到的页面负责 |

---

## 八、一句话回答

- **512MB** —— 对（另注意只有 0.1 CPU）
- **15 分钟休眠** —— 对（是「15 分钟无入站流量」，冷启动约 1 分钟）
- **每月 750 小时** —— 对，但要写成「**每个 workspace 每月 750 实例小时，所有免费服务共享**」
- **Workers 每天 10 万次请求** —— 对（100,000 requests/day，UTC 零点重置）；别和 Workers AI 的 10,000 Neurons/天 搞混
