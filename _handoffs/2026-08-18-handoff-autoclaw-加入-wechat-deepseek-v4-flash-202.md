---
layout: default
title: 交接文档 · AutoClaw 加入 [WeChat] Deepseek-v4-flash（2026-08-18 23_26）
date: 2026-08-20 23:30:00 +0800
---

# AutoClaw 加入 [WeChat] Deepseek-v4-flash（2026-08-18 23:26）

- **日期**：2026-08-18
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-18-12-42-34\进度_20260818_2327_autoclaw加wechat.md

## 任务
用户说「给autoclaw的模型清单也加入这个模型」——把微信小程序大赛的 [WeChat] Deepseek-v4-flash 加入 AutoClaw。

## AutoClaw 配置机制（重要认知）
- **模型配置真身**：`C:\Users\Administrator\.openclaw-autoclaw\openclaw.json` → `models.providers`（dict，key=`<provider>__<uuid>`，apiKey **明文**）
- `AppData\Roaming\autoclaw\settings.json` 的 `models.catalog` 只是 UI 视图，由 openclaw.json 自动同步生成，**不要手动改**
- 8/16 打过 app.asar 补丁（syncSettingsCatalog 只增不删 + 禁用 stale provider 删除），app.asar 时间戳 8/16 11:16 确认补丁仍生效
- 远程 model-provider-config 仍需在 AutoClaw 设置里关掉/忽略（若 UI 消失再查）

## 已执行
1. 备份：`openclaw.json.bak-add-wechat-20260818-2326`
2. 注入 provider：
```json
"wechat__6d8ca8d1-963a-48ff-910a-1bfb7ebee082": {
  "baseUrl": "https://chatapi.weixin.qq.com/openai/v1",
  "api": "openai-completions",
  "apiKey": "Vz9uhg...(微信大赛key)",
  "models": [{
    "id": "Deepseek-v4-flash",
    "name": "[WeChat] Deepseek-v4-flash (小程序大赛)",
    "contextWindow": 200000,
    "maxTokens": 32000,
    "reasoning": true
  }]
}
```
3. 校验：JSON 合法，providers 72→73，id 精确 `Deepseek-v4-flash`，无 id 冲突

## 与现有 Deepseek-flash 系列共存检查
| provider | id | 说明 |
|---|---|---|
| sensenova | deepseek-v4-flash | 小写，不同 provider |
| b-ai | deepseek-v4-flash | 小写，走 proxy 127.0.0.1:7897 |
| custom__ | DeepSeek-v4-flash | 大写S，b.ai 残留 |
| **wechat（新）** | **Deepseek-v4-flash** | D大写s小写，无 proxy |

全部不同 id/provider，无冲突。

## 待用户执行
重启 AutoClaw（当前 6 个进程运行中，装在 D:\Program Files\AutoClaw\）。重启后模型列表应见 `[WeChat] Deepseek-v4-flash (小程序大赛)`。

## 备份
- `C:\Users\Administrator\.openclaw-autoclaw\openclaw.json.bak-add-wechat-20260818-2326`
