---
layout: default
title: 技术点 · MemOS 接入 AutoClaw/Hermes 排障（看板空白 · 网关 slots 重置 · 智谱 v4 模型接入）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · MemOS 接入 AutoClaw/Hermes 排障（看板空白 · 网关 slots 重置 · 智谱 v4 模型接入）

> 对应项目轴 Handoff：`2026-08-09-handoff-memos-接入-autoclaw_hermes-排障-看板空白-网关-slot.md`
> 目的：把这轮「Hermes/AutoClaw 排障」里可复用的**技术资产**抽出来——环境变量与数据路径的绑定关系、网关插件注册的隐藏约束、国产模型 openai_compatible 的 v4/v1 协议坑、以及一套「先查实再下结论」的排障纪律。下次遇到同类看板空白 / 插件重启丢配置 / 模型接不通，能直接对照定位。

## 一、技术选型

| 选型项 | 选定 | 落选 | 依据 |
|---|---|---|---|
| 看板后端环境变量修复 | **`setx /M HERMES_BIN` + 全套 env（含 HERMES_HOME）** | 改 `start_studio.ps1` 脚本 | 用户要求「不碰配置、不重启」；Machine 级变量能被开机自启的 PowerShell 继承，一个脚本都不用改（T1 实测） |
| 网关插件持久化 | **补 `plugins.installs["memos-local-plugin"]` 注册** | 只改 `slots.memory` 字段 | 缺 installs 注册时，网关 normalize 会在重启时把 slot 重置为 none（只改内存不写盘），补注册才持久（T1 读源码定位） |
| 技能进化模型 | **`deepseek-v4-flash` @ `https://api.deepseek.com`** | 智谱 GLM v4 | 智谱 v4 真实 chat 路径是 `/v4`，MemOS 的 openai_compatible 强制拼 `/v1` 永远 404；DeepSeek 端点末不含 /v1，拼完正好命中（T0 一手实测） |
| 摘要模型 | 待 zhipuai 专用 provider 直通 `glm-4-flash-250414` | 走 openai_compatible 配智谱 | v1 强制拼接下智谱 v4 方程无解（T1 实测 404） |
| Node 运行时 | **v24.19.0 LTS，与 22.22.2 并存** | 覆盖旧版 | hermes-web-ui engines 要求 node>=23；并存保留回滚余地（T1） |
| 启动方式 | 前台 `node ...mjs` + 全套 env | `.cmd` spawn detached server | detached 子进程在沙箱里活不下来会被回收（T1） |

## 二、实施要点与关键技术

1. **看板空白先做「双层根因」拆分**：第一层是 ENOENT（env 缺 `HERMES_BIN` → 后端 spawn hermes 找不到可执行 → 整块空白）；第二层更关键——`kanban.db` 本来就是**空库（0 任务）**，状态机 triage→todo→scheduled→ready→running→blocked→done 全 0。只修崩溃不查清空库，会一直误以为「还没修好」（T1）。
2. **`HERMES_HOME` 决定 kanban.db 位置**：缺 HOME 时数据落到 `%LOCALAPPDATA%\hermes\kanban.db`，有 HOME 时落到 `C:\Users\Administrator\.hermes\kanban.db`，**两个库互不相通**。看板「空」可能只是读错了库，不一定是故障——这是当天最容易误判的坑（T1 一手定位）。
3. **环境变量要成套带全**：手动拉起时只带 `HERMES_BIN`+`PORT` 会丢工作区与模型列表（漏 `HERMES_HOME`/`WORKSPACE_BASE` → hermes.exe 退出码 1）。正确做法是把 `.ps1` 里的全套 env（HERMES_AGENT_ROOT / HERMES_HOME / WORKSPACE_BASE / GATEWAY_* / 代理）原样提出，并 `unset PYTHONPATH` 防止污染内嵌 Python（T1）。
4. **网关插件重启即丢的实测定性**：磁盘 `openclaw.json` 的 `slots.memory` 值本就正确，但 `plugins` 块缺 `installs` 注册；Gateway 启动 normalize 时发现 slot 指向的插件没在 installs 表里 → 重置为 none。**这层重置只改内存不写盘**，所以磁盘文件一直是对的不代表生效。补写 `plugins.installs["memos-local-plugin"]`（`source:path` + `installPath` + `version`）才真正持久（T1 读 CHANGELOG #3192 + 源码）。
5. **智谱 v4 接入必 404 的根因（一手实测）**：MemOS `openai_compatible` 拼接逻辑 = `base_url + "/v1/chat/completions"`；智谱 BigModel v4 真实路径是 `.../api/paas/v4/chat/completions`（末是 `/v4`，没 v1）。实测 `POST /v4` → 200，拼出 `/v4/v1` → 404。只要 MemOS 强制拼 `/v1`，智谱 v4 在 openai_compatible 下**方程无解**，活清单 12 家里只有 GLM 是 v4 协议（T0 实测）。
6. **DeepSeek 模型名必须去前缀**：填 `deepseek-v4-flash`（去掉活清单 id 的 `deepseek/` 前缀），否则服务端拒（`only accept deepseek-v4-flash / deepseek-v4-pro`）。端点 `https://api.deepseek.com` 末不含 /v1，MemOS 拼出 `/v1/chat/completions` 正好命中官方端点，实测返回 `reasoning_content`（T0 实测）。
7. **Node 升级要并存不覆盖**：下载 zip 解压到独立版本目录，与旧版并存；停旧 PID → 用 v24 node 拉起 mjs。注意 Git Bash 下 curl 写文件必须用 Windows 风格 `C:/Users/...` 路径，`/c/Users/...` 会报「系统找不到指定的文件」（T1 踩坑）。
8. **沙箱里跑不了 `.ps1`/`cscript`**：前者被 ExecutionPolicy 拦、后者被当 LOLBin 拦。等效做法：提取脚本 env，直接 `node .../hermes-web-ui.mjs start --port 8650 --no-open`。**detached 子进程在沙箱里活不下来会被回收**，必须前台 exec（T1）。

## 三、模块职责划分

- **Hermes 可执行（hermes.exe）**：看板后端 spawn 的对象，强依赖 `HERMES_BIN` 与 `HERMES_HOME` 才能正确读取 kanban.db 与 profile。
- **HERMES_HOME 变量**：决定数据根与看板库的物理位置，是「读对库」的唯一开关。
- **AutoClaw Gateway（18789）**：插件注册与 slot 分配的仲裁者；启动 normalize 会校正缺注册的 slot。看门狗只自动重启 OpenClaw 网关，不拉起 Hermes 侧进程。
- **MemOS 插件（memos-local-plugin）**：记忆/技能自进化组件，两个模型（摘要/进化）需各自配通；其内部 `openai_compatible` 对 base_url 有 `/v1` 强制拼接约束。
- **Node 运行时**：hermes-web-ui 的运行底座，版本需 >=23；多版本并存由绝对路径选择。
- **机器级环境变量（setx /M）**：覆盖启动脚本漏配的最优层，开机自启链继承，无需改脚本。

## 四、如何选型（可复用的决策方法论）

- **「X 和 Y 是不是同一个」一律先默认不同**：用户以「区别 / 分别」框架提问时，调查差异而非合并。本例 Hermes **Studio**（npm `hermes-web-ui` = EKKOLearnAI/hermes-studio，TypeScript）与 **WebUI**（NESquena/hermes-webui，Python）是两条独立开发线，名字撞车纯属 npm 包名巧合。结论必须拉 T0 来源（仓库 metadata / registry / git history）再下，不能凭单个本地文件反推。
- **排障先做「双层根因」再动手**：看板空白 = 崩溃层 + 空库层，只修一层会误判。任何「界面没东西」先确认「是渲染崩了还是数据真没有」。
- **配置被重置要先读源码定性是「内存态」还是「磁盘态」**：本例重置只改内存不写盘，所以单纯改字段没用，必须补 installs 注册让 normalize 放过。
- **国内模型接入先分清 v4/v1 协议**，别盲信 base_url 字段：openai_compatible 的默认 `/v1` 拼接对 v4 厂商是死路，先看厂商真实 endpoint 再选接入方式。

## 五、深化学习指引

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Hermes kanban / profile 机制、HERMES_HOME 作用 | Hermes 官方源码 + `hermes kanban --help` 实核 | 官方/自测 | T0 |
| AutoClaw Gateway 插件注册与 normalize 逻辑 | openclaw.json 结构 + CHANGELOG #3192 + 源码 | 官方/自测 | T1 |
| 智谱 BigModel v4 API（/v4 路径，非 /v1） | open.bigmodel.cn 官方文档 | 官方 | T0 |
| DeepSeek API（端点末不含 /v1、模型名去前缀） | platform.deepseek.com 官方文档 | 官方 | T0 |
| MemOS openai_compatible 拼接约束 | MemOS 官方文档/源码 | 官方 | T1（v4 厂商支持待逐一核实） |
| Node engines 与多版本并存 | nodejs.org 官方文档 | 官方 | T0 |
| `setx /M` 系统级环境变量 | Microsoft 官方文档 | 官方 | T0 |
| Electron/Hermes 启动器编码与单实例锁 | 待补具体参考 | 待补 | T2 |

## 六、技术结合点

- **HERMES_BIN + HERMES_HOME 是一对**：缺 BIN → 崩溃空白；缺 HOME → 读错库空白。两者共同决定「看板能不能显示、显示的是不是正确的库」，排查时必须一起带全。
- **setx /M + 启动脚本漏配**：系统级变量覆盖脚本漏配，实现「不碰配置、不重启」也能修好整条启动链——环境变量层是比改脚本更稳的修复平面。
- **网关 installs 注册 + slot 分配**：缺 installs 注册时 slot 在重启被 normalize 重置，补注册让 slot 持久。这是「配置看着对但重启就丢」类问题的通用定位套路（先判内存态 vs 磁盘态）。
- **智谱 v4 协议坑 + DeepSeek 备选**：v4 厂商在 openai_compatible 下方程无解 → 换末不含 /v1 的 DeepSeek 端点 + 去前缀模型名才接通。协议差异直接决定选型结果，不是模型能力问题。
- **排障纪律 + T0 实证**：「先默认不同、再拉 T0 实证」「先查实再下结论」是贯穿本例的护栏——无论是断定两个 UI 是否同一，还是定位插件重置根因，靠的都是一手来源而非反推。这条纪律本身是比具体修复更值钱的可复用资产。

---
> 技术点轴文章（对应 Handoff 2026-08-09）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合点。
