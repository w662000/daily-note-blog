---
layout: default
title: 每日工作总结 · 2026-07-23
date: 2026-07-23 23:30:00 +0800
---

# 每日工作总结 · 2026-07-23

## 一、今日完成事项

1. **Hermes 完成 Windows 原生部署**
   把已停的 Docker 版 Hermes 迁移到 Windows 原生运行：agent 跑在 `D:\hermes-agent`，Web 界面（端口 8787）和网关接口（端口 8642，兼容 OpenAI 格式）都已通；配置沿用原来的 `.hermes` 目录。Docker 容器保留未删，作为回退。

2. **修复 Hermes「连接已断开」并做到无窗口启动**
   一连串排错：之前窗口被误关导致网关死掉、清理 PID 的位置找错、沙箱里回收站不可用卡死、API 服务开关没传进子进程。改法——把开关和密钥写进 `.hermes/.env`、用 Python 启动器以「脱离父进程 + 完全隐藏窗口」的方式拉起，登录自启入口也换成隐藏式 VBS。现在桌面不再有 Hermes 黑窗口，8787/8642 正常监听。

3. **顺手消除 Web 界面切窗口时的黑框闪烁**
   发现浏览器切到前台时弹出黑框，是 Hermes 后台调 `git` 命令没隐藏窗口所致，已在 `workspace.py`、`updates.py` 两处补上隐藏窗口标志并重启生效。

4. **补齐 Hermes「慢/卡」的根因——本机没有 POSIX 环境**
   Hermes 跑命令工具极慢，因为机器上既没有 Git for Windows、也没有可用 WSL。今天装好了 Git for Windows（已加入系统 PATH），又下载并导入了 WSL Ubuntu 24.04。两套环境就位后，本地命令工具恢复正常，重启即可生效。

5. **生成一张「悟空踩五彩祥云」高清壁纸**
   因画布插件连不上，直接走生图工具出了一张 1920×1080 的壁纸（悟空主题）。

6. **建立 Gridea 浓缩版每日总结工作流**
   按你的要求，把每日总结压成 ≤200 字放进 Gridea Pro 待发布目录（手动点同步发布），统一命名为 `YYMMDD工作总结.md`，并补回了 7/18–7/21 几篇；新建了 23:35 的自动化专门干这事。

7. **梳理并加固「三端自动发布」链路**
   - 把发布流程「教会」Hermes，万一以后卸载 WorkBuddy、只剩 Hermes 也能自动发布：脚本副本进了 Hermes 目录、更新了发布手册、预建了两个「暂停态」定时任务。
   - 查清 Ech0（说说）与 daily-note-blog 是两套独立系统，并核实了 Ech0 官方推荐的部署方式、本地数据位置，做了在线备份脚本。
   - **决策：从自动发布里移除 Ech0（说说）**，最终只保留「博客 + 语雀 + Gridea 浓缩版」三路。

## 二、关键决策 / 注意事项

- **API 服务开关必须写进 `.hermes/.env`**（环境变量名 `API_SERVER_ENABLED`、`API_SERVER_KEY`），不能只在启动脚本里 `set`，复杂启动链下子进程会拿不到。
- **Gateway 的 PID/lock 真实路径是 `%LOCALAPPDATA%\hermes\gateway.{pid,lock}`**（即 `C:\Users\Administrator\AppData\Local\hermes\`），不是 `.hermes\`——之前清错位置一直 fail-closed。
- **`aiohttp` 漏装会导致 API 网关被静默禁用**，必须确认已安装。
- **WorkBuddy 沙箱会注入 `PYTHONPATH` 导致文件删除 hook 异常，且禁用 `wsl` 等系统级工具**——这类操作要在真实管理员终端执行（如 WSL 导入就是在真实 PowerShell 完成的）。
- **Git Bash 已加入 Machine PATH**（`C:\Program Files\Git\bin`）；WSL Ubuntu 导入前必须先建好 `C:\wsl` 父目录，否则报路径找不到。
- **Gridea 浓缩版（23:35）是有意保留的**，与博客全文版不重复，不是矛盾。
- **发布脚本里硬编码了本机端口（如 localhost:6277）**，将来若把 Ech0 迁到 VPS 需要改地址。
- 当天把 7/18–7/21 的旧稿就地浓缩并重命名为统一格式，全文源仍保留在博客与项目目录。

## 三、生成的有用文件

| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| Hermes 无窗口启动器 | `D:\AI work\workbuddy\2026-07-23-12-06-55\.workbuddy\start_hermes.py` | 清理 PID/lock、隐藏窗口拉起 gateway+WebUI |
| Hermes 启动脚本 | `D:\hermes-native\start_hermes.bat` | 设环境变量并调用上面的 Python 启动器 |
| 登录自启入口（VBS） | `C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes-AutoStart.vbs` | 开机隐藏式自启 Hermes |
| API 网关密钥 | `D:\hermes-native\api_server.key` | 网关 8642 接口的访问密钥 |
| API 服务配置 | `C:\Users\Administrator\.hermes\.env` | 持久化 `API_SERVER_*` 开关与密钥 |
| Hermes agent 源码 | `D:\hermes-agent` | Windows 原生部署的 agent 代码与 venv |
| Hermes WebUI 源码 | `D:\hermes-webui` | Web 界面（已补 git 窗口隐藏修复） |
| 启动器日志 | `D:\hermes-native\logs\launcher.log` | 启动器运行输出 |
| Hermes 发布脚本副本 | `C:\Users\Administrator\.hermes\memories\publish_daily_summary.py`<br>`sync_logs_to_github.py`<br>`gridea_write_condensed.py` | 卸载 WB 后由 Hermes 独立发布用 |
| Hermes 兜底定时任务 | `C:\Users\Administrator\.hermes\cron\jobs.json` | 两个「暂停态」每日发布任务（接管道具） |
| Hermes cron 配置脚本 | `D:\hermes-native\setup_hermes_publish_cron.py` | 幂等重建 Hermes 兜底定时任务 |
| WSL rootfs | `D:\hermes-native\tmp\ubuntu-noble-wsl.rootfs.tar.gz` | Ubuntu 24.04 WSL 导入包（340MB，已校验完整） |
| Ech0 备份脚本 | `D:\shuoshuo\backup_ech0.py` | 在线备份 Ech0 数据库（合并 WAL）并导出 Markdown/JSON |
| Ech0 备份产物 | `D:\shuoshuo\backups\ech0_backup_20260723_175506.db`<br>`echos_export_20260723_175506.{md,json}` | 当日首次备份的 5 篇文章 |
| 悟空壁纸 | `D:\AI work\workbuddy\generated-images\Cinematic_fantasy_wallpaper__1_2026-07-23T06-00-00.png` | 1920×1080 主题壁纸 |
| Gridea 稿件 | `C:\Users\Administrator\Documents\Gridea Pro\posts\YYMMDD工作总结.md` | 浓缩版待发布（手动点同步） |

## 四、待办 / 风险

- **重启电脑后需验证自启链路**：① `127.0.0.1:8787` → 200；② `127.0.0.1:8642/v1/models`（带密钥）→ 含 `hermes-agent`；③ `D:\hermes-native\logs\` 下有 `listening`；④ 确认 `server.py` 单实例不双开；⑤ 在 Hermes 里跑一条命令，确认 agent.log 不再出现 `snapshot bootstrap failed` / `WSL (NN - Relay) ERROR`。
- **Hermes 当前进程是装 Git 之前启动的，PATH 不含 Git，必须等重启才生效——勿手动重启**（此前为重启已耗费多轮）。
- **WSL Ubuntu 已导入成功**，但 Hermes 主目标只依赖 Git Bash，WSL 是补充 fallback，非必需。
- **Ech0 已退出自动发布**，本地 Docker 仍在；删容器/镜像文章不丢（数据在 `D:\shuoshuo\data`）。
- **发布脚本硬编码本机端口**（如 6277），迁 VPS 需改地址。
- **GitHub 同步：待 gh 登录后生效**（本机复制与本地提交已完成，配好 `gh auth login` 后下次即推送成功；属预期内，不判定失败）。
- **Hermes 兜底任务路径依赖 `D:\AI work\workbuddy\<日期>_每日工作总结.md` 与两个 GitHub 仓库**，若卸载 WB 时删除该目录，需保留或调整脚本里的路径。
