---
layout: default
title: 交接文档 · 本地 agent-teams 修复记录（2026-10-22）
date: 2026-10-23 23:30:00 +0800
---

# 本地 agent-teams 修复记录（2026-10-22）

- **日期**：2026-10-20
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-20-14-43-25\对比_20261022\本地agent-teams修复记录-20261022.md

对应前置排查报告：`对比报告_本地agent-teams_同类问题排查.md`（11 个问题）。
本轮按用户指令 **"1 2 3 4 全部修复，4 参考 CF 版接入 Tavily"** 全部落地，
另修正了排查阶段的一个事实错误（免费模型是 3 个不是 2 个，见文末）。

代码位置：`D:\workspace\workbuddyai\agent-teams\`

---

## 修复清单

### ① 数字锚点（`mcp/lib/anchors.mjs`，新建）

- 移植 CF 版 `numberAnchors()`：程序化抽取用户原话里的数字并换算绝对值
  （「10万」→ 100,000；「6000-7200元」→ 6,000 ~ 7,200 元），**带 ±12 字上下文**。
- 上下文是必需的：2026-10-22 实测（任务 20261022-BLILP）只给数字不给语境，
  模型把「每月租金收入 6000-7200 元」当成「每套每年的费用」，算出 3.3% 回报率。
- 上下文必须从**原始串**切（不能从被空格盖掉的 rest 切），否则出现
  "每年空置 ，还要扣" 这种空洞。
- 单测 `tests/anchors.test.mjs`：5 条，覆盖 10万→100,000、区间、亿、小数、
  空值、上下文无空洞、无重复。

### ② 用户原话进评审 + rubric 闭环破除（`quality.mjs`）

- `buildReviewTaskFile` 新增 `<original_question>` 块，位于**所有派生文本之前**
  （objective / acceptance / 产物之前）——派生文本与之冲突时派生文本错。
- `buildRubricFile` 新增 "Ground truth override" 段：**与 `<original_question>`
  数字/事实冲突的 acceptance 一律作废**——既不许当缺陷提，也不许拿来判分；
  照着用户原话做的生产环节是对的。
- 取值链 `team.goal ?? team.description ?? task.objective`
  （`agent_teams_create` 的 goal 实际落在 description，见 tools.mjs）。
- 这一修针对 20261022-YCJBE 的闭环机制：用户「10 万」被改成「10,000」，
  审核员因为 acceptance 与这个错误一致而判"符合要求"。

### ③ severity 分级门禁（`quality.mjs` + 两个 schema）

- 评审输出契约从 4 字段扩到 5 字段：
  `{"pass", "score", "reasons", "mustFix", "severity":"<致命|重要|提示|none>"}`。
- 派生逻辑：`pass=true` → pass；`pass=false` 且 severity=提示 → **note**
  （任务 done、verdict=note 留痕、不推进轮次、不消耗返工预算）；
  其余（致命/重要/漏给）→ needs_revision。**漏给 severity 按"重要"处理**，
  向后兼容旧评审器。
- `reviewDecision`：note → `action:'complete'`；
  `canDeclareDelivery`：`verdict='note'` 与 pass 一样放行
  （`schema/task.schema.json` 与 `schema/team-state.schema.json` 四个 enum 同步加 note）。
- 为什么值得做：一次返工 = 一次完整模型会话。二值门禁会把" intro 句子太啰嗦"
  这种提示级问题和"数字错 10 倍"同等对待，烧完预算后真正要命的工作反而被 escalate。

### ④ Tavily 外部核查（`mcp/lib/grounding.mjs`，新建）

- 移植 CF 版全部取舍：
  - **不让任何模型出裁决**：Tavily answer（由检索结果生成，不是模型记忆）作为
    检索事实，代码只做确定性数字核对（一致/未出现），真假判断交审核员；
  - 政策类声明**插队**进核查名额（`POLICY` 正则）——2 条名额会被
    "总投资 90 万元"占满，税率断言反而漏掉；
  - 政策类检索锁官方域名 `chinatax.gov.cn / mof.gov.cn / gov.cn` +
    "政策原文"前缀（两个动作都必要，少一个就被自媒体/导航页占位）；
  - **百分比严格核对**：同句里 8000 对上、20% 是错的，旧逻辑"任一命中即通过"
    会盖章放行；
  - 政策类在官方站点检索不到 → 显式记 `mismatch`，不静默丢弃。
- 本地适配：D1 `gquota` 表 → `stateDir/grounding-quota.json`（跨进程共享，
  记当日次数 + 熔断标记）；无 key / 超日限（默认 30 次/天）/ key 失效
  （401/429/432/433 当日熔断）/ 网络故障 → **全部静默降级**，门禁不依赖它。
- 检索原文 + 真实 URL 组成 `<external_evidence>` 块进评审 prompt，
  条目标注 `[MISMATCH]` / `[NO OFFICIAL SOURCE]`。
- 调用点：judge 模式与 pipeline 模式都接（`groundArtifact`），
  锚点块先从送检文本里剥掉（程序生成的「15万」→ 150,000 送检纯烧额度）。
- 单测 `tests/grounding.test.mjs`：14 条（插队/域名/百分比/熔断/日限/quota/降级）。

### 配置链路（`mcp-server.mjs` + `tools.mjs`）

- `loadConfig` 新增 4 个 key（`AGENT_TEAMS_TAVILY_API_KEY` 或裸 `TAVILY_API_KEY`、
  `AGENT_TEAMS_GROUNDING`、`AGENT_TEAMS_GROUNDING_DAILY_CAP`、
  `AGENT_TEAMS_GROUNDING_MAX_CLAIMS`），并按仓库既有教训同步进
  `startServer` 的 tools 白名单和 `qualityCfg()`——只加 loadConfig 不拷贝，
  env 开关会静默失效（`AGENT_TEAMS_CONTRACT_ENFORCE` 踩过的坑）。
- 新增零依赖 `.env` 加载（`loadDotEnv()`，仅 CLI 入口调用，已存在的环境变量优先），
  key 放在 `.env`（已加 `.gitignore`）；`--print-config` 对 key 脱敏。
- 启动日志打印 grounding 状态（配了 key 却静默不工作是最难发现的故障，
  CF 版吃过"跑 18 次零产出没人知道"的亏）。
- reviewHistory 新增 `severity` 与 `grounding` 两个留痕字段（schema 同步）。

---

## 验证

- **全量测试 459/459 通过**（新增 31 条：anchors 5 + grounding 14 + quality 12）。
- quality 新测试覆盖：锚点真进评审 prompt（`「10万」→ 100,000`）、
  rubric 作废规则、severity 三档行为（note 放行/致命返工/漏给按重要）、
  grounding 有 key 时证据块进 prompt 且发真请求（假 fetch，免联网）、
  无 key 时门禁照常。
- **真实 key live 验证**（用户提供，已写入 `.env`）：3 条政策声明全部检索到
  官方来源（mof.gov.cn / chinatax.gov.cn 各地方税局站点），
  「月租金 10 万以内免征增值税」与官方口径一致。

### 已知局限（照实记录）

1. **Tavily 回声**：声明本身是错误说法时，检索结果可能复述它，数字核对会判"对上"。
   live 验证第 3 条「个人出租住房综合所得税率 20%」就是这样被判 mismatch:false
   （真实综合税负是 3%，来源是一份马来西亚投资指南）。
   缓解：证据块把检索原文 + URL 全给审核员，代码不假装裁决。
2. **模型的中国税制知识不可靠**：CF 版三次答错三种错法，prompt 修不了根，
   本轮只是让错误**有机会**被外部证据拦住，不是保证。
3. pipeline 模式在本机依旧不可用（produce 步骤超 peer 600s 超时），
   本轮改动对它只是保持一致性，实际生效的是默认的 judge 模式。

---

## 附带修正：免费模型数量

排查报告里写的"只有 2 个免费模型"是照搬旧记忆、未验证的错误说法。
实测确认 **3 个、且分属三个家族**：`hy3`（腾讯混元）、
`step-5-preview`（阶跃星辰）、`deepseek-v4.1-flash`（DeepSeek），
满足用户"三角色不共模"的硬规则。CF 版那三个模型
（`custom-local:@cf/qwen/qwen3-30b-a3b-fp8` 等）在本地 CLI 不可用
（429 限流/无输出），不在此列。

## 清理

删除 3 个临时探针脚本：`tests/_probe_models.mjs`、`tests/_probe_models2.mjs`、
`tests/_probe_step5.mjs`。
