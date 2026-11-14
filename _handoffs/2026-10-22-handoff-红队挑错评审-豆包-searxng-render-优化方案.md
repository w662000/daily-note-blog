---
layout: default
title: 交接文档 · 红队挑错评审：豆包 SearXNG-Render 优化方案
date: 2026-11-14 23:30:00 +0800
---

# 红队挑错评审：豆包 SearXNG-Render 优化方案

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\旧团队产物备份_searxng评审\rev-r1\att_mvjr0p5y00elb\report.md

> 立场：怀疑。所有结论引用输入文件证据编号 [C*]/[E*]，无证据者标"推测"。
> 范围：只评豆包方案（第 2 节）与官方事实（第 3 节）、实测（第 4 节）的冲突，不评接入方代码。

---

## 一、致命级错误（会直接导致部署失败 / 服务不可用，必须改）

### 1. `ui.default_locale: zh_CN`（3.3）— 部署即崩 / 全站 500
[C9] 下划线写法（`zh_CN`）会被 preferences 校验拒绝，**每个请求返回 500，连 `/healthz` 都挂，Render 报 Deploy failed**。
这是整个方案里**最危险**的单点：3.3 把它写在"关闭不需要的功能"里，误以为是低风险调整，实际是直接触发部署失败。
合法值只有 `zh-HK` / `zh-Hans-CN` / `zh-Hant-TW`（连字符）。注意 `search.default_lang: zh-CN` 用下划线反而是对的（走另一套校验），两套不能混 [C9]。

### 2. `server.limiter: true` + limiter 块（3.2）— 启动崩溃 / 配置位置全错
- [C4] `server.limiter` 强依赖 **valkey 数据库**，Render 免费档没有 → 开启即启动失败。
- [C10] `botdetection:` 段**已从 settings.yml 移除**，限流配置应在 `/etc/searxng/limiter.toml`，写在 `server` 下无效。
- [C11] `x-captcha-validation` 不是合法配置项。
- 3.2 里 `limiter:` 作为键**出现两次**（先 `limiter: true` 后 `limiter: {limit:...}`），YAML 后值覆盖前值，结构自相矛盾。
结论：这条"限速调严"不仅调不了严，反而会因 limiter 无 valkey **把实例搞挂**。

### 3. `server.method: "POST"`（3.2）— 切断所有接入方，业务侧服务不可用
该字段本身是合法的（SearXNG `server.method`），但设为 `POST` 后 **GET 请求被拒**。
反证：[E2][E3] 实测证明当前用 `GET /search?...&format=json` 能 200 返回；方案五的 Python 示例也用 `requests.get`。两个 grounding 接入方（CF 版 `grounding.js`、本地版 `grounding.mjs`）均依赖 GET JSON 接口 [E2][E3][第5节]。
设成 POST 后，所有现有调用直接失败 → 对问答系统是**功能性不可用**。方案内部自相矛盾（3.2 写 POST，五写 GET）。

---

## 二、字段名错误（配置无效 / 被静默忽略，应改，不致命但误导）

| 方案写法 | 问题 | 证据 |
|---|---|---|
| `search.lang: zh-CN` (3.1) | 非合法字段，应为 `search.default_lang` | [C1] |
| `search.max_search_time: 6` (3.1) | 非合法字段，应为 `outgoing.request_timeout` / `outgoing.max_request_timeout` | [C2] |
| `search.max_results: 10` (3.1) | 不存在的字段，整条无效 | [C3] |
| `ui.infinite_scroll: false` (3.3) | 非合法字段，无限滚动是插件 `searx.plugins.infinite_scroll.SXNGPlugin` | [C8] |
| `ui.theme: simple` (3.3) | 非合法字段，应为 `ui.default_theme` | [C7] |
| `server.metrics: false` (3.3) | 非合法字段，应为 `general.enable_metrics` | [C6] |
| `botdetection:` 整段 (3.4) | 已从 settings.yml 移除，写了也无效 | [C10] |
| `x-captcha-validation: null` (3.4) | 非合法配置项 | [C11] |

说明：SearXNG 对未知键通常只警告不崩溃，所以这些大多"不致命"，但它们让方案作者误以为做了优化（如 max_results 限流、metrics 关闭），实际什么都没发生——属于"看起来合理其实无效"的典型陷阱。

---

## 三、环境变量 / 插值陷阱

- **步骤一.5 `SEARXNG_LIMITER_ENABLED=true`**：[C5] 该环境变量在 SearXNG 中**根本不存在**，设了无效。结合 [C4] 无 valkey，limiter 实际永远开不了。这条"立刻验证"是假动作。
- **`secret_key: "${SEARXNG_SECRET}"` / `base_url: "${SEARXNG_BASE_URL}"`（3.2）**：[C14] SearXNG 不支持环境变量插值，`${...}` 会变成字面量。
  - 缓解：**推测**——方案只改 settings.yml、未动 entrypoint，若仓库既有 `entrypoint.sh` 仍在做启动前替换（[C14] 提及"项目 entrypoint.sh"），则安全；若有人按方案字面推送纯 settings.yml，密钥会变成字面量 `"${SEARXNG_SECRET}"`（不触发 [C15] 的 ultrasecretkey 退出，但密钥错误），`base_url` 字面量会导致重定向/链接错误。需确认 entrypoint 替换机制未丢失。

---

## 四、对方案"必须做"的反证

- **一.5 验证限速 limiter 是否开启** → 反证 [C5][C4]：变量不存在 + 无 valkey，limiter 在 Render 免费档开不起来，"验证"无意义。
- **3.2 限速调严** → 反证 [C4][C10][C11]：配置位置已变（limiter.toml）、依赖 valkey、含非法键，整段要么无效要么崩。
- **"精简引擎，其余全部 disabled"** → 反证 [C19]：正确做法是 `use_default_settings.engines.keep_only` 白名单（未列入直接不加载，启动更快、内存更稳），逐引擎 `disabled` 既慢又易漏。
- **四.方案A"外界不能直接访问 onrender.com"** → 反证（**推测**）：Render 始终暴露 `*.onrender.com`，Cloudflare 代理不隐藏 origin，攻击者直连 onrender 域名即可绕过 Worker 的 Basic Auth。方案未阻断 origin 直连，鉴权可被绕过。[E7] 已证明当前裸奔，方案未补此洞。
- **四.方案B token 鉴权** → 与 [C17]（OSS 无 API token）一致，方向对；但方案称"不建议改源码"且 token 须在反代层做，却未给出反代实现，等于留空。

---

## 五、与线上实测证据的冲突（方案回避了真实问题）

- **保留 brave / duckduckgo**：[E5] brave 当日第 2 次查询即被限流（"请求过于频繁"），[E3] duckduckgo 持续超时。方案精简后仍保留这俩，在 AI 高频调用下必然不稳定，方案未正视也未加降级。
- **`site:` 运算符不可靠**：[E4] `site:gov.cn` 在 bing 长中文查询下返回完全无关的 A 股股评。[E4] 结论："任何依赖 `site:` 运算符的方案都不可靠"。方案七/八未涉及查询构造，接入方 CF 版改用 Tavily `include_domains` 是对的，但 SearXNG 侧没兜底。
- **冷启动超时**：方案五 Python 示例 `timeout=45`、重试 3 次、sleep 12，基本合理；但 3.2 的 `method: POST` 会让这个 GET 示例直接失败（见一.3），方案自相矛盾。

---

## 六、最危险的 3 个改动（按"把服务搞挂"的确定性排序）

1. **`ui.default_locale: zh_CN`** [C9] — 确定性最高：部署即 Deploy failed，全站 500，连 /healthz 都挂。条件是只要推送这条，100% 触发。
2. **`server.limiter: true`（无 valkey）+ limiter 块 / botdetection 段** [C4][C10][C11] — 启动崩溃或配置全无效；条件是 Render 免费档无 valkey，limiter 一开就崩。
3. **`server.method: "POST"`** [E2][E3][方案五] — 切断所有 GET 接入方，问答系统拿不到搜索结果，业务侧"服务不可用"；条件是接入方用 GET（已实测）。

---

## 七、如果只能做 3 件事

1. **删掉 `ui.default_locale: zh_CN`**，或改成 `zh-Hans-CN`（连字符）[C9]。这是救部署的第一刀。
2. **彻底移除 limiter 开启与 limiter 块、botdetection 整段**；Render 免费档无 valkey 就别开 limiter，真要限速改用 `limiter.toml` + valkey（免费档做不到则放弃）[C4][C10][C11]。
3. **批量修正非法字段名**并保 GET：`lang`→`default_lang`、`max_search_time`→`outgoing.request_timeout`、`max_results` 删除、`ui.theme`→`ui.default_theme`、`server.metrics`→`general.enable_metrics`、`infinite_scroll` 改插件声明；`server.method` 保持默认（GET）与接入方一致 [C1][C2][C3][C6][C7][C8][E2][E3]。并确认 entrypoint 仍做 `${}` 替换 [C14]。
