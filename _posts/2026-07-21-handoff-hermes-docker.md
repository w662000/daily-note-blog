---
layout: default
title: hermes-webui本地Docker两容器部署 · 交接文档
date: 2026-07-21 23:30:00 +0800
---

# hermes-webui 本地 Docker 两容器部署 — 交接文档（人读）

> 更新于 2026-07-21。项目目录：`D:\hermes-webui\`（compose `docker-compose.two-container.yml`）。
> 给接手的同学看。本 handoff 只聚焦「本地 Docker 两容器（webui + agent）」这一条路径；同期调研的 Back4App/CloudFlare/Render/Koyeb/SnapDeploy 文档为别家平台，不属本项目。

---

## 0. 一句话成果

用官方两容器方案跑通 hermes-webui（WebUI 容器）+ hermes-agent（gateway 容器），WebUI :8787、Agent gateway :8642，完整 Agent 能力（AIAgent）可用，修通网关鉴权/网络/Provider 模型路由。

---

## 1. 背景与目标

- 本机（Windows Docker Desktop）跑 Hermes WebUI（对话界面）+ Agent（执行 shell/工具），两容器通过 Docker bridge 网络互联，Agent 源码以命名卷挂进 WebUI 让其在内 `import run_agent`。
- 网络环境：docker.io 直连被墙（auth.docker.io 断开），ghcr.io 可达，GitHub 大克隆被干扰。

---

## 2. 时间线（已完成）

- **2026-07-21 上午**：两容器方案跑通；修网关（aiohttp 缺失、API_SERVER_ENABLED、API_SERVER_HOST=0.0.0.0、API_SERVER_KEY）；Provider key 实测（Gemini 地区封禁、OpenRouter 可用、HuggingFace 不可达）；开日本代理后 Gemini 通；默认模型切 `openrouter/free`→ 因不支持 tools 改 `nvidia/nemotron-3-nano-30b-a3b:free`；Gemini 免费额度打满切回 OpenRouter；修流式输出页面抖动（overflow-anchor）。
- **2026-07-21 晚**：Hermes GLM 模型白名单；`docker compose up -d --force-recreate` 事故（全量重装 95+ 包近 1 小时）→ 立红线：改 env 只用 `restart`，禁 `--force-recreate`。

---

## 3. 关键认知 / 必踩的坑（重点）

1. **"AIAgent not available" 根因**：agent 源码卷 `hermes-agent-src` 是空的——agent 不在 webui 仓库里。必须首启由 agent 镜像 `/opt/hermes` 填充命名卷，挂到 webui 的 `/home/hermeswebui/.hermes/hermes-agent`，WebUI 启动时 editable 安装 `hermes-agent==0.18.2`。
2. **网关 heartbeat failed 四连坑**（缺一不可）：① agent 容器缺 `aiohttp` → `uv pip install aiohttp`；② `API_SERVER_ENABLED=1` 才启动 HTTP 监听；③ `API_SERVER_HOST=0.0.0.0`（默认 127.0.0.1 仅容器内回环，跨 bridge 访问不到）；④ `API_SERVER_KEY` 必须 webui/agent 一致（本机 `hermes-local-dev-key-2026`）。
3. **Provider key 不生效的 env 坑**：LLM 调用层读 `os.environ`，但 Providers 检测从 `.env` 文件读 → 要把 `GEMINI_API_KEY`/`OPENROUTER_API_KEY`/`GLM_API_KEY` 写成 compose `environment:` 真实环境变量（两个 service 都加），否则聊天 401。
4. **base_url 全局覆盖坑**：切换默认 provider 时，残留的 `base_url: https://openrouter.ai/api/v1` 会被套到 gemini → 401。切 provider 必须清空/改 `base_url`。
5. **镜像拉取**：`python:3.12-slim` 用 `docker.1ms.run/library/python:3.12-slim` 拉后 `docker tag`；agent `nousresearch/hermes-agent:latest`（3.81GB）同走 `docker.1ms.run`。
6. **CRLF 坑**：Windows 克隆把 LF 转 CRLF → `docker_init.bash` shebang 变 `#!/bin/bash\r` → 容器 exec "no such file"。修：git `core.autocrlf=false` + Python 批量剥离 CR。
7. **Providers 页面 "Failed to fetch"**：bedrock_adapter 懒加载 boto3 超时死锁 → 阿里云镜像预装 `boto3==1.42.89`。
8. **样式持久化坑**：`/app/static` 不是挂载卷，直接改容器内文件会被入口 `rsync /apptoo → /app` 覆盖。正确：把 `style.override.css` 挂到 **rsync 源** `C:/Users/Administrator/.hermes/style.override.css:/apptoo/static/style.css:ro`。
9. **🔥 `--force-recreate` 红线**：加 GLM_API_KEY 后误执行 `--force-recreate` 触发 webui 全量重装（rsync 1.2G + pip 95+ 包，近 1 小时）。改 compose env 后用 `docker compose restart`，绝对禁 `--force-recreate`。加 `UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/` 避免重装超时。
10. **Provider 实测结论**：本机出口 IP 受限 → 仅 OpenRouter 真正可用；Gemini 需代理出口；HuggingFace 推理 API 被墙。`openrouter/free` 自动路由器**不支持 tools**，不能做 Agent 默认模型。

---

## 4. 部署状态

- WebUI：`http://localhost:8787`（容器 `127.0.0.1:8787->8787`，healthy，`/health` 200）
- Agent gateway：`127.0.0.1:8642->8642`（容器名 `hermes-agent`），OpenAI 兼容 `/v1/models` 返回 `hermes-agent`
- 启动：`cd D:\hermes-webui && docker compose -f docker-compose.two-container.yml up -d`
- 镜像：webui `hermes-webui-hermes-webui:latest`；agent `nousresearch/hermes-agent:latest`
- `hermes-home` 已改 bind mount `C:/Users/Administrator/.hermes`

---

## 5. 关键文件清单

- `D:\hermes-webui\docker-compose.two-container.yml` — 两容器编排核心（env/卷/端口/key）
- `C:\Users\Administrator\.hermes\config.yaml` — Hermes 主配置（model.default/provider/白名单）
- `C:\Users\Administrator\.hermes\style.override.css` — 持久化样式修复（overflow-anchor:none）
- `D:\hermes-webui\api\workspace.py` / `updates.py` — 含 `_run_git()`（项目「Hermes Windows 原生迁移」在此修黑框）
- `hermes-webui-snapdeploy/README.md`、`hermes-webui-back4app-cloudflare-deploy.md`、`hermes-webui-render-koyeb-deploy.md` — 别家平台调研（非本路径）

---

## 6. 发布记录

- 未对外发布（本地部署调试，无 handoff 文档历史）。后续 Hermes 已迁 Windows 原生，见 handoff「Hermes Windows 原生部署迁移」。