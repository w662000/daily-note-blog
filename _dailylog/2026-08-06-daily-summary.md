---
layout: default
title: 每日工作总结 · 2026-08-06
date: 2026-08-06 23:30:00 +0800
---

# 每日工作总结 · 2026-08-06

> 来源：合并当日三份机器日志——workspace 根 `.workbuddy/memory/2026-08-06.md`（09:50 离线兜底巡检 + 11:00 发布链路 FAILOVER 巡检）+ session `2026-08-05-20-37-33/.workbuddy/memory/2026-08-06.md`（00:04–11:54 模型能力核查线）+ session `2026-08-05-21-15-16/.workbuddy/memory/2026-08-06.md`（11:58 bat 复盘 + 14:45–18:05 Debian 双启装机线）。

## 一、今日完成事项（分点，通俗语言）

### A. 模型能力核查线（接续 08-05 的 models.json 元数据核查）
1. **step-1o-audio 图片输入实测**：结论——该端点不支持图片输入，接口层直接 400 拒绝（"unsupported multipart type, only support text and audio"）。纠正一个认知偏差：阶跃官方宣传的"文本/视觉/语音三模态一体化"是系列 / 技术路线层面的说法，不是单个 API 端点的开放能力；判断模型能吃什么，只信该端点官方文档 + 实际打一枪。
   - 又挖出活清单 bug：`step-3.7-flash` 声明 `supportsImages=false`，但官方文档说支持、实测也答对 → 与 08-05 发现的 `supportsToolCall` 漏标 21 个同类，models.json 能力元数据不可全信。

2. **文本推理类 54 模型「图片 / 音频」全量实测 + 分类标签更新（落地）**：
   - 用 `probe_modality.py` 9 平台并发、平台内串行，每模型 2 枪（48×48 上红下蓝 PNG 问色 / 1s 440Hz 正弦 WAV 问内容），逐条 fsync 落盘。
   - **图片**：7 个模型实测支持（gemma-3-12b-it、step-3.7-flash、agnes-2.5-flash、agnes-2.5-pro-alpha、agnes-2.5-pro、agnes-2.0-flash、stepfun-ai/step-3.7-flash）；2 个存疑（deepseek-v4-flash、mistral-small-3.1-24b 接图但答错色），保守未改。
   - **音频**：首轮把 8 个模型误判"支持音频"（题目泄露选项 + 盲猜），经阴性对照 + 双轮硬验证（数 3 声 vs 5 声哔声）全部翻车 → 文本推理类无可靠音频支持证据，未盲标。
   - **活清单更新**（`C:\Users\Administrator\.workbuddy\models.json` 权威份）：7 个图模 `supportsImages=false→true` + `caps.image=true`，共 16 处改动；备份 `models.json.bak_20260806_004518`。改后 79 模型 / 图输入 30 / 音频 9。
   - **daemon 修复**（`speed_daemon.py` 4 处）：`load_models` 加 `caps.audio`；`classify_capability` 音频判定改为 `bool(caps.get("audio"))`；多模态分列与聚合榜纳入 audio。`py_compile` 通过。
   - **关键定位**：活清单有两份——`C:\Users\Administrator\.workbuddy\models.json`（权威，config.json 指向）与 `D:\AI work\workbuddy\models.json`（陈旧 71 模型副本，缺 HF/CF/Groq）。以后改分类只动 C:\ 那份。

3. **测速间隔 1h→4h 并重启 daemon**：`interval_sec` 3600→14400。机制确认 daemon 启动时读 config 进内存、主循环 `time.sleep` 不热加载 → 改文件必须重启。用户授权重启（stop.bat 杀 8848 旧进程 → start.bat 用 pythonw 拉新）→ 验证 8848 由新 PID 监听、`/api/state` 返回 `interval_sec=14400`、`round_no=67` 正常续接历史。

4. **接入 DeepSeek 官方模型并对齐格式**（数据 T0：api-docs.deepseek.com / platform.deepseek.com）：
   - `deepseek-v4-flash`（2026-07-31 公测主推）+ `deepseek-v4-pro`；`deepseek-chat` / `deepseek-reasoner` 已于 2026-07-24 弃用（08-06 过期 13 天）未加。
   - 修正 `deepseek-v4-pro`：name 补 `[DeepSeek]` 前缀、url 由完整 `/chat/completions` 改 base `https://api.deepseek.com`（修 daemon 双拼 bug：speed_daemon.py 自动拼后缀）；新增 `deepseek/deepseek-v4-flash`（vendor=DeepSeek，supportsToolCall=true，supportsImages=false，supportsReasoning=true，apiKey 复用 v4-pro 的 sk-）。
   - 模型数 80→81；SenseNova 托管的 `deepseek-v4-flash` 与 HF 占位的 `DeepSeek-V4-Flash-0731` 不动（不同渠道）。daemon 每轮 `load_models` 实时读，无需重启。

5. **导出「79 模型能力清单」供用户查阅**：`build_capability_list.py` 读 C:\ models.json → 生成可筛选 HTML（`模型能力清单_2026-08-06.html`，含分类筛选按钮）+ MD 备份。统计：79 模型 / 图片输入 30 / 音频输入 9 / 工具调用 41 / 推理 23；分类：全模态 3 · 多模态图 27 · 音频输入 6 · 生成图 1 · 生成视频 1 · 文本推理 41。

6. **用户认可的工作流固化**：① 先官网 T0 源确认再动手；② 修改 models.json / config.json 前必须 `.bak` 备份；③ 优先不重启——已验证 daemon 每轮 `load_models()` 实时读 models.json、但 config.json 不热加载（改配置才需重启）。这套"查源 → 备份 → 免重启"节奏即用户认可的标准动作，下次动活清单自动套用。

### B. 跨会话踩坑复盘 + 双系统装机线
7. **11:58 bat 启动脚本反复踩坑自我复盘（用户质问）**：用 Python walker 扫 07-20~08-05 日志 + 读 `~/.workbuddy/MEMORY.md` 全 181 行，确认同一根因（bat UTF-8 无 BOM 含中文 → cmd 按 GBK 拆行乱码 → 双击一闪而过 / 静默失败）**5 次复犯**（07-30 OmniRoute / 08-02 / 08-03 model-speed-radar / 08-05 限流雷达 / 08-05 Hermes Desktop，跨 4 项目）。根因三层：① 教训未蒸馏到自动注入层（最核心，07-30 铁律只写进当日流水日志未进 MEMORY.md，新会话根本看不到）；② 写 bat 前无前置失败回溯习惯（conversation_search / Read 未主动用）；③ 编译型护栏 skill 产生太晚（第 5 次才建）。已把"写 Windows 启动器类文件前必须调 `windows-launcher-safety` 自查 + bat 纯 ASCII 无 BOM + 写完跑 check_launcher.py"**提升为本文件顶部硬红线**（每次会话自动注入），并加"高价值教训必须蒸馏到自动注入层"红线。诚实结论：非纯智能问题，是跨会话经验无法自动携带 + 我的流程未补足，修法是提升注入层 + 固化前置回溯习惯。

8. **14:45–18:05 联想 N50-80 双系统装机（用户另一台独立笔记本，非本机迷你主机）**：
   - Win10（Rufus MBR/Legacy 正规 U 盘）→ 修 0xc000000d 引导（bootrec / bcdboot）→ msinfo32 确认 BIOS 模式 = 传统(Legacy/MBR)；Debian 13.6 XFCE 双启成功，GRUB 接管。全程只动 18G 未分配分区，C 盘(系统卷) / D 盘(数据卷) 不碰。
   - **LocalSend 跨设备传命令打通**：从 Win 把命令经 LocalSend 发到 Debian 终端执行。踩坑链及解法：deb 安装用 `sudo dpkg -i LocalSend-*.deb && sudo apt -f install`（勿点右键"解压"）；进中文"下载"目录用 `cd "$(xdg-user-dir DOWNLOAD)"` 免输入法；清华源 sed 改的是空的 `sources.list` 白改，Debian 13 用 deb822 `debian.sources`；清华 CDN 家庭宽带 403 → 换阿里云 `mirrors.aliyun.com/debian`；旧 `gir1.2-appindicator3` 改名 `gir1.2-ayatanaappindicator3-0.1`；apt 无候选根因是 DVD-1 残留 cdrom 源 + sources.list 白改，重写 deb822 即解。
   - **中文输入法方案**：Linux 主流中文 IM 无内置语音输入；基础打字首选 fcitx5 + fcitx5-chinese-addons(拼音) 或 fcitx5-rime；语音靠 fcitx5 语音插件（audiov 本地离线 / fcitx5-voice-input 接国内云）。
   - **关键红线**：C 盘(系统卷 50G) 严禁在 Debian 挂载 / 写入（会破坏 Win10 引导）；D 盘(47G) 可挂但默认因 Win 快速启动脏标志只读，需回 Win 关快速启动 + Shift 完全关机后才能读写。

### C. 自动化巡检线（本机）
9. **09:50 离线兜底巡检**（automation-1784739275903）：核查 08-05 / 08-04 / 08-03 三天的 `d_每日工作总结.md` 全部存在（mtime 23:10 / 23:06 / 23:01），无缺失，全部跳过；未执行 sync、未触发 gh workflow、未做任何 git push。全程用 Glob 规避 Git Bash `find` 对中文文件名返回空的坑。

10. **11:00 发布链路 FAILOVER 兜底巡检（目标日 08-05）**（automation-1785646936067）：**12/12 全绿、零补发**（4 端 × 日志 / handoff / 技术点），为本自动化上线以来首次不需要补发。**技术点稿件历史首次成功产出并全端发布**（`260805_技术点_handoff.md`，7 技术点 + 5 教训）；Gridea 连续三漏渲染链条被打断，但成因是当晚跑了两次 deploy（23:08:45 接 handoff+技术点、23:16:07 接 23:12 落盘的日志），**竞态窗口本身未修复，属侥幸**。新增判定经验：Gridea output 仓无 upstream tracking，`git status -sb` 只显示 `## master`，须用 `git rev-list --count origin/master..HEAD`（为 0 即已同步）。远端只读 5 次（语雀 1 GET + 论坛 4 板块各 1 list_topics）、写 0 次、未触发限流。

## 二、关键决策 / 注意事项
- **活清单权威份在 C:\**：`C:\Users\Administrator\.workbuddy\models.json` 才是 config.json 指向的权威份；`D:\AI work\workbuddy\models.json` 是陈旧 71 模型副本（缺 HF/CF/Groq）。今后任何分类 / 能力改动只动 C:\ 那份并先 `.bak`。
- **音频能力判定方法学**：文本推理类"是否支持音频"极易误判（选项泄露 + 盲猜），必须用阴性对照 + 硬验证（数声哔声）才能采信；本轮把首轮 8 个误判全部推翻，未盲标，避免污染清单。
- **推理型模型测小 max_tokens 会误判**：`step-3.7-flash` 首测 HTTP 200 但 content 为空，真因是推理吃掉 max_tokens；探针应自动放大 ≥1500，否则把"参数不够"误判成"能力不行"。
- **Debian 13 换源必须用 deb822**：旧 `sources.list` sed 写法已失效；清华 CDN 家庭宽带常 403，优先阿里云；写源前先 `curl -sI` 探活。
- **bat 红线已升注入层**：写任何 .bat / .cmd / .lnk 前必须调 `windows-launcher-safety` 自查 + 纯 ASCII 无 BOM + 跑 check_launcher.py，否则就是重复踩坑。
- **高危操作仍需弹框**：重启 / 覆盖 / 重写 / 升级 / 删除，必须 AskUserQuestion 确认（用户 08-04 立的红线，本次接入 DeepSeek / 改间隔均走授权流程）。

## 三、生成的有用文件
| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| step-1o-audio 图片输入实测报告 | D:\AI work\workbuddy\进度\进度_20260806_0010_step-1o-audio图片输入实测.md | 模态能力核查记录 |
| 视觉探针数据 | D:\AI work\workbuddy\toolcall_probe\vision_test.json、test_img.png | 图片理解验证原材料 |
| 模态分类更新报告 | D:\AI work\workbuddy\model-speed-radar\modality_probe\分类更新报告_2026-08-06.md | 54 模型实测结论 |
| 模态实测数据 | D:\AI work\workbuddy\model-speed-radar\modality_probe\results_modality.json、audio_hard_verify.json、raw\*.jsonl | 落盘证据 |
| 活清单备份 | C:\Users\Administrator\.workbuddy\models.json.bak_20260806_004518 | 改前回滚点 |
| 79 模型能力清单 | D:\AI work\workbuddy\model-speed-radar\模型能力清单_2026-08-06.html / .md | 可筛选查阅 |
| DeepSeek 接入脚本 | D:\AI work\workbuddy\model-speed-radar\add_deepseek_models.py | 增量入库 |
| bat 复盘 md | D:\AI work\workbuddy\进度\进度_20260806_1158_bat_recurrence_postmortem.md | 跨会话踩坑根因 |
| Debian 安装手册 | D:\AI work\workbuddy\进度\进度_20260806_1447_debian_install_manual.md | 按键级装机步骤 |
| LocalSend / Debian 排错补丁 md | D:\AI work\workbuddy\进度\进度_20260806_1529~1738_*.md（共 12 份） | 各踩坑速查 |
| FAILOVER 巡检报告 | D:\AI work\workbuddy\进度\巡检_20260806_1100_failover.md | 发布链路核验 |

## 四、待办 / 风险
- **需授权（覆盖类，未自行执行）**：① 给 `step-3.7-flash` 补 `supportsImages=true` + `caps.image=true`；② 补全 models.json 21 个漏标 `supportsToolCall`（P0）；③ 删旧限流雷达 skill（P0）。三项均需用户弹框授权。
- **模型线**：NIM 的 `stepfun-ai/step-3.7-flash` 同样标 false 待验证；视觉能力做一轮全量实测（23~24 候选）验证清单标记准确率；探针改进（推理型自动放大 max_tokens≥1500）；DeepSeek v4 下一轮 4h 测速自动续接。
- **Debian 线**：可 `apt upgrade -y` 更新系统；C 盘严禁在 Debian 挂载 / 写入；D 盘因 Win 快速启动脏标志只读，需回 Win 关快速启动 + Shift 完全关机后才能读写；中文输入法语音方案待用户选 fcitx5 插件。
- **发布链路**：Gridea 竞态窗口未修复（同步后移至次日 00:40 或改回调触发未采纳，属侥幸断链）；技术点第三轴今日首次有产出。
- **安全**：本机防火墙三档全关（局域网可直达所有端口，未经确认未代为执行）；schtasks 被安全策略禁致计划任务指向死锁。
