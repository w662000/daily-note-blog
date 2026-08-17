---
layout: default
title: 交接文档 · MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进
date: 2026-08-17 23:30:00 +0800
---

# MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进

- **日期**：2026-08-09
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260809_MemOS 接入 AutoClaw_Hermes 排障：看板空白·网关 slots 重置·智谱 v4 模型接入与摘要_进_handoff.md（编码探测：utf-8）

> 来源：项目文档 `2026-08-09-16-44-16\HANDOFF_MemOS_Hermes_部署排障.md`
> 由 handoff_flow.py（scan 阶段）自动收集，标题取自文档 H1（即主要干的活），待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。


> 交接文档（项目轴）｜会话：2026-08-09-16-44-16｜时间：2026-08-09 晚 ~ 08-10 凌晨
> 主线：把 MemOS Local Plugin 2.0 装进 AutoClaw/Hermes 做「记忆自进化」，过程中连带着修好了 Hermes Studio 看板空白、Node 升级、网关 slots 被重置、以及 MemOS 模型接入的智谱 v4 协议坑。

## 背景与目标

用户想让 Hermes Agent 具备「长期记忆 + 技能自进化」能力，按一篇微信文章（MemOS Local Plugin 2.0 装 Hermes）实施。需要先配两个模型：**摘要模型（小快非思考型）** 与 **技能进化模型（思考型）**。实施中发现 MemOS 的 `openai_compatible` provider 对国内模型（尤其智谱）存在协议不兼容的硬坑，并连带暴露了 AutoClaw 网关插件注册缺失的问题。

## 一、Hermes Studio 看板空白（本会话起点）

- **现象**：`http://127.0.0.1:8650/#/hermes/chat` 看板打不开 / 不展示。
- **根因（双层）**：
  1. 启动脚本 `start_studio.ps1` 漏配 `HERMES_BIN` → spawn hermes 报 `ENOENT`；
  2. 本机 `C:\Users\Administrator\.hermes\kanban.db` 是**空库**（0 任务）——看板状态机 triage→todo→scheduled→ready→running→blocked→done，没有任务自然空白。
- **修复**：系统变量 `setx /M HERMES_BIN` 指向 `D:/hermes-agent/venv/Scripts/hermes.exe`；并用 node 直接拉 `hermes-web-ui.mjs` + 全套 env（`HERMES_HOME` / `WORKSPACE_BASE` / `GATEWAY_*`）修复被手动重启弄丢的工作区/模型列表。

## 二、Node 升级到 v24

`hermes-web-ui` 要求 node>=23。本机下载 **v24.19.0 LTS** 并存到 `C:\Users\Administrator\.workbuddy\binaries\node\versions\node-v24.19.0-win-x64\`，切 Studio 到 v24（PID 5196 监听 8650，HTTP 200）。

## 三、MemOS Local Plugin 2.0 部署（AutoClaw + Hermes 两条线）

- 插件包下载解压 v2.0.14：OpenClaw 目录 `~/.openclaw/extensions/memos-local-plugin/`（92 包）、Hermes 目录 `~/.hermes/memos-plugin/`（91 包）。
- `better-sqlite3` 编译 + 加载通过；两份 `config.yaml`、两个 `memos.db` 均创建。
- Viewer 起好：**OpenClaw :18799**、**Hermes :18800**，均 HTTP 200。
- 部署本身「服务能跑、页面能开」，但**插件没真正接入 Gateway**（见第四节）。

## 四、网关 slots.memory 被重置（关键根因 + 修复）

- **现象**：重启 Gateway 后 `plugins.slots.memory` 又被还原成 `none`，`plugins.allow` 为空，插件列表里看不到 memos。
- **根因（实测定位，非猜测）**：
  - 唯一配置 `~/.openclaw/openclaw.json` 磁盘值本来就正确（`slots.memory=memos-local-plugin`），但 `plugins` 块**缺 `installs` 注册记录**（install.sh 本应写入却没写）。
  - AutoClaw Gateway 源码（CHANGELOG #3192）在启动 normalize 时会 **reset stale `plugins.slots.memory`**——当 slot 指向的插件没在 `installs` 注册表时，重置为 `none`。每次重启都重新 normalize → 一重启就丢。
  - 注意：这个重置**只改内存、不写回磁盘**，所以磁盘文件一直是对的。
  - 用户之前怀疑的 `.runtime-patch.json` / `.compile-cache` 经读源码确认**不碰配置**（前者是补丁清单、后者是 Node 编译缓存）。
- **修复（方案1，已落地）**：
  1. 备份 `openclaw.json` → `openclaw.json.bak-20260809-235150`；
  2. 补写 `plugins.installs["memos-local-plugin"]`（`source:path`、`installPath:~/.openclaw/extensions/memos-local-plugin`、`version:2.0.14`）；
  3. PowerShell 杀旧 Gateway PID 15580 → AutoClaw 看门狗自动拉起新 Gateway（PID 2748 监听 18789）。
  - 验证：重启后 `openclaw.json` mtime 仍是补 installs 的时间，没被写回 `none` ✅。
- **环境坑**：AutoClaw 看门狗**只自动重启 OpenClaw 网关（18789）**；杀掉 Hermes 网关(11692)/Hermes bridge(12752) 后**不自动复活**，需手动拉起（Hermes 网关 `hermes.exe gateway run --replace --accept-hooks`；18800 bridge `node ...bridge.cjs --agent=hermes --daemon`）。

## 五、MemOS 模型配置（重点：智谱 v4 协议坑 + 选型推荐）

### 5.1 智谱 v4 接入必 404 的根因（一手实测，T0）

- MemOS 的 `openai_compatible` 拼接逻辑 = `base_url + "/v1/chat/completions"`。
- 智谱 BigModel v4 真实 chat 路径是 `https://open.bigmodel.cn/api/paas/v4/chat/completions`（**末尾是 `/v4`，没有 v1**）。
- 实测对照（用本机智谱 key）：
  - `POST /api/paas/v4/chat/completions` → **HTTP 200**，真实回复；
  - `POST /api/paas/v4/v1/chat/completions` → **HTTP 404**（与用户截图完全一致）。
- **结论**：只要 MemOS 强制拼 `/v1`，智谱 v4 在 `openai_compatible` 下**永远配不通**（方程无解）。活清单 12 家厂商里只有 GLM API 是 v4 协议，其余 11 家都是真 v1 兼容。
- **解法**：① 看 MemOS 下拉有没有 `zhipuai/智谱/BigModel` 专用 provider（base 由 provider 硬编码，不拼 v1）；② 否则换 v1 兼容厂商。

### 5.2 摘要模型 / 技能进化模型选型（国内直连、排除 GLM 系已单独列全）

- **摘要模型（必须小快非思考型）**：受 v1 拼接坑限制，活清单内「非 GLM + 国内直连 + url 末不含 /v1」的非思考模型**不存在**（DeepSeek 是思考型不适用）。可行：等 zhipuai 专用 provider 直通 `glm-4-flash-250414`，或走海外 v1 厂商（需代理）。
- **技能进化模型（思考型，不要 GLM）**：活清单标记 `supportsReasoning=true` 且非 GLM 的共 **19 个**（DeepSeek 1 / Agnes 1 / SenseNova 2 / Gemini 1 / NVIDIA NIM 9 / OpenRouter 4 / HuggingFace 1）。**实测唯一确认能过 MemOS v1 硬拼的 = DeepSeek-V4-Flash 直连**：
  - 端点 `https://api.deepseek.com`（末不含 /v1，MemOS 拼完 = `/v1/chat/completions` 正好命中官方端点）；
  - **模型名必须填 `deepseek-v4-flash`**（去掉活清单 id 的 `deepseek/` 前缀，否则服务端拒：`only accept deepseek-v4-flash / deepseek-v4-pro`）；
  - 实测 HTTP 200 + 返回 `reasoning_content`（真思考过程）✅。
- ⚠️ 注意：`agnes-2.5-pro`（非 alpha）的 `supportsReasoning=False`，**不是推理型**，不能做技能进化；Agnes 系唯一推理型是 `agnes-2.5-pro-alpha`（且其 url 末自带 /v1，在 MemOS 下会 double-v1 同样 404）。

## 六、Hermes Studio "profile worker default exited before ready"（待续）

- **现象**：Studio 报 `profile worker default exited before ready`。
- **定位**：错误来自 `bridge_transport.py:121`——Studio 通过 Python 桥 spawn `hermes_bridge.py` 子进程做 profile worker，子进程在 120s 窗口内直接挂了（`proc.poll() is not None`）。`hermes_bridge.py` 真实位置在 `hermes-web-ui/dist/server/agent-bridge/python/`（与 bridge_transport 同目录，非 FileNotFound）。
- **状态**：手动 spawn 复现子进程崩溃的命令已构造但**尚未跑完取 stderr**，根因（Python 环境 / 参数）待下一轮定位。本会话未闭环。

## 七、handoff 发布断更诊断（本会话收尾）

- **现象**：8.5 之后 handoff 一篇没发。
- **根因**：`handoff 生产·scan` 自动化（每天 23:05）只收集 session 目录里的 `HANDOFF*.md`，守「项目轴绝不读每日日志」护栏。8.6–8.9 所有工作都写成了 `每日工作总结.md` / 分析 doc，**没有一篇 `HANDOFF*.md`**，所以每天正常退出（exit 0）但 0 产出。最后成功发布就是 8.5 那两篇。
- **本会话动作**：把今晚（MemOS/Hermes 排障）按 HANDOFF 格式补写，交由 scan/publish 发布（即本文档的来由）。

## 可复用配置清单

| 项 | 值 |
|---|---|
| Hermes bin | `D:/hermes-agent/venv/Scripts/hermes.exe` |
| HERMES_HOME | `C:\Users\Administrator\.hermes` |
| WORKSPACE_BASE | `D:\hermes-studio` |
| Studio 端口 / 进程 | 8650 / node v24（PID 5196） |
| OpenClaw Gateway | 18789（看门狗自动重启） |
| OpenClaw Viewer / Hermes Viewer | 18799 / 18800 |
| MemOS 技能进化模型 | `deepseek-v4-flash` @ `https://api.deepseek.com`（模型名去前缀） |
| MemOS 摘要模型 | 待 zhipuai 专用 provider 直通 `glm-4-flash-250414`（v1 拼接待解） |
| kanban.db | `C:\Users\Administrator\.hermes\kanban.db`（空库，需建任务才有内容） |

## 待办 / 风险

- **P0**：MemOS 摘要模型仍未配通（受智谱 v4 坑限制），需确认 MemOS 有无 zhipuai 专用 provider，或换 v1 厂商。
- **P1**：Hermes Studio profile worker 崩溃根因未定位（第六节）。
- **P1**：看板空白是「空库」导致，需实际建任务（或导入示例）才能验证看板展示。
- **P2**：AutoClaw 看门狗不拉起 Hermes 侧进程，机器重启后 18800/13704 需手动救活（或做开机自启，属高危待授权）。
- **方法学沉淀**：① 国内模型接入先分清 v4/v1 协议，别盲信 base_url 字段；② 改 Gateway 插件配置必须补 `plugins.installs` 注册，否则重启即丢；③ 项目交接文档务必用 `HANDOFF*.md` 命名，否则 scan 不收。
