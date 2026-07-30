---
layout: default
title: 每日工作总结 · 2026-07-30
date: 2026-07-30 23:30:00 +0800
---

# 每日工作总结 · 2026-07-30

## 一、今日完成事项

1. **OmniRoute 本地网关从安装到跑通**
   - 把 OmniRoute（一个把多家大模型聚合成单一 OpenAI 兼容接口的工具）装到本机，并一路排查它启动黑屏/数据库报错的问题，最终定位根因是安装包自带的数据库原生模块与运行环境版本不匹配，打补丁后 GUI 正常启动。
   - 在 OmniRoute 里接好了 8 个上游大模型平台（Cloudflare、Groq、智谱 GLM、Gemini、OpenRouter、Cerebras、NVIDIA NIM、HuggingFace），并配置 GLM 中国区走直连、其余走代理，实测全网通。

2. **OmniRoute 接入 WorkBuddy（作为可用模型源）**
   - 在 WorkBuddy 的模型配置里加了通过 OmniRoute 访问的条目；经反复实测，最终把"智能路由 auto/*"换成 3 个已验证能正常出字的具体免费模型（Ling / Gemma 视觉 / GLM 备用），避免卡死和吞输出。

3. **OmniRoute 接入 Hermes（让 Hermes 多一个上游 provider）**
   - 在 Hermes 配置里把 OmniRoute 注册为自定义 provider，端到端实测 Hermes → OmniRoute → OpenRouter 链路打通；后又补了 4 条具体模型并核实改模型列表无需重启 gateway。

4. **Agnes AI 接入 WorkBuddy**
   - 排查 Agnes 国内站 401 报错，根因是 Base URL 填错（写成了 apihub 而非官方 api 域名），改对后同一把 key 立刻通；随后把 Agnes 国内站全部 4 个模型（对话 / 推理 / 文生图 / 文生视频）都加进了 WorkBuddy。

5. **论坛每日工作日志补齐"离线兜底"**
   - 发现之前 28 号论坛缺帖是因为代理离线时主发布任务没跑、而旧兜底只补"每日工作总结"不补论坛日志。新建了一个每天 10:00 直连补发论坛工作日志的兜底自动化（幂等、不依赖代理），并修了脚本分页漏判旧帖的 bug。

6. **Hermes 读 WorkBuddy 文档的排查与索引**
   - 排查 Hermes 读不到工作区 md 的真因（是读目录而非文件、以及历史会话上下文爆了导致幻觉），转而生成了一份全工作区 md 文件索引和 10 个批次包，方便 Hermes 一次读一批；同时把 Hermes 单轮工具调用上限从 50 提到 150。

7. **例行 Failover 巡检**
   - 00:15 巡检确认 07-29 的博客源与语雀两边均已正常发布，无需补发。

8. **本机清理**
   - 把 6 个 OmniRoute 安装器残留的临时目录（约 4.5GB）送回收站（非永久删除，可恢复），并评估了 3 个 D 盘相关目录的处置建议。

## 二、关键决策 / 注意事项

- **OmniRoute 黑屏真因 = 安装包缺陷，不是配置/数据问题**：安装包自带 better-sqlite3 原生模块是用 Node 22（ABI 137）编的，而 OmniRoute 运行环境是 Node 24（ABI 148），版本不匹配导致数据库加载失败黑屏。已用正确版本的原生模块覆盖三处副本后修复。之前猜测的"路径空格 / WAL 残留 / 全新库引导卡死"等都被实测推翻。
- **不轻信单次超时判定地址不可用**：Agnes 排障时两次 curl `api.agnes-ai.cn` 超时，差点误判该地址坏了，实际是对方同域名的另一个接入点（apihub）在返回合法 401，真因是 Base URL 指错了网关。第三方 API 的地址务必以官方文档最新版为准，401 也可能只是 URL 指错节点。
- **免费层下"智能路由"不稳，生产要 pin 具体模型**：OmniRoute 的 auto/* 智能路由在免费额度下会卡死/503，WorkBuddy 客户端超时后误显示"任务完成"且吞掉回复。最终改用具体模型 ID。
- **WorkBuddy 模型配置改完要重启进程**：models.json 改动不是热重载，必须完全退出重启 WorkBuddy 才生效（今天多次因没重启导致请求仍走旧模型）。
- **给 WorkBuddy 配模型要避开会返回 reasoning_content 的模型**：GLM-4.5-air 会先吐推理链再吐正文，WorkBuddy 客户端会把整条回复判空。优先选不返回推理字段的模型（如 OpenRouter Ling）。
- **批处理脚本禁含中文**：写 .bat 启动脚本时，UTF-8 中文在中文 Windows 的 cmd 下变乱码、咬断变量名、把注释当命令。.bat 必须纯 ASCII。
- **复制 Electron/Next.js 应用前先杀源进程并校验文件数**：robocopy 复制时若源 app 被残留进程锁住，大量文件被静默跳过（退出码却显示成功），导致目标应用残缺黑屏。复制后必须核对关键目录文件数。
- **SQLite WAL 类应用切勿 taskkill /F 强杀**：强杀会留下陈旧共享内存文件，下次启动报 "Database closed"。
- **测试红线（本周固化）**：验证连通性只能单次低频发请求，禁止短时间连发/循环轰炸，否则触发平台 429/503 误判路由坏了。
- **OmniRoute provider 配置方法**：禁止硬改内部数据库批量注入（key 是加密存储），须用户在 Dashboard 手动逐个填；国内站(.cn)与国际站(.com)账号体系分离。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| OmniRoute 安装与对接教程 | `D:\AI work\omniroute\OmniRoute安装与对接教程.md` | 安装/启动/对接 WorkBuddy 与 Hermes 的图文教程 |
| OmniRoute 启动脚本 | `D:\omniroute\start-omniroute.bat`（及 `D:\AI work\omniroute\` 下副本） | 纯 ASCII 启动脚本，含 DATA_DIR 与代理变量 |
| 工作区 md 文件索引 | `D:\AI work\workbuddy\md文件索引.md` | 全工作区 174 个真实文档的绝对路径索引，供 AI 直接 read_file |
| Hermes md 批次包 | `D:/workspace/workbuddy_md_batches/batch_01~10.md` + `D:/workspace/workbuddy批次索引.md` | 把 175 个 md 预拼为 10 批，避免免费小模型逐文件读爆上下文 |
| WorkBuddy 模型配置 | `C:\Users\Administrator\.workbuddy\models.json` | 新增 OmniRoute 直连 3 条 + Agnes 4 条（共 7 条新接入） |
| Hermes 配置 | `C:\Users\Administrator\.hermes\config.yaml` | 新增 custom_providers.omniroute（19 模型）；max_iterations 50→150 |
| 论坛兜底自动化 | `automation-1785341574261`（每日 10:00 直连补发论坛工作日志） | 补齐发布链路离线兜底 |

## 四、待办 / 风险

- **需重启 WorkBuddy**：新加的 OmniRoute 直连条目与 Agnes 4 模型要完全退出重启 WorkBuddy 才生效，当前进程尚未加载。
- **需重启 Hermes gateway**：max_iterations=150 改动非热加载，今晚关机明天开机重启后生效。
- **回收站待清空**：6 个 NSIS 临时目录（约 4.5GB）已进回收站，等用户手动清空释放空间。
- **D 盘目录处置待定**：`D:\omniroute`（1.5GB 冗余副本，当前未运行）、`D:\omniroute-data`（5MB 旧数据，建议保留或先备份）、`D:\omni_tmp`（空壳）可按需删，未执行。
- **OmniRoute 上游稳定性**：auto 路由在免费层仍会间歇 503/卡死，生产已 pin 具体模型缓解；GLM 直连会遇免费层冷却 429（正常现象）。
- **发布链路残留脆弱点**：博客/语雀的同步脚本对 git push 失败是"非致命"的，若 09:30/10:00 兜底时代理也离线，push 仍会静默失败（后续可加重试/告警）。
