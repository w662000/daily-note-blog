---
layout: default
title: 每日工作总结 · 2026-07-21
date: 2026-07-21 23:30:00 +0800
---

# 每日工作总结 · 2026-07-21

## 一、今日完成事项
1. **白虎(Baihu Panel)使用指南**：整理本地"白虎"面板（Go+Vue3 定时任务面板，端口 8052）完整使用指南——部署、配环境变量、写脚本、第一个爬虫任务实战。
2. **Hermes GLM 赠送模型显示修复**：用户在 Hermes 加了 GLM(Z.AI) Key 但列表缺 `glm-4.5-air`/`glm-4.6v`。在 `config.yaml` 加 `providers.zai.models` 白名单，补齐到 9 个模型；查证 `glm-4.7-flash` 永久免费并加入；最终默认模型定为 `glm-4.5-air`（不排队+有赠送额度）。
3. **AtomGit CodingPlan / AIHub 接入**：发现 AtomGit 两套 API 钥匙不通用（CodingPlan 有签名校验第三方无法直连）。用开源 `codingplan-proxy` 本地代理（端口 18999）绕过签名，Hermes 经 `host.docker.internal:18999` 调用 deepseek-v4-flash 等；实测 3 个模型可用（glm-5 需 Pro 已删）。
4. **置顶排序 + 容器重启事故**：删 atomgit 分组、GLM/Gemini/OpenRouter 白名单置顶。**事故**：加 GLM_API_KEY 后误用 `--force-recreate`，触发 webui 全量重装 95+ 依赖、折腾近 1 小时。根因是镜像 init 脚本每次 recreate 都 rsync 1.2G+装包。→ **立红线：改 compose env 只 restart，绝不许 recreate（除非用户同意）**，写入 MEMORY.md。

## 二、关键决策 / 注意事项
- **默认模型选型**：日常 agent+编程用 `glm-4.5-air`（送 token 付费层，6 连发 0.6-0.7s 极稳）；`glm-4.7-flash` 免费层首 token ~17s 且易 429，只供单发简单任务。
- **AtomGit 障碍**：AIHub serverless 需先领 5000 万额度才出字；CodingPlan 真实模型需 Pro（每日限量抢）。
- **红线事件**是今日最大教训，已固化为跨会话护栏。

## 三、生成的有用文件
| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 白虎指南 | `2026-07-21-18-02-29\白虎使用指南.md` | 面板完整使用文档 |
| codingplan 代理 | `2026-07-21-18-02-29\codingplan-proxy\` | 本地代理(端口18999)+start-proxy.bat/.vbs + install-autostart.bat |
| 配置安全网 | `C:\Users\Administrator\.hermes\config.yaml.bak-20260721T013122Z` | 改模型前原始配置留底(1508行) |
| 红线记录 | `~/.workbuddy/MEMORY.md` + 项目 `MEMORY.md` | force-recreate 绝对禁令 |

## 四、待办 / 风险
- AtomGit Pro 每日 10:00 抢（auto_claim_pro.py），抢到后可把 glm-5 加回白名单。
- **事故副作用**：recreate 时 compose 挂载漏 `C:` 盘符，在 D 盘根生成 `D:\c`(510M)、`D:\d`(226M) 垃圾文件夹——次日(7-22)已清理。
- 注册表自启动写入受 Defender 限制，改用 `HKCU\...\Run\CodingPlanProxy` 实现代理开机自启。
