---
layout: default
title: 交接文档 · AutoClaw「云端方案优化」对话频繁 403 诊断报告
date: 2026-09-17 23:30:00 +0800
---

# AutoClaw「云端方案优化」对话频繁 403 诊断报告

- **日期**：2026-09-16
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-09-16-09-28-11\AutoClaw_403_诊断报告.md

- 日期：2026-09-16（含下午第二轮更新）
- 结论（终版）：**403 来自 AutoClaw 内置 `zai` 共享通道（云端中继）**——
  - 若是 GLM-5.3/Auto-Fast：其「限时免费额度」用完（服务端码 `810000`）；
  - 切到 Auto 后仍间歇 403：属**该共享通道服务端限制（额度/频率/风控）的间歇性拒绝**；叠加**无模型回退**，单次 403 即整轮失败。
  - **非用户本地/网络问题**（对照组：用户自有 `agnes-ai` 通道当天 0 失败）。
- 处理：**未做任何配置改动**（用户未授权改动）

---

## 1. 现象

- 2026-09-15，AutoClaw「云端方案优化」对话（sessionKey `agent:main:fe0b96f6`）频繁弹出 `403 status code (no body)`。
- 用户当时用的是「平台自带的 GLM5.3 系列模型」，且账号还剩 1.7 万积分。

## 2. 根因（三条证据对齐）

### 证据 A：AutoClaw 官方模型配置（最硬）
文件：`C:\Users\Administrator\.openclaw-autoclaw\logs\autoclaw-dev.log:725`（RemoteConfig 下发的模型定义）

`GLM-5.3`（内部 id `zaicoding_glm-5.3`，消耗等级「高」）带有 `forbiddenNotice`：

- title：**限时权益已用完**
- desc：**「GLM5.3 免费额度已用完，推荐切换至 Auto 模型，由系统智能选择可用模型继续完成任务；也可开通连续包月会员继续使用 GLM5.3，或购买智谱 Coding Plan 自行配置模型。」**
- actions：`成为会员` / `购买 Coding Plan`（**没有「用积分」这条路**）

对照：
- `zai_auto-fast`（Auto-Fast）：desc 写「…免费额度已用完，**24 小时后会进行重置**…」
- `zai_auto`（Auto）：配置里**没有** forbiddenNotice（不受此限）→ 这就是官方推荐切 Auto 的原因。

### 证据 B：实弹请求
用当前有效 token 直接打 `zaicoding_glm-5.3`：

```
HTTP 403
{"code":810000,"message":"GLM-5.3 免费额度已用完,开通连续包月会员继续使用"}
```

### 证据 C：网关日志
文件：`.openclaw-autoclaw\logs\gateway_old.log`（9/15）

```
[agent/embedded] embedded run agent end: runId=... isError=true
  model=zaicoding_glm-5.3 provider=zai error=LLM request failed. rawError=403 status code (no body)
[agent/embedded] embedded run failover decision: ... reason=auth from=zai/zaicoding_glm-5.3
[model-fallback/decision] candidate_failed requested=zai/zaicoding_glm-5.3 reason=auth next=none
```

## 3. 两个易错点

- **日志 `no body` ≠ 真无 body**：AutoClaw 的 HTTP 客户端没把 JSON 响应体读出来，统一渲染成了 `403 status code (no body)`；真实 body 是 `{"code":810000,...}`。
- **「积分」≠「GLM-5.3 免费额度」**：账号积分是一个池，模型的「限时免费额度」是另一个池。官方给出的续用方式只有「切 Auto / 开会员 / 买 Coding Plan」，没有「用积分」——所以「还有 1.7 万积分」与「GLM-5.3 免费额度用完」同时成立。

## 4. 解法清单（均未执行）

| 方案 | 验证 | 说明 |
|---|---|---|
| ① 切到 Auto 模型（`zai_auto`） | AutoClaw 官方推荐 | 对话里把模型下拉切成 Auto，系统自动选可用模型，免费。 |
| ② 改用 `glm-api` provider | ✅ 实弹 200 | 用已配的 49 位智谱官方 API key（`open.bigmodel.cn`），如 `glm-4-flash-250414`；不受平台限时权益限制。 |
| ③ 开连续包月会员 | 官方付费路径 | App 内开会员，继续用 GLM-5.3。 |
| ④ 买智谱 Coding Plan | 官方付费路径 | App 内购买后自行配置模型。 |
| ⑤ 改用 `agnes-ai` provider | ✅ 实弹 200 | `agnes-3.0-flash`，绕开平台额度。 |

补充：`Auto-Fast` 额度**每 24 小时重置**；`GLM-5.3` 的限时权益提示未写重置，属活动期一次性免费额度。

## 5. 自查命令（下次再遇 AutoClaw 403 可用）

```bash
# 1) 看是否限时权益用完（官方文案）
grep -rn "额度已用完\|限时权益" "C:/Users/Administrator/.openclaw-autoclaw/logs/autoclaw-dev.log"

# 2) 看失败模型/provider
grep -n "provider=zai\|rawError=403\|failover decision" "C:/Users/Administrator/.openclaw-autoclaw/logs/gateway.log"
```

## 6. 我自己踩的坑（记录以示反省）

1. 第一版误判为「zai 的 24h JWT 过期」——未实弹就打脸。
2. 第二版笼统说「额度耗尽」——把「积分」和「模型限时免费额度」混为一谈，被用户以「还有 1.7 万积分」纠正。
3. 正确做法：**先实弹请求看真实响应体，再查官方下发的模型元数据（forbiddenNotice），最后才下结论**。

---

## 7. 第二轮更新（2026-09-16 下午）：切 Auto 后仍 403

用户反馈：改用 Auto（`zai_auto`）后**仍频繁** `403 status code (no body)`。

### 7.1 现场事实（今天 9/16）
- 失败点：`provider=zai`，`model.id=zai_auto`，url 仍是 `.../autoclaw-proxy/proxy/autoclaw/chat/completions`；时间 13:14:49 / 13:20:10 / 13:21:31。
- **间歇性**：同一轮 agent 里前面多次 200，某一次突然 403（今日 zai：200×49 / 403×3）。
- **快拒绝**：403 都在 ~0.4s 返回（200 需 2~5s）→ 服务端前置校验拒绝。
- **对照实验**：用户自有 `agnes-ai` 通道今日 **200×21 / 0 失败** → 问题只在**内置 zai 共享通道**。

### 7.2 三条辅助证据
- **账号有积分**（`autoclaw-dev.log` 12:14 `[IPC] Wallet v2`）：`total_balance=19982`（reward 奖励积分 1.9w；daily/subscription/fuel_pack 均 0）→ **不是"没积分"**。
- **错误映射缺失**：`[RemoteConfig] autoclaw-error-mapping: empty response ({})` 每 5 分钟报一次 → AutoClaw 无法翻译错误码，只能显示裸 `403 (no body)`。
- **无回退**：`openclaw.json` 无任何 fallback/retry 配置；failover `reason=auth next=none` → **单次 403 即整轮 "failed before reply"**。

### 7.3 结论与不确定项
- 结论：**403 = 内置 zai 共享通道的服务端限制（额度/频率/风控）间歇性拒绝**；叠加"无回退 + 无错误映射"→ 体感频繁且信息缺失。非本地问题。
- 不确定项：**未能拿到 Auto 场景 403 的真实 body**（裸探针复现不出 AutoClaw 完整报文，均 `400 invalid request`；app 不记录错误 body）。故无法进一步区分"额度"与"限流"。

### 7.4 建议解法（未执行）
1. **默认模型改走自有 provider**：`agnes-ai`（今日 0 失败）或 `glm-api`（官方 key）——绕开共享免费通道，最稳。
2. 若 AutoClaw UI 支持**模型回退**，配置备用模型，让偶发 403 自动切换而非整轮失败。
3. 等额度/时间重置，或开通会员。
4. 升级 AutoClaw（当前 1.15.2，最新 1.18.4，灰度日志提到修复"对话流卡顿"等）。

### 7.5 自查命令
```bash
grep -n "provider=zai\|rawError=403\|next=none" ~/.openclaw-autoclaw/logs/gateway.log
grep -n "autoclaw-error-mapping\|Wallet v2\|forbiddenNotice" ~/.openclaw-autoclaw/logs/autoclaw-dev.log
grep "provider=agnes-ai" ~/.openclaw-autoclaw/logs/gateway.log | grep -oE "status=[0-9]+" | sort | uniq -c
```
