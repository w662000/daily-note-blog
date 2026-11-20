---
layout: default
title: 技术点 · 2026-11-20
date: 2026-11-20 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-19-19-59-56\.workbuddy\memory\2026-11-20.md, D:\AI work\workbuddy\2026-11-20-16-30-22\.workbuddy\memory\2026-11-20.md

## SSH 连接拒绝排查（th-bkk05.altare.global）
- 用户反映 `ssh root@th-bkk05.altare.global -p 25055` 报 Connection refused。
- 实测定位：DNS 正常（→185.207.8.83，泰国曼谷 RackCorp 机房 AS56038，非腾讯云）；25055 端口关闭，22 与 443 开放；22 端口确认为 SSH 服务（返回 ED25519 主机密钥与密码认证提示）。
- 结论：端口用错，SSH 实际在 22 端口，非认证问题。
- 详细证据与修复步骤见 `进度/进度_20261120_1632_SSH连接拒绝排查.md`。
- 待用户确认：22 端口登录凭据、目标是改用 22 还是恢复 25055、25055 是否为转发端口。
- 16:35 追加：用户改 22 端口后连续 3 次密码认证失败。本机无该机器 SSH 密钥、无 config；旧 known_hosts 无该机记录；三方 DNS 一致排除劫持。判断为密码错误或服务端禁 root 密码登录，已提醒停止重试防 fail2ban，建议走 RackCorp Portal KVM 或机房开通邮件找回初始密码。完整记录见上述进度文件。
- 16:45 追加：用户给出 Altare 面板链接（console.altare.gg/server/ba604928-...）。访问被跳转登录页，无登录态看不到服务器详情；页面有"当前需求激增，服务可能不稳定"横幅。等用户登录后再看详情页的 VNC/端口/防火墙/密码重置入口。
- 16:47 ✅根因确认：用户已在 tabbit 浏览器登录面板。用 tabbit-cli 接管已登录标签页（tabId 959940405）读到详情——沙盒 TestServer261120（Debian12 / Bangkok / 节点 th-bkk05），面板明确标注 SSH 端口就是 25055，**状态=已停止**（CPU/内存/网络全 0），今天新建。SSH 连不上的真正原因是机器没开机，不是端口或密码问题。之前 22 端口的 Permission denied 来自机房别的服务，与本沙盒无关。解决=面板点「电源」开机后再连。开机属外部动作，已询问用户是否代点，未擅动。
- 工具经验：接管 tabbit 浏览器登录态用 `tabbit-cli create --task X` → `nodejs --task X --tab <id>` 读页面 → `finish --task X` 释放（保留用户 tab）。CDP web-access skill 不支持 tabbit/ego 浏览器，别走错路。
- 16:51 开机实测：用户授权开机。点电源→Start 成功，状态"已停止"→"正在连接…"（开机生效），但 12s 后仍卡在"正在连接"没进"运行中"。想查活动/控制台日志确认是否自动关机，两页面都被平台侧大面积 429 限流卡死读不到（等 15s 不退）。已停手避免制造更多 429。结论：开机生效，但"是否马上自动关机"无法证实——平台自报不稳定+限流风暴，状态同步滞后。建议等 5-10 分钟限流退后再看最终状态/日志，反复关机就找 Altare 客服。详见进度文件。
- 16:56 配置密钥登录（参考华为云，保留密码登录）：面板"设置→SSH"机制=粘贴公钥到 textarea + 点"添加密钥"，另有"关闭密码登录"按钮（用户明确不要碰）。找到本机华为云公钥 `id_ed25519_huawei_sg.pub`：`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICC8S0c3xsqXf9ljeeR4zqTYQIGgEeLHSx1UNohfcsqA autoclaw@huawei-sg-20261116`。粘贴并提交后，面板返回"Altare didn't respond just now, probably a quick restart"——平台重启+限流导致**提交未能确认成功**，刷新后页面卡加载态读不到密钥列表。已停手，不重复添加避免重复 insert。结论：密钥配置未完成，等平台恢复后需重试并验证；密码登录全程未被触碰（提交前后页面均显示"密码登录已开启"）。任务已 finish 保留用户 tab。
- 17:02 创建定时任务 `automation-1795165376357`「Altare 沙盒 SSH 密钥落地看门狗」，每10分钟（rrule `FREQ=HOURLY;BYMINUTE=0,10,20,30,40,50;BYSECOND=0`，因 rrule 不支持 MINUTELY 用 HOURLY+BYMINUTE 等效）。逻辑：tabbittab 接管面板→读 SSH 设置页→密钥没加就尝试加一次（幂等，绝不点关闭密码登录）→确认密钥在就用 id_ed25519_huawei_sg 私钥 SSH 验证→结果写进度文件。遇 429/重启跳过不硬刚。cwds=本项目。ACTIVE。
- 17:04 应用户要求更新该任务：仅当 SSH 返回 SSH_KEY_LOGIN_OK（密钥登录真正成功）时，才调用 automation_update 把自己 status 改 PAUSED 暂停；其余情况（密钥没加/429/连接拒/超时）一律不暂停，继续每10分钟重试。铁律"不碰关闭密码登录"保留。频率与 cwds 未变。
- 19:00 用户贴容器启动日志：Sandbox ready / SSH is on port 25055 / root@sandbox shell 可用 → 机器这次真起来了。实测 25055 端口 OPEN（T0）。但面板 SSH 设置页与控制台页仍被 429 卡在"加载中"（textarea=0，读不到密钥列表、拿不到 shell 输入框），团队名还在 Default/Sel

## beacon.qq.com 上报来源排查（10:11–10:30，✅ 完成）
- 用户截图 sing-box 日志：`otheve.beacon.qq.com/analytics/v2_upload?appkey=0WEB0702WZNO5AO2` 每秒上报。
- 定位：**雷霆游戏《九牧之野》PC 端**（`D:\jmzy_LTLauncher\`，jmzy.exe + LTLive.exe）内嵌腾讯灯塔 SDK。
- 证据链：netstat 抓连入 sing-box(127.0.0.1:10808) 的进程 → LTLive×7、jmzy×4；config 指向 leiting.com；官网核对 jmzy.leiting.com=九牧之野（com.leiting.jmzy）。
- 建议已给：退出游戏验证法；sing-box 路由加 `domain_suffix: beacon.qq.com → block`（走代理时 hosts 无效）。
- 进度文件：`进度/进度_20261120_1020_beacon排查.md`。

## 环境遗留问题（未修，需用户拍板）
- managed Python 3.13.12 缺 Lib/ 整个标准库 → 影响 WB 内所有 python 脚本。建议重装 managed python 或让其自愈。本会话 PowerShell 工具输出被吞，只能"落盘再读"绕过。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-20-19-46-45\.workbuddy-ai\memory\2026-11-20.md

## 19:46 排查曼谷 VPS xray 无法联网（查会话 ded810a4-1691-4e8e-baa1-a22617e99783）

- 会话 ded810a4（另一个 WB 会话）当天在 Altare 曼谷沙盒（th-bkk05.altare.global，Debian 12 proot 容器）手动部署了 Xray-core v26.11.9 VLESS-REALITY / TCP 443，导入 v2rayN 后没网。
- 本会话找到根因：**外部 443 端口没有映射到沙盒**，是 Altare 节点宿主机自己的服务（CloudFlare Origin Certificate）。证据：①沙盒"已停止"、Xray 未安装时外部 443 就 OPEN；②外部 openssl s_client 返回 CloudFlare Origin 证书；③沙盒内 127.0.0.1:443 返回 *.google.com（REALITY 正确转发 dl.google.com）；④服务端 debug 日志零公网连接；⑤服务端自连 127.0.0.1 测试成功。客户端报 x509 unknown authority = 连到宿主机的假证书。
- 沙盒唯一确认的外部映射：25055 → 容器 22（SSH）。
- 修复方向：面板"网络/端口分配"页加一条端口分配（外端口=容器端口），改 Xray config.json 端口并重启，vless 链接换新端口重新生成。
- 次要发现：本机全局环境变量 HTTP_PROXY/HTTPS_PROXY=127.0.0.1:10808（v2rayN 本地端口），会干扰 curl 等诊断工具。
- SSH 登录方式（持久有效）：`ssh -i ~/.ssh/id_ed25519_huawei_sg -p 25055 root@th-bkk05.altare.global`；Xray 服务端配置在 /usr/local/etc/xray/config.json，守护脚本 /usr/local/bin/xray-run.sh，PID 文件 /run/xray.pid，日志 /var/log/xray/。密钥登录已验证可用（会话 ded810a4 收尾时）。

## 19:52-20:20 用 tabbit 修面板端口分配（续上）

- 面板 console.altare.gg（Heliactyl Next 21.2.65，tenant 2f136cce-026b-4550-8f8d-f49e80cce719，server ba604928-7019-4588-b840-6bee810f2aa2）。tabbit CLI 在 %LOCALAPPDATA%\Tabbit\LocalAgent\bin\tabbit-cli.exe（nodejs 单次调用有 60 秒硬超时；任务中断后可用 finish + nodejs --group <groupId> 恢复保留的标签页）。
- 面板确认：免费档只有 1 个端口分配（25055 Primary）。「额外端口分配槽位」11.25 bolts 一次性，已购买成功（余额 50→38.75），槽位已绑定到服务器（显示 1/2 在用）。
- 卡点：创建分配的 POST /api/tenants/…/network/allocations 连续 502（Cloudflare 错误页=后端真挂，非限流），重试 6+ 次跨约 20 分钟未恢复；「域名」子页也报错（且疑似 Max 套餐功能）。平台当天全线不稳。
- 已建自动重试任务："Altare端口分配自动重试（成功后自动暂停）"，id 58607cef-b369-46cc-a802-a457e2b36202，每 15 分钟（FREQ=HOURLY;BYMINUTE=0,15,30,45），成功后自动改 Xray 端口+验证+写 D:\workspace\workbuddyai\Altare_新端口vless链接.txt 并自暂停。
- 本机附带修复：v2rayN GUI 在跑但 xray 内核死了（10808 无监听）——**用户澄清：内核是被上一个 WB 会话排查不出原因后主动杀掉的，非自崩**。Windows 系统代理 ProxyEnable 原为 1 指向 10808，我曾临时置 0；20:18 用户重启 v2rayN 后内核恢复（PID 6180，10808 监听），系统代理也已由 v2rayN 重新接管（ProxyEnable=1）。注意：自动任务跑面板靠 Tabbit 浏览器走系统代理，用户在 Altare 新端口链接生成前**不要**把 v2rayN 切到那个坏节点，否则浏览器又断。
- 21:39 用户拍板：B 方案（CF Tunnel/VLESS+WS 反代）**暂不执行，等几天看端口分配 API 恢复**，B 方案须等用户明确同意。决策已写入 D:\workspace\workbuddyai\Altare端口分配进度.md。已向用户口头预告过 B 方案细节（方案A=Altare面板域名功能可能要 Max 套餐；方案B=CF Tunnel 更推荐）。Tabbit 浏览器走系统代理，之前 ERR_PROXY_CONNECTION_FAILED 也是这个原因。

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）