---
layout: default
title: 交接文档 · Q6 核对报告：Render 三个数字 + Workers 额度单位
date: 2026-11-14 23:30:00 +0800
---

# Q6 核对报告：Render 三个数字 + Workers 额度单位

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\Q6_核对报告_20261023.md

## ⚠️ 共享模型限制声明

核对对象 Q6 调研稿**由我（deepseek-v4.1-flash）自己撰写**。核对者与调研员同模型、同知识盲区、同检索偏好，**这不构成模型级交叉验证**。故本报告不采用「再读一遍确认没错」的做法，改为对手视角：把官方原句**逐字抄出**，与稿中转述**逐字对比**找失真。凡未取到官方原文的，一律标「未核实」，不因「我自己写过」而默认成立。

核对日期 2026-10-23｜`agent_teams_web_search` 共 4 次。

---

## 一、512MB / 0.1 CPU —— **对，无失真**

官方原句：
> "Memory allocation: **512MB RAM** for web services / CPU allocation: **0.1 CPU**"
> — https://render.com/articles/from-side-project-to-production-scaling-your-first-app

稿中：「512MB RAM，同时只有 0.1 CPU」「512MB 是上限，CPU 只有 0.1 核」。数字、单位、并列关系一致。稿中「CPU 才是瓶颈」为主观判断，已用「补充」标注，未冒充官方。

---

## 二、15 分钟休眠 / 冷启动 1 分钟 —— **部分对**

官方原句：
> "Free web services **spin down after 15 minutes of inactivity** and restart on the next request…"
> — https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026
> "…spin down after **15 minutes of inactivity**… **Cold start occurs when spinning up from idle state**, taking about **one minute**…"
> — 同第一节链接

结论：15 分钟、约 1 分钟 **对**；官方触发词确为 **inactivity**。
但稿中写「官方口径是 inactivity / 无入站流量，**不是 idle**」有两处瑕疵：
1. 「无入站流量」是第三方（codecapsules、temps）措辞，被并入「官方口径」标签；
2. **"idle" 确实出现在同篇官方文章**（"spinning up from idle state"），只是描述冷启动起点，不是触发条件。→ 「不是 idle」切过头。

---

## 三、750 实例小时 —— **每 workspace 共享，非每服务｜对**

决定性官方原句（文档页）：
> "Render grants **750 Free instance hours to each workspace per calendar month**"
> — https://render.com/docs/free

第二处独立佐证：
> "**Each workspace gets 750 Free instance hours per calendar month.**"
> — https://render.com/articles/how-much-does-cloud-application-hosting-cost-for-small-businesses

博客佐证「池化」：
> "gives every user **750 hours of compute time every month** to run **as many free services as you'd like**"
> — https://render.com/blog/free-tier

稿中转述「每 workspace 每月 750 实例小时，所有免费服务共享，不是每个服务各 750」——与原文一致，**未失真**；把用户「账号」纠正为「workspace」方向正确。

需补标注：稿中「750÷730≈1.03，只够一个服务常驻」是**算术推算**（休眠不计费），官方未如此表述，应标「推算」。

---

## 四、100,000 req/day 与 10,000 Neurons/day —— **两套东西，未混用｜对**

> "Accounts on the Workers Free plan have a **daily request limit of 100,000 requests**, resetting at **midnight UTC**… returns **Error 1027**."
> — https://developers.cloudflare.com/workers/platform/limits
> Pricing：`Requests | **100,000 / day**`；`Duration | **13,000 GB-s / day**`
> — https://developers.cloudflare.com/workers/platform/pricing
> "Our free allocation allows anyone to use a total of **10,000 Neurons per day** at no charge."
> — https://developers.cloudflare.com/workers-ai/platform/pricing

稿中把两者分列单位对照表不同行，并显式写「数量级差 10 倍、单位不同」→ **未混用**，UTC 重置与 Error 1027 亦吻合。

**未核实**：稿中「每次调用 10ms CPU」——本次 4 次检索未取到官方原文（唯一提及者为第三方 buildoto），应标未核实。

---

## 五、链接审计：第三方是否冒充官方

| 链接 | 归属 | 稿中标注 | 结果 |
|---|---|---|---|
| render.com/docs/free、blog/free-tier、两篇 articles | 官方 | 官方 | ✅ |
| CF workers limits / pricing / workers-ai pricing | 官方 | 官方 | ✅ |
| livemy / codecapsules / srvrlss / buildoto | 第三方 | 「第三方印证」 | ✅ 未冒充 |

**未发现第三方当官方**。唯一瑕疵是第二节把第三方措辞并入「官方口径」标签。

---

## 六、总判定

| # | 项目 | 判定 | 问题 |
|---|---|---|---|
| 1 | 512MB / 0.1 CPU | **对** | 无 |
| 2 | 15 分钟 inactivity / 冷启动 1 分钟 | **部分对** | 「不是 idle」过正；第三方措辞混入官方标签 |
| 3 | 750 小时 = 每 workspace 共享 | **对（已由官方文档原句确认）** | 「只够一个服务」应标推算 |
| 4 | 100,000 req/day ≠ 10,000 Neurons/day | **对** | 「10ms CPU/次」应标未核实 |
| 5 | 第三方链接审计 | **未发现问题** | 仅标签瑕疵 |

修改建议：①「不是 idle」改为「触发词是 inactivity；idle 仅见于冷启动描述」；②「无入站流量」标为第三方措辞；③「10ms CPU/次」补出处或标未核实。
