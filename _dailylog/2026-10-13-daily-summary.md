---
layout: post
title: "每日工作总结 · 2026-10-13"
date: 2026-10-13 22:55:00 +0800
categories: [daily-log, workbuddy]
tags: [workbuddy, daily-summary]
---
# 每日工作总结 · 2026-10-13

## 一、今日完成事项

- **模型测速雷达·能力明细清单 + 综合分排行**（10:24 起）
  - 从测速雷达 `http://127.0.0.1:8848/api/capabilities` 拉取 WB 活清单全部 99 个模型能力数据，落盘 `model-speed-radar/进度/capabilities_live.json`，生成 `模型能力明细_2026-10-13.md`。
  - 99 模型中仅 34 个主流可评分（其余 57 个免费接力/边缘/路由 + 5 个生图/生视频专用无公开基准分），按红线不编造原则置说明。
  - 34 个可评分 → 21 个基础模型组（供应商别名去重）。派 4 个后台 agent 调研 Artificial Analysis / LMArena / OpenCompass / Vellum 四个评分平台真实分。
  - 12:03 用户实测校准：原表误把 WB `hy3`(b.ai 路由)对应到 OpenCompass `Hy3-preview`(73.6，实为腾讯混元系)，误差>30%，已删错误映射，hy3 改按用户实测经验值 40–45 单列。教训：跨平台综合分方差可达 30%，WB 别名模型须严格核对是否=榜单同名独立模型。
  - 评分算法修正：首版用 min-max 归一导致 Agnes 被归成 100 排第一失真，改为**综合分 = OpenCompass 百分制均分 + Vellum HLE% 均值**；AA/LMArena 仅作展示列不参与综合分。
  - 别名补丁：补了 `z-ai/glm-5.2`、`moonshotai/kimi-k2.6` 等带前缀 WB id 的匹配，修复 `EXTRA_ALIAS`。
  - 20:48 评分表补充：OpenCompass 分项（知/推/数/码）并进主表；LMArena ELO 列补满（arena.ai 主通道被 Cloudflare 拦，走 prompeteer.ai / metatext.io T1 镜像取到 10 个模型真实 ELO，Inkling 镜像 1441.31 与官方 1441.4 交叉验证一致）。
  - 21:02 用户指正重大遗漏：WB 活清单每个自定义模型名前 `[]` 中的文字 = 「提供平台」（接入路由），与「模型厂商(vendor)」不同。已补：能力明细表加独立「提供平台」列 + 「按平台统计」小节；综合分表每个 WB 别名标 `[平台]` 并加平台汇总列。99 模型平台分布：OurFree 24、NVIDIA NIM（含 Nvidia 大小写合并）25、Agnes-AI 11、Loomy 9、BazaarLink 5、Cloudflare 5、GLM API 4、Groq 4、SenseNova 4、Gemini 3、DeepSeek 2、b.ai 2、WeChat 1。
  - 交付：`综合分排行_2026-10-13.html`(16.5KB) + `.md`(5.7KB)，有综合分 7 个（Qwen3.8-Max 80.6 居首，Gemini 67.7，GLM-5.3 64.8，Kimi-K2.6 63.9，DeepSeek-V4-Pro 62.9，DeepSeek-V4-Flash 62.7），参考组 4 个（Inkling/Agnes/MiMo/gpt-oss-120b），无公开分 72 个。

- **12 模型温和测速**（21:20）
  - 脚本 `进度/probe_12models.py` 复用 speed_daemon.probe_model：串行、rounds=1、gap=3s、timeout=25s、失败不重试、log 静默，写 `进度/probe_12models_result.json`（不污染雷达 data/ 域）。
  - 结果：可用 3/12，用时 58.0s。成功 3 个全为直连（DeepSeek-V4-Pro 1150/2253ms、DeepSeek-V4-Flash 667/1123ms、WeChat Deepseek-v4-flash 762/836ms）。
  - 失败 9 个均为环境前置问题（非限流，全程零 429/503）：① 5× Loomy 路由全指向本机 `127.0.0.1:17890` 网关未起（Remote end closed）；② 2× Gemini code 400 国内地域封锁；③ 1× b.ai balance=0；④ 1× SenseNova 额度耗尽 code 8。
  - 下一步待用户拍板：Loomy 网关起后单独重试；Gemini 需代理；b.ai/SenseNova 需充值续额。

- **Loomy2api 网关双开修复**（21:40）
  - 根因：`loomy2api/server.py` 的 `main()` 无单实例/端口锁，Windows `SO_REUSEADDR` 允许第二个 `bind()` 成功 → 两个 `pythonw` 同绑 127.0.0.1:17890（PID 6492/11708）→ 连接竞态 → `Remote end closed` / 空回复（`/health` 实测连发 5 次全 `curl exit 52`）。这正是 10-12 修复文档(1155)自己警告过的雷区。触发双开 = 启动文件夹 `loomy2api-AutoStart.vbs` 登录自启 + 手动启动叠加。
  - 启动链：`Startup\loomy2api-AutoStart.vbs` → `start_silent.vbs` → `pythonw server.py`（本机禁用 schtasks/reg/PowerShell COM，自启走 Startup 文件夹）。
  - 修复（根治）：① `server.py` 加 `ensure_singleton(cfg)`（pidfile `.loomy2api.pid` + 端口探测双保险，重复实例主动 `sys.exit(0)`，atexit 清理 pidfile；main 首行调用；新增 imports ctypes/atexit/socket；py_compile 通过）；② `start_silent.bat` 改幂等（端口已监听则跳过）。
  - 处置：taskkill 6492/11708 → 端口释放 → 干净起一个实例（本会话以 `python.exe` 后台任务 PID 14112 托管，因 `start pythonw` 会被沙箱回收）。验证：17890 仅 1 监听者；`/health` 连发 5×稳定 200 且 `session_found:true`（已提取本机 Loomy session userid=261008140706211184）；单发聊天探测 `deepseek-v4-flash-0731` 返回标准 OpenAI 兼容响应（content=OK）。
  - 产物：`2026-10-12-11-05-04/loomy2api/进度_20261013_2140_网关双开修复.md`。网关当前随本会话存活；重启/登录靠 Startup .vbs 自启且新守卫杜绝双开。

- **Loomy 5 模型温和重测 + 12 合并**（21:56）
  - 新建 `进度/probe_loomy5.py`（复用 speed_daemon.probe_model，温和参数同 12 模型版：rounds=1/gap=3s/timeout=25s/不重试），只测 5 个 [Loomy] 模型，落 `进度/probe_loomy5_result.json`。
  - 结果：可用 3/5（Kimi-k2.6 14055ms/14056ms/38字、deepseek-v4-flash-0731 1475/2089/189、DeepSeek-V4.1-Flash 6184/9661/121）；失败 2/5（qwen-3.8-max 上游 25s 挂起超时、GLM-5.3-Flash 上游 502）。
  - 归因核对源码（speed_daemon.py 543-559）：探针 `建连超时`=urlopen 25s 超时，而网关 `_proxy_chat` 是先拿上游响应才回 200 头 → 该超时实为「网关连 Loomy 上游被挂起」，确属 Loomy 上游侧（挂起/502），非网关、非限流（全程零 429/503）。
  - 12 模型合并总览：可用 6/12（3 直连 DeepSeek/WeChat + 3 Loomy 修复后恢复）；失败 6/12（2 Loomy 上游 + b.ai 余额 0 + 2 Gemini 地域 + SenseNova 额度）。网关修复净恢复 3 个可用模型。
  - 产物：`进度/probe_loomy5.py`、`进度/probe_loomy5_result.json`、`进度_20261013_2156_Loomy5重测.md`。

## 二、关键决策 / 注意事项

- **跨平台综合分算法**：放弃 min-max 归一（边界效应失真），改用 OC 均分 + Vellum HLE 均值；AA/LMArena 量纲/可信度不一仅作展示列。
- **WB 别名模型须严格核对**：`hy3` ≠ `Hy3-preview`（腾讯混元系），误对应误差>30%。教训：跨平台归一必须逐条核对是否=榜单同名独立模型，不可张冠李戴。
- **arena.ai 取数套路**：主 agent WebFetch 通道被 Cloudflare 拦，但后台 agent 通道能过；或走 prompeteer.ai / metatext.io T1 镜像（LMArena via HuggingFace，2026-10）。多源交叉验证（官方 vs 镜像）是防数据失真有效手段。
- **Loomy2api 网关双开根因**：Windows `SO_REUSEADDR` 允许同端口多 bind，原代码无单实例守卫。修复方式：pidfile + 端口探测双保险 + atexit 清理 + start_silent.bat 幂等检查。
- **温和测速参数**：rounds=1/gap=3s/timeout=25s/失败不重试/log 静默，避免触发平台限流（429/503）。测速脚本一律落 `进度/` 子目录，不污染 radar data/ 域。
- **Vellum HLE 窄基准方差**：跨平台方差可达 30%，综合分是相对排序非绝对能力值，汇报时须标注。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 模型能力明细清单 | `D:/AI work/workbuddy/model-speed-radar/模型能力明细_2026-10-13.md` | 99 模型能力表格 + 平台统计 |
| 综合分排行（HTML） | `D:/AI work/workbuddy/model-speed-radar/综合分排行_2026-10-13.html` | 交互排行表（16.5KB） |
| 综合分排行（MD） | `D:/AI work/workbuddy/model-speed-radar/综合分排行_2026-10-13.md` | 文本版排行表（5.7KB） |
| 能力明细 JSON | `D:/AI work/workbuddy/model-speed-radar/进度/capabilities_live.json` | 雷达 API 实时数据源 |
| 12 模型测速脚本 | `D:/AI work/workbuddy/model-speed-radar/进度/probe_12models.py` | 温和测速工具 |
| 12 模型测速结果 | `D:/AI work/workbuddy/model-speed-radar/进度/probe_12models_result.json` | 可用 3/12 明细 |
| Loomy5 测速脚本 | `D:/AI work/workbuddy/model-speed-radar/进度/probe_loomy5.py` | 修复后 Loomy 重测 |
| Loomy5 测速结果 | `D:/AI work/workbuddy/model-speed-radar/进度/probe_loomy5_result.json` | 可用 3/5 明细 |
| 网关双开修复记录 | `D:/AI work/workbuddy/2026-10-12-11-05-04/loomy2api/进度_20261013_2140_网关双开修复.md` | ensure_singleton 补丁说明 |
| Loomy5 重测记录 | `D:/AI work/workbuddy/2026-10-12-11-05-04/loomy2api/进度_20261013_2156_Loomy5重测.md` | 12 模型合并总览 |
| 评分表补充记录 | `D:/AI work/workbuddy/model-speed-radar/进度/进度_20261013_2048_评分表补充.md` | OC 分项 + LMArena ELO 列 |
| 今日工作日志 | `D:/AI work/workbuddy/.workbuddy/memory/2026-10-13.md` | 本次生成的工作日志 |

## 四、待办 / 风险

- **Loomy 网关随本会话存活**：当前网关以 `python.exe` 后台任务 PID 14112 托管，重启/登录靠 Startup .vbs 自启且新守卫杜绝双开。下次登录验证自启是否正常。
- **qwen-3.8-max / GLM-5.3-Flash Loomy 上游故障**：2 个模型上游挂起/502，非网关问题，待 Loomy 上游恢复后重测。
- **Gemini 地域封锁**：2 个 Gemini 模型 code 400 国内封锁，需代理才能用。
- **b.ai 余额 0 / SenseNova 额度耗尽**：需用户充值续额后重测。
- **综合分排行 HTML/MD 已发布到 model-speed-radar 目录**，待用户确认是否需要推送 GitHub / 论坛。
- **论坛/语雀/Gridea 发布**：本次工作涉及模型测速雷达数据产品化，非日常 handoff/技术点，是否需要走 4 端发布链路待用户指示。
