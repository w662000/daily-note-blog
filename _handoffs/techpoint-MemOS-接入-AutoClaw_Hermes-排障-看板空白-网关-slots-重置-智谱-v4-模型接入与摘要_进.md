---
layout: default
title: 技术点 · MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进
date: 2026-08-09 23:30:00 +0800
---

# 技术点 · MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进

> 来源：260809_MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
- **摘要模型（必须小快非思考型）**：受 v1 拼接坑限制，活清单内「非 GLM + 国内直连 + url 末不含 /v1」的非思考模型**不存在**（DeepSeek 是思考型不适用）。可行：等 zhipuai 专用 provider 直通 `glm-4-flash-250414`，或走海外 v1 厂商（需代理）。
- **技能进化模型（思考型，不要 GLM）**：活清单标记 `supportsReasoning=true` 且非 GLM 的共 **19 个**（DeepSeek 1 / Agnes 1 / SenseNova 2 / Gemini 1 / NVIDIA NIM 9 / OpenRouter 4 / HuggingFace 1）。**实测唯一确认能过 MemOS v1 硬拼的 = DeepSeek-V4-Flash 直连**：
  - 端点 `https://api.deepseek.com`（末不含 /v1，MemOS 拼完 = `/v1/chat/completions` 正好命中官方端点）；
  - **模型名必须填 `deepseek-v4-flash`**（去掉活清单 id 的 `deepseek/` 前缀，否则服务端拒：`only accept deepseek-v4-flash / deepseek-v4-pro`）；
  - 实测 HTTP 200 + 返回 `reasoning_content`（真思考过程）✅。
- ⚠️ 注意：`agnes-2.5-pro`（非 alpha）的 `supportsReasoning=False`，**不是推理型**，不能做技能进化；Agnes 系唯一推理型是 `agnes-2.5-pro-alpha`（且其 url 末自带 /v1，在 MemOS 下会 double-v1 同样 404）。

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260809_MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进_handoff.md（编码探测：utf-8）
- > 来源：项目文档 `2026-08-09-16-44-16\HANDOFF_MemOS_Hermes_部署排障.md`
- **根因（双层）**：
- 1. 启动脚本 `start_studio.ps1` 漏配 `HERMES_BIN` → spawn hermes 报 `ENOENT`；
- **修复**：系统变量 `setx /M HERMES_BIN` 指向 `D:/hermes-agent/venv/Scripts/hermes.exe`；并用 node 直接拉 `hermes-web-ui.mjs` + 全套 env（`HERMES_HOME` / `WORKSPACE_BASE` / `GATEWAY_*`）修复被手动重启弄丢的工作区/模型列表。
- 部署本身「服务能跑、页面能开」，但**插件没真正接入 Gateway**（见第四节）。
- **根因（实测定位，非猜测）**：
- 唯一配置 `~/.openclaw/openclaw.json` 磁盘值本来就正确（`slots.memory=memos-local-plugin`），但 `plugins` 块**缺 `installs` 注册记录**（install.sh 本应写入却没写）。
- 用户之前怀疑的 `.runtime-patch.json` / `.compile-cache` 经读源码确认**不碰配置**（前者是补丁清单、后者是 Node 编译缓存）。
- **修复（方案1，已落地）**：
- **环境坑**：AutoClaw 看门狗**只自动重启 OpenClaw 网关（18789）**；杀掉 Hermes 网关(11692)/Hermes bridge(12752) 后**不自动复活**，需手动拉起（Hermes 网关 `hermes.exe gateway run --replace --accept-hooks`；18800 bridge `node ...bridge.cjs --agent=hermes --daemon`）。
- 智谱 BigModel v4 真实 chat 路径是 `https://open.bigmodel.cn/api/paas/v4/chat/completions`（**末尾是 `/v4`，没有 v1**）。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 插件包下载解压 v2.0.14：OpenClaw 目录 `~/.openclaw/extensions/memos-local-plugin/`（92 包）、Hermes 目录 `~/.hermes/memos-plugin/`（91 包）。
- `better-sqlite3` 编译 + 加载通过；两份 `config.yaml`、两个 `memos.db` 均创建。
- Viewer 起好：**OpenClaw :18799**、**Hermes :18800**，均 HTTP 200。
- 部署本身「服务能跑、页面能开」，但**插件没真正接入 Gateway**（见第四节）。
