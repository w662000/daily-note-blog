---
layout: default
title: 技术点 · 队长架构评审与仲裁底稿（2026-10-23）
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · 队长架构评审与仲裁底稿（2026-10-23）

> 来源：261022_队长架构评审与仲裁底稿（2026-10-23）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
| # | 豆包主张 | 队长裁定 |
|---|---|---|
| B1 | JSON 接口无鉴权是高危点，方案A 用 Cloudflare Worker 前置 Basic Auth | **方向对，实现换**。Worker 方案要多接一个域名到 CF DNS、多一跳外部依赖。更稳的做法是在**容器内**加一层 WSGI 中间件：只对非 html 的 `format` 要求 key，其余（网页 UI、`/healthz`、`/static`）全放行。依据：官方入口最后一行硬编码 `exec granian searx.webapp:app` 且忽略 CMD [C12]，所以由 `render-entrypoint.sh` 在启动前把该行替换为 `granian search_auth:app`，**并校验替换成功、失败则拒绝启动**（fail-closed）。不改 SearXNG 源码、不加外部依赖、内存代价约等于零 |
| B2 | 代码必须处理超时/502/冷启动，Python 示例 `timeout=45` + 重试 + `sleep(12)` | **完全正确，原样吸收**。并补一条豆包没提到的：必须配 **SearXNG 熔断器**——连续失败后本次不再尝试 SearXNG 直接走 Tavily。否则每次冷启动都先干等 45 秒再降级，既慢又会在"看起来降级了"的错觉里把 Tavily 额度烧光 |
| B3 | 精简引擎 | **保留，但换名单**。豆包的 bing/ddg 名单不成立（见 A6） |

### 关键技术要点（自动抽取）
- | A2 | `botdetection: { limiter: true, x-captcha-validation: null }` | **无效配置**。新版 SearXNG 已把 botdetection 移出 settings.yml，改到 `/etc/searxng/limiter.toml`；`x-captcha-validation` 不是合法项 | [C10][C11] |
- | A3 | `server.limiter: true` + `limit: "8/minute..."` | **开不了**。limiter 强依赖 valkey 数据库，Render 免费档没有 | [C4] |
- | A4 | 基础检查第 5 项「验证 `SEARXNG_LIMITER_ENABLED=true`」 | **这个环境变量在 SearXNG 里根本不存在**，加了也没用 | [C5] |
- 不像是能搞挂服务的改动。这类"看似无害实则致命"的配置正是必须靠官方源码逐条核实的原因。
- | B1 | JSON 接口无鉴权是高危点，方案A 用 Cloudflare Worker 前置 Basic Auth | **方向对，实现换**。Worker 方案要多接一个域名到 CF DNS、多一跳外部依赖。更稳的做法是在**容器内**加一层 WSGI 中间件：只对非 html 的 `format` 要求 key，其余（网页 UI、`/healthz`、`/static`）全放行。依据：官方入口最后一行硬编码 `exec granian searx.webapp:app` 且忽略 CMD [C12]，所以由 `render-entrypoint.sh` 在启动前把该行替换为 `granian search_auth:app`，**并校验替换成功、失败则拒绝启动**（fail-closed）。不改 SearXNG 源码、不加外部依赖、内存代价约等于零 |
- | B2 | 代码必须处理超时/502/冷启动，Python 示例 `timeout=45` + 重试 + `sleep(12)` | **完全正确，原样吸收**。并补一条豆包没提到的：必须配 **SearXNG 熔断器**——连续失败后本次不再尝试 SearXNG 直接走 Tavily。否则每次冷启动都先干等 45 秒再降级，既慢又会在"看起来降级了"的错觉里把 Tavily 额度烧光 |
- | C1' | `max_results: 10` 限制返回数量省内存 | 字段不存在 [C3]；SearXNG 内存主要取决于**并发引擎数**，不取决于返回条数。真要省内存就减引擎，已经做了 |
- | C2' | 关闭 `infinite_scroll` 省资源 | 它是前端插件 [C8]，省的是用户浏览流量，不是服务端内存 |
- | C3' | 加 Cloudflare Worker 鉴权 | 除非本来就要用 CF 做别的事，否则为一个小实例多加一跳外部依赖不划算。容器内中间件已覆盖同一风险 |
- | C4' | `server.method: "POST"` | 已在现有配置里。只影响网页表单提交方式，**GET 查询照样可用**——这正是接入方要用的方式，不用动 |
- | brave | 语义友好（独立索引，非 Google/Bing 代理）、中文覆盖好 | [C16] 存在；[E2][E3] 实测能出中文结果 |
- | mojeek | 独立爬虫，**几乎不对机房 IP 限流**，是 brave 被限流时的多样性补充 | [C16] 存在 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
