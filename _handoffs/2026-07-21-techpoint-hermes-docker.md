---
layout: default
title: 技术点 · hermes-docker
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · hermes-docker（双容器编排 + 跨容器网关鉴权 + 镜像/依赖国内化）

> 对应项目轴 Handoff：`2026-07-21-handoff-hermes-docker.md`
> 目的：从该项目提炼**可复用技术资产**——「前端容器 + 执行容器」双容器编排范式、跨容器 HTTP 网关的鉴权与监听排错法、受限网络下的镜像与依赖获取、以及容器内文件持久化的正确姿势。下次做任何「WebUI + Worker 双容器」应用可直接复用。

## 一、技术选型

| 选型项 | 选定 | 落选 | 依据 |
|---|---|---|---|
| 部署形态 | **双容器（WebUI + Agent gateway）** | 单容器塞两个进程 | 官方支持路径；两者依赖差异大，混装易互相污染（T1） |
| 容器间通信 | **Docker bridge 网络 + HTTP 网关** | 共享 volume / IPC | Agent 暴露 OpenAI 兼容 `/v1` 接口，WebUI 当普通 provider 调用，解耦（T1） |
| 源码共享方式 | **命名卷（named volume）由 Agent 镜像填充** | 直接 bind mount 宿主目录 | Agent 源码不在 WebUI 仓库里，必须由 Agent 镜像的 `/opt/hermes` 首启填充卷（T1） |
| 配置目录 | **bind mount 宿主 `~/.hermes`** | 匿名卷 | 配置要能在宿主直接编辑、要能跨重建存活（T1） |
| 镜像源 | **`docker.1ms.run` 镜像站 + `docker tag` 改名** | 官方 docker.io 直连 | `auth.docker.io` 被阻断，官方直连拉不动（T1） |
| pip 源 | **`UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/`** | PyPI 官方 | 重装时 95+ 包走官方源必超时（T1） |
| LLM Provider | **OpenRouter** | Gemini（需代理）/ HuggingFace（被墙） | 本机出口 IP 下仅 OpenRouter 直连可用（T1 实测） |
| Agent 默认模型 | **支持 tools 的具体模型**（如 `nvidia/nemotron-3-nano-30b-a3b:free`） | `openrouter/free` 自动路由器 | 自动路由器**不支持 tools**，Agent 无法调用工具（T1，硬约束） |
| 配置变更的重启方式 | **`docker compose restart`** | `docker compose up -d --force-recreate` | recreate 触发入口脚本全量 rsync 1.2G + 重装 95+ 包，耗时近 1 小时（T1 事故，已立红线） |

## 二、实施要点与关键技术

1. **"AIAgent not available" 的根因是空卷**（T1）：WebUI 容器里挂的 `hermes-agent-src` 命名卷初始为空——Agent 源码根本不在 WebUI 仓库中。正解：让 Agent 镜像首启把 `/opt/hermes` 内容填充进该命名卷，再挂到 WebUI 的 `/home/hermeswebui/.hermes/hermes-agent`，WebUI 启动时以 editable 方式安装（`hermes-agent==0.18.2`）。

2. **跨容器网关 heartbeat failed 的四连坑（缺一不可）**（T1）：
   - ① Agent 容器缺 `aiohttp` → `uv pip install aiohttp`；
   - ② `API_SERVER_ENABLED=1` 才会真正启动 HTTP 监听；
   - ③ `API_SERVER_HOST=0.0.0.0`——默认 `127.0.0.1` 只在容器内回环，跨 bridge 网络访问不到；
   - ④ `API_SERVER_KEY` 必须两个容器完全一致。
   这四条构成一个通用排查清单：**依赖装没装 → 开关开没开 → 监听地址对不对 → 鉴权密钥一不一致**。

3. **环境变量读取路径不统一的坑**（T1）：LLM 调用层读 `os.environ`，而 Provider 检测逻辑从 `.env` 文件读。结果是「`.env` 里配了 key，检测显示已配置，实际聊天 401」。正解：把 `GEMINI_API_KEY` / `OPENROUTER_API_KEY` / `GLM_API_KEY` 写进 compose 的 `environment:`（**两个 service 都要加**），成为真实环境变量。

4. **`base_url` 全局覆盖污染**（T1）：切换默认 provider 时，配置里残留的 `base_url: https://openrouter.ai/api/v1` 会被套用到新 provider（Gemini）上 → 401。**切 provider 必须同步清空或改写 `base_url`。**

5. **镜像获取绕行**（T1）：`docker pull docker.1ms.run/library/python:3.12-slim` 后 `docker tag` 回官方名，Dockerfile 无需改动。大镜像（Agent 镜像 3.81GB）同法。

6. **CRLF 行尾破坏 shebang**（T1）：Windows 下 git 克隆默认把 LF 转 CRLF，`docker_init.bash` 的 shebang 变成 `#!/bin/bash\r`，容器内 exec 报 "no such file"（极具迷惑性——文件明明存在）。双修：`git config core.autocrlf false` + 用脚本批量剥离已存在文件的 CR。

7. **懒加载依赖导致页面超时**（T1）：Providers 页面 "Failed to fetch" 根因是 `bedrock_adapter` 懒加载 `boto3` 时联网超时形成死锁。解法：镜像内预装 `boto3==1.42.89`（走国内源），让懒加载瞬间命中。

8. **容器内文件被入口脚本覆盖**（T1）：`/app/static` 不是挂载卷，直接改容器内文件会被入口的 `rsync /apptoo → /app` 覆盖。正解是**挂到 rsync 的源目录**：`C:/Users/Administrator/.hermes/style.override.css:/apptoo/static/style.css:ro`。通用规律：**改容器内文件前先确认入口脚本是否会做同步覆盖，要挂就挂在同步链的上游。**

9. **`--force-recreate` 红线事故（本项目最大教训）**（T1）：为加一个环境变量执行了 `--force-recreate`，触发镜像 init 脚本全量重跑（rsync 1.2G + pip 95+ 包），耗时近 1 小时。后续固化为跨会话红线：**改 compose env 只用 `restart`，禁用 `--force-recreate`**（除非用户明确同意）。

10. **recreate 的连带副作用**（T1，7-22 日志）：那次 recreate 还因 compose 宿主挂载路径漏写盘符 `C:`，Docker 把它当相对路径，在 D 盘根自动创建了 `D:\c`(510M)、`D:\d`(226M) 两个垃圾目录，次日才清理。**教训：挂载路径必须写全盘符，Windows 下漏盘符不会报错、会静默造垃圾。**

11. **缓存型配置的生效机制**（T1，7-22 日志）：应用在 agent 构造时缓存配置文件（非实时读盘），改完必须重启进程；但用 `restart` 即可，无需 recreate——实测重启后接口已返回新内容。

12. **前端流式输出抖动修复**（T1）：流式渲染时页面自动锚定导致抖动，用 CSS `overflow-anchor: none` 抑制。

## 三、模块职责划分

- **WebUI 容器**：只负责对话界面与 provider 路由；不直接执行 shell/工具，通过 HTTP 调 Agent 网关。
- **Agent 容器（gateway）**：执行层，暴露 OpenAI 兼容 `/v1/models`、`/v1/chat/completions`；持有 shell/工具能力。
- **命名卷 `hermes-agent-src`**：源码分发通道，由 Agent 镜像单向填充、WebUI 只读消费。
- **bind mount `~/.hermes`**：配置与样式的**唯一真相源**，跨容器重建存活。
- **Docker bridge 网络**：容器间唯一通信面；因此 Agent 必须监听 `0.0.0.0` 而非回环。
- **compose 文件**：端口、env、卷、密钥的单一声明点；改这里就等于改全局。

## 四、如何选型（可复用的决策方法论）

- **单容器 vs 多容器**：两个组件依赖栈差异大（一个是 Web 框架、一个是重型执行环境）就拆容器；共享的是**数据/源码**而非进程，用卷传递。
- **容器间通信协议选型**：优先选目标组件已有的标准接口（此处是 OpenAI 兼容 HTTP），比自造 RPC 或共享文件省事，也便于把 Agent 当普通 provider 复用。
- **"配置不生效"的通用排查顺序**：依赖是否安装 → 功能开关是否打开 → 监听地址/端口是否对外 → 鉴权是否两端一致 → 配置读取路径（`os.environ` vs `.env` 文件）是否一致 → 是否有全局字段（如 `base_url`）覆盖。按这个顺序走，不要乱试。
- **受限网络下的依赖获取**：镜像走国内镜像站 + `docker tag` 还原原名（不污染 Dockerfile）；Python 包走国内 index（用环境变量注入，不改代码）。原则是**替换获取通道，不改工程结构**。
- **重启动作的破坏力分级**：`restart`（无损）< `up -d`（可能重建变更的服务）< `--force-recreate`（必然重跑 init）。**任何操作前先问它会不会触发 init 脚本重跑**。
- **Provider 可用性以本机实测为准**：同一把 key 在不同出口 IP 下结果完全不同，官方"支持地区"文档只是参考，必须自己打一遍。

## 五、深化学习指引

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Compose 服务/网络/卷语义 | docs.docker.com/compose | 官方文档 | T0 |
| 命名卷首启填充与生命周期 | Docker Volumes 官方文档 | 官方文档 | T0 |
| bridge 网络与容器间寻址 | Docker Networking 官方文档 | 官方文档 | T0 |
| `restart` vs `up --force-recreate` 差异 | Docker Compose CLI 文档 | 官方文档 | T0 |
| Hermes Agent gateway / API server 参数 | Hermes 官方文档 | 官方文档 | T0 |
| OpenRouter 模型能力（tools 支持） | openrouter.ai/docs | 官方文档 | T0 |
| `overflow-anchor` 滚动锚定 | MDN | 官方文档 | T0 |
| git `core.autocrlf` 与 shebang | git-scm 文档 | 官方文档 | T0 |
| 国内镜像站可用性与稳定度 | 自己实测（`docker.1ms.run`） | 实测 | T1 |
| 本机出口 IP 下各 Provider 连通性 | 自己实测 | 实测 | T1 |
| `openrouter/free` 路由器不支持 tools | 自己实测 | 实测 | T1 |
| init 脚本 rsync 1.2G 的具体触发条件 | 未逐条验证镜像 entrypoint | 推测 | T2（待核实） |

## 六、技术结合点

- **命名卷填充 + editable 安装**：卷负责把 Agent 源码送进 WebUI 容器，editable 安装负责让 WebUI 进程内直接 `import` 到它。只有卷没有安装 → 找不到模块；只有安装没有卷 → 装的是空目录。两者配合才让"跨容器共享执行能力"成立。
- **`API_SERVER_ENABLED` + `0.0.0.0` + 共享 KEY**：分别解决"服务起不起""外面够不够得着""够得着让不让进"。三者是串联关系，任一缺失表现都是同一个 heartbeat failed，所以必须当成一个整体清单来查。
- **国内镜像站 + 国内 pip index**：前者解决拉镜像，后者解决容器内装包。只做前者，一旦触发重装还是卡在 pip；两者齐备，即使误触 recreate 也能在可接受时间内恢复——这是把"事故"降级为"麻烦"的关键。
- **bind mount 配置目录 + restart-only 红线**：配置在宿主可编辑，改完只需 restart 即可生效，从而**根本上消除了使用 recreate 的动机**。这是"预防事故"优于"事后补救"的典型设计。
- **rsync 上游挂载 + 只读标记**：把定制样式挂在同步源并加 `:ro`，既保证覆盖生效方向正确，又防止容器写回污染宿主文件。

---
> 本文为技术点轴文章（对应 Handoff 2026-07-21）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合点。
