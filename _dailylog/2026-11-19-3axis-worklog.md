---
layout: default
title: 多 Agent 工作日志 · 2026-11-19
date: 2026-11-19 23:30:00 +0800
---

# 多 Agent 每日工作日志 · 2026-11-19

> 机器汇总（模型不可用，原文按 agent 分节保留，未做润色）

## 一、WB 国内版（wb-cn）
> 数据源：D:\AI work\workbuddy\2026-11-17-22-32-26\.workbuddy\memory\2026-11-19.md


# 2026-11-19 工作日志

## intern-ai 谁真正能用（双雷达实测，纯只读无请求）

- 需求：结合测速8848+限速8849雷达，找真正能用/流畅/限流少的模型。
- 方法：加载 model-radar-topn skill，纯本地只读统计近3天窗口，不发任何请求。
- **结果（实测可用性，可信度T0）**：
  - 流畅首选（100%成功、TTFT0.5s、0限流）：qwen3.8-27b、Agents-A1、Sage-A1.5
  - 稳稍慢：glm-5.3(1.27s)、Sage-S2.1-Flash(1.07s)、intern-s2(1.55s)
  - 慢但稳：Atria-Dawn(6.3s)、Sage-A1.5-Taiyi(8.3s)
  - **不可用**：deepseek-v4.1-flash-1017（限速429率43.3%、测速多轮rate_limit+cooldown）、kimi-k3.1-pro（全http_4xx/http_error通道不通，非限流）
- **关键洞察**：跑分排名与实测可用性几乎相反——kimi跑分第1实测0%成功垫底，qwen跑分垫底实测第一。跑分=能力上限，雷达=此刻通道稳不稳。
- 产物：`intern-ai_谁真正能用_双雷达实测_20261119.md`、`分析脚本/intern_ai_radar.py`、可用性条形图。
- 口径细节：kimi的0% 429率不能读作好，因全是http_error；deepseek的cooldown计入限流证据。

## intern-ai 10 模型评分（锚点 glm-5.3=80）

- 需求：对 Agents-A1 / Atria-Dawn / Sage-A1.5 / Sage-A1.5-Taiyi / Sage-S2.1-Flash / deepseek-v4.1-flash-1017 / glm-5.3 / intern-s2 / kimi-k3.1-pro / qwen3.8-27b 打分，glm-5.3=80。
- 方法：**只用搜索，不循环实测**（平台深度思考不可关、单次25-102秒、TPM限流紧曾撞429，遵守温和测试红线）。
- 数据源（已核实可信度）：
  - T0 上海AI实验室官网 shlab.org.cn / news/5444320（书生系列定位、Sage-S2.1-Flash 智能体基准4项第一）。
  - **T1 SuperCLUE 2026-11 通用榜**（superclueai.com/homepage、/generalpage，多家媒体交叉）：kimi-k3.1-pro 61.46（国内第一）、deepseek-v4.1-flash-1017 58.95（第二）、glm-5.3 50.66（第三）、qwen3.8-flash 39.81。这是唯一能核对的第三方综合硬分。
  - T1 端砚平台公众号实测文（模型列表/上下文/计费/429/测速）、T2 explainx.ai（Atria-Dawn 744B/MIT/GLM-5.2架构）。
- 打分规则：有 SuperCLUE 硬分的用差值映射 `80+(总分-50.66)`；无榜的 7 个按官方定位推断、可信度标"低"。
- 结果：kimi91 / deepseek88 / Sage-S2.1-Flash85 / glm-5.3(锚)80 / Atria-Dawn79 / Sage-A1.5 78 / intern-s2 77 / Agents-A1 76 / Sage-A1.5-Taiyi 74 / qwen3.8-27b 69。
- 产物：`intern-ai_10模型评分报告_20261119.md` + 内联评分条形图（蓝色=硬分3个，琥珀=推断7个）。
- 注意：只有 3 个模型有硬分，其余 7 个是推断档位、误差可能大，已如实标注；未把速度计入评分。

会话ID：31652b9c-1b03-4c33-92b9-e925c12d1736

## 二、WB 国际版（wb-intl）

今日无机器日志记录。

## 三、AutoClaw 1.15（autoclaw-115）

今日无机器日志记录。

## 四、ZCode（zcode）

今日无机器日志记录。

## 五、总计

- 当天有日志的 agent：1/4
- 日志总字符数：1800