---
layout: default
title: 技术点 · Render 免费档三个数字 + Cloudflare Workers 免费额度 · 调研稿（Q6）
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · Render 免费档三个数字 + Cloudflare Workers 免费额度 · 调研稿（Q6）

> 来源：261022_Render 免费档三个数字 + Cloudflare Workers 免费额度 · 调研稿（Q6）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | 3 | 账号每月 **750 小时**额度 | **对（口径需精确）** | **每个 workspace 每月 750 实例小时**（免费服务**共享**该额度，不是每个服务各 750 小时） |
- **补充（容易漏的点）**：内存 512MB 是**上限**，同时 CPU 只有 **0.1 核**。跑 SearXNG 这类要起 Python 进程 + 聚合多个搜索引擎的服务，512MB 属于「能跑但紧」，CPU 0.1 核才是更常见的瓶颈。
- 2. 归属是 **每个 workspace 每月**，不是每个服务各 750 小时；同一 workspace 下所有免费服务**共享**这 750 小时。
- 3. 算术：750 ÷ 730（一个月约 730 小时）≈ **1.03**，即这额度基本只够**一个免费服务 7×24 常驻**。想同时挂两个常驻免费服务会超额。超过额度后免费服务会被暂停（第三方口径，官方页面未逐字确认具体处置方式，标「未核实」）。
- | Render 免费 Web 服务 | 512 | **MB（内存）** | 常驻上限 | render.com/articles/…scaling-your-first-app |
- | Render 免费 Web 服务 | 0.1 | **CPU 核** | 常驻上限 | 同上 |
- | Render 免费服务休眠 | 15 | **分钟（无入站流量）** | 每次触发 | render.com/articles/platforms-with-a-real-free-tier… |
- 1. **内存**：512MB 对 SearXNG（Python + 多引擎并发抓取）偏紧，建议限制 worker 数、关掉重型引擎（如需要浏览器渲染的引擎）。
- 3. **额度**：750 小时/workspace/月 ≈ 只够一个服务常驻；如果还要在同一 workspace 挂别的免费服务，会互相抢额度。
- 4. **持久化**：官方文档明确「Free web services 不能挂持久磁盘」（https://render.com/docs/free ），SearXNG 的配置需走环境变量或每次重建，**不要指望本地文件持久化**。
- | 超出 750 小时后免费服务的具体处置（暂停/收费） | **未核实** | 第三方称「all your free services are suspended」，官方页未逐字确认 |
- **每月 750 小时** —— 对，但要写成「**每个 workspace 每月 750 实例小时，所有免费服务共享**」

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
