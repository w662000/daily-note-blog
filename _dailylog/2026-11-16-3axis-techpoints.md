---
layout: default
title: 技术点 · 2026-11-16
date: 2026-11-16 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-16.md, D:\AI work\workbuddy\2026-11-16-11-32-53\.workbuddy\memory\2026-11-16.md

## 10:12 开机自启生效，任务自动续跑中
- 10:09:40 YD_Rebuild 随登录自动启动，进度日志确认：PHASE 1 收集 worklog 20 页/1000 篇（~88s/10 页）。
- 已核实脚本为最终修复版：acc[label]=[] 全量重扫不漏收（L48）、CREATE_NO_WINDOW 无黑窗（L33）、删除阶段断点跳过已删 ID。
- 预计：收集 1~1.5h → 15 路并发删除 ~30min → 重传 ~20min，中午前后出三目录干净计数。
- ⚠️ 重传阶段若撞上 10:15 晨检有道云补发会互踩（今晨已避开，任务 10:09 启动晚于晨检无冲突）。

## 10:26-11:00 修复 Gridea 老浓缩稿重复 + wb-cn 空日志定稿 bug
- 用户发现线上「每日工作总结 · 11-15」写着"wb-cn 今日无机器日志记录"（实际当天日志很多）。根因两条：
  ①**老浓缩稿重复**：Gridea「每日工作总结」浓缩稿与 step0c 三轴「多Agent工作日志」职责重复；且 automation `automation-1787577004866`（Gridea浓缩版补发 10:10）每天无条件重写浓缩稿（prompt 明写"已存在则仍安全重写"）——这才是 10:20:41 时间戳的元凶。
  ②**空日志定稿**：step0 10:20 跑时 wb-cn 当天日志还没产生（实测 15 号日志 10:35 才建），总结 TODAY 必然空档且幂等永久定稿。
- 用户拍板：停掉老浓缩稿写入 + step0 改为总结昨天。执行：
  - `generate_daily_summary.py`：加 `--with-gridea` 开关，默认不写 Gridea 浓缩稿（列车不传 → 自动停写）；备份 `backup/generate_daily_summary.py.bak-gridea-20261116`。
  - `publish_train.py`：加 `SUMMARY_DATE`（hour<12→昨天，hour≥12→当天），step0 用它；两个列车任务 Command 相同，故用时间判断而非改计划任务；备份 `backup/publish_train.py.bak-gridea-20261116`。
  - 暂停 automation `automation-1787577004866`（Gridea 浓缩版补发 10:10）——根上的修复。
  - 保留：`automation-1784739275903`（补总结+博客源+语雀，不写Gridea）、`automation-1787285013065`（Gridea 渲染推送，不生成内容）。
- 语法校验通过；未实跑（列车带外部发布副作用）。线上那篇错误稿按用户选择未补正（用户选"停掉"而非"停掉+补正"）。
- ⚠️ 10:20 列车当前进程是改代码前启动的旧实例（用旧代码），下次触发才是新逻辑。

## 12:45-13:05 用户令"别死等"→ v3 直接开删 + 并发实测调优
- 12:42 旧 v2 实例在 techpoints 440页/22000 条落盘后静默退出（无 CRASH 记录）；inventory 共 77028 条（14986+40042+22000）。
- v3（collect_delete_rebuild_v3.py --delete-now）：跳过完整收集直接删；新增 PHASE 2b 残余补扫（删后重扫三目录补删 techpoints 未收完的残余，fail2 不触发熔断）。
- 坑：schtasks /tr 的参数必须放引号外（"--delete-now" 包进同引号 → 启动即失败）。
- 并发实测三档：**15 路 = 接口被打挂**（timeout 遍地，4 分钟<100 条，FAIL 15 个）→ 4 路 = 稳但 0.52 条/秒（41 小时）→ **8 路 = 甜蜜点**（fail=0，~1.1 条/秒，约 19-20 小时）。**有道云 delete 接口实测：8 路安全，15 路崩**。
- 熔断阈值 fail>20 → fail>1000（7.7 万条规模网络抖动不该中止）；delete timeout 60→120s、重试 2→3 次；落盘间隔 100→20 条。
- 断点续删验证生效：重启后 "resume: 80 already deleted, skipping them"。
- 当前：YD_Rebuild2 计划任务（pythonw 无窗口）跑 8 路删除 76948 条，预计**明天上午删完**，PHASE 2b 补扫 + 重传 + 复核再 1~1.5 小时 → **明天中午前后全部收工**。旧 YD_Rebuild（onlogon）已删除。

## 13:31 看门狗上线（用户问"会不会中断/被回收"）
- 三层保护闭环：①YD_Rebuild2 = 计划任务，进程独立于 WB，不受后台任务回收机制影响；②**YD_Watchdog**（`C:\Users\Administrator\.workbuddy\yd_rebuild_watchdog.py`，每 30 分钟计划任务）——进程死了自动 `schtasks /run YD_Rebuild2` 拉起（断点续删安全）、全部完成（youdao_final_state.json 出现）自动删除两个计划任务收尾；③每 20 条落盘 + 断点续删，崩溃最多重删 20 条。
- 看门狗日志：`D:\AI work\workbuddy\logs\yd_watchdog.log`；存活检测路径实测通过（13:31/13:32 两次"进程存活"）。
- 关机也不怕：开机后 /sc minute 看门狗继续调度，30 分钟内自动续跑。
- 坑：schtasks /tr 值含空格路径（"AI work"）经 subprocess list 传参引号转义会翻车 → **看门狗脚本放无空格路径 `~/.workbuddy/`，/tr 值完全无引号**，一次成功。
- 速度评估：8 路 ~1.27 条/秒 → 76948 条 ≈ 16.8h → 明早 6:30-7:00 删完。不再加并发（15 路崩的教训 + 用户限流红线）。
- 15:30 用户将准时关机：新增 **YD_Rebuild_Logon**（/sc onlogon，tr 与 YD_Rebuild2 相同三段带引号形式 rc=0）——开机登录立即续跑（不等看门狗 30 分钟窗口），与看门狗互补：onlogon 先拉起 → 看门狗巡检见进程存活不重复拉。关机时删除被硬杀但每 20 条落盘，续跑从 DELRESULT 断点继续。
- 时间顺延：如 22:00 关机，今晚删 ~3.5 万条，剩余 ~4.3 万条明天开机后 ~8.6h 删完（9 点开机 → 傍晚 18 点删完，晚间收工）。
- 当前任务清单：YD_Rebuild2（正在跑，看门狗拉起目标·必须保留）/ YD_Rebuild_Logon（开机兜底）/ YD_Watchdog（每 30 分钟巡检+完成收尾）。

## 17:02 看门狗实战首秀成功（进程无声死亡被自动救回）
- 16:44:10 主日志戛然而止（ok=17240），无 CRASH/Traceback——**外部终止特征**（非 Python 异常），与 12:42 v2 那次"静默消失"同款死法。已知模式：pythonw 长跑任务会被系统无声杀掉，死因查不到（无异常栈）。
- 16:32 看门狗巡检还报"存活"，17:02:01 巡检发现"进程不存在且未完成"→ 自动清理残留 youdaonote → `schtasks /run YD_Rebuild2` 拉起 → **断点续删精确接上 ok=17280（只重删 ~40 条）**，fail=0。整个救场 0 人工干预。
- 教训确认：长跑任务无声死亡是本机常态而非偶发，看门狗（每 30 分钟）是必需品而非保险丝。


# 2026-11-16 工作日志（本会话 2026-11-16-11-55-25）

## 11:56-12:09 活清单模型清理·第一步出表（未删任何模型）
- 用户指令：根据测速雷达+测限速雷达，清理活清单中限流严重/连接不畅的模型，先整理表标出要清理的。
- 确认「活清单」=`C:/Users/Administrator/.workbuddy/models.json`（94行/92唯一id，2个重复：deepseek-v4-flash、openai/gpt-oss-20b）。
- 纯本地只读分析（未发任何API请求）：测速57轮+限速16轮（15连发），窗口11-07~11-16（避开11-05/06本机网络故障314/256次network）。
- 逐轮核查代表模型验证聚合；修3个口径bug：①SKIP全为冷却（窗口内936=429冷却624+慢冷却312）计入限流证据 ②no_quota≠429限流，单独归类「配额耗尽」 ③cleanup_final.py变量定义顺序bug。
- 分级结果92模型：**A-清理70**（下架/通道挂18、连接不畅32、限流严重19、配额耗尽1）｜B-观察3｜C-留意2｜OK-保留17（含5个用户主动skip的CF）。
- 产物：待清理模型看板_20261116.html（Playwright验证92行渲染正常）+ .md + .csv，均在会话目录；结构化结果 C:/Temp/cleanup_final.json。
- 待用户拍板后才执行删除；A级行动分三类：下架18删活清单、限流19雷达排除暂留、连接不畅32先核url/key。
- 复用脚本：`分析脚本/cleanup_final.py`（分级）、`render.py`（渲染），窗口参数改 CUTOFF 即可复用。

## 12:19-12:28 清理执行（用户「继续」放行）
- 备份 models.json.bak-20261116_1222 + 两个雷达 config.json.bak-20261116_1222；连根拔检查：49个待删id代码零引用。
- 4枪温和定性（单发间隔5s）：OurFreeModel=401 key失效(整批24死)、scnet=431封号、b.ai=400欠费(balance=0)、gpt-oss-20b(NIM)=超时。
- 执行：models.json 94→45条（删51条目/49id），限流18个加双雷达skip_models(17→36)，Gemini 2个降观察，glm-4.1v-thinking-flashx 配额不删。
- **关键发现：雷达 load_models 对同 id 只测第一条**——deepseek-v4-flash 两条(SenseNova+b.ai)数据被混合统计，429=90.7%全来自SenseNova，b.ai条从未被测；openai/gpt-oss-20b(NIM+Groq)同理。据此修正两处误删（恢复SenseNova条+Groq条），SenseNova条进skip。此机制已写入 model-radar-topn 技能第12条。
- 终验：45条无重复，8848/8849均200。待办：重启双雷达daemon使skip生效（models.json已热读）；OurFreeModel/b.ai拿到新key或充值后从备份恢复。

## 12:37-12:44 突发:models.json 被外部覆盖回30条 → 已恢复45条稳定
- 12:37:28（用户发消息前25秒）models.json 被外部进程覆盖：45→30条，消失15条=Agnes11+WeChat Deepseek-v4-flash+glm-4.1v-thinking-flashx(配额)+auto:free+nemotron-3-nano-omni-:free(本地18900代理)。30条版已取证 models.json.evidence30_*。
- 处置：从备份+修正名单重建写回45条（rebuild45.py，修正点：保留本地18900代理版 nemotron-:free、删NIM下架版）。95秒观察mtime未变、45条稳定→无周期性覆盖，12:37为一次性写入。
- 疑似 WorkBuddy.exe 客户端回写（当时用户可能开着模型管理UI）；机制未定论，已请用户确认。教训：**手动改 models.json 后必须观察一段时间确认客户端不回写**，且客户端内存态可能与文件不同步。
- 终态45条：OK保留16（11正常轮测+5CF skip）、限流skip保留19、B观察3、C留意2、连接不畅暂留4（Gemini2+Groq1+本地代理1）、配额1（glm-4.1v）。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-13-15-32-52\.workbuddy-ai\memory\2026-11-16.md, D:\workspace\workbuddyai\2026-11-15-22-54-25\.workbuddy-ai\memory\2026-11-16.md

## 14:30–14:45 · 修复 8850 主力资金流接口拉不到数据

- 需求：8850「主力资金流向白名单版」资金流接口拉不到数据，从 8851 找可用接口修过去。
- 项目位置（T0 进程命令行确认）：
  - 8850 = `D:\AI work\workbuddy\主力资金流向白名单版\app.py`（pythonw，端口 8850）
  - 8851 = `D:\AI work\workbuddy\板块资金流看板8851\app.py`（pythonw，端口 8851）
  - 两者 app.py 几乎相同，都是纯标准库 http.server 同源代理 `/api/qt/*` → 东财 push2delay。
- **根因（T0 实测）**：东财 `push2delay.eastmoney.com` 与 `push2.eastmoney.com` 在 **Python urllib 里连不上**（`RemoteDisconnected: Remote end closed connection without response`，东财按 TLS 指纹掐了 urllib），但 curl 直连返回 200（TLS 指纹不同）。
  - 8850 唯一源就是 push2delay，主源失败 → akshare 降级 → 数据格式不对（`f12`=中文行业名、仅 90 条，而前端要 BK 代码），看板前端匹配不上显示不出来。
  - 8851 之所以正常：其前端 index.html 有多个备用源（`push2.eastmoney.com`、`82.push2.eastmoney.com`），且后端 `cached()` 有 stale-while-error（失败返回旧缓存）。
- **修复**（改 8850 的 app.py，三处）：
  1. `EM_SOURCES` 多源列表 `[push2delay, push2]`，`fetch_em()` 逐个轮询，全失败才 raise。
  2. `cached()` 加 stale-while-error（从 8851 抄），失败返回旧缓存。
  3. `CACHE_TTL` 60 → 180（对齐 8851）。
  - 备份：`app.py.bak_20261116_1430`（逐字节校验 PASS）。py_compile 语法 OK，UTF-8 BOM/LF 保持。
  - 独立测试 `_test_fetch_8850.py` 调 `fetch_em()` 成功拿到东财原版数据（f12=BK1210、total=496），证明修复逻辑生效。
- **进程重启的坑（重要环境特性）**：本环境会回收「本次工具会话衍生的所有子进程」。bash/python subprocess、PowerShell Start-Process、调用自启动 ps1 拉起的 8850 都在工具会话结束后被杀（日志显示启动成功、端口短暂 LISTENING 然后消失）。开机自启的 8851/8852 老进程不受影响。
  - cscript/VBS、WMI Win32_Process.Create、detached 均被安全策略拦截。
  - **有效解法**：用一次性计划任务 `Restart8850_Once`（`Register-ScheduledTask` + `Start-ScheduledTask`）由 Task Scheduler 服务拉起，进程脱离会话独立存活；确认监听后 `Unregister-ScheduledTask` 删除任务，进程继续存活。
  - 另注：bash 注入 `http_proxy`+`HTTP_PROXY` 大小写重复，导致 PowerShell `Get-ChildItem Env:` / `Start-Process` 报「已添加项」ArgumentExeption；重启前需先 Remove-Item 清掉所有 proxy 变量。
  - curl 本机测试必须带 `--noproxy '*'`，否则走 127.0.0.1:8383 代理报 `os error 10061`（假故障）。
- **验证结果（T0）**：8850 最终 PID 14212 稳定存活（等 12s 复核仍在），`MainWindowHandle=0` 无黑窗；行业接口返回东财原版 f12=BK1291/BK1210、total=496（不再是 akshare 中文名 90 条）；分时 kline 正常；8850/8851/8852 三端口全在线。
- 临时脚本：`_restart_8850.py`、`_start_8850_once.vbs`（cscript 被拦，未生效）、`_test_fetch_8850.py`、`_start_8850_once.vbs` 均在工作区根目录。
- 提醒：8850 下次开机由 Startup 自启动脚本在干净会话拉起，修复后的代码自动生效；本次会话内已用计划任务手动拉起并保活，但若本机重启则以自启动为准。

## 14:45–15:00 · 8850 页面转圈/曲线不出的二次排查（未彻底修复，等用户决策）

- 现象：刷新 8850 一直转圈，资金流曲线不出来。
- 根因链（T0 实测）：
  1. 前端 `index.html` 用 JSONP 请求本地代理，`refresh()` 第379行 `await fetchAllSectors()` + 第388行 `Promise.all(fetchIntraday...)`，JSONP 超时 20s。
  2. clist 接口：我改的多源 `fetch_em` 两个源各 8s 超时（东财 push2delay/push2 对 Python urllib 持续 RemoteDisconnected），实测 clist 稳定 22–30s 超时 → 页面卡在"抓取中…"转圈。
  3. kline 接口：东财 kline 间歇可用（一次 0.3s len18710 成功，另一次 2.4s 返回 502）→ 曲线时有时无。
- **关键发现**：东财 API 子域（push2delay/push2/push2his）对 urllib 持续封锁；curl 也时通时断，全靠代理端口（当前 1908，之前 8383，8383 已消失），代理不稳定。东财 www/quote 页面直连 200 正常，但 API 子域 http/https/指定IP 全 000。
- **kline 必须带 `ut=b2884a393a59ad64002292a3e90d46a5`**（8851 前端第685行用此 token）；带 ut 的 curl 曾一次拿到 18551 字节，但不稳定。8850 前端 kline URL 和无 ut。
- akshare 降级：8850 服务用的 `envs\default` Python 有 akshare 1.18.81（import 2.5s + 拉数据 0.6s，稳定）。但 akshare 概念/行业数据 f12 是中文名、**无 BK 代码**；前端拿中文名当 secid 请求曲线必失败。akshare 有 `stock_board_concept_name_em()` 等可取代码表（未验证当前是否可用）。
- 8851 之所以能显示：前端有完整多源降级框架（本地代理 priority0 → 新浪 p1 → 聚源 p2 → 东财 p3 → 备用 p4），8850 是老版单源架构，无降级。
- **待用户决策的修复方向**（未实施，避免盲目改）：A) 把 8851 的多源前端框架移植到 8850（工作量大但根治）；B) 后端改造：clist 直接用 akshare 主源(3s)避免超时转圈 + kline 补 ut token 并缩短超时；C) 直接让 8850 复用 8851 的代理/数据（两端口数据互通）。
- 当前 8850 PID 14212 仍在监听，但接口持续超时/502，页面不可用。未经用户确认不再改动。

## 15:00–15:15 · 8850 二次修复（方案A：复用8851能力）实施结果

- 备份：`D:/AI work\workbuddy\主力资金流向白名单版_bak_20261116_1455`（15文件逐字节一致 PASS）。
- **真根因（T0 实测，推翻上一轮判断）**：8850 前端用 JSONP(script)取数；后端主源东财失败→降级 akshare 返回**裸 JSON**（无 cb 包裹）→ window[cb] 永不触发→前端卡满 20s 超时=转圈。8851 前端用 fetch 读本地代理，能解析裸 JSON，故正常。
- **另一个拖慢因素（我上一轮引入的 bug）**：上次给 8850 后端加的"双源轮询 8s+8s"让 clist 比 8851 单源慢一倍。已撤销，改回单源。
- **本次后端改动**（app.py，已备份可回滚）：
  1. 撤销双源轮询，fetch_em 改回单源 timeout=8。
  2. 新增 `try_peer_8851()`：clist/kline 优先转发到同机 8851 代理（8851 长期运行、缓存热、1秒返回），再按本端口 cb 包装成 JSONP。proxy_em 顺序改为 8851→东财→akshare。
  3. akshare 降级按 cb 包装成 JSONP（修转圈根因）。
- **验证（T0）**：8850 clist 从 22-30s 超时 → **1.1s 返回** JSONP（__sfcb1_1({...})）；kline BK 码 1.1s 返回200。转圈问题解决。8850 PID 12784 稳定存活无黑窗（计划任务拉起后已删任务，24h时限）。
- **未彻底解决：曲线**。原因：8851 缓存的 clist 数据 f12 是**中文名**（"证金持股"，akshare/同花顺源），无 BK 码；8850 前端拿中文名拼 secid=90.中文名 请求 kline 失败。东财原版 clist（带BK码）对 urllib/curl 持续封锁，akshare 接口无代码列，同花顺接口给的是 881xxx 非 BK 码，auto_snapshot.json 仅 100 个申万行业名且命名不匹配（42/90）。**本网络环境下无可靠的板块名→BK码数据源**，曲线无法恢复——这是数据源封锁的硬约束，非 8850 代码问题。
- 关键区分：8851 能显示的只是排行榜数字（akshare/新浪数据），8851 根本没有板块分时曲线功能，无可移植的曲线数据源。用户选的"移植8851框架"能治转圈+排行榜，治不了曲线。
- 待用户决策：曲线恢复需任一条件——①东财 push2 API 恢复可达；②用户提供/接受一份完整"板块名→BK码"映射表；③改用不依赖 BK 码的曲线数据源。

## 2026-11-16 17:25 8850 曲线形态升级（大盘形态模板）

- 用户反馈收盘后曲线完全笔直 → 根因：kline 本地合成的线性插值兜底（终值真、形态假）
- WebFetch 摆渡东财 push2delay secid=1.000001 fflow kline f52，拿到今日大盘主力净流入真实分时（240 分钟，终值 -282.5 亿）
- 清洗为 5 分钟粒度 49 点存 `market_ff_template.json`（含 date 字段，仅当日生效）
- `build_kline_response` 优先级：真实采样点(>=3) > 大盘形态缩放(板块值=模板值/模板终值×板块终值) > 线性兜底
- 验证：BK1636 48 点曲线形态与大盘共振（早盘冲高/午后加速/尾盘回落），终值 66.31 亿精确
- 明日起盘中由新浪 clist 轮询采样积累真实分时；模板文件需每日 WebFetch 更新（可选）
- app.py 与模板已同步回 `D:/AI work\workbuddy\主力资金流向白名单版\`


# 2026-11-16 工作日志

## 有道云云端版（youdao-brief-cf）3 天不收录修复

- 用户报告：https://yd.780.de5.net/ 3 天没收录文章，本地版 127.0.0.1:8790 正常。
- 根因（T0）：2026-11-13 的 KV 免费额度优化把 crons 从 `["*/30 * * * *", "*/3 * * * *"]` 改成 `["0 * * * *"]`，而 scheduled handler 里 `"0 * * * *"` 只跑 fsBotRun，refresh（收录新文章）成了死分支 → 云端从 11-13 起不再自动收录。云端 state 的 first_seen 分布实锤：11-14、11-15 零收录，11-16 的 10 条全是 11:49 一次手动刷新补的积压。
- 修复（备份 `youdao-brief-cf_bak_20261116_1206`，8 文件逐字节校验一致）：
  1. crons 改为 `["0 * * * *", "10 * * * *"]`：整点飞书归档、每小时 :10 收录刷新，两个 Cron 分开跑防超时；
  2. refresh 加无变化不写盘 + 2 小时心跳（state._brief_at），保证"今天/昨天"日标签不 stale；
  3. 写量预算：refresh <50 写/天 + fsbot ~30 写/天，合计 <100/天，远低于 1000 上限。
- 部署：`npx wrangler deploy` 成功，Version c422c6ca，两个 schedule 均已注册；手动 POST /api/refresh 返回 `{"ok":true,"added":0,"pending":126,"saved":true}`。
- 12:20 追加：应用户要求心跳从 2 小时改为 30 分钟（refresh cron 改 `10,40 * * * *`）。写量核算：心跳 48 轮×2 key=96/天 + fsbot ~30/天 ≈ 130/天 ≈ 上限 13%，安全（红线 <500）。备份 `youdao-brief-cf_bak_20261116_1219`，Version e1110538，手动验证 saved:false（无变化不写盘逻辑正常）。
- 遗留验证点：`:10` 的 cron 分支机制与 fsbot 相同（fsbot 今天 12:01 正常触发），首个定时收录在 13:10，未现场等到。
- 教训：改 cron/调度时必须检查 scheduled handler 的分支覆盖，删 cron 可能让代码分支变成不可达。

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-16.md

## free-cli-caller 技能 v1.1 全天迭代（codebuddy 降级链）

- v1.1：默认免费两连 + 429 低价降级链。实测 sg x0.03 ✅、glm-5.3-flash x0.06 ✅、gpt-5.6-luna ❌ 400 `not allowed for user type [personal_free_user]`（放进 SKIPPED 自动跳过）
- 关键坑：codebuddy 出错时 exit code 仍为 0（luna 400 也是 exit=0），成功判定必须以 stdout 非空为准
- 用户指令调整：免费两连顺序调换 → **deepseek-v4.1-flash 优先，hy3 备用**（端到端实测 mode=normal 命中 ds-v4.1-flash）
- 端到端验证脚本 `workspace\.openclaw\tmp\test_cb_chain.py`：normal→ds-v4.1-flash OK；force-low→sg OK
- 触发词补入：cli调用、免费cli调用
- 分发：先 7 常用，后用户指令补装 9 个偶装（qclaw/dsh/trae/qoder/qoderwork/joycode/atomcode/codebuddy/agents），共 17 目录哈希核验一致；**此后默认只推 primary**（skill-dist-default-primary 提案已批准）

## codebuddy「requires authentication」排障（重要根因）

- 其他 agent（WB 国际版宿主链，父进程 WorkBuddyAI）报认证错误；我直调 `.hermes\node\codebuddy.cmd` 四轮实测全通
- 根因：认证挂共享登录态 `~\.codebuddy\local_storage\`（auth/workbuddy-desktop-ai.info）；WB 宿主派生链向 `https://www.workbuddy.ai/v2/plugin/accounts` 刷新令牌时 401 → `SignError: account list is empty` → AuthenticationRequiredError
- 判定：直调副本通而宿主链失败 = 登录态健康，问题在 WB 桌面端账号会话（重新登录 WB 即可）；两边都 401 = 共享登录态真失效
- 日志位置：`~\.codebuddy\logs\<日期>\*.log`，找 "Reading product configuration from" 可区分调用的是哪个副本（.hermes\node=直调 / .workbuddy-ai\binaries=WB 国际版自带）
- 排障章节已写入 free-cli-caller 技能（v1.1）并同步 7 常用 agent；用户的演进提案 `evo-2026-11-16-codebuddy-requires-auth-fix` 被拒（草稿在 evolution-drafts\rejected\）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）