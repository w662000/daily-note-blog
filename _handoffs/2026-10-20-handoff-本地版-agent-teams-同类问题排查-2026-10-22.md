---
layout: default
title: 交接文档 · 本地版 agent-teams 同类问题排查 · 2026-10-22
date: 2026-10-23 23:30:00 +0800
---

# 本地版 agent-teams 同类问题排查 · 2026-10-22

- **日期**：2026-10-20
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-20-14-43-25\对比_20261022\对比报告_本地agent-teams_同类问题排查.md

> 排查对象：`D:\workspace\workbuddyai\agent-teams\`（本地多 agent 协作系统）
> 对照基准：CF 多 agent 问答系统刚修完的 8 项结构性问题 + 3 项未解决的根本问题
> 排查方法：读源码 + 定位每个问题在本地是否有对应机制，不跑实测（本地可用模型不足，见第 4 节）

---

## 结论先说

**本地版不是"没这些问题"，而是"问题类型不同"——CF 的 11 个问题里，有 6 个在本地版**连对应机制都不存在**，剩下 5 个原样存在，其中 3 个比 CF 更糟。**

更要紧的一点：**本地版是工程交付编排系统，不是问答事实核查系统。** 拿它答「0.75% 公式」这类题，工具从一开始就不匹配。

---

## 一、11 个问题逐条对照

| # | CF 版的问题 | 本地版 | 判定 |
|---|---|---|---|
| 1 | 「10万」被写成「10,000」（差 10 倍） | 没有 `numberAnchors` 这类机制，用户数字直接进 task body | ❌ **同样有，且更没有防线** |
| 2 | 汇总把用户正确的「10万」判成"笔误" | judge 按 rubric 判，而 rubric 由队长写的 `task.acceptance` 生成 | ❌ **同样有**，且错误源头更集中 |
| 3 | 审核只审来源，不复算数字 | judge 审的是「产物是否满足验收标准」，**不查事实真伪** | ⚠️ **性质不同**：压根不审事实 |
| 4 | 鸡毛蒜皮也触发返工 | `pass` / `needs_revision` 二值，**没有 severity** | ❌ **更糟**：连分级都没有 |
| 5 | 核查名额被无害算术句占满 | 没有核查环节 | ➖ 不适用 |
| 6 | 政策检索被自媒体/回声污染 | **完全不检索** | ➖ 不适用，但**后果更糟** |
| 7 | 百分比核对宽松 | 没有数字核对 | ➖ 不适用 |
| 8 | 锚点无语境导致角色错配 | 没有锚点 | ➖ 不适用 |
| 9 | 模型的中国税制知识本身错误 | 同样只有模型知识，且**无法外部纠错** | ❌ **更糟** |
| 10 | 审核员与生产者有同样知识盲区 | judge 和 producer 都从 `codebuddy` CLI 出来，同账号同免费模型池 | ❌ **同样有** |
| 11 | 产权年限（70 年 vs 40 年）没人提 | 没有任何机制强制检查关键变量 | ❌ **同样有** |

---

## 二、逐条说明

### 问题 1：单位换算 —— 本地版零防线

CF 版至少有 `numberAnchors()` 把「10万」程序化换算成 100,000 再喂给模型。

本地版的链路是：

```
队长建 task（数字由模型手写进 acceptance/body）
  → codebuddy --print 成员执行
  → judge 审产物
```

**整条链上没有一次程序化的数字校验。**「6 套 × 15 万 = 90 万」这种换算完全靠模型自己做，和 CF 版修复前的处境一样——但 CF 版修了，本地版没有对应代码可修。

### 问题 2：rubric 的错误会被放大

`buildRubricFile()`（quality.mjs:756）生成的 rubric 来自：

```js
const acceptance = task.acceptance ?? [];
parts.push('## Acceptance criteria');
parts.push(acceptance.length ? acceptance.map(...) : '1. The artifact satisfies the stated objective.');
```

而 `task.acceptance` 是**队长（也是模型）写的**。

这形成一个危险的闭环：

> 队长把「月租 10 万免增值税」写成「10,000」→ 写进 acceptance → 成员照着错的验收标准做 → judge 也照着错的 rubric 判 → **三方一致地错，而且看起来"通过"了**。

CF 版至少还有一层：`compose` 不允许把用户数字判成"笔误"，且审核员能看到 `<anchors>`。本地版的 judge prompt 只给它 rubric 和 artifact，**根本看不到用户原话**——它连"队长篡改了用户数字"这件事都无从发现。

### 问题 3：judge 不审事实

`buildJudgePrompt()`（quality.mjs:801）说的是：

```
You are a strict reviewer. Judge the LATEST artifact below against the rubric.
Judge the artifact the producer actually wrote — do NOT rewrite it, do NOT run commands.
{"pass": <boolean>, "score": <0-10>, "reasons": [...], "mustFix": [...]}
"pass" is true only if EVERY acceptance criterion is met.
```

注意最后一句：**判过的标准是"acceptance criterion 是否满足"，不是"内容是否属实"。**

所以 judge 能抓"代码没实现需求"，抓不了"个税税率写错了"。本地版的 quality 门禁（`canDeclareDelivery`、路径审计、artifact digest）**全是工程指标**——git diff 是否越界、产物是否齐、staging 是否已批——没有一项是事实指标。

### 问题 4：二值审核，没有 severity

```js
export const REVIEW_STATUSES = ['pass', 'needs_revision', 'unavailable', 'error', 'disabled'];
```

```js
if (review.status === 'pass') return { action: 'complete', ... };
// needs_revision
if (repairs >= policy.maxRepairAttempts) return { action: 'escalate', ... };
if (round >= maxRounds) return { action: 'escalate', ... };
return { action: 'repair', ... };
```

**CF 版的问题（鸡毛蒜皮也返工）在本地版更严重**：CF 至少有 severity 分级可以只返工"致命/重要"，本地版是二值——judge 说 needs_revision 就返工，没有"提示"档。

护栏只有预算：
```js
codeMaxRounds: 3,
maxRepairAttempts: 2,
requirementsMaxRounds: 4,
```

也就是说最多烧 3 轮 + 2 次 repair。CF 版同样的上限，但多了"提示不返工"这一层过滤。

### 问题 6：没有外部检索 —— 这一条最致命

我在整个 `agent-teams` 目录 grep `tavily|Tavily|web_search|webSearch|联网|检索`，**零命中**。

这意味着：

> CF 版至少能把「月租金收入 10 万元以内免征增值税」送到财政部 PDF 和税务总局解读面前——即使被 Tavily 回声污染，**它见过正确答案**。
> 本地版从头到尾只有模型自己的记忆。

CF 版的 Tavily 回声效应确实是个 bug，但那个 bug 的前提是"有检索能力"。本地版连这个前提都没有。

### 问题 9 & 10：知识盲区 + 异构性不足

```js
export const BUILTIN_FREE_MODELS = ['deepseek-v4.1-flash', 'step-5-preview', 'hy3'];
```

`buildModelPlan()` 里已经有正确的规则：

> 「不要为了凑人数重复用同一个模型，也不要用任何未列入 freeModels 的 id」

但同文件里：

```js
const degraded = usable.length < 3;
```

实测这台机器上（2026-10-22 记录）：
- `deepseek-v4.1-flash` ✅
- `hy3` ✅
- `glm-4-flash-250414` ❌ 跑 7 分钟无产物
- `qwen3.7-flash:free` ❌ 429 限流
- `step-5-preview` 未验证

`usable.length < 3` → **degraded 模式**，只能建 1-2 个成员。这正是用户明确反对的情况——「三个角色共用一个模型，容易形成共识」。CF 版用的是 Cloudflare Workers AI 的三个异构模型（qwen3-30b / gpt-oss-120b / gemma-4-26b），模型层面是真异构；本地版在免费账号下凑不齐。

**judge 与 producer 同源**：`producer = cfg.reviewProducer ?? 'codebuddy'`，judge peer 也从同一批免费模型里挑。所以本地版的"交叉审核"比 CF 版更弱——CF 版审核员至少是 gemma，跟队员1 的 gpt-oss 不同家族。

---

## 三、三个更深层的差异

### 差异 1：本地版没有"协作记录"那层透明

CF 版把每个成员的原话（plan / extract / critique / evidence）原样拼进答案，不经过模型的手。所以用户能亲眼看到"队员2 只审了 1 条"、"Tavily 把 8% 标成了无来源"。

本地版的产物是文件和 exit-report，审核结论只留 `pass/needs_revision` + `reasons`。**过程不透明，错了更难发现。**

### 差异 2：本地版的"验收"是队长自定的

CF 版的 extract prompt 里有硬性的数据红线（T0/T1 来源、不许虚构、分税种、禁止断言政策不存在），这些是**系统级**约束，不随题目变化。

本地版的 acceptance criteria 是**每个 task 自己写的**，队长想写多松就多松。没有系统级的"不许改用户数字""政策必须给条款号"这类红线。

### 差异 3：本地版的能力边界是"能不能跑完"

`reviewDecision` 的 escalate 条件是：

```js
if (repairs >= policy.maxRepairAttempts) return { action: 'escalate', reason: 'repair attempts exhausted' };
if (round >= maxRounds) return { action: 'escalate', reason: 'review rounds exhausted' };
```

**escalate 的原因是"轮次用完了"，不是"发现致命错误"。** CF 版的门禁横幅至少会说「1 项致命问题经 2 轮返工仍存在」，本地版的 escalate 只说"repair attempts exhausted"——**用户看不出到底是内容有问题还是流程跑不动**。

---

## 四、本地版在"答题"上的实际表现

2026-10-22 早先那次对比里（`对比报告_本地vs云端.md`），本地版得分 ≈72，云端 ≈53。当时的结论是本地版更好。

**但那轮对比的题目是"如何找到一个城市里租金回报率高的房子，给出 3 个可行方案"——方案题，不是事实核查题。** 方案题上，本地版的工程化流程（选/买/装/租/管/停 六字诀）确实比 CF 版的四节结构更可执行。

换成这道税制题，结论会反过来：

| 题目类型 | CF 版 | 本地版 |
|---|---|---|
| 方案/流程题（不需要精确外部事实） | 四节结构，偏泛 | 工程化步骤，可执行性更强 |
| 事实核查题（税率、门槛、条款） | 有检索能力（虽然被回声污染），**能给出财政部原文链接** | **完全没有检索**，纯模型记忆 |
| 需要复算的数字题 | 有锚点 + 数字复算维度 + 百分比核对 | 零校验 |

**本地版赢在流程编排，CF 版赢在事实可达性。** 这是两个系统设计目标的差异，不是实现质量的差异。

---

## 五、建议

### 如果继续用本地版答题

按性价比排序：

1. **补一个数字锚点模块**（照抄 CF 的 `numberAnchors()`）。纯函数、零依赖、60 行，直接修掉"10万→10,000"整类错误。这是唯一一个"低成本高确定性收益"的修复。
2. **judge prompt 里注入用户原话**。现在 judge 看不到 `<q>`，所以无法发现"队长篡改了用户数字"。加一个 `<original_question>` 块，rubric 里明确写"与用户原话中的数字冲突的 acceptance 一律作废"。
3. **给 REVIEW_STATUSES 加 severity**。至少 `pass / needs_revision / note` 三档，`note` 只记录不返工。现在二值，返工成本无法控制。
4. **给成员加一个外部检索工具**。这是最大的短板，但要先解决账号和模型可用性——不然加了工具也没模型能稳定调用。

### 如果不改本地版

**别用它答需要精确政策/税制/条款的题。** 它会给你一个结构漂亮、步骤清晰、但税率全错的答案——而且看起来是"通过验收"的。这类题目前只有联网核实政策原文一条路（也就是我刚写的那份 `0.75%公式复核-15万公寓实测算账.md` 的做法）。

---

## 六、一句话总结

> **CF 版修完的是"逻辑类错误"（数字篡改、单位换算、把用户正确数据判成错误）；本地版连这些逻辑防线都没有。**
> 反过来，CF 版修不了"知识类错误"（税制记错），本地版更修不了——因为它连检索能力都没有。
> 两个系统各缺一半，而缺的那一半恰好互补。

---

*排查：2026-10-22 20:55 · 依据源码 `mcp/lib/quality.mjs`（50KB）、`mcp/lib/member-models.mjs`、`mcp/lib/constants.mjs`，未跑实测*
