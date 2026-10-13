---
layout: default
title: 交接文档 · dsh-our-free-model → 本地 OpenAI 代理 实测接入指南（2026-10-12 实测版）
date: 2026-10-13 23:30:00 +0800
---

# dsh-our-free-model → 本地 OpenAI 代理 实测接入指南（2026-10-12 实测版）

- **日期**：2026-10-12
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-12-12-32-56\free-model-proxy\runbook.md

> 结论先行：**standalone 匿名免密免费通道已在本机跑通并验证可用，但它只暴露 25 个带 `-free` 的模型。
> 你最初要的 DeepSeek V4.1 Flash、Kimi K3 不在匿名免费通道（仅在需登录的 EAC 渠道），
> 所以"免登录免 key 免费用 deepseek/kimi"在当前版本不成立。**

## 一、实测核心结论
1. 免费机制：opencode.ai `Bearer public` 车道 + kilo.ai 公共网关（无 key）。**不是 DeepSeek 网页 Cookie**。
2. standalone（`packages/standalone`）自带 OpenAI 兼容本地代理：端口 18900(loopback)、零运行时依赖（**无需 npm install**）、自带自动生成 API Key。
3. **匿名免费通道只暴露带 `-free` 后缀或 kilo 免费池的模型（共 25 个）。** `catalog.js` 的 `isFreeLane` 规则：必须 `ALWAYS_FREE` 集合或 id 带 `-free`。`deepseek-v4.1-flash`/`kimi-k3` 不带 `-free`，被排除。
4. **deepseek/kimi 实测不可用（匿名）**：
   - opencode `Bearer public` 直连 → `401 Missing API key`
   - kilo 无 key 直连 → `401 PAID_MODEL_AUTH_REQUIRED: You need to sign in`
   - standalone 调 → `404 model not found`
   - 它们只在 **EAC 登录渠道**（`deepseek-ai/deepseek-v4.1-flash`、`moonshotai/kimi-k3`），需登录/账号/积分。
5. 区域限制：部分模型（如 `muse-spark-*`）在你网络下 `502 not available in your country`，其他可用。

## 二、本机已跑通的服务
- 启动（仓库根目录）：`node packages/standalone/cli.mjs`
- 端口：18900（仅绑定 127.0.0.1）
- API：`http://127.0.0.1:18900/v1`
- Key（`~/.our-free-model/settings.json` 的 `forwardKey`）：`ofm-t0WOIAyMfqGj8tBRVBajEvKM-d8Y4ATD`
- 管理页：`http://127.0.0.1:18900/#login=...`（用于登录 EAC 渠道）

## 三、WorkBuddy / AutoClaw 配置（匿名免费模型）
- 添加自定义模型 → 提供商：自定义
- Base URL：`http://127.0.0.1:18900/v1`
- API Key：`ofm-t0WOIAyMfqGj8tBRVBajEvKM-d8Y4ATD`
- 模型 ID：填下方**已验证可用**的免费模型之一
- 勾选：流式输出、工具调用

## 四、实测可用的匿名免费模型清单
**已 curl 实测返回正常内容（✅）**：
- `ling-3.1-flash-free` ✅（opencode 车道，实测返回 pong）
- `kilo-auto/free` ✅（kilo 免费路由，实测返回 pong）

**standalone `/v1/models` 暴露的全部 25 个匿名免费模型**（部分未逐个实测，个别可能有区域限制）：
- opencode 车道：ling-3.1-flash-free、mimo-v2.6-flash-free、muse-spark-1.2-contributor-free、muse-spark-1.3-contributor-free（⚠️你网络下 502 区域限制）、nemotron-3.5-lightning-free、jev-1.13-free、step-5-preview-free、longcat-2.5-preview-free、space-bunny-free、stepfun/step-5-preview-free
- kilo 车道：kilo-auto/free、inclusionai/ling-3.1-flash、poolside/laguna-s-2.1:free、nvidia/nemotron-3-ultra-550b-a55b:free、dots-studio/dots-3-note-preview:free、stealth/glyph-cluster

## 五、若坚持用 DeepSeek V4.1 Flash / Kimi K3（需登录 EAC 渠道）
**不满足"免登录免 key"，但能用**：
1. 浏览器打开管理页 `http://127.0.0.1:18900/#login=...`
2. 登录/绑定 EAC 账号（需要账号，可能需 GitHub star 等授权）
3. 之后 standalone 暴露 `deepseek-ai/deepseek-v4.1-flash` 和 `moonshotai/kimi-k3`
4. WB 模型 ID 填这两个（带 org 前缀的 EAC id）

## 六、风险
- 网关会话转发非官方 API，可能随时改版/限流/区域封锁。
- 匿名免费模型数量随上游变动；个别有区域限制。
- MIT 允许源码修改自用，但**禁止商用大规模调用**。
- kilo 免费池提示：免费模型的 prompt 可能被上游记录用于改进（README 免责声明）。

## 七、为什么用 standalone 而非手写代理
standalone 已正确实现 SSE 解析、工具指纹闸门（bash/glob/grep/read 四件套）、会话配额复用、多车道故障转移，比手写脚本稳得多。

## 八、WB 批量导入已执行（2026-10-12）
- 已生成独立导入文件：`free-model-proxy/wb-import.json`（24 条，纯 WB schema 数组）。
- 已追加进真实配置：`C:/Users/Administrator/.workbuddy/models.json`（追加前已备份为 `*.bak-OurFree-<时间戳>`，JSON 校验通过）。
- vendor 统一为 `OurFreeModel`，url=`http://127.0.0.1:18900/v1/`，apiKey=standalone 生成的 forwardKey。
- **已验证可用（text 对话）**：`ling-3.1-flash-free`（128k）、`kilo-auto/free`（256k）。
- **本网络区域被封**：`muse-spark-1.2/1.3-contributor-free`（502 not available in your country）。
- 其余 21 个未逐模型探，catalog 里存在即可路由；建议首次使用各发 1 条测试。
- ⚠️ 能力字段保守默认：`supportsToolCall/Images/Reasoning` 全为 false（未验证）。验证某模型支持后，把对应 flag 改 true 即可。
- ⚠️ **必须保持 standalone 服务在跑**（后台进程），WB 才能调到这些模型。服务断了 WB 会报连接错误。
