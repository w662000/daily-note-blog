---
layout: default
title: 技术点 · 2026-11-23
date: 2026-11-23 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-23.md, D:\AI work\workbuddy\2026-11-23-10-45-04\.workbuddy\memory\2026-11-23.md

## 定时任务模型清单盘点（10:45）
- 用户要求列出所有已配置定时任务的模型。当前会话目录为空、系统 crontab 为空；定时任务全部在 WorkBuddy 全局 SQLite：`~/.workbuddy/workbuddy.db` 的 `automations` 表。
- 共 21 个（ACTIVE 15 / PAUSED 6），全部 recurring、全部有 model_id、全部 `model_is_thinking=0`。
- 模型映射源：`~/.workbuddy/models.json`（51 条自定义模型）。6 个 model_id：glm-4-flash-250414(7)、gemma-4-26b-a4b-it(4)、hy4free(3)、qwen3-30b-a3b-fp8(3)、hy4flash-free(2)、glm-4.7-flash(2)。
- 坑位：`automation_update view/list` 都不返回 model 字段，必须直接读 sqlite；hy4*/glm-4.7-flash 中 hy 系列是内置混元 ID，不在 models.json，版本不可考；#9 任务名写 qwen 实际是 glm；#18 名称 10:00 实际 rrule 10:05。
- 进度文件：`进度/进度_20261123_1045_定时任务模型清单.md`。

## 10:56 批量改模型
- 用户指令：2 个 glm-4.7-flash 任务改为 glm-4-flash-250414。用 `automation_update mode=update id=... modelId=glm-4-flash-250414` 逐个改。
- 已改：#7 automation-1794562873327 美团领券、#13 automation-1785848159433 签到+喵旅行合并。读库验证 model_id 均变更成功，库中已无 glm-4.7-flash 未删除任务；status/专家绑定未动。
- 改后分布：glm-4-flash-250414=9、gemma-4-26b-a4b-it=4、hy4free=3、qwen3-30b-a3b-fp8=3、hy4flash-free=2、glm-4.7-flash=0。

## 10:59 hy4free 3 任务改 hy4flash-free
- 用户判断 hy4free 已不免费。查 T0 本地库：3 任务近期会话 `sessions.model`=hy4free 且 credit_json 非零（19.75 / 65.79 / 86.41 / 54.56 / 35.58）→ 确实在扣积分；credit key 非模型ID简单哈希，归属推断可信度中，无官方公告原文。
- 已改并验证：#4 夜秣git雷达 automation-1794800521709、#5 有道云G5 automation-1794800083381、#6 天气站月度 automation-1794744436826 → hy4flash-free。库中 hy4free 归零。
- 最终分布：glm-4-flash-250414=9、hy4flash-free=5、gemma-4-26b-a4b-it=4、qwen3-30b-a3b-fp8=3。
- 关键坑：`session_usage.credit_json` 记录积分消耗，`sessions.model` 记录会话实际模型，两者是核查"定时任务是否扣积分"的 T0 证据（automation_runs 里没有积分字段）。

## 11:02 核查 hy4flash-free 是否扣积分
- 用户问改之前用 hy4flash-free 的 2 个任务（#1虚拟商品选品雷达、#2老王GitHub副业雷达）扣积分没有。
- 结果：未扣。各 5 次运行（10 会话）credit_json 全 null；全库后台会话按模型统计：hy4free 6/6 全扣，hy4flash-free(12)、glm-4-flash-250414(482)、hy3(1036)、glm-4.7-flash(59)、qwen/gemma 全 0 扣。
- 全库仅 2 个 hy4flash-free 会话有积分，但都是普通手动会话（is_background_automation=null），与定时任务无交集。
- 结论：hy4flash-free 定时任务不扣积分，无需继续改；此前把 hy4free 3 任务改过来正确。
- 方法沉淀：判断模型是否扣积分 = sessions.model 分组 + session_usage.credit_json 非空计数，务必限定 is_background_automation=1 排除手动会话干扰。


# 2026-11-23 工作日志

## WB 国内版左侧积分余额显示 0（实际 4888）诊断
- 用户反馈：左侧栏积分余额显示 0，点进去详情是 4888，问能否修复。
- 只读调查（未改任何安装文件）：
  - 应用数据在 `~/.workbuddy/app/session/`；Local Storage / IndexedDB 里**无积分缓存 key**，
    左侧栏的 0 不是本地缓存值。
  - 全文搜 "4888" 全部是 UUID 片段/网页缓存误匹配，非积分数值。
  - 用 `workbuddy-asar-inspect` skill 解析 `D:/Program Files/WorkBuddy/resources/app.asar`：
    "积分/积分余额/points/remainingQuota" 0 命中，左侧栏积分是运行时从服务端接口拉取，非本地常量。
  - `resources/client-menu-preload.js` 只是自建菜单鉴权桥接，与积分无关。
- 结论：属左侧栏取数/渲染链路问题，服务端数据正常（详情 4888）；最可能是登录态/账户信息缓存过期。
- 立场：不建议 patch 官方客户端硬编码 4888（账户/计费数据、升级会被覆盖、合规风险）。
- 下一步：等用户确认 A(帮清会话缓存)/B(自己完全退出+重登)/C(提供版本截图再判)。
- 进度备份：`进度/进度_20261123_1404.md`。会话 ID cfb175f7-94f0-4137-aabf-7bb9c3257ed7。
- **14:12 更新**：用户称该 BUG 多天、每天重启仍对不上，已放弃修复。据此排除"缓存过期"假设，
  倾向客户端版本级 bug 或两入口取不同字段口径；正解只剩等官方修复/换版本/官方反馈。
  未执行清缓存、未改任何客户端文件。


# 2026-11-23 工作日志

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-22-12-57-38\.workbuddy-ai\memory\2026-11-23.md, D:\workspace\workbuddyai\2026-11-23-10-42-19\.workbuddy-ai\memory\2026-11-23.md

## 修复 VBS 启动器变量未定义错误（10:20）
- 用户双击桌面 bat 报 Windows Script Host 错误：`行17 字符1 变量未定义:'cmdLine2' 800A01F4`
- 根因：脚本第 3 行 `Option Explicit`，但第 5 行 `Dim shell, key, cmdLine` 漏声明 `cmdLine2`（第 17 行赋值）；此 bug 从建脚本起就存在，因本机安全策略禁止执行 wscript 无法实测所以一直没暴露
- 修复：两处（桌面 `LightVela-OpenList-Tunnel.vbs` + skill `assets/` 同文件）第 5 行改为 `Dim shell, key, cmdLine, cmdLine2`
- 备份：`Desktop/LightVela-OpenList-Tunnel.vbs.bak-before-dimfix-20261123`（skill 那份备份也在桌面 `LightVela-OpenList-Tunnel-bak-port/`）
- 验证：静态校验（正则提取 Dim/赋值，UNDECLARED=NONE PASS）；安全策略拦 wscript/cscript/heredoc python 无法实测执行，改用等价 ssh 命令后台拉起两条隧道 → 15244 LISTENING + /ping=pong，26800 LISTENING + aria2.getVersion=1.36.0，均正常
- skill 已重新 sync 到各 agent（仅 1 文件变动），清理各 skill 树里的 .bak-* 残留
- 教训：**以后凡带 Option Explicit 的 VBS 交付前必须静态核对所有赋值变量都 Dim 过**（本机禁 wscript 实测，只能静态查）

## Van.Helsing 6.7G 下载"变 4G"真相（10:40）
- 用户以为昨晚下的 6G 多、早上只剩 3G 多 = 文件被截断/回退。查证：**不是回退，是根本没下完**
- 真相：`/d/Van.Helsing.2004.BD1080P.HDR.X265.10Bit.AC3.DDP5.1.Mandarin&English.PGS-CHS-ENG.mp4`
  - 文件**总大小 6866M（6.7G）**= 用户记的"6G多"；**已下 4133M（≈4.0G）**，进度 **60%** = 用户看到的"3G多/4G"
  - 走的是沙箱里 agent 起的 **curl 单线程**下载（不是 we 配的 aria2，aria2 里那批 qaiu 任务全是 removed/totalLength=0），日志 `/d/van_download.log` 3.2MB 全是 curl 进度条 `\r` 刷屏
  - 速度只有 **~99KB/s**，已跑 11h46m，ETA 还有 7h47m；10:40 实测 10 秒内 size 从 4339331072→4340445184（+1.06MB≈106KB/s），仍在下载中，没有回退
- 结论：慢是源站/链路限速（curl 单连接），不是额度或文件丢失。要提速需换多线程 aria2 + 有效直链，或换源
- 排查路径：aria2 RPC(26800) tellStopped 看任务 → OpenList `/api/fs/list` 拿真实文件名+size → `/p/d/van_download.log` 按 `\r` 拆 curl 进度看最终行 → 间隔 10s 两次 list 比对 size 判活跃；注意文件名含 `&`，`/api/fs/get` 拼路径会失败，改用 fs/list 取 size 更稳

## 尝试 aria2 16 连接重下失败（11:20，结论：此路不通）
- 用户要求：重新生成不过期直链 + aria2 16 连接重下，原 curl 单线程任务不要动
- qaiu 重新解析成功：`auth_key=1795544132` 到 11-25 02:15 有效（39h，纠正之前"几分钟过期"的误判）；真凶更可能是 aria2 请求特征被夸克 CDN 拒（非 IP/UA：本机+跳板机换 3 种 UA 测 Range 全 206、Accept-Ranges: bytes、Content-Length=7200520476）
- 实测三条路径全部卡 `totalLength=0 / connections=1 / speed=0`，无一例外：
  1. aria2 RPC(26800) addUri 带 split=16/max-conn=16/浏览器UA → 卡 0 字节（GID f4b0ad2c43bf5b85，已 remove）
  2. OpenList 离线下载 API 提交同链 → `[aria2]: aria2: active` 但 bytes=0（tid I6aTR5...，已 cancel）
  3. 对照：沙箱宿主机 curl 同一时段 4333→4340MB 正常增长
- 结论：**沙箱内 aria2（容器 + OpenList 内置 downloader）消费不了夸克签名链，但宿主机 curl 可以**；16 连接 aria2 方案在现环境下行不通。想在沙箱提速只能另想：让 agent 在宿主机跑多线程 curl/aria2c（需重开带 CDP 9223 的 Tabbit 派活，当前 Tabbit 在跑但无 CDP），或接受 curl ~100KB/s 慢慢下
- 用户明确要求原 curl 任务不动，全程未碰它（仅观察 size 增长）

## 生成带 CDP 端口的 Tabbit 快捷方式（11:20）
- 用户要自己关掉 Tabbit 再开带调试端口的，让我发快捷方式；准备在沙箱宿主机跑多线程下载绕开坏掉的 aria2
- 现有 `Desktop\Tabbit浏览器.lnk` 解析（COM 被安全策略禁、无 pywin32，用纯 Python 解析 .lnk 二进制）：Target=`D:\Program Files (x86)\Tabbit Browser\Application\Tabbit Browser.exe`，**参数为空**（默认 profile，有收藏夹），WorkDir=同目录，LinkFlags=0xd7
- 生成 `Desktop\Tabbit浏览器-CDP9223.lnk`：在 ICON_LOCATION 字段**之前**（StringData 顺序 NAME→REL→WORKDIR→ARGS→ICON，ARGS 位 0x20 排在 ICON 位 0x40 前）插入 UTF-16 字段 `--remote-debugging-port=9223`，LinkFlags 0xd7→0xf7
- 踩坑：第一次插在 ICON 之后导致字段错位（ARGS 读到图标路径），按 StringData 规范顺序重插才对
- 关键：不要加 `--user-data-dir`，保持默认 profile 才有收藏夹（上次丢收藏夹就是乱加这个参数）
- 待用户手动关闭 Tabbit → 双击新快捷方式 → 端口 9223 起来后我派 agent 去沙箱宿主机跑多线程下载

## CDP 9223 今天彻底开不了 + 改走手动粘贴指令（11:36）
- 用户坚持用昨天第二次方式（收藏夹在的那次）。翻历史确认昨天成功命令：`Start-Process 'Tabbit Browser.exe' -ArgumentList '--remote-debugging-port=9223 --user-data-dir="...\Tabbit Browser\User Data" <URL>'`（完整字符串单参数），昨天 CDP 通、内核 Chrome/153.0.8010.37，大量 WS 操作成功记录
- 但今天用**完全相同的命令/参数/profile/exe**反复 6 种方式全部失败（9223 不监听、无 DevToolsActivePort）：干净全清进程、独立新 profile、new_Tabbit 内核直启、快捷方式包装器、带/不带 user-data-dir、杀后台保活任务后重启。排除参数/锁/残留/exe/端口保留，疑系统层变化（Tabbit 自动更新或安全软件拦截），无法在当前环境确认
- 让用户重启 Tabbit 好几次都没用，已停止试错。改走**手动粘贴**：生成 `Desktop\给LightVela的下载指令.txt`，用户复制到 LightVela 网页让 agent 在沙箱宿主机跑
- 指令要点：16 段 curl 并行（走已验证可用的宿主机 curl，不用坏掉的 aria2 容器）、输出到新文件 `Van.Helsing.2004.MULTI.mp4`、明确禁止碰原 curl 单线程任务、带浏览器 UA、失败只重试单段、412/403 别猛试
- 新链：从跳板机解析成功（本机 qaiu 现在 502/000 连不上），auth_key=1795545583 有效至 11-25 02:39（39h），文件 7200520476 字节(6.71GiB)
- 教训：CDP 不可用时不要反复折腾用户重启；直接给可粘贴指令更快。派 agent 类任务不一定非要 CDP

## 越南免费主机 slg.de5.net 建站成功（13:30）
- 主机：dataonline.vn 免费虚拟主机，103.137.185.66，DirectAdmin + LiteSpeed，1GB NVMe/20GB流量/2域名额度
- 静态测试页：`C:\Users\Administrator\Desktop\slg-site\index.html`，已传 `/domains/slg.de5.net/public_html/index.html`
- FTP：`webuser@slg.de5.net / Admin661777888`（另有 webuser@661777.xyz 同密码）；FTP 根目录锁死，网站根是 `public_html/`，传根目录无效（踩过两次）
- 关键坑：光改 CF DNS 不够，主机必须绑定域名 vhost 才认 Host 头——在 DirectAdmin → Domains → ADD NEW 加了 slg.de5.net（2/2 额度）才通。之前只改 CF 时 slg.de5.net 一直返回 LiteSpeed 默认页
- 最终：HTTP+HTTPS 全 200，橙云 Proxied 生效，CF 自动签证书 CN=slg.de5.net（Google Trust Services，到 12-25），Server: cloudflare
- 清理：删了 FTP 根目录传错的 index.html，恢复 661777.xyz 原首页

## DataOnline 续期脚本（14:07）
- 用户提供 `D:\HDDownload\dataonline.py`（青龙/Playwright 续期脚本），优惠码 FreeHostRE
- 脚本机制：Playwright 驱动 Chromium 登录 my.dataonline.vn → 读服务到期日 → 剩≤60天才续 → 进 renewal 填 promocode → 校验购物车总额必须 $0 才 Checkout → 复核到期日延后（安全设计：非$0 绝不提交）
- 生成青龙版 `D:\HDDownload\dataonline_renew.py`：内置 PROMO=FreeHostRE，补缺参数检查；原文件备份 .bak-20261123；语法 py_compile 通过
- 用户要求先只写脚本不部署青龙；青龙需另找机器（免费主机无SSH/Docker跑不了）
- 环境变量需用户配：DATAONLINE_EMAIL/PASSWORD/SERVICE_ID（DOMAIN可选）；cron 建议每月1号
- 风险：登录页可能被 Cloudflare 拦（脚本自带提示，BROWSER_HEADLESS=0 排障）；青龙容器需 playwright+chromium（脚本自动装）

## 探测 my.dataonline.vn 防护 → 可弃用浏览器（14:26）
- 用户问替代无头浏览器部署哪个。实测：普通 curl 访问 https://my.dataonline.vn/login/ 直接 200，body 无 Just a moment/Turnstile/recaptcha/challenge 任何标记，`Server: cloudflare` 只是套了 CF 但登录页没开人机验证
- 登录表单：`<form action="login/default" method="post">`，字段 `security_token`(hidden) + `username`(email) + `password` + `action=login`；还有 csrf `token=...`。标准表单，无验证码
- 结论：**续期根本不需要 Playwright/Chromium**，用 requests 或 curl_cffi 纯 HTTP 走登录→服务页→cart 填 promocode→checkout 即可，-libs 几 KB，青龙容器零浏览器依赖。curl_cffi 比 requests 多一层 TLS 指纹伪装（防 JA3 风控），更稳
- 这也解释了为何博主脚本能写在 512MB 无 SSH 主机上跑（若用纯 HTTP）——但用户手上的 dataonline.py 是 Playwright 版，确实跑不了，需重写成 requests/curl_cffi 版
- 本机 WorkBuddy 内置 python 3.13.12 有 requests 2.34.2，无 curl_cffi（可 pip 装）


# 2026-11-23 工作日志

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）