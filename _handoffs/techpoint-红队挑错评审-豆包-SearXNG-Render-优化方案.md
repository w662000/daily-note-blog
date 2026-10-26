---
layout: default
title: 技术点 · 红队挑错评审：豆包 SearXNG-Render 优化方案
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · 红队挑错评审：豆包 SearXNG-Render 优化方案

> 来源：261022_红队挑错评审：豆包 SearXNG-Render 优化方案_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- > 范围：只评豆包方案（第 2 节）与官方事实（第 3 节）、实测（第 4 节）的冲突，不评接入方代码。
- 这是整个方案里**最危险**的单点：3.3 把它写在"关闭不需要的功能"里，误以为是低风险调整，实际是直接触发部署失败。
- [C4] `server.limiter` 强依赖 **valkey 数据库**，Render 免费档没有 → 开启即启动失败。
- [C10] `botdetection:` 段**已从 settings.yml 移除**，限流配置应在 `/etc/searxng/limiter.toml`，写在 `server` 下无效。
- [C11] `x-captcha-validation` 不是合法配置项。
- 结论：这条"限速调严"不仅调不了严，反而会因 limiter 无 valkey **把实例搞挂**。
- 反证：[E2][E3] 实测证明当前用 `GET /search?...&format=json` 能 200 返回；方案五的 Python 示例也用 `requests.get`。两个 grounding 接入方（CF 版 `grounding.js`、本地版 `grounding.mjs`）均依赖 GET JSON 接口 [E2][E3][第5节]。
- 设成 POST 后，所有现有调用直接失败 → 对问答系统是**功能性不可用**。方案内部自相矛盾（3.2 写 POST，五写 GET）。
- | 方案写法 | 问题 | 证据 |
- | `x-captcha-validation: null` (3.4) | 非合法配置项 | [C11] |
- 说明：SearXNG 对未知键通常只警告不崩溃，所以这些大多"不致命"，但它们让方案作者误以为做了优化（如 max_results 限流、metrics 关闭），实际什么都没发生——属于"看起来合理其实无效"的典型陷阱。
- **步骤一.5 `SEARXNG_LIMITER_ENABLED=true`**：[C5] 该环境变量在 SearXNG 中**根本不存在**，设了无效。结合 [C4] 无 valkey，limiter 实际永远开不了。这条"立刻验证"是假动作。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
[C9] 下划线写法（`zh_CN`）会被 preferences 校验拒绝，**每个请求返回 500，连 `/healthz` 都挂，Render 报 Deploy failed**。
这是整个方案里**最危险**的单点：3.3 把它写在"关闭不需要的功能"里，误以为是低风险调整，实际是直接触发部署失败。
合法值只有 `zh-HK` / `zh-Hans-CN` / `zh-Hant-TW`（连字符）。注意 `search.default_lang: zh-CN` 用下划线反而是对的（走另一套校验），两套不能混 [C9]。
