---
layout: default
title: 交接文档 · SearXNG-Render 优化方案 · 多 agent 评审输入（2026-10-23）
date: 2026-11-14 23:30:00 +0800
---

# SearXNG-Render 优化方案 · 多 agent 评审输入（2026-10-23）

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\多agent评审_输入_20261023.md

> 本文件是评审的唯一事实来源。**所有结论必须引用本文件中的证据编号**（如 [C3]、[E5]）。
> 不允许凭记忆断言 SearXNG 配置项——本文件第 3 节已用官方源码/文档逐条核实过。

---

## 1. 背景与目标

一个 SearXNG 实例部署在 Render 免费档，要改造成**两个多 agent 问答系统的主搜索源**：

| 项 | 值 |
|---|---|
| 线上实例 | `https://searxng-render-gn0d.onrender.com`（healthz 返回 OK，已实测通） |
| 本地仓库 | `D:\AI work\workbuddy\2026-10-22-22-03-16\searxng-render`（4 文件：Dockerfile / entrypoint.sh / settings.yml / README.md，已推送 GitHub，Render 自动部署） |
| 平台约束 | Render Free：512MB 内存、750 小时/月（**账号全局共享**）、闲置 15 分钟休眠、冷启动 30–80 秒、无持久化磁盘 |
| 出口 IP | 数据中心 IP，Google 几乎必 429/CAPTCHA |
| 搜索定位 | **SearXNG 为主搜索，Tavily 为备用**（Tavily 免费 1000 次/月，约 33 次/天，必须省着用） |
| 接入方 1 | CF 版：`C:\Users\Administrator\WorkBuddy AI\2026-10-20-11-50-43\cf-multi-agent-qa\src\grounding.js` 的 `searchOne(env, claim)` / `verifyClaims(env, finding)` |
| 接入方 2 | 本地版：`D:\workspace\workbuddyai\agent-teams\mcp\lib\grounding.mjs` 的 `searchOne(apiKey, claim, fetchImpl)` / `verifyClaims({...})` |
| 共同结构 | `extractClaims`（政策类声明插队）→ 逐条检索 → **代码做确定性数字核对**（`numbersIn`/`pctIn`）→ 返回 `{claims:[{claim,finding,mismatch}], sources}` |

**grounding 的设计铁律（不可违反）**：不让任何模型出裁决。检索只提供"检索事实"，
数字是否一致由代码确定性核对，`mismatch=true` 只表示"声明里的数字没在检索事实中出现"，
供审核员与草稿原文比对。任何搜索失败都静默降级，绝不阻塞主链路。

---

## 2. 待评审对象：豆包优化方案（全文）

> 环境背景：Render Free，512M内存，闲置15min自动Sleep；账号共享750小时运行额度；出口IP搜索引擎风控；公网JSON接口；无鉴权。

### 一、立刻做的基础检查（5项）
1. 网页访问域名，确认页面加载、UI 中文正常
2. JSON 接口测试 `curl ".../search?q=大模型发展&format=json"`；403 = settings.yml 漏写 `search.formats: [html,json]`；大量空 results = 出口 IP 风控
3. 看 Render Logs：大量 `429 Too Many Requests` / `OOM killed`
4. 核对环境变量：`SEARXNG_SECRET` 不是默认示例字符串；`SEARXNG_BASE_URL` 末尾带 `/`、域名一致
5. **验证限速 limiter 是否开启：`SEARXNG_LIMITER_ENABLED=true`**

### 二、现存风险
1. 闲置 15 分钟 Sleep，AI 调用第一次要等 30–80 秒冷启动，脚本易超时；UptimeRobot 保活只能缓解
2. 512MB 内存，多引擎并发查询易 OOM
3. **JSON 接口完全公开无鉴权**：被爬虫扫到会疯狂刷，耗尽带宽 + 750 小时，Render 可能冻结服务
4. Render 出口 IP 风控：Google 必 429；Bing/DuckDuckGo 跑久了也可能被封
5. 750h 账号全局共享，旧实例不 Suspend 会吃掉时长；**Sleep 状态也消耗时长，只有手动 Suspend 才释放**
6. 免费实例无持久化存储，日志缓存全丢

### 三、配置优化（改 settings.yml 推送 GitHub，Render 自动重新部署）
#### 3.1 内存优化
```yaml
search:
  safe_search: 0
  lang: zh-CN
  max_search_time: 6   # 原来8，缩短超时
  formats: [html, json]
  max_results: 10      # 新增，限制返回结果数量
```
精简引擎，保留 bing、duckduckgo、brave、wikipedia、github，其余全部 disabled。

#### 3.2 限速调严
```yaml
server:
  secret_key: "${SEARXNG_SECRET}"
  limiter: true
  limiter:
    limit: "8/minute, 120/hour, 400/day"
  public_instance: false
  image_proxy: false
  method: "POST"
  base_url: "${SEARXNG_BASE_URL}"
```

#### 3.3 关闭不需要的功能
```yaml
ui:
  infinite_scroll: false
  theme: simple
  default_locale: zh_CN
server.metrics: false
general:
  debug: false
```

#### 3.4 botdetection
```yaml
botdetection:
  limiter: true
  x-captcha-validation: null
```

### 四、接口安全优化（最重要）
> Render 本身不能在 Web Service 层面加 Basic Auth，两种方案二选一：
- **方案A（简单，推荐）Cloudflare Worker 前置鉴权**：Render 域名接入 Cloudflare DNS，Worker 做代理加 Basic Auth，外界不能直接访问 onrender.com
- **方案B（代码层面 token 鉴权）**：调用时带自定义 header 做前置校验。SearXNG 原生不支持 API token，需反向代理层实现，**不建议直接改 searxng 源码**
- ⚠️ 不要把 onrender 域名公开到互联网

### 五、保活配置（UptimeRobot）
1. 监控目标填首页域名，不要访问 /search
2. 轮询间隔 10 分钟一次，不要低于 5 分钟
3. 关闭告警通知
4. Render 会识别监控 User-Agent，保活间歇性失效，**代码必须处理超时、502、冷启动等待**

Python 调用示例（适配休眠）：
```python
def searxng_query(query, max_retries=3):
    params = {"q": query, "format": "json"}
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, timeout=45)  # 冷启动需要长超时
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"尝试 {attempt+1} 失败，可能休眠冷启动：{e}")
            time.sleep(12)
    return None
```

### 六、运维监控
1. Render 日志看 OOM killed / 429；OOM 就删减引擎
2. 每月留意 750 小时消耗
3. Bing/DDG 大量 429 时没有很好解法，只能减少调用频率
4. 本地文件夹就是完整备份

### 七、长期改进
1. 本地可开机电脑：**Cloudflare Tunnel + 本地 Docker**，无休眠、无小时额度
2. 继续用 Render：强烈加 Cloudflare Worker 鉴权

### 八、避坑总结
1. Sleep ≠ Suspend，不用时手动 Suspend 释放时长
2. 512M 不要开一堆引擎
3. JSON 无鉴权是高危点，不要泄露 URL
4. AI 调用代码必须写重试、长超时

---

## 3. 已核实的官方事实（依据 searxng/searxng master 源码 + docs.searxng.org，2026-10-23）

| # | 事实 | 依据 |
|---|---|---|
| C1 | `search.lang` **不是合法字段**，正确的是 `search.default_lang` | 项目 README「与豆包版指南的差异对照」已记录此修正 |
| C2 | `search.max_search_time` **不是合法字段**，真实旋钮是 `outgoing.request_timeout` / `outgoing.max_request_timeout` | 同上 |
| C3 | `search.max_results` **不是合法字段**，SearXNG 无此设置 | 同上 |
| C4 | `server.limiter` 强依赖 **valkey 数据库**，Render 免费档没有 → 开不了 | docs.searxng.org/admin/settings/settings_server.html |
| C5 | `SEARXNG_LIMITER_ENABLED` **这个环境变量在 SearXNG 里根本不存在** | 项目 README 已记录 |
| C6 | `server.metrics` 不是合法字段，指标开关在 `general.enable_metrics` | 官方 settings 文档 |
| C7 | `ui.theme` 不是合法字段，正确的是 `ui.default_theme` | 官方 settings 文档 |
| C8 | `ui.infinite_scroll` 不是合法字段，无限滚动是**插件** `searx.plugins.infinite_scroll.SXNGPlugin` | 官方 settings 文档 |
| C9 | `ui.default_locale: zh_CN`（下划线）**会被 preferences 校验拒绝 → 每个请求 500，连 /healthz 都挂 → 部署 Deploy failed**。合法值只有 `zh-HK` / `zh-Hans-CN` / `zh-Hant-TW`（连字符）。注意 `search.default_lang` 用 `zh-CN` 走另一套校验（sxng_locales），两套体系不能混 | 项目 README「部署实战踩坑记录」第 2 条，2026-10-22 真实踩坑 |
| C10 | `botdetection:` 段**已从 settings.yml 移除**，限流配置在 `/etc/searxng/limiter.toml`；上游仓库确认 `limiter.toml` 存在 | 上游 git tree 实测 |
| C11 | `x-captcha-validation` 不是合法配置项 | 官方 settings 文档 |
| C12 | 官方入口脚本 `/usr/local/searxng/entrypoint.sh` 最后一行是**硬编码** `exec /usr/local/searxng/.venv/bin/granian searx.webapp:app`，**完全忽略 CMD 参数** | 上游 container/entrypoint.sh 原文（已抓取） |
| C13 | 官方镜像 `GRANIAN_HOST="::"`（IPv6），Render 不支持 IPv6，必须 `0.0.0.0`；`GRANIAN_WORKERS` 默认 1，512MB 必须钉死 | 上游 container/Dockerfile |
| C14 | SearXNG **不支持环境变量插值**，`${SEARXNG_SECRET}` 会变成字面量，必须由 entrypoint 在启动前替换 | 上游源码 + 项目 entrypoint.sh |
| C15 | SearXNG 拒绝以 `ultrasecretkey` 字面量启动（webapp.py 会 sys.exit(1)） | 项目 README |
| C16 | 上游共 **252 个引擎模块**。存在：mojeek / wikipedia / baidu / brave / 360search / bilibili / chinaso / sogou / quark / startpage / duckduckgo / github / qwant / yandex / acfun。**不存在：seekport / wiby / stackoverflow**（注意：项目 README「后续可选」里建议加的 stackoverflow 实际不存在） | 上游 git tree 实测 |
| C17 | JSON API 无鉴权是 SearXNG 的固有限制，OSS 版没有 API token 机制 | docs.searxng.org/dev/search_api.html |
| C18 | 请求未启用的 format 会返回 **403 Forbidden** | 同上 |
| C19 | `use_default_settings.engines.keep_only` 是白名单机制，未列入的引擎**完全不加载**（不是 disabled，是不加载）→ 启动更快、内存更稳 | 官方 settings 文档 |
| C20 | `plugins:` 段在 `use_default_settings` 下是**整体替换**而非逐键合并，必须把官方默认插件全部列出 | settings_loader.py |

---

## 4. 线上实测证据（2026-10-23 00:10–00:12，对 `searxng-render-gn0d.onrender.com`）

| # | 操作 | 结果 |
|---|---|---|
| E1 | `GET /healthz` | `OK`（200） |
| E2 | `GET /search?q=增值税小规模纳税人起征点&format=json` | 200 JSON，brave 返回中文结果（m.dongao.com 等） |
| E3 | `GET /search?q=爱因斯坦 相对论&format=json` | **34 条结果**；实际出结果的引擎只有 `bing` + `brave`；`unresponsive_engines: [["duckduckgo","超时"]]`；wikipedia/github 未出结果也未报错 |
| E4 | `GET /search?q=政策原文 小规模纳税人增值税起征点 site:gov.cn&format=json` | **10 条结果全部来自 bing，但内容全是 X(推特) 上的 A 股股评帖子，与税务毫无关系**；`unresponsive_engines: [["brave","请求过于频繁"],["duckduckgo","超时"]]` |
| E5 | 同上查询的引擎健康度 | **brave 在当日第 2 次查询就被限流（"请求过于频繁"）**，duckduckgo 持续超时 |
| E6 | JSON 顶层结构 | `keys: query, results, answers, corrections, infoboxes, suggestions, unresponsive_engines`；`results[]` 含 `title/content/url/engine/engines/score/category/publishedDate` 等字段 |
| E7 | 未带任何认证头的 JSON 请求全部成功 | **JSON 接口当前完全裸奔** |
| E8 | 直连 `www.baidu.com/s?wd=test` | 302（非 Render IP，仅作信号，不能证明 Render 出口可用） |

**E4 是关键负面证据**：`site:gov.cn` 运算符方案在该实例上产出完全不相关的结果。
原因是多引擎语义不一致 + bing 在长中文查询下返回噪声。**任何依赖 `site:` 运算符的方案都不可靠。**

---

## 5. 现有接入点代码结构（评审时请对照）

### CF 版 `src/grounding.js`
- `searchOne(env, claim)`：只调 Tavily（`https://api.tavily.com/search`），政策类加 `"政策原文 "` 前缀 + `include_domains: POLICY_DOMAINS`
- `verifyClaims(env, finding)`：入口。先查 D1 `gquota` 表的 `calls/broken`，超日限或熔断则直接返回空
- 政策域名白名单：`chinatax.gov.cn` / `mof.gov.cn` / `gov.cn`
- 政策类无结果 → 显式记 `mismatch:true`（"未找到对应政策原文"），不静默丢弃
- 401/429/432/433 → 账户级熔断，当日不再调用

### 本地版 `mcp/lib/grounding.mjs`
- 同源移植；D1 `gquota` → 本地 JSON 文件 `stateDir/grounding-quota.json`（`{"YYYYMMDD":{calls,broken}}`）
- `apiKey` 显式传入，缺 key 静默降级返回空
- 可注入 `fetchImpl` 便于单测
- 本地测试套件现有 **461 条测试**，任何改动必须全绿

### 已知未解决局限（评审时必须考虑，不要假装已解决）
- **Tavily 回声效应**：错误声明被检索结果复述 → 数字核对判"对上"
- **模型中国税制知识本身错误**：prompt 修不了根
- 本地新事实核查层未用真评审器端到端验证

---

## 6. 输出要求

1. 只输出 Markdown，不要写代码文件
2. **每条结论必须标注证据编号**（[C1]…[C20]、[E1]…[E8]），没有证据支撑的一律标"推测"
3. 明确区分三档：**必须改（会直接导致故障/资损）/ 应该改（明显收益）/ 不建议改（负优化或无效）**
4. 最后给出"如果我只能做 3 件事，是哪 3 件"
5. 不要复述本文件内容，直接给判断
