---
layout: default
title: 技术点 · hermes-windows
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · hermes-windows（把容器化 Agent 迁移到 Windows 原生 · 无窗口自启 · POSIX 环境补齐）

> 对应项目轴 Handoff：`2026-07-23-handoff-hermes-windows.md`
> 目的：从该项目提炼**可复用技术资产**——「Docker 容器 → Windows 原生进程」迁移的要点、Windows 下完全隐藏窗口的后台进程拉起、gateway 鉴权与监听坑、`localhost` 即宿主机带来的便利、以及给 Windows 补 POSIX bash 环境的方法。下次任何"本地长期运行服务迁 Windows 原生"场景可直接复用。

## 一、技术选型

| 选型项 | 选定 | 落选 | 依据 |
|---|---|---|---|
| 运行形态 | **Windows 原生进程**（agent + WebUI 各跑进程） | 保留 Docker 容器 | 容器停了很麻烦；原生进程下 `localhost` 即宿主机，三端发布链路更顺；保留 Docker 作回退（T1） |
| 配置目录 | **复用在宿主的 `~/.hermes`** | 容器内配置 | 配置不丢、可直编（T1） |
| 网关启动方式 | **`hermes gateway run --replace --accept-hooks`** | `--no-supervise` | 原生 Windows 下 `--no-supervise` 不监听 8642（T1 实测） |
| 鉴权配置落点 | **`~/.hermes/.env`（持久化）** | 仅在启动脚本里 `set` | 复杂启动链下子进程拿不到只在当前 shell 设的变量（T1） |
| 自启入口 | **`.vbs` 隐藏式脚本** | `.bat` / `.lnk` | `.lnk` 被安全策略 COM 拦截；`.bat` 双击会留窗口；VBS 可彻底无窗口（T1） |
| 启动器实现 | **Python 启动器（subprocess + 窗口标志）** | 纯 bat | 需要精细控制「脱离父进程 + 完全隐藏窗口」（T1） |
| POSIX 环境 | **Git for Windows + WSL Ubuntu 24.04 双重补齐** | 仅其一 | Git Bash 主用；WSL 作 fallback（T1） |
| Python 环境 | **Windows 重新建 venv** | 复用 Linux `.venv` | 容器里的 `.venv` 是 ELF 二进制，Windows 无法执行（T1，硬约束） |

## 二、实施要点与关键技术

1. **Docker 的 Linux venv 不能跨平台复制**（T1，硬结论）：容器里 `/opt/hermes` 下的 `.venv` 含 ELF 格式可执行文件，复制到 Windows 后 `pip`/`python` 全废。**必须在本机用对应的 Windows Python 重新 `pip install` 建 venv**（本项目用 Python 3.13.12 + 阿里云 pip 镜像）。

2. **gateway 的 API server 不是默认开**（T1，与 Docker 版同样适用）：必须同时满足三件事——
   - `API_SERVER_ENABLED=true`（才启动 api_server 平台）；
   - 启用后**强制**要求 `API_SERVER_KEY`（即使 loopback 也要）；
   - `aiohttp` 必须已安装——漏装时 api_server 会**静默禁用**（日志里 `AIOHTTP_AVAILABLE=False`），不会报错，极难发现。

3. **环境变量必须落到 `.env` 而非只 `set`**（T1）：只在启动脚本里 `set API_SERVER_ENABLED=true`，复杂启动链下子进程拿不到 → 表现就是"网关起来了但没有 API 接口"。正解：写进 `C:\Users\Administrator\.hermes\.env`，启动脚本读取它。**通用规律：会被子进程继承的配置，优先用 `.env`/文件，别赌进程继承链。**

4. **`--no-supervise` 在原生 Windows 不监听端口**（T1）：改用 `hermes gateway run --replace --accept-hooks` 才能正常监听 8642。这是 Docker 迁移到原生后第一个必须改的启动参数。

5. **容器迁移用 tar 流式同步**（T1）：`docker cp` / tar 流式把 `/opt/hermes` 同步到 `D:\hermes-agent`，**排除 `.venv` 和 `.playwright`**（二进制不跨平台），随后本机重建 venv。容器保留 Exited 状态不删，作为回退。

6. **git_info 黑框修复**（T1）：WebUI 的 `/api/git-info` 调 `subprocess.run(['git', ...])` 时缺窗口标志，每次浏览器切前台就弹黑色 CMD 框。修法：在 `workspace.py` 与 `updates.py` 的 `_run_git()` 里加 Windows `CREATE_NO_WINDOW` 标志，重启 WebUI 生效。**规律：凡是桌面应用里 spawn 子进程，都要显式控制窗口可见性。**

7. **完全无窗口拉起的核心组合**（T1）：最终 Startup 入口是 VBS，它调用一个 Python 启动器，启动器用 `CREATE_BREAKAWAY_FROM_JOB`（脱离父进程树，避免随登录会话退出被杀）+ `FreeConsole()` + `STARTUPINFO(wShowWindow=SW_HIDE)`（彻底无窗口）拉起 gateway 与 WebUI。**三个标志缺一个都可能留下可见窗口或进程随父死。**

8. **Startup 路径必须含 `Programs`**（T1）：`...\Start Menu\Programs\Startup\` 才是真正生效的自启目录，漏掉 `Programs` 会**静默失败**——脚本放对位置却从不自启。正确路径：`C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`。

9. **`.lnk` 被安全策略拦截**（T1）：本机安全策略会用 COM 拦截 `.lnk` 自启，所以自启入口选 VBS 而非 `.lnk`/`.bat`。**在受限策略机器上，自启载体选型要先确认策略对哪种文件类型放行。**

10. **补 POSIX 环境的真实路径**（T1）：
    - Git for Windows 2.55 用 `/VERYSILENT /TASKS=addtopath` 静默安装，加入 **Machine PATH** (`C:\Program Files\Git\bin`)；
    - WSL Ubuntu 24.04 导入：`wsl --import Ubuntu "C:\wsl\Ubuntu" "D:\...\ubuntu-noble-wsl.rootfs.tar.gz" --version 2`，**且必须先 `New-Item -ItemType Directory -Force -Path "C:\wsl"`** 建父目录，否则报路径找不到。
    - Hermes 的 `_find_bash()` 优先级：`HERMES_GIT_BASH_PATH` → 自带 PortableGit → `shutil.which("bash")`；本机前两者皆无时才落到 `which`，所以装好 Git for Windows 即命中。

11. **PATH 变更要重启才生效**（T1，重要）：当前运行进程（本次迁移期间已启动的 Hermes）PATH 不含新装的 Git，必须等**用户重启电脑**后，自启链以新 PATH 拉起才生效。**不要手动重启进程去试——重启可能打断既定自启验证节奏。**

12. **沙箱对系统级工具的拦截**（T1）：WorkBuddy 沙箱会注入 `PYTHONPATH` 导致文件删除 hook 异常，且禁用 `wsl` 等系统级工具。WSL 导入这类操作要在**真实管理员 PowerShell** 执行，不能靠沙箱内的命令。

13. **PID/lock 真实路径**（T1）：gateway 的 PID/lock 在 `%LOCALAPPDATA%\hermes\gateway.{pid,lock}`（即 `AppData\Local\hermes\`），**不是** `.hermes\`。早期清错位置导致一直 fail-closed——**查进程状态前先确认文件真实落点。**

## 三、模块职责划分

- **`D:\hermes-agent`**：Agent 执行层（gateway :8642），Windows 原生 venv；与 Docker 版职责相同，只是进程形态变了。
- **`D:\hermes-webui`**：WebUI 进程（:8787），进程内调用 agent。
- **`~/.hermes`**：配置唯一真相源（`config.yaml` + `.env` + 记忆/脚本），跨形态复用。
- **Docker 容器（Exited 未删）**：回退方案，验证原生版有问题时可临时起回。
- **Python 启动器 + VBS**：职责是「完全无窗口 + 脱离会话 + 清理旧 PID/lock + 带正确 env 拉起」；env 来自 `.env` 文件。
- **Git for Windows / WSL**：为 Hermes 的命令执行工具提供 POSIX bash 环境，是两个独立 fallback。

一句话：**配置在中心目录，进程在宿主，启停由无窗口启动器统一管控，POSIX 环境作为能力底座。**

## 四、如何选型（可复用的决策方法论）

- **"要不要迁到原生"的判断**：如果容器停机后重启繁琐、且应用需要常访宿主 `localhost` 服务 → 迁原生更省心。但**保留容器作回退**，迁完验证通过再考虑删容器。
- **跨平台迁移的二进制处理**：先问"这些文件里有可执行二进制/原生库吗"。有 → 排除它们、在目标平台重建（venv / 依赖）；纯代码/数据才直接复制。
- **"配置不生效"的 Windows 版排查顺序**：是否在子进程继承链里（用 `.env` 兜底）→ 是否关键依赖漏装（如 aiohttp 静默禁用）→ 启动参数是否适配目标形态（如 `--no-supervive` 在原生 Windows 不监听）→ PID/lock 路径是否找对。
- **无窗口后台进程**：需要"脱离父进程 + 隐藏窗口"两个维度同时处理，Windows 下没有单一开关能全做到，必须组合 `CREATE_BREAKAWAY_FROM_JOB` + `FreeConsole` + `SW_HIDE`。
- **自启载体选型先看策略**：先确认机器安全策略对 `.lnk`/`.bat`/`.vbs` 各放不放行，再选载体，别默认用 `.lnk`。
- **PATH 类变更一律按"下次重启生效"规划**，不要当场手动重启去验证，避免打断既定流程。

## 五、深化学习指引

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| Hermes gateway 启动参数与 API server | Hermes 官方文档 | 官方文档 | T0 |
| Windows `CREATE_NO_WINDOW` / `STARTUPINFO` | Microsoft Win32 API 文档 | 官方文档 | T0 |
| Windows Startup 文件夹路径规范 | Microsoft 文档 | 官方文档 | T0 |
| Git for Windows 静默安装参数 | git-for-windows.github.io | 官方文档 | T0 |
| WSL `--import` 与 rootfs | Microsoft WSL 文档 | 官方文档 | T0 |
| subprocess 窗口控制（Python） | Python `subprocess` / `subprocess.CREATE_NO_WINDOW` 文档 | 官方文档 | T0 |
| `.env` 在应用启动链中的加载 | Hermes 配置文档 | 官方文档 | T0 |
| ELF venv 不可跨平台复制 | 自己实测 | 实测 | T1 |
| `--no-supervise` 原生 Windows 不监听 | 自己实测 | 实测 | T1 |
| 沙箱对 `wsl` / 删除 hook 的拦截 | 自己实测（WorkBuddy 沙箱） | 实测 | T1 |
| `.lnk` 被本机安全策略拦截 | 自己实测 | 实测 | T1 |
| VBS 无窗口拉起最优组合 | 自己实测 | 实测 | T1 |

## 六、技术结合点

- **原生进程 + 复用 `~/.hermes`**：前者去掉容器开销并让 `localhost` 直达宿主，后者保证配置、记忆零迁移成本。两者合起来，迁移的代价只剩"重建 venv"，其余全部平滑。
- **`.env` 持久化 + Python 启动器读它**：`.env` 解决"配置跨子进程继承"的可靠性，启动器解决"带正确 env 且隐藏窗口拉起"。只设 shell 变量不写文件 → 子进程拿不到；只写文件不做无窗口拉起 → 桌上留黑框。
- **`CREATE_BREAKAWAY_FROM_JOB` + `FreeConsole` + `SW_HIDE`**：分别解决"进程随登录会话退出被杀""残留控制台""可见窗口"三个独立问题。缺任一都会出现一种可见/可死的现象，必须三者齐备。
- **Git for Windows + WSL 双重 POSIX 环境**：Git Bash 命中主路径，WSL 兜底。Hermes 的 `_find_bash` 优先级设计让装好其一即生效，二者并存时互不干扰——这是"能力底座"该有的冗余度。
- **tar 排除二进制 + 本机重建 venv**：排除 `.venv`/`.playwright` 保证复制的是可移植的纯代码，本机重建保证执行体适配 Windows。两者配合才把"容器迁移"从"整体搬运"降级为"代码搬运 + 依赖重建"。
- **Docker 回退保留**：它不是多余——它是迁移期的安全网，让"先迁、验证、再弃"成为可能，避免一锤子迁移失败就服务中断。

---
> 本文为技术点轴文章（对应 Handoff 2026-07-23）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合点。
