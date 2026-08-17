---
layout: default
title: 交接文档 · 进度：把 WorkBuddy 活清单模型导入有道龙虾(LobsterAI)
date: 2026-08-17 23:30:00 +0800
---

# 进度：把 WorkBuddy 活清单模型导入有道龙虾(LobsterAI)

- **日期**：2026-08-17
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-17-00-05-49\进度_20260817_2151_活清单导入有道龙虾.md

## 结论
- 有道龙虾「JSON 导入模型」的真实机制 = 写入 `AppData\Roaming\LobsterAI\openclaw\state\openclaw.json` 的 `models.providers`（provider 模式：baseUrl+apiKey+models[]），**无需改 app.asar**。
- 已把 `~/.workbuddy/models.json`（活清单 28 模型/9 vendor，与 handoff 文档对齐）转成 9 个 `wb-<vendor>` provider 注入；原有 `lobsterai-server`(20 内置模型)保留。
- 现在 openclaw.json 共 10 provider / 48 模型。备份 `openclaw.json.bak-import-<时间戳>`。
- 独立导入文件导出：`D:\AI work\workbuddy\handoff\lobsterai_models_import.json`（仅 9 个 wb-* provider，备 UI 复核/重导/回滚）。

## 关键坑（已处理）
- openclaw 的 `openai-completions` 是 base 直拼 `/chat/completions`（不自带 /v1）；参照 lobsterai-server base 末尾 `/v1`。DeepSeek 活清单 URL 为 `https://api.deepseek.com`（给 WB 客户端用，会自加 /v1），对 openclaw 须改成 `https://api.deepseek.com/v1`，已改。

## 待用户
- **重启有道龙虾** 让配置生效（启动时加载）。
- 沙箱无网，未实测各端连通；若某 vendor 报 404 多为 base 缺 /v1 后缀，反馈即改。
- 图片/视频生成类(agnes-image-2.1-flash/agnes-video-v2.0)按对话模型导入，可能不可用，无害。
- 另有更大集合 `/d/AI work/workbuddy/models.json`(含 StepFun/OpenRouter/OmniRoute) 未导入，待用户决定是否扩导。
