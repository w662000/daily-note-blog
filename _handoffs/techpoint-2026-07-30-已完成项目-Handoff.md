---
layout: default
title: 技术点 · 2026-07-30 已完成项目 Handoff
date: 2026-07-30 23:30:00 +0800
---

# 技术点 · 2026-07-30 已完成项目 Handoff

> 来源：260730_每日完成项目_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260730_每日完成项目_handoff.md（编码探测：utf-8）
- 把 OmniRoute（一个把多家大模型聚合成单一 OpenAI 兼容接口的工具）装到本机，并一路排查它启动黑屏/数据库报错的问题，最终定位根因是安装包自带的数据库原生模块与运行环境版本不匹配，打补丁后 GUI 正常启动。
- 在 OmniRoute 里接好了 8 个上游大模型平台（Cloudflare、Groq、智谱 GLM、Gemini、OpenRouter、Cerebras、NVIDIA NIM、HuggingFace），并配置 GLM 中国区走直连、其余走代理，实测全网通。
- 在 WorkBuddy 的模型配置里加了通过 OmniRoute 访问的条目；经反复实测，最终把"智能路由 auto/*"换成 3 个已验证能正常出字的具体免费模型（Ling / Gemma 视觉 / GLM 备用），避免卡死和吞输出。
- 在 Hermes 配置里把 OmniRoute 注册为自定义 provider，端到端实测 Hermes → OmniRoute → OpenRouter 链路打通；后又补了 4 条具体模型并核实改模型列表无需重启 gateway。
- 排查 Agnes 国内站 401 报错，根因是 Base URL 填错（写成了 apihub 而非官方 api 域名），改对后同一把 key 立刻通；随后把 Agnes 国内站全部 4 个模型（对话 / 推理 / 文生图 / 文生视频）都加进了 WorkBuddy。
- 发现之前 28 号论坛缺帖是因为代理离线时主发布任务没跑、而旧兜底只补"每日工作总结"不补论坛日志。新建了一个每天 10:00 直连补发论坛工作日志的兜底自动化（幂等、不依赖代理），并修了脚本分页漏判旧帖的 bug。
- 6. **Hermes 读 WorkBuddy 文档的排查与索引**
- 排查 Hermes 读不到工作区 md 的真因（是读目录而非文件、以及历史会话上下文爆了导致幻觉），转而生成了一份全工作区 md 文件索引和 10 个批次包，方便 Hermes 一次读一批；同时把 Hermes 单轮工具调用上限从 50 提到 150。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
