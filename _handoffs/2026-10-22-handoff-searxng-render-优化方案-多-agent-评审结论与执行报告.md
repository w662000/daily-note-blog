---
layout: default
title: 交接文档 · SearXNG-Render 优化方案：多 agent 评审结论与执行报告
date: 2026-11-14 23:30:00 +0800
---

# SearXNG-Render 优化方案：多 agent 评审结论与执行报告

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\SearXNG优化方案_多agent评审与执行_20261023.md

> 生成时间：2026-10-23
> 输入：豆包《SearXNG-Render 部署完成：检查清单 + 优化&风险方案》
> 方法：按用户 P0 规则做多 agent 评审（**角色不共模 + prompt 对立 + 队长仲裁**），
> 再把评审结论与本人线上实测交叉验证后执行。
> 评审团队：红队挑错员（hy3）、事实核对员（hy3，因 deepseek-v4.1-flash 账号级 429 改派）、
> 队长架构仲裁（本人，第三个模型）。

---

## 〇、一句话结论

豆包方案的**方向对、字段错、优先级错**：8 条配置字段名全部写错（其中 2 条会直接搞挂服务）、
1 个环境变量不存在、1 条"最危险改动"是误判；而它自己标记为"紧急提醒"的
**JSON 接口裸奔**，反而没有被列进它的"必须做"清单。
已按评审结论执行完毕，**本地版 480/480 测试全绿，CF 版线上实测主备切换生效、Tavily 零消耗**。

---

## 一、多 agent 评审：三条结论

### 1. 红队挑错员（hy3）抓到 2 个我漏掉的问题

| # | 问题 | 证据 |
|---|---|---|
| 1 | `server.limiter: true` + `limiter:` 块 **YAML 键重复自相矛盾**，且 limiter 需要 valkey（Render 免费档没有）→ 启动崩溃 | 官方 settings 模板 |
| 2 | 方案 A（Cloudflare Worker 前置鉴权）**挡不住 origin 直连**——外界拿到 `*.onrender.com` 仍可绕过 Worker 直连后端 | 红队自标"推测"，维持推测 |

### 2. 红队有 1 条实证错误，队长已仲裁

红队称 `server.method: "POST"` 会切断所有 GET 接入方、列为"最危险第 3"。
**证伪**：线上实例当前正配着 `method: "POST"`，而我的 GET 探测（`/search?...&format=json`）
**全部 200 返回**。SearXNG 的 `server.method` 只决定 HTML 表单提交方式，
`/search` 路由 GET/POST 都接收。→ 无需改回 GET。

**这条错误有实质危害**：它把注意力从真正未解的最高危项（JSON 裸奔）上引开了。

### 3. 事实核对员（独立）逐条证实/证伪，并重排危险项

| 项目 | 结论 |
|---|---|
| `ui.default_locale: zh_CN`（下划线） | **证实**——被 preferences 校验拒绝，每请求 500，连 `/healthz` 都挂 |
| `server.limiter: true` + `botdetection:` 段 | **证实**——无 valkey 开不了；`botdetection` 段上游已移除 |
| 8 条字段名错误 | **全部证实**（`search.lang`→`default_lang`、`max_search_time`→`outgoing.request_timeout`、`max_results`（无此键）、`ui.theme`→`default_theme`、`server.metrics`→`general.enable_metrics`、`infinite_scroll`→插件段、`botdetection` 删除、`x-captcha-validation` 非法） |
| `SEARXNG_LIMITER_ENABLED=true` | **证实**——该变量在 SearXNG 中不存在，是假动作 |
| `method: "POST"` 切断 GET | **证伪**（见上） |
| `${SEARXNG_SECRET}` 插值风险 | **证伪**——仓库 entrypoint.sh 的 sed 替换机制完好，风险已化解 |
| JSON 接口裸奔 | **证实且至今未解**——替补为真实最高危项 |

---

## 二、已执行的改动

### A. `searxng-render/`（SearXNG 部署仓库）

| 文件 | 改动 |
|---|---|
| `settings.yml` | **重写**。引擎换血为 `brave / wikipedia / mojeek / baidu`（`keep_only` 白名单）；8 条非法字段全部修正；`default_locale` 改连字符；`limiter: false`；`outgoing.request_timeout: 6.0`；删除 `botdetection` 段。已用 PyYAML 校验结构通过 |
| `search_auth.py` | **新建**。容器内 WSGI 鉴权中间件：只对机器可读格式（json/csv/rss）要求 `X-Search-Key`，HTML 网页 UI 全放行；**同时解析 POST body**，堵住 `curl -X POST -d 'format=json'` 绕过 GET 查询串检查 |
| `entrypoint.sh` | 启动前改写官方硬编码的 `exec granian searx.webapp:app` 行，包装进鉴权中间件；**替换失败即拒绝启动（fail-closed）**——不fail-closed 的话配置漂移会静默退回无鉴权状态 |
| `Dockerfile` | 同步更新启动链 |
| `test_search_auth.py` | **新建**。WSGI 级单测，**22/22 通过**，含：POST 绕过被挡、`wsgi.input` 正确归还（否则 SearXNG 收不到表单）、根路径覆盖 |

### B. 本地多 agent 版（`agent-teams`）

`mcp/lib/grounding.mjs` 重写为 **SearXNG 主 / Tavily 备**；配置三处同步
（`loadConfig` → `startServer` 白名单 → `qualityCfg()`，这是 `AGENT_TEAMS_CONTRACT_ENFORCE`
踩过的坑）；`quality.mjs` 的 `groundArtifact` 透传；README 增补章节。
**新增测试 19 条，全量 480/480 通过。**

### C. CF 多 agent 版（`cf-multi-agent-qa`）

`src/grounding.js` 同源改造；`wrangler.jsonc` 加 `SEARXNG_URL`；
`scripts/test-grounding.mjs` 支持 `--searxng=` 并逐条标注证据来源。
**线上实测通过**（见下节）。

---

## 三、接入后线上实测：4 个设计被数据推翻/修正

全部来自对 `searxng-render-gn0d.onrender.com` 的真实调用。

### ① `site:` 运算符不可用 —— 证实，改为代码层域名过滤

`q=政策原文 小规模纳税人增值税起征点 site:gov.cn` 返回的 10 条结果全部来自 bing，
内容却是 X(推特) 上的 A 股股评帖，与税务毫无关系。
→ 查询词保持干净，拿到结果后**代码层按 host 后缀过滤**。
匹配写 `h === d || h.endsWith('.' + d)`，不用 `endsWith(d)`——后者会把 `notgov.cn`
判成官方站点。

### ② "政策原文"前缀在 SearXNG 上**有害** —— 新发现，已删

同一条税务声明，四次对照：

| 查询 | 结果数 | 内容 |
|---|---|---|
| 无前缀 | 29 | brave 返回 `chinatax.gov.cn`、福建税局**官方原文**，完全对题 |
| 有前缀 | 10 | bing 返回 gov.cn 门户首页 + "政策"百科/维基词条；brave 还被限流 |

前缀让引擎改去匹配"政策"这个词本身，把实质内容全丢了。
→ **SearXNG 路径删除前缀**；Tavily 路径保留（它的前缀有 Tavily 自己的依据，
且我没有反证）。两条路径行为不同是**有意的**——证据只推翻了一个，不改另一个。

### ③ 厂商配额句被误判成政策类 —— 新发现，已加厂商排除

`POLICY` 正则里的「额度」「上限」「年限」过度宽泛：
「Cloudflare Workers AI 的免费额度是每月 10 万次请求」含"额度" → 被判政策类
→ 域名锁到 gov.cn → 官方站点当然搜不到云厂商定价 → 记一条**假 mismatch**。
实测这类句子能占满 3 条核查名额，真正的税率句反而没轮到。
→ 新增 `isPolicyClaim()`：命中 POLICY **且**命中 VENDORS 时按厂商配额句处理，不锁域名。
判据：中国税务政策句不会提 Cloudflare/OpenAI/AWS。
（顺带发现 `OpenRouter` 不在 VENDORS 列表里——本项目自己就在用它，已补。）

### ④ 主搜索空手 ≠ 官方没有 —— 语义修正，改为落 Tavily 备用

原设计：政策类域名过滤后为空 → 直接记"未找到对应政策原文"，不落备用。
实测反例：同一条税务声明，SearXNG 这一轮官方域名被引擎限流打空，
而 Tavily 明明能取到 `chinatax.gov.cn` 原文。两条最危险的声明
（「10 万以下免征」「20% 综合所得税率」）因此零证据。
→ 改为：SearXNG 空 → 落 Tavily；**两条都认真试过**仍无官方原文才判否。
反向保护：**检索失败**（网络抛错）不写"无官方依据"——没查到不等于政策不存在。

### ⑤ 额外修正

- **空串超时陷阱**：`Number('')` 是 `0`，`AbortSignal.timeout(0)` 会让每次请求立即中止，
  主搜索全盘假死。Worker/wrangler 里未设置变量可能是 `""`。→ 加 `numOr()`，
  空串/非有限数回退默认，同时保留 `0`（单测要归零延时加速）。
- **证据召回不足**：finding 只取前 3 条摘要、900 字符，实测正确数字出现在第 2 条
  却被截断在外 → 误判 mismatch。→ 改为前 5 条、1600 字符。

---

## 四、引擎选择：与豆包建议的差异（重要）

豆包和此前其他 AI 建议的"语义友好引擎"里，**3 个在 SearXNG 上游根本不存在**
（已用 GitHub git trees API 核实，上游共 252 个引擎模块）：

| 建议的引擎 | 上游是否存在 |
|---|---|
| Mojeek | ✅ 存在 |
| Brave | ✅ 存在 |
| Wikipedia | ✅ 存在 |
| Startpage | ✅ 存在 |
| **Seekport** | ❌ **不存在** |
| **Wiby** | ❌ **不存在** |
| **Stackoverflow** | ❌ **不存在** |

**已选定 4 个：brave / wikipedia / mojeek / baidu**
（baidu 是中文网络覆盖最好的；brave 实测能返回 `chinatax.gov.cn` 官方原文；
wikipedia 稳定；mojeek 语义友好）。

⚠️ **必须如实说明的未解张力**：
我逐引擎强制测试时发现 `engines` 查询参数**被实例忽略**（9 次请求返回完全相同的结果集），
说明**线上跑的仍是旧配置**，我的引擎换血尚未部署。
在我能观察到的范围内：**brave 第 2 次查询即被限流、duckduckgo 持续超时、
只有 bing 在稳定出中文结果**——而 AI 建议恰恰是关掉 bing（机房 IP 验证码风险）。
这个矛盾**无法在部署前解决**，需要部署后用真实流量观察。
已做的缓解：grounding 层有熔断器（单轮连续 2 次失败即停用、进程内累计 3 次进 5 分钟冷却）
+ Tavily 兜底，单个引擎不稳不会拖垮核查链路。

---

## 五、需要你执行的事项（我做不了的部分）

本机无 Docker、无 Render API token，**无法完成部署**。按优先级：

### P0 — 部署 SearXNG 新配置（解锁引擎换血 + JSON 鉴权）

```bash
cd "D:/AI work/workbuddy/2026-10-22-22-03-16/searxng-render"
git add -A && git commit -m "引擎换血 + WSGI JSON 鉴权 + 8 处字段修正" && git push
```
Render 会自动重新部署。**同时必须设两个环境变量**（Render 面板 → Environment）：

| 变量 | 值 |
|---|---|
| `SEARXNG_SECRET` | 自己生成的随机密钥（不要用示例串） |
| `SEARCH_API_KEY` | JSON 接口鉴权 key，下面两个系统要用同一个值 |

**通过标准**：
```bash
curl -s "https://searxng-render-gn0d.onrender.com/healthz"                    # 200 OK
curl -s "https://.../search?q=测试&format=json"                              # 401/403（未认证被挡）
curl -s -H "X-Search-Key: <key>" "https://.../search?q=测试&format=json"     # 200 + JSON
```

### P1 — 配置两个 agent 系统

**本地版**（写进 `.env`，已 gitignore）：
```bash
AGENT_TEAMS_SEARXNG_URL=https://searxng-render-gn0d.onrender.com
AGENT_TEAMS_SEARXNG_API_KEY=<上面的 SEARCH_API_KEY>
```
验证：`node mcp-server.mjs --print-config` 应看到 `searxngUrl` 非空、key 已脱敏。

**CF 版**：
```bash
npx wrangler secret put SEARXNG_API_KEY    # 同一个值
# wrangler.jsonc 里把 "SEARXNG_URL": "" 改成实际地址
```

### P2 — 保活与监控（豆包这部分的建议基本采纳）

- UptimeRobot 监控**首页域名**（不要打 `/search`，避免产生真实搜索），10 分钟一次，关告警。
- 代码侧已处理冷启动：20s 短超时 + 12s 后 60s 长超时重试 + 熔断器。
  **不要**把超时调短——那会把正常冷启动误判为故障，反而浪费 Tavily 备用额度。
- 每月看 Render 运行小时（750h 是账号全局共享）；不用时手动 **Suspend**（Sleep 也消耗时长）。
- 长期最优解仍是豆包提的方向：**Cloudflare Tunnel + 本地 Docker**，无休眠、无小时额度。

---

## 六、验证结果汇总

| 项 | 结果 |
|---|---|
| SearXNG WSGI 鉴权单测 | **22/22 通过**（含 POST 绕过、`wsgi.input` 归还、根路径覆盖） |
| `settings.yml` YAML 结构校验 | 通过（PyYAML） |
| 本地版全量测试 | **480/480 通过**（原 461 → 新增 19） |
| CF 版主备切换线上实测 | 3 条声明全部拿到官方证据，**Tavily 零消耗**（`searches:0`），来源含 `chinatax.gov.cn`、福建税局、`app.www.gov.cn` |
| CF 版厂商配额句假警报 | 已消除（来源从 gov.cn 门户噪音变为真实 Cloudflare 页面，含定价页） |
| 配置层→工具层链路 | `--print-config` 实证透传，key 脱敏；新增 judge 路径端到端回归测试守护 |

---

## 七、已知遗留（不掩饰）

1. **引擎换血未部署验证**——线上仍是旧配置，brave 限流 / duckduckgo 超时 / bing 是唯一稳定中文源
   这个矛盾要等部署后用真实流量判断。已用熔断器 + Tavily 兜底缓解。
2. **Tavily 回声效应**未根治——错误声明被检索结果复述时，数字核对会判"对上"。
   设计上不让任何模型出裁决，检索原文 + URL 全进评审 prompt，由审核员对照判断。
3. **数字核对只查一致性**——实测「月租金 10 万元，按 1.5% 缴纳增值税」，
   检索事实确认了 1.5% 却没提 10 万元，仍判 mismatch。方向安全（宁可多报），
   但审核员必须自己看懂证据块，不能只盯 mismatch 标记。
4. **CF 版未重新部署**——`wrangler deploy` 需要你执行；CF 版最后部署版本未端到端验证。
5. **本地版新事实核查层未用真评审器端到端验证**——目前是假 orchestrator 集成测试 + 线上直调
   `verifyClaims` 双轨，缺一环"真 codebuddy CLI 当评审员"的完整跑通。
