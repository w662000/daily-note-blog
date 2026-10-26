---
layout: default
title: 技术点 · 事实核对：红队挑错评审逐条证实/证伪
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · 事实核对：红队挑错评审逐条证实/证伪

> 来源：261022_事实核对：红队挑错评审逐条证实_证伪_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
1. **确保 `ui.default_locale` 为连字符合法值**
   - 动作：确认 settings.yml `default_locale: zh-Hans-CN`（非 `zh_CN` / `zh‑CN` 非ASCII连字符）。
   - 通过标准：`GET /healthz` 返回 `OK`(200)；`GET /search?q=测试&format=json` 返回 200 且 results 为非空数组（无 500）。
2. **保持 `limiter: false`、删除 botdetection / x-captcha-validation**
   - 动作：settings.yml 中 `server.limiter: false`，无 `botdetection:` 段、无 `x-captcha-validation`。
   - 通过标准：部署后 Render 日志无 valkey/limiter 启动报错；`GET /healthz` 200。
3. **字段名保持修正态**
   - 动作：确认使用 `search.default_lang` / `outgoing.request_timeout` / `ui.default_theme` / `general.enable_metrics` / plugins 段；无 `search.lang` / `max_search_time` / `max_results` / `ui.theme` / `server.metrics`。
   - 通过标准：部署后实例正常出结果（[E2][E3] 类查询 200）；SearXNG 启动日志无 "unknown key" 致命警告。
4. **保持 `method: "POST"`（无需改回 GET）**
   - 动作：不改。红队建议改 GET 属误判（#3 已证伪）。
   - 通过标准：`GET /search?q=...&format=json` 200（与 [E2][E3] 一致），证明 POST 不阻断 GET。

### 关键技术要点（自动抽取）
- > 工具限制声明：本环境无 Bash / WebFetch，无法重新 curl 线上实例。所有"实测"证据沿用输入文件第4节 [E1]–[E8]（对 `searxng-render-gn0d.onrender.com` 的 2026-10-23 实测）与仓库源码。
- 2. 因此"字段名错误"核验分两层：①红队说"豆包方案写了 X 错字段"是否属实（对照输入第2节原文）→ 属实；②该错误当前仓库是否已不存在 → 已不存在（证明修正生效）。
- **核对**：输入第2节 3.3 原文确为 `default_locale: zh_CN`（下划线，line78）；[C9] 标注为"2026-10-22 真实踩坑"，属已核实官方事实。
- **补充**：仓库当前 settings.yml line78 已改为 `default_locale: zh-Hans-CN`（连字符），故该致命错误在当前部署中已被消除——证实红队所指的"方案错误"确实存在过，且已被修正。
- **红队断言**：[C4] 需 valkey（免费档无）→ 开不了；[C10] botdetection 段已移除、限流在 limiter.toml；[C11] x-captcha-validation 非法；limiter 键重复自相矛盾。
- **红队断言**：设为 POST 后 GET 被拒；[E2][E3] 实测当前 GET 可用、方案五用 GET，故设 POST 会使所有 GET 调用失败。
- 仓库 settings.yml line66-67 注释明确写明："只影响网页表单的提交方式；GET 查询请求照样可用（webapp.py 中 /search 路由 GET/POST 都接收）"。
- 输入 [E2] `GET /search?q=增值税小规模纳税人起征点&format=json` → 200 JSON（brave 返回中文结果）；[E3] `GET /search?q=爱因斯坦 相对论&format=json` → 200、34 条结果。两处均为**线上实例实测**，该实例即由本仓库部署（method:POST 生效中）。
- ⇒ 在 method:POST **已生效**的部署下，GET /search 仍然 200。
- **说明**：红队把 `server.method` 误当成"限制 /search 路由只收 POST"。SearXNG 的 `server.method` 仅决定 HTML 表单的提交方式，/search 路由本身 GET/POST 都接收（见仓库注释与 webapp 路由行为）。故红队"方案内部自相矛盾（3.2 写 POST、五写 GET）"的定性不成立——两者可共存，无需改回 GET。
- → 8 条字段名错误全部 **证实**：它们在豆包方案原文中确实存在，且仓库已逐条修正（修正方向与红队建议一致），证明红队技术判断正确。
- **`${SEARXNG_SECRET}` / `${SEARXNG_BASE_URL}` 插值 [C14]**：红队将此列陷阱并"推测"若 entrypoint 仍在做替换则安全。核对仓库 entrypoint.sh：line34 用 sed 按整行替换 `secret_key`；line40/42 替换或删除 `base_url`。**entrypoint 替换机制完好** → 该风险在当前仓库中**不成立（证伪"当前仓库存在此风险"）**。相反证据：entrypoint.sh line20-43 实际执行替换。注意：[C14] 的"核心事实（SearXNG 自身不插值）"仍真，只是本仓库因有 entrypoint 而化解。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
5. **JSON 接口鉴权（最高优先级未解项）[E7][C17]**
   - 动作：在反代层（Cloudflare Worker 或 Render 前置代理）对 `/search` 加 Basic Auth / token 校验；SearXNG 原生无 token，按 [C17] 必须在反代层实现，不改源码。
   - 通过标准：未带认证头的 `GET /search?q=测试&format=json` 返回 401/403；带正确头的返回 200。且直连 onrender.com 与经代理访问均受同一校验（杜绝[推测]的 origin 绕过）。
6. **弱化 / 降级 brave、duckduckgo [E3][E5]**
   - 动作：将 brave 默认 `disabled: true` 或进一步降权；duckduckgo 在高失败率下由接入方 Tavily 兜底（已有设计，[E8]/接入方结构）。
   - 通过标准：连续 5 次 `GET /search` 后，`unresponsive_engines` 中 brave/duckduckgo 超时率下降；或 brave 默认 disabled 时日志不再出现"请求过于频繁"。
7. **清理 `SEARXNG_LIMITER_ENABLED` 误用 [C5]**
   - 动作：确认部署文档/检查清单不再写 `SEARXNG_LIMITER_ENABLED=true`（该变量无效）。
   - 通过标准：仓库 README/检查步骤中无此变量；limiter 状态以 `server.limiter` + valkey 为准。

---

## 6、部署状态
- **红队断言**：[C9] 下划线 locale 被 preferences 校验拒绝 → 每请求 500、连 /healthz 都挂、Deploy failed。
- **核对**：输入第2节 3.3 原文确为 `default_locale: zh_CN`（下划线，line78）；[C9] 标注为"2026-10-22 真实踩坑"，属已核实官方事实。
- **结论：证实**。
- **补充**：仓库当前 settings.yml line78 已改为 `default_locale: zh-Hans-CN`（连字符），故该致命错误在当前部署中已被消除——证实红队所指的"方案错误"确实存在过，且已被修正。
