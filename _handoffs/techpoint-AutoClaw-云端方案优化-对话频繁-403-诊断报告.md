---
layout: default
title: 技术点 · AutoClaw「云端方案优化」对话频繁 403 诊断报告
date: 2026-09-16 23:30:00 +0800
---

# 技术点 · AutoClaw「云端方案优化」对话频繁 403 诊断报告

> 来源：260916_AutoClaw「云端方案优化」对话频繁 403 诊断报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 若是 GLM-5.3/Auto-Fast：其「限时免费额度」用完（服务端码 `810000`）；
- 切到 Auto 后仍间歇 403：属**该共享通道服务端限制（额度/频率/风控）的间歇性拒绝**；叠加**无模型回退**，单次 403 即整轮失败。
- 处理：**未做任何配置改动**（用户未授权改动）
- 2026-09-15，AutoClaw「云端方案优化」对话（sessionKey `agent:main:fe0b96f6`）频繁弹出 `403 status code (no body)`。
- desc：**「GLM5.3 免费额度已用完，推荐切换至 Auto 模型，由系统智能选择可用模型继续完成任务；也可开通连续包月会员继续使用 GLM5.3，或购买智谱 Coding Plan 自行配置模型。」**
- `zai_auto`（Auto）：配置里**没有** forbiddenNotice（不受此限）→ 这就是官方推荐切 Auto 的原因。
- 用当前有效 token 直接打 `zaicoding_glm-5.3`：
- ```
HTTP 403
{"code":810000,"message":"GLM-5.3 免费额度已用完,开通连续包月会员继续使用"}
```
- ```
[agent/embedded] embedded run agent end: runId=... isError=true
  model=zaicoding_glm-5.3 provider=zai error=LLM request failed. rawError=403 status code (no body)
[agent/embedded] embedded run failover decision: ... reason=auth from=zai/zaicoding_glm-5.3
[model-fallback/decision] candidate_failed requested=zai/zaicoding_glm-5.3 reason=auth next=none
```
- | 方案 | 验证 | 说明 |
- | ② 改用 `glm-api` provider | ✅ 实弹 200 | 用已配的 49 位智谱官方 API key（`open.bigmodel.cn`），如 `glm-4-flash-250414`；不受平台限时权益限制。 |
- | ③ 开连续包月会员 | 官方付费路径 | App 内开会员，继续用 GLM-5.3。 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. 第一版误判为「zai 的 24h JWT 过期」——未实弹就打脸。
2. 第二版笼统说「额度耗尽」——把「积分」和「模型限时免费额度」混为一谈，被用户以「还有 1.7 万积分」纠正。
3. 正确做法：**先实弹请求看真实响应体，再查官方下发的模型元数据（forbiddenNotice），最后才下结论**。

---
