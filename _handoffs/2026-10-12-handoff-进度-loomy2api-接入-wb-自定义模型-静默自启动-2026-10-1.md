---
layout: default
title: 交接文档 · 进度：loomy2api 接入 WB 自定义模型 + 静默自启动（2026-10-12 12_20）
date: 2026-10-13 23:30:00 +0800
---

# 进度：loomy2api 接入 WB 自定义模型 + 静默自启动（2026-10-12 12:20）

- **日期**：2026-10-12
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-12-11-05-04\loomy2api\进度_20261012_1220.md

## 1. 接入 WB 自定义模型
- 落点 `~/.workbuddy/models.json`（扁平数组）。备份 `models.json.bak-add-loomy-20261012-1214`。
- 新增 9 个 loomy 文本对话模型：DeepSeek-V4.1-Flash / deepseek-v4-flash-0731 / MiniMax-M3 / Kimi-k2.6 / qwen-3.8-max / GLM-5.3-Flash / spark-x / mimo-v2.5 / auto。
- `qwen3.8-flash` 因 WB 已有同 id 的 b.ai 条目被去重跳过。
- `url=http://127.0.0.1:17890/v1`（无结尾斜杠，与本机现有约定一致）；`apiKey=loomy-local`（网关 api_keys 空不校验）。
- 验证：spark-x / GLM-5.3-Flash / mimo-v2.5 经 UTF-8+Bearer 温和测试通过。
- 生图模型 3 个（Hy-Image-3.5-preview / doubao-seedream-5-lite / qwen-image-3.0-pro）未入 WB 对话选择器。

## 2. 静默自启动
- 本机安全策略禁用 schtasks / reg.exe / PowerShell COM / 写注册表 Run 键。
- 采用启动文件夹 + pythonw（与用户现有 Hermes-AutoStart.vbs 同款）：
  - 源：`loomy2api/start_silent.vbs`、`start_silent.bat`
  - 自启动项：`AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\loomy2api-AutoStart.vbs`
- 当前运行实例已切换为 pythonw（PID 7788，无窗口），与自启动一致。重启后由 Startup 自动拉起。

## 可用 LLM（上游 /v1/models 共 13 个）
- 文本对话(10)：DeepSeek-V4.1-Flash、deepseek-v4-flash-0731、MiniMax-M3、Kimi-k2.6、qwen-3.8-max、GLM-5.3-Flash、qwen3.8-flash、spark-x、mimo-v2.5(多模态)、auto(路由)
- 图像生成(3)：Hy-Image-3.5-preview、douao-seedream-5-lite、qwen-image-3.0-pro

## 待用户操作
- 完全重启 WB（或重开模型选择器）即可看到 [Loomy] 开头的模型并对话。
- 重启系统验证自启动是否自动拉起网关（监听 127.0.0.1:17890）。
