---
layout: default
title: Hermes_Windows原生部署迁移 · 交接文档
date: 2026-07-23 23:30:00 +0800
---

# Hermes Windows 原生部署迁移 + 启动器自启修复 — 交接文档（人读）

> 更新于 2026-07-23（当天多 session）。目录：`D:\hermes-webui\` + `D:\hermes-agent\`，配置 `C:\Users\Administrator\.hermes\config.yaml`。
> 给接手的同学看。本 handoff 聚焦「Docker 版迁 Windows 原生 + 启动器自启/黑框修复 + bash 工具修复」。

---

## 0. 一句话成果

把已停的 Docker 版 Hermes 迁移到 Windows 原生：`D:\hermes-agent`（gateway :8642）+ `D:\hermes-webui`（WebUI :8787），配 `config.yaml` + 自启 VBS，并修通 git_info 黑框、补 Git for Windows + 导入 WSL Ubuntu 修复 bash 工具。

---

## 1. 背景与目标

- Docker 容器 `hermes-agent`/`hermes-webui` 停止后，迁到 Windows 原生进程直接跑（localhost=宿主机，三端发布更顺）。保留 Docker 容器作回退。

---

## 2. 时间线（已完成）

- **核心迁移**：tar 流式同步容器 `/opt/hermes`→`D:\hermes-agent`（排除 `.venv`/`.playwright`）；venv `D:\hermes-agent\venv`（Python 3.13.12，pip 阿里云镜像）；WebUI `D:\hermes-webui` 进程内跑 agent，:8787；gateway `hermes gateway run --replace --accept-hooks`，:8642；config 复用 `C:\Users\Administrator\.hermes`；自启脚本入 Startup；单实例守卫。
- **12:49**：启动窗口闪现 / 黑框排查 → **git_info 黑框修复**（workspace.py/updates.py `_run_git()` 加 `CREATE_NO_WINDOW`）；Startup 残留 `.bak` 清理，仅留 `Hermes-AutoStart.vbs`；启动器加固（`CREATE_BREAKAWAY_FROM_JOB` / `FreeConsole` + `SW_HIDE`）。
- **13:51**：Hermes 慢根因 = 本机无 POSIX bash → 装 **Git for Windows 2.55**（silent，入 Machine PATH `C:\Program Files\Git\bin`）+ 导入 **WSL Ubuntu 24.04**（`wsl --import`，沙箱拦截，用户在真实管理员 PowerShell 执行）。
- **16:54**：bash 工具环境确认：Git Bash + WSL Ubuntu 均可用。

---

## 3. 关键认知 / 必踩的坑

1. **gateway 默认不启用 API server**：必须 `API_SERVER_ENABLED=true` 才启动 api_server 平台。
2. **启用后强制 API_SERVER_KEY**（即使 loopback）：key 存 `D:\hermes-native\api_server.key`，启动脚本读取。
3. **aiohttp 漏装** → `AIOHTTP_AVAILABLE=False` → api_server 静默禁用 → `pip install aiohttp`。
4. **`hermes gateway run --no-supervise` 在原生 Windows 不监听 8642** → 用 `--replace --accept-hooks`。
5. **Docker 的 Linux `.venv`（ELF）不能复制到 Windows** → 必须 Windows 重新 `pip install`。
6. **git_info 黑框**：WebUI `/api/git-info` 调 `subprocess.run(['git',...])` 缺 `CREATE_NO_WINDOW` → 每次弹 CMD 黑框。修：`D:\hermes-webui\api\workspace.py` + `updates.py` 的 `_run_git()` 加 Windows `CREATE_NO_WINDOW`，重启 WebUI 生效。
7. **启动器无窗口**：最终 Startup 入口是 `Hermes-AutoStart.vbs`（非 .bat/.lnk——`.lnk` 被安全策略 COM 拦截）；它调用固定版启动器（`start_hermes.py`/`start_hermes.bat`），用 `CREATE_BREAKAWAY_FROM_JOB` + `FreeConsole()` + `STARTUPINFO(wShowWindow=SW_HIDE)` 彻底无可见窗口。
8. **Startup 正确路径必须含 `Programs`**：`...\Start Menu\Programs\Startup\`，漏 `Programs` 会静默失败。
9. **Git for Windows + WSL Ubuntu 修复 bash**：Hermes `_find_bash()` 优先级 `HERMES_GIT_BASH_PATH → 自带 PortableGit → shutil.which("bash")`。本机两者皆无 → 装 Git for Windows 2.55（`/VERYSILENT /TASKS=addtopath`）+ `wsl --import Ubuntu "C:\wsl\Ubuntu" "D:\hermes-native\tmp\ubuntu-noble-wsl.rootfs.tar.gz" --version 2`（**须先 `New-Item -ItemType Directory -Force -Path "C:\wsl"`**）。沙箱拦截 `wsl` 执行，需用户在真实终端跑。
10. **重启才生效**：当前运行进程 PATH 不含新 Git → 必须等用户重启电脑，启动项以新 PATH 拉起 Hermes。

---

## 4. 部署状态

- WebUI：`D:\hermes-webui`，端口 **8787**（HTTP 200）
- Gateway：`hermes gateway run --replace --accept-hooks`，端口 **8642**（`/v1/models` 返回 `hermes-agent`，带 Bearer key）
- Agent 源码：`D:\hermes-agent`，venv `D:\hermes-agent\venv`（Python 3.13.12）
- 配置：`C:\Users\Administrator\.hermes\config.yaml`
- 自启：`C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes-AutoStart.vbs`
- key 文件：`D:\hermes-native\api_server.key`
- Docker 容器 `hermes-agent`/`hermes-webui` 保持 Exited 未删（回退）
- Git：`C:\Program Files\Git\bin\bash.exe`；WSL：`C:\wsl\Ubuntu`（root）

---

## 5. 关键文件清单

- `C:\Users\Administrator\.hermes\config.yaml` — Hermes 主配置
- `D:\hermes-native\start_hermes.bat` — 启动脚本（设 API_SERVER_ENABLED + 读 api_server.key）
- `D:\hermes-native\api_server.key` — gateway API key
- `C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes-AutoStart.vbs` — 登录自启（无窗口）
- `D:\AI work\workbuddy\2026-07-23-12-06-55\.workbuddy\start_hermes.py` — 加固版启动器
- `D:\hermes-webui\api\workspace.py` + `updates.py` — `_run_git()`（修 CREATE_NO_WINDOW 黑框）
- `D:\hermes-agent\venv` — Windows 原生 agent venv
- `C:\wsl\Ubuntu` — WSL Ubuntu 24.04 rootfs（bash 工具 fallback）

---

## 6. 发布记录

- 未对外发布（本地部署调试）。