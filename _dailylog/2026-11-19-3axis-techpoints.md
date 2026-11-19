---
layout: default
title: 技术点 · 2026-11-19
date: 2026-11-19 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-17-22-32-26\.workbuddy\memory\2026-11-19.md, D:\AI work\workbuddy\2026-11-18-14-41-01\.workbuddy\memory\2026-11-19.md

## intern-ai 墨点发放规则（用户问注册送1万是否用完就没）

- **结论：按月循环发，不是一次性**。决定性证据：实测文控制台「墨点收支」截图 `2026-09-22 15:55 | 平台发放 | +10.000 | 每月免费基础包`。多来源一致"每月送10墨点/每月自动refill/按月领"。
- **"1万墨点"是误解**：那是 5小时使用限额 10,000（滚动窗口上限，不是赠送余额）；7天限额 50,000 同理。实际每月到账=10墨点。
- 官方公告原话："测试期间每位用户每月可获免费Token"。清零：一次性发放到期日24点清空、按月发放按自然月清空。0墨点自家模型不限额(测试期内)。
- 可信度：官方公告T0 + 控制台截图T1；"10墨点"具体数来自第三方统计，以用户自己控制台为准。

## intern-ai(书生端砚)墨点消耗规则表

- 需求：查intern-ai模型积分(墨点)消耗规则，出表格。
- 数据源：T0 shlab.org.cn官方 + T1/T2实测文(11-01/11-12)转述控制台截图；官方控制台是SPA+登录，抓不到实时价。
- **单价(墨点/百万Token)**：免费0档=Agents-A1/Atria-Dawn/Sage-A1.5/intern-s2；deepseek-v4.1-flash-1017缓存命中0.02/未命中1.0/输出4.0(官方示例高可信)；qwen3.8-27b输入0.8/输出2.7；glm-5.3输入2~8/输出27~28；kimi-k2.6输出27。
- **未公开不编**：Sage-S2.1-Flash(官方仅称成本约星河1/10)、Sage-A1.5-Taiyi、kimi-k3.1-pro 无公开单价，明确标注。
- 额度：月约10墨点(第三方口径)、5h 10000、7d 50000、RPM50/TPM2M、Key≤10共享。429分rate_limit(可退避)/quota_exceeded(见底)。
- 交付：intern-ai_墨点消耗规则_20261119.md + 输出单价对比图。

## ⚠️ 国际版会话ID二次修复（上次路径建错）

- 上次建 `~/.workbuddy-ai/MEMORY.md` 无效——日志实证国际版实际读 `~/.workbuddy-ai/user-d1bc765b-...-personal/MEMORY.md`（scoped=yes，11-19 11:50 仍读它）。根目录那份白建，已删。
- 正确修复：在 personal/MEMORY.md **顶部第3行**插会话ID规则（注入有4000字符上限，头部才保进上下文）；备份 `.bak-sid-fix-20261119`；验证会话ID `wb-intl|2d146397...`（"给intern-ai打分"会话）。
- 定位实际路径的杀手锏：`grep -rh MemoryCollector ~/.workbuddy-ai/logs/` 看 `user MEMORY.md dir=`。
- 已修正 agent-session-id skill 的错误路径。注入在会话启动时，进行中会话不生效，需新开会话/重启。

## 修复 WB 国际版会话ID缺失（asar实证根因）

- 问题：国际版「全面评估所有模型分数」会话(e0fd1a60...)底部无会话ID，其他agent都有。
- 排查：规则在USER.md里没被删；会话11-19建晚于规则写入→排除会话旧。用 workbuddy-asar-inspect 扒国际版app.asar：
  - `user-context-identity.tpl` 模板：注入USER.md靠 `WorkspaceIdentityMode` 开关，国际版该会话没注入 `<identity_context>`。
  - `read_when` frontmatter 不被WB用来控制注入（只在连接器市场代码出现）。
  - **可靠通道**：`MemoryCollector.getUserInstructionsContent()` 读 `用户目录/MEMORY.md` → `<user_instructions>`，无条件注入（非quickPrompt）。国际版 `~/.workbuddy-ai/MEMORY.md` **不存在**→通道空。
- 修复：新建 `~/.workbuddy-ai/MEMORY.md` 写会话ID规则；USER.md 去 read_when 双保险；备份 `.bak-sid-fix-20261119`。验证 `get_session_id.py --agent wb-intl` 返回 e0fd1a60 成功。更新 agent-session-id skill。
- **关键**：注入在会话启动时发生，当前会话不生效，需新开会话/重启国际版。
- 教训：WB系agent常驻指令有两条独立通道——identity模板(USER.md,受WorkspaceIdentityMode限制) + 用户级MEMORY.md(user_instructions,无条件)。后者更可靠，优先用它。

## ⚠️ 活清单评分 v2 返工（修复 GLM-5.2 倒挂，重要教训）

- 用户抓到 v1 硬伤：锚点 GLM-5.3=80，但 GLM-5.2=84，倒挂。
- **根因**：混用两套量纲——GLM-5.3 用 SuperCLUE 通用榜(50.66→80)，GLM-5.2 却套 08-02 内部「干活榜」绝对分(那套把 GLM-5.2 标91，明显高估)，线性缩放后84。教训：**不同来源的绝对分绝不能混用做锚定/缩放**。
- **修复 v2**：只用 SuperCLUE 官方公开数据。①通用榜2026-11(21模型)差值映射；②编程竞技场ELO(40模型,11-02)只做同家族相对排序(铁证 GLM-5.3 1319>5.3F 1249>5.2 1245>5 985>4.7 903)；③金融榜/历史综合辅助。加家族单调断言。
- 结果：GLM-5.2=76 < GLM-5.3=80 ✓；DeepSeek V4.1(88)>V4Pro(74)>V4Flash(72)；Gemini 3.6(72)>3F(64)>3.1Lite(62)。21个有公开依据/30个推断。
- 脚本：score_all_models_v2.py（含单调断言）。看板/报告同名文件已用 v2 覆盖。
- **通用工作原则（值得记住）**：给同类对象打分时，锚点必须与所有被比对象来自同一评测体系；跨体系分数只能用于相对排序，不能当绝对分混算。

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


# 2026-11-19 工作日志

## 14:00 核查用户反馈"有道云工作日志8月中-11月中缺失"（只读）
- 用户称:工作日志只有7月~8月中+1篇11月,8月中~11月中没了。
- 全量 list 分页拉尽工作日志目录:实际145篇,按月分布 7月16/8月43/9月37/10月38/11月11。**8月中-11月的都在**(08-18~08-31、9月全月、10月全月连续),用户看到的"缺"是客户端只显示部分/排序问题,不是真丢。
- search双重验证:09-15/10-15/10-31/11-01 均 True(云端确在);08-20 返回 None(search接口抽风,list里明明有 每日工作总结·2026-08-20.md,判为误报)。
- 真实缺口(本地源本身就没有,非上传丢失):11-02~11-12 共11天本地无daily-summary源;08-25、09-09 也缺。本地 _dailylog 的 11月 daily-summary 只有 11-01/11-13~11-18。
- 结论:不是删除BUG复发,数据没丢;是本地11月上旬本来就没生成日报(可能那段时间没跑每日总结)。未做任何写入。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-19-11-44-58\.workbuddy-ai\memory\2026-11-19.md, D:\workspace\workbuddyai\2026-11-19-13-30-30\.workbuddy-ai\memory\2026-11-19.md

## intern-ai 十模型评分（WorkBuddy国际版自定义模型列表）

- 从 `~/.workbuddy-ai/cache/acc-product-config-v3-*.json` 提取到 intern-ai 通道的自定义模型列表（10个）：
  Agents-A1, Atria-Dawn, Sage-A1.5, Sage-A1.5-Taiyi, Sage-S2.1-Flash,
  deepseek-v4.1-flash-1017, glm-5.3, intern-s2, kimi-k3.1-pro, qwen3.8-27b
- API 端点：https://discovery-api.intern-ai.org.cn/v1（上海AI实验室 discovery 平台）
- 评分结论（用户设定 glm-5.3=80 锚点，满分100）：
  kimi-k3.1-pro=89, Atria-Dawn=83, glm-5.3=80, deepseek-v4.1-flash-1017=80,
  Sage-S2.1-Flash=79, intern-s2=76, qwen3.8-27b=75, Sage-A1.5-Taiyi=74,
  Sage-A1.5=72, Agents-A1=70
- 关键评测数据出处：AA Intelligence Index（Kimi K3.1 Pro 55分全球第4/国产第1；GLM-5.3 与 DeepSeek-V4.1-Flash-1017 均为32分）、LMArena（GLM-5.3-max 1487 Elo）、Terminal-Bench 4.0（K3.1 Pro 65.7% 超 GPT-6 Astra）、SWE-bench Pro（Qwen3.8-27B 超 Claude Opus 4.6 Max 8.3分）、OmniDocBench（Sage-A1.5 91.5 SOTA）、ToolSpace（Atria-Dawn 744B 与 Claude Opus 5 持平）
- 评分图表 HTML 存于工作区 score_chart.html

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）