---
layout: default
title: 交接文档 · DeepSeek 官方 flash「挂了」故障分析与修复
date: 2026-09-11 23:30:00 +0800
---

# DeepSeek 官方 flash「挂了」故障分析与修复

- **日期**：2026-09-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-09-10-12-50-38\DeepSeek_flash故障分析与修复_20260910.md

**日期**：2026-09-10
**结论**：不是余额问题，也不是平台问题 —— **是模型 id 写错了**。你的 key 和充值都正常。

---

## 一、根因

### 官方实际只有 2 个模型

```
GET https://api.deepseek.com/v1/models
→ {"data":[{"id":"deepseek-flash"},{"id":"deepseek-v4-pro"}]}
```

**官方的 flash 叫 `deepseek-flash`，没有 `deepseek-v4-flash` 这个名字。**

### 你配置里写的是 `deepseek-v4-flash-official`

直接请求，官方返回了明确报错：

```json
{
  "error": {
    "message": "The supported API model names are deepseek-flash, deepseek-v4-pro, but you passed deepseek-v4-flash-official.",
    "type": "invalid_request_error"
  }
}
```

HTTP 400，模型名无效 → 被雷达记成 `http_4xx`，30 轮全挂。

### 为什么不是余额问题

同一个 key、同一个 url 下的 `deepseek-v4-pro` **日常成功率 100%、连发 100%、限流 0%**。key 有效、余额充足，只是 flash 那条 id 打错了。

---

## 二、当初为什么改成了 `-official`

你当时是为了**和别的平台的 `deepseek-v4-flash` 区分开**（b.ai、SenseNova、微信都有同名或近似条目）。

但这是个误解：

| 平台 | 模型 id |
|---|---|
| DeepSeek 官方 | `deepseek-flash`（**不带 v4**） |
| b.ai | `deepseek-v4-flash` |
| SenseNova | `deepseek-v4-flash-sensenova` |
| 微信 | `Deepseek-v4-flash` |

**官方的 `deepseek-flash` 和 b.ai 的 `deepseek-v4-flash` 本来就是两个不同的字符串，根本不会撞。**

### 正确的避撞方式

- ❌ 改 `id` —— id 是要原样发给 API 的，改了就 404/400
- ✅ 改 `name`（显示名）—— 只在 UI 上区分，不影响请求

修复后就是这个结构：`id = deepseek-flash`（API 用）、`name = [DeepSeek] DeepSeek-V4-Flash (官方)`（UI 显示，仍带"官方"字样便于区分）。

---

## 三、实测能力（改 id 后验证）

`deepseek-flash` 实测：

| 能力 | 结果 |
|---|---|
| 对话 | ✅ HTTP 200 |
| 推理 | ✅ 响应带 `reasoning_content` |
| 工具调用 | ✅ 返回规范 `tool_calls` |
| 图像 | ❌ 不支持 |

所以 WB 条目已补全 `caps: {text, reason, tool}`。

---

## 四、修复范围（5 处，全部完成）

| # | 位置 | 改前 | 改后 |
|---|---|---|---|
| 1 | WB `~/.workbuddy/models.json` | `deepseek-v4-flash-official` | `deepseek-flash` |
| 2 | DSH `~/.dsh/settings.yaml` → providers.deepseek | `deepseek/deepseek-v4-flash` | `deepseek-flash` |
| 3 | AutoClaw `settings.json` → models.catalog | `deepseek/deepseek-v4-flash` | `deepseek-flash` |
| 4 | 有道龙虾 `custom_7` | `deepseek/deepseek-v4-flash` | `deepseek-flash` |
| 5 | 有道龙虾 内置 `deepseek` 供应商 | `deepseek-v4-flash` | `deepseek-flash` |

> 注意 #2/#3/#4 原本写的是 `deepseek/deepseek-v4-flash`（带 `deepseek/` 前缀），这个是 OpenRouter/BazaarLink 风格的命名，DeepSeek 官方同样不认。

**撞名检查**：`deepseek-flash` 这个精确字符串在 5 处的所有层级（WB 全局、DSH 全部 provider、AutoClaw 全部 catalog、龙虾全部 provider）**均无同名命中**，安全。

**Hermes**：当前没有配置 DeepSeek 供应商，无需改动。

---

## 五、备份文件（可回滚）

- `~/.workbuddy/models.json.bak-fix-dsflash-20260910-1705`
- `~/.dsh/settings.yaml.bak-fix-dsflash-20260910-1705`
- `AppData\Roaming\autoclaw\settings.json.bak-fix-dsflash-20260910-1705`
- `AppData\Roaming\LobsterAI\lobsterai.sqlite.bak_20260910_172138`

---

## 六、做完要做的事

重启 WorkBuddy / DSH / AutoClaw / 有道龙虾，新 id 才会生效。下一轮雷达（2 小时内）就会开始记录 `deepseek-flash` 的真实成绩。

---

## 七、通用教训

**模型 id 必须与 API 提供方的真实名称逐字符一致，不能为了"本地不重名"而改写。**

需要区分同名模型时：
1. 先 `GET {baseURL}/v1/models` 拿到官方真实 id（最权威，1 次请求搞定）
2. id 保持原样
3. 用 `name` / `alias` / `displayName` 字段做 UI 区分
