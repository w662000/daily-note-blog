---
layout: default
title: 项目流 · 2026-11-14 · 主力模型能力分选型
date: 2026-11-14 23:30:00 +0800
---

# 项目流 · 2026-11-14 · 主力模型能力分选型（双雷达近 10 天）

> 数据源：本机 8848 测速雷达 + 8849 限速雷达（2026-11-05 ~ 11-14，57 轮 / 5,219 条 + 16 轮 / 18,645 次 15 连发，T0 实测）
> 能力分：本机《模型干活选型排行榜》2026-08-02 榜 A「得分」列（纯能力、不含速度，T2）；公开基准分：《综合分排行》2026-10-13（T1）
> 项目内容：CF 5 个 + NVIDIA NIM 4 个作免费主力，spark-x2.6 作主力，DeepSeek 官方收费模型作备用兜底；按能力分重排并出场景推荐

## 〇、结论先说

1. **按能力分（纯能力「得分」列）第一是 NIM 的 `nvidia/nemotron-3-ultra-550b-a55b`（84，同模型 OR 免费版给 78），CF 第一是 `@cf/google/gemma-4-26b-a4b-it`（80）**。这批免费模型几乎没有公开基准分，能力分全部来自本机 08-02 内部干活榜（T2）。
2. **能力分和"干活综合 A"排序差很多**：`@cf/nvidia/nemotron-3-120b-a12b` 能力 73 排第 4，但综合 A 只有 43.9（速度分 31.4 拖垮）；`@cf/qwen/qwen3-30b-a3b-fp8` 能力只有 63，综合 A 却有 62.4 排第二。**要能力还是要速度，得按场景分开挑，不能只看一列。**
3. **本次入选共 11 个模型**：CF 5 个 + NIM 4 个（免费主力 9 个）+ `spark-x2.6`（主力）+ `deepseek-flash`（收费兜底）。其中 `nemotron-3.5-lightning-30b-a3b`、`spark-x2.6`、`deepseek-flash` 无可查能力分，排在表尾，不编数字。
4. **CF 5 个现在还停测着**：11-14 被 `config.json` 的 `skip_models` 排除出雷达轮询（额度让给发布链）。要当主力得先放行重启，且 CF 免费模型窗口小，装不下 WB agent 会话。详见第五节。
5. **兜底换成收费的 `deepseek-flash` 是稳的**：T0 240/240 全成功、零 429、824ms；T1 公开基准分 62.7 是全场唯一能查到的官方基准。

## 一、口径说明（这次按哪个"能力分"排，为什么）

| 列名 | 定义 | 来源 | 可信度 |
|---|---|---|---|
| **能力分**（主排序键） | 08-02 干活榜榜 A 的「得分」列，**纯能力分，不含速度** | `model-speed-radar/模型干活选型排行榜.md` 第 43/44/49/52/57/59/62/67/76 行 | **T2**（本机内部推算，非官方基准） |
| 干活综合 A | 同榜「综合」列 = `0.7×速度分 + 0.3×得分`，**含 70% 速度** | 同上 | **T2** |
| T1 公开基准分 | OpenCompass 与 Vellum 原始分均值（0–100） | `model-speed-radar/综合分排行_2026-10-13.md` | **T1**（公开评测平台） |
| 近10天成功率 / 429率 / TTFT / 靠谱分 | 两个雷达 daemon 原始 jsonl 聚合 | `data/history.jsonl`、`~/.cache/rate-limit-radar/data/history.jsonl` | **T0**（本次实算） |
| 免费 / 收费 | 需求口径 + 本机配置与工作日志；`deepseek-flash` 的 url 为 `api.deepseek.com` | `~/.workbuddy/models.json`、`config.json`、11-13/11-14 工作日志 | T0/T1；**本机数据不含官方价格，不给任何金额** |

**为什么用纯能力得分排**：上一份表按"靠谱分"（可靠性 + 速度）排，本次要求按能力分换维度；「综合 A」里 70% 还是速度，排出来跟上一份高度重叠，等于没换。所以用不含速度的「得分」列做主排序，综合 A、T1、T0 可靠性并列展示做交叉验证。

**三处不确定，如实标出**：
- `nvidia/nemotron-3-ultra-550b-a55b` 在 08-02 榜里有两个不一致的分数：NIM 直连行「得分 84 / 综合 25.2」、OpenRouter 免费行「得分 78 / 综合 48.7」。表里写 `84 / 78`，按 84 排序；保守按 78 排它会掉到第 2。差异原因是当时 NIM 直连版 0% 可靠率（network 失败）把综合分压到 25.2，属旧数据，近 10 天已恢复到 72.08% 成功。
- `poolside/laguna-xs-2.1`、`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` 的能力分取自 08-02 榜里**同模型的 OpenRouter 免费版**行（榜里没有 NIM 直连同名行），属跨通道引用，标 `*`。
- `spark-x2.6` 在 10-13 报告里 `spark-x` 被列入「未取到公开分(主流类)」，08-02 榜也无 `spark-x2.6`；`nvidia/nemotron-3.5-lightning-30b-a3b` 同样无分。**三个无分模型不参与能力排序，一律填 `—`。**

## 二、主表 · 按能力分从高到低

| # | 模型 id | 平台 | 角色 | 能力分 T2 | 综合A T2 | T1 基准 | 近10天限速成功率 T0 | 429率 T0 | TTFT中位 T0 | 靠谱分 T0 | 费用 | 类型 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA NIM | 主力·免费 | **84** / 78 | 25.2 | — | 72.08% | 0.0% | 2085ms | 65.94 | 免费预览 | 推理 · 550B 旗舰 |
| 2 | `@cf/google/gemma-4-26b-a4b-it` | Cloudflare | 主力·免费 | **80** | 64.7 | — | 76.19% | 0.0% | 1473ms | 68.13 | 免费额度 | 多模态 · 通用 |
| 3 | `@cf/openai/gpt-oss-120b` | Cloudflare | 主力·免费 | **74** | 59.7 | — | 76.19% | 0.0% | 1398.0ms | 70.23 | 免费额度 | 推理 · 120B |
| 4 | `@cf/nvidia/nemotron-3-120b-a12b` | Cloudflare | 主力·免费 | **73** | 43.9 | — | 77.14% | 0.0% | 1567ms | 69.32 | 免费额度 | 推理 · 120B |
| 5 | `@cf/qwen/qwen3-30b-a3b-fp8` | Cloudflare | 主力·免费 | **63** | 62.4 | — | 77.62% | 0.0% | 1128.5ms | 71.31 | 免费额度 | 文本 · 轻快 |
| 6 | `@cf/qwen/qwq-32b` | Cloudflare | 主力·免费 | **62** | 54.8 | — | 77.62% | 0.0% | 1651.5ms | 67.45 | 免费额度 | 推理链 |
| 7 | `poolside/laguna-xs-2.1` | NVIDIA NIM | 主力·免费 | **57** | 52.3 | — | 75.0% | 0.0% | 680ms | 72.27 | 免费预览 | 代码向 |
| 8 | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | NVIDIA NIM | 主力·免费 | **47** | 51.1 | — | 81.25% | 0.0% | 697ms | 78.32 | 免费预览 | 全模态 · 推理 |
| 9 | `nvidia/nemotron-3.5-lightning-30b-a3b` | NVIDIA NIM | 主力·免费 | — | — | — | 81.25% | 0.0% | 725.0ms | 77.51 | 免费预览 | 文本 · 快档 |
| 10 | `spark-x2.6` | Xunfei | 主力（用户指定） | — | — | — | 98.33% | 0.0% | 3711ms | 78.13 | 按平台政策 | 文本 · 推理 |
| 11 | `deepseek-flash` | DeepSeek | 备用兜底·收费 | — | — | 62.7 | 100.0% | 0.0% | 824ms | 91.76 | 官方计费 | 文本 · 推理 |

> `能力分 84 / 78` = NIM 直连行 / OpenRouter 免费行两个不一致的评分，按 84 排序。带跨通道引用的分数见表后第 3 条说明。
> 「靠谱分」是上一份报告的可靠性+速度综合分，这里只作对照，**本次不按它排**。
> 无能力分的 3 个模型按指定席位保留在表尾：`nvidia/nemotron-3.5-lightning-30b-a3b`（T0 零限流、725ms）、`spark-x2.6`（T0 98.33% 成功）、`deepseek-flash`（T1 62.7、T0 240/240 全成功）。

### 2.1 逐条关键说明

1. `nvidia/nemotron-3-ultra-550b-a55b`（NVIDIA NIM，能力分 **84** / 78）：⚠️ 同模型两个通道评分不一致：NIM 直连行得分84、OpenRouter 免费行78；08-02 直连版当时 0% 可靠率(network失败)故综合A仅25.2，近10天实测已恢复到 72.08% 成功、零 429。
2. `@cf/google/gemma-4-26b-a4b-it`（Cloudflare，能力分 **80**）：CF 阵营能力分第一；08-02 榜标多模态。近10天零 429。
3. `@cf/openai/gpt-oss-120b`（Cloudflare，能力分 **74**）：推理系大身位，适合复杂推理；TTFT 1398ms。
4. `@cf/nvidia/nemotron-3-120b-a12b`（Cloudflare，能力分 **73**）：能力分第4但综合A只有43.9——速度分仅31.4（TTFT 1567ms）被拖垮，典型的「强但慢」。
5. `@cf/qwen/qwen3-30b-a3b-fp8`（Cloudflare，能力分 **63**）：综合A 62.4 是全部入选模型里第二高；CF 里最快（1128.5ms），限速成功率 77.62% 并列最高。
6. `@cf/qwen/qwq-32b`（Cloudflare，能力分 **62**）：显式推理过程，适合数学/逻辑；TTFT 1651.5ms 偏慢。
7. `poolside/laguna-xs-2.1`（NVIDIA NIM，能力分 **57**）：能力分取自同模型的 OpenRouter 免费版（榜里无 NIM 直连同名行），属跨通道引用；TTFT 680ms 很快。
8. `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`（NVIDIA NIM，能力分 **47**）：能力分取自同模型的 OpenRouter 免费版（跨通道引用）；近10天 81.25% 成功、TTFT 697ms，是 NIM 里最均衡的。
9. `nvidia/nemotron-3.5-lightning-30b-a3b`（NVIDIA NIM，能力分 —）：无可查能力分，按 T0 实测入选：81.25% 成功、零 429、TTFT 725ms。不要拿它跟有分模型比能力。
10. `spark-x2.6`（Xunfei，能力分 —）：⚠️ 无任何能力分；入选依据是 T0 可靠性 98.33% 成功、零 429、测速 89.47%。但 TTFT 3711ms 全场最慢，只适合不赶时间的任务。
11. `deepseek-flash`（DeepSeek，能力分 —）：⚠️ 活清单无 deepseek-4.1-flash；按 [DeepSeek] DeepSeek-V4-Flash（api.deepseek.com 官方计费）处理。T1 62.7 来自 10-13 公开基准。T0：240/240 全成功、零 429、824ms，是兜底最硬的一个。

### 2.2 如果按「干活综合 A」排（含 70% 速度），次序会变成

1.`@cf/google/gemma-4-26b-a4b-it` 64.7 | 2.`@cf/qwen/qwen3-30b-a3b-fp8` 62.4 | 3.`@cf/openai/gpt-oss-120b` 59.7 | 4.`@cf/qwen/qwq-32b` 54.8 | 5.`poolside/laguna-xs-2.1` 52.3 | 6.`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` 51.1 | 7.`@cf/nvidia/nemotron-3-120b-a12b` 43.9 | 8.`nvidia/nemotron-3-ultra-550b-a55b` 25.2

对照可见：`gemma-4-26b` 稳居第一；`qwen3-30b` 从能力第 5 升到综合第 2；`nemotron-3-120b` 从能力第 4 掉到综合第 8；`ultra-550b` 用 OR 免费版 48.7 排第 7、用 NIM 直连版 25.2 垫底。**所以"按能力分"和"按干活速度综合"是两套结论，别混着用。**

## 三、按场景推荐（严格只用本次入选的 11 个模型）

| 场景 | 首选 | 次选 | 兜底 | 理由 |
|---|---|---|---|---|
| **日常对话 / 大批量免费跑** | `@cf/google/gemma-4-26b-a4b-it` | `@cf/qwen/qwen3-30b-a3b-fp8` | `deepseek-flash` | 能力分 80 最高、CF 零 429；次选综合A 62.4 且 TTFT 1128.5ms 最快。免费主力挂了才切收费兜底。 |
| **复杂推理 / 长链思考** | `nvidia/nemotron-3-ultra-550b-a55b` | `@cf/openai/gpt-oss-120b` / `@cf/qwen/qwq-32b` | `deepseek-flash` | 550B 旗舰能力分 84；gpt-oss-120b 74、qwq-32b 带显式推理链。注意 ultra-550b 的 84 分与 OR 免费版 78 分不一致。 |
| **看图 / 多模态** | `@cf/google/gemma-4-26b-a4b-it` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | `deepseek-flash`（不支持图像，仅文本兜底） | gemma-4-26b 是入选里唯一 08-02 榜明确标「多模态」的 CF 模型；nano-omni 是全模态+推理。 |
| **代码 / 工程任务** | `poolside/laguna-xs-2.1` | `@cf/qwen/qwen3-30b-a3b-fp8` | `deepseek-flash` | Poolside 是代码向模型，TTFT 680ms；能力分 57 是跨通道引用值，别当精确基准。 |
| **快问快答 / 低延迟** | `nvidia/nemotron-3.5-lightning-30b-a3b` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` / `poolside/laguna-xs-2.1` | `deepseek-flash` | 三者 TTFT 分别 725 / 697 / 680ms，是入选里最快的一档；lightning 无能力分，按速度入选。 |
| **不许失败 / 高可靠批量** | `spark-x2.6` | `@cf/qwen/qwen3-30b-a3b-fp8` | `deepseek-flash` | spark-x2.6 限速 98.33% 成功、零 429、测速 89.47%，是免费/指定席位里最稳的，代价是 3711ms 慢。 |
| **免费额度耗尽 / 主力集体失效** | `deepseek-flash` | — | — | 唯一的收费兜底：240/240 全成功、零 429、TTFT 824ms、T1 基准分 62.7。平时不用，出事才切。 |
| **专用任务（非主力，按需调用）** | `nvidia/riva-translate-4b-instruct-v2`（翻译） | `nvidia/nemotron-parse-2.0`（文档解析）/ `nvidia/llama-3.1-nemotron-safety-guard-8b-v3`（内容审查） | — | 这 3 个 NIM 模型近10天零 429、TTFT 658–907ms、靠谱分 66–79，但都是专用模型，不进主力表。 |

### 3.1 组合建议（免费优先、收费只兜底）

```
主链路（免费）：gemma-4-26b 〔通用/看图〕 + qwen3-30b 〔快答〕 + gpt-oss-120b 〔推理〕
           └ 需要 550B 重推理时切 nemotron-3-ultra-550b；代码任务切 laguna-xs-2.1
高可靠批处理（慢但稳）：spark-x2.6  〔98.33% 成功、零 429，3711ms〕
兜底（收费，平时不用）：deepseek-flash 〔240/240 全成功、824ms、T1 62.7〕
触发条件：CF/NIM 免费额度耗尽、两家平台同时不可用、或连续 2 次调用失败
```

## 四、名单里两个 id 的核实结果（不瞎猜）

| 需求中的模型名 | 活清单实际情况 | 本次处理 |
|---|---|---|
| 「deepseek 的收费模型 deepseek 4.1 flash」 | `models.json`（94 条）里**没有** `deepseek-4.1-flash`。DeepSeek 官方只有 `deepseek-v4-pro`、`deepseek-flash`（= `[DeepSeek] DeepSeek-V4-Flash`），两者 url 都是 `api.deepseek.com`。10-13 报告第 19 行出现过别名 `DeepSeek-V4.1-Flash[Loomy]`，但该条目当前已不在活清单。 | **`deepseek-flash`**（官方计费），T1 62.7 |
| 「spark-x2.6 作为主力」 | 活清单里有 `spark-x2.6` = `[xf] spark-x2.6`，vendor `Xunfei`，`maxTokens` 未填。10-13 报告把 `spark-x` 列入「未取到公开分」，08-02 榜无 `spark-x2.6` → **无能力分**。 | 按 T0 可靠性入选，能力分填 `—` |

> 若 4.1 flash 指另一条目（如 Loomy 中转），需按实际 id 重新核对；本次不推断活清单外的模型。

## 五、部署前必须做的 3 件事（不做就用不起来）

**① 把 CF 5 个从 `skip_models` 里放出来，否则雷达根本不监控它们**

`model-speed-radar/config.json` 第 35–53 行的 `skip_models` 含这 5 个：
```
    "@cf/google/gemma-4-26b-a4b-it",
    "@cf/qwen/qwen3-30b-a3b-fp8",
    "@cf/qwen/qwq-32b",
    "@cf/nvidia/nemotron-3-120b-a12b",
    "@cf/openai/gpt-oss-120b",
```
配置第 55 行注释 `_comment_cf_skip` 原文：「2026-11-14 用户指令：@cf 系列排除出雷达轮询，额度让给发布链（直连生成+雷达互抢免费额度）」。
要重新启用：编辑 `config.json` 删掉这 5 行 → 重启 8848/8849 两个 daemon（`stop.bat` 然后 `start.bat`）→ 等一轮确认 5 个模型重新出现在 `latest.json`。
⚠️ **副作用**：重新启用会跟发布链抢 CF 免费额度，这正是当初停测的原因；如果发布链还在跑直连生成，建议先只放 2–3 个 CF 模型试水。

**② CF 免费模型上下文窗口装不下 WB agent 会话**

11-13 工作日志（T1）实测：CF 探针显示 WB agent 会话体积约 53,974 token，而 `qwen3-30b` 窗口 32,768、`qwq-32b` 仅 24,000 → 物理装不下，这也是当晚判定「CF 方案死刑」的原因。`models.json` 里所有条目的 `maxTokens` 统一填 16384，那是**输出上限配置值，不是上下文窗口**，别拿它当窗口用。
结论：CF 这 5 个适合**短请求 / 独立任务 / 脚本直连**，不适合塞进 WB agent 会话当主模型。需要长上下文就用 `deepseek-flash`（收费）或 NIM 里窗口更大的模型（需另行核实窗口，本机无此数据）。

**③ NIM 预览模型容易下架，要定期核对 id**

近 10 天 NIM 平台有 **180 个 `untestable` 轮次、219 次 `model_gone`**，26 个模型里一半是死的。当主力前建议每周核一次 `models.json` 里的 id 是否仍返回 200；`nvidia/nemotron-3.5-lightning-30b-a3b` 这类新模型尤其容易换名。

## 六、数据质量与局限

| 项 | 结果 |
|---|---|
| 数字一致性 | ✅ 能力分逐条核对 08-02 榜原始行（43/44/49/52/57/59/62/67/76 行）；T0 可靠性逐条取自上一轮已校验的聚合 JSON（`Σok+Σ429+Σother=18,645` 成立） |
| 未编造 | ✅ 3 个无能力分模型一律填 `—`；跨通道引用值标 `*`；同模型双分数冲突如实并列 |
| 可信度 | 能力分 / 综合A = **T2**（08-02 内部推算，非官方）；T1 基准分 = **T1**；成功率/429率/TTFT = **T0**；费用 = 需求口径 + 本机配置，无价格数字 |
| 时间性 | ⚠️ 能力分是 2026-08-02 的历史值，距今 3 个多月，期间模型可能已更新；可靠性是近 10 天 T0 实测 |
| 探针局限 | ⚠️ 两个雷达都是 64-token 短请求（「用一句话介绍北京」/「回复两个字：正常」），能力分不能代表长上下文、工具密集、多轮真实负载 |
| 窗口数据 | ⚠️ 本机没有各模型的上下文窗口实测值，仅 11-13 日志记了 CF 两个模型的窗口，其余不推断 |
| 免费额度 | ⚠️ 本机数据不含任何官方额度/价格数字，"免费"按需求口径与配置注释记录，以平台官方为准 |

## 七、交付物

| 产物 | 说明 |
|---|---|
| 完整报告（Markdown） | 口径、主表、场景推荐、部署步骤、可信度与局限 |
| 模型明细 CSV | 11 行 × 21 列，含能力分来源与 T0 可靠性 |
| 交互式看板 HTML | 零外部依赖、可离线打开，支持按平台 / 角色 / 有无能力分筛选与表头排序 |
| 看板预览图 | 浏览器实测截图 |
| 可复现脚本 | 聚合脚本 + 渲染脚本（纯本地只读，不发 API 请求） |

> 本文所有成功率、429 率、TTFT、样本量均为本机两个雷达 daemon 原始落盘数据的 T0 实算；能力分为 2026-08-02 内部干活榜 T2 推算值；公开基准分为 10-13 整理的 T1 值。无数据处一律标「—」，未编造数字。
