---
layout: default
title: 交接文档 · [WeChat] Deepseek-v4-flash 接入 DSH + Hermes（2026-08-18 23_22）
date: 2026-08-20 23:30:00 +0800
---

# [WeChat] Deepseek-v4-flash 接入 DSH + Hermes（2026-08-18 23:22）

- **日期**：2026-08-18
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-08-18-12-42-34\进度_20260818_2323_wechat接入dsh-hermes.md

## 任务
用户说「新增模型 给DSH和hermes(8787和8648)都加上这个模型 [WeChat] Deepseek-v4-flash」→ 触发 custom-model-onboarding skill。

## 模型信息
- id: `Deepseek-v4-flash`（**D 大写、s 小写**，微信大赛后台精确拼写，大小写敏感）
- name: `[WeChat] Deepseek-v4-flash (小程序大赛)`
- vendor: WeChat
- url: `https://chatapi.weixin.qq.com/openai/v1`
- apiKey: Vz9uhg...（敏感，写入 .credentials.yaml / hermes config.yaml，勿外泄）
- 能力：文本、工具调用、思考模式；不支持图片

## 已修改文件（4 个，全部先备份 .bak-add-wechat-20260818-2322）
1. `~/.dsh/.credentials.yaml` → 追加 `WB_KEY_12: <key>`（WB_KEY_1..11 → 12）
2. `~/.dsh/settings.yaml` → `llm-pi-ai.providers.wechat`（apiKeyEnv=WB_KEY_12, baseURL=chatapi.weixin.qq.com/openai/v1, models=[Deepseek-v4-flash]）
3. `~/.hermes/config.yaml`（WebUI 8787 + Studio 8648 + Gateway 5324 共用）→ `custom_providers` 加 `wechat`
4. `~/.hermes-web-ui/config.json` → `modelVisibility` + `customModels` 两处加 `custom:wechat: [Deepseek-v4-flash]`

## 校验结果
- 4 文件 YAML/JSON 全部合法
- DSH providers：13 个（含 wechat）
- Hermes custom_providers：8 个（含 wechat）
- 缓存：provider-model-catalog.json 主文件不存在，无陈旧缓存

## 待用户执行
重启 DSH(3080) + Hermes WebUI(8787) / Studio(8648) / Gateway(5324)
重启后：
- DSH 模型列表见 `[WeChat] 小程序大赛`
- WebUI/Studio 模型列表见 `custom:wechat / Deepseek-v4-flash`

## 备份清单
- `~/.dsh/settings.yaml.bak-add-wechat-20260818-2322`
- `~/.dsh/.credentials.yaml.bak-add-wechat-20260818-2322`
- `~/.hermes/config.yaml.bak-add-wechat-20260818-2322`
- `~/.hermes-web-ui/config.json.bak-add-wechat-20260818-2322`
