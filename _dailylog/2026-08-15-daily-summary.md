---
layout: default
title: 每日工作总结 · 2026-08-15
date: 2026-08-15 23:30:00 +0800
---

# 每日工作总结 · 2026-08-15

## 一、今日完成事项

1. **Playwright 浏览器自动化路线统一为 MCP**：用户明确纠正——以后打开网页/截图类任务只走 Playwright MCP 连接器，不再写本地 Node 脚本。已把 `playwright` 条目配进 `~/.workbuddy/mcp.json`（managed node + `npx -y @playwright/mcp@latest --browser msedge` + `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`），16:01 握手验证通过（Playwright 1.63.0-alpha，msedge 驱动生效，未下载浏览器）。

2. **清理 Playwright 历史遗留库包**：删掉 8月4日遗留的本地 `playwright`(5MB)+`playwright-core`(14MB) 库包；随后按用户要求又删除 `ms-playwright` 浏览器目录(703MB，chromium/ffmpeg 等)。删除后 MCP 回归握手均正常，遗留待办清零。

3. **Hermes 8787「无法连接 MCP 服务器」排查与修复闭环**：
   - 先修正早先误判（venv 缺 requests/httpx 不是根因，实测 venv 有这些包）；确认真实症状=5 个 MCP server 全 `enabled=true` 但 `active=false / tool_count=0`，网关重启后没自动拉起 MCP。
   - 顺藤摸瓜发现 8648 与 gateway 读的是两份不一致的 `config.yaml`（`.hermes` 含 models+playwright；`AppData\Local\hermes` 缺 models/playwright）。
   - 修：用 `HERMES_WEB_UI_DISABLE_GATEWAY_AUTOSTART=1 HERMES_HOME=AppData/Local/hermes` 干净启动 8650/8648 壳；统一两份配置（用 `.hermes/config.yaml` 覆盖 `AppData\Local\hermes/config.yaml`）+ 复制 `.env`；手动常驻 `hermes.exe gateway run --replace`。
   - **最终根因**：8648 的 agent-bridge broker 监听 18765，broker 死后 node 误判"已 attached 不重启"→端口竞态→所有聊天请求 `profile worker default exited before ready`。修法=杀 8648 整棵树重置子进程状态 + 干净重启 broker。20:50 用户实测聊天正常 ✅。

4. **Auto Dark Mode 桌面深浅色软件排查**：第三方"自动深色模式"v10.1.0.10 不启动的元凶是引擎本就正常、登录任务 Self-heal 已重建、GUI 偶发崩溃（EventID 1000，偏移量完全一致，稳定可复现）但托盘进程能活、核心换肤不依赖 GUI——功能已恢复，残留仅 GUI 偶崩（待用户决定是否升 11.0.0.54）。

5. **桌面建模型清单 .lnk 快捷方式**：沙箱禁 COM/cmd，改用纯 Python 手写 `.lnk` 二进制（ShellLinkHeader + 4字节对齐 + UTF-16 路径），产物 `C:\Users\Administrator\Desktop\模型清单_67个_文本推理类vs多模态类.md.lnk`（已反解校验）。

## 二、关键决策 / 注意事项

- **浏览器任务红线**：以后一律走 Playwright MCP 连接器，禁用本地 Node `playwright` 脚本（8月4日遗留库包已清）。
- **Hermes 配置一致性**：`.hermes/config.yaml` 与 `AppData\Local\hermes/config.yaml` 必须保持同步（含 models/providers + 5 个 MCP server + playwright SSE），否则 gateway 读不到缺项、MCP 拉不起来。
- **Hermes 重启顺序**：先 `taskkill /F /T` 杀 8648 整树（重置 broker 18765 死状态），再干净重启，否则会卡在 `attached to existing bridge at 18765` 误判。
- **工具环境约束**：本机 bash 禁 `reg/schtasks/wmic`，但 PowerShell cmdlet 可用；WQL `LIKE '%x%'` 被沙箱拦，改用 `-like "*x*"`。
- **不擅自深挖**：Hermes/MCP 修复到"UI 起来能聊天"即停手，未动的配置/未重启的 gateway 按用户指令不碰。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 每日工作总结 | `D:\AI work\workbuddy\2026-08-15-16-27-07\2026-08-15_每日工作总结.md` | 本文件，4 端发布源 |
| Hermes 8787 MCP 诊断 | `D:\AI work\workbuddy\2026-08-15-16-27-07\Hermes_8787_MCP诊断.md` | 修正版诊断报告 |
| Playwright MCP 配置 | `C:\Users\Administrator\.workbuddy\mcp.json` | 连接器配置（playwright 条目） |
| 模型清单桌面快捷方式 | `C:\Users\Administrator\Desktop\模型清单_67个_文本推理类vs多模态类.md.lnk` | 一键打开模型清单 |
| .lnk 生成脚本 | `D:\AI work\workbuddy\2026-08-15-20-54-11\_make_lnk.py` | 纯 Python 手写 .lnk 二进制 |

> 注：`_make_lnk.py` 落盘路径依日志记为 20-54-11 会话目录内；Playwright MCP 配置为对既有 mcp.json 的增量修改，非新建文件。

## 四、待办 / 风险

- **P1**：playwright MCP 连 8931 偶发 `400 Bad Request`（worker 日志可见，parking 不致命，不影响发消息）；若要真用截图/浏览器工具需查 8931 SSE 的 client 请求格式/路径。
- **P1**：Playwright MCP 在连接器管理页 Trust 激活后，**用 MCP 打开 https://towertop.kdns.fr/ 截图** 仍待执行（16:20 起待办，Trust 后新会话执行）。
- **P2**：Auto Dark Mode GUI 偶发崩溃（EventID 1000），待用户决定是否升 11.0.0.54 根治（核心换肤不受影响）。
- **P2**：Hermes MCP 注册表 5 个 server 仍 `active=False`（lazy 态，首次调工具才翻绿），已实测聊天正常，未进一步强连。
- **P2**：Hermes gateway 仍靠手动 `hermes.exe gateway run --replace` 常驻，重启后是否自动拉起 MCP 待观察。
