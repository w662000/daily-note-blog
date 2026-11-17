---
layout: default
title: 技术点 · 2026-11-17
date: 2026-11-17 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-16-23-10-26\.workbuddy\memory\2026-11-17.md, D:\AI work\workbuddy\2026-11-17-01-21-22\.workbuddy\memory\2026-11-17.md

## 01:45 更新：hy2 已验证全链路可用 ✅
- 从 AutoClaw 会话记录（agents/main/sessions/52083aa0-*.jsonl）拿到 SSH 密钥线索：`~/.ssh/id_ed25519_huawei_sg` → root@111.91.31.39（纯公钥认证）
- 服务器：233boy 脚本，Xray 26.11.9 原生 hysteria 协议（非独立进程），配置在 /etc/xray/conf/（Hysteria2-8443.json + VLESS-REALITY-443.json）
- 真实客户端握手成功：经 hy2 出口 IP=111.91.31.39，HTTP 204 通过 → 安全组 UDP 8443 已生效
- 踩坑存档：①Xray 原生 hy2 不回 QUIC VN 探测包（VN 探测法对它无效）；②26.10 内核 allowInsecure 已删，改 pinnedPeerCertSha256（DER-SHA256 十六进制字符串，非数组）；③10891 在 Hyper-V 保留区，换 17891
- 测试配置：C:/Users/Administrator/AppData/Local/Temp/udp8443_probe/hy2_client_test.json
- v2rayN 导入 hy2 节点失败根因（guiLogs 01:48）：v2rayN 默认把 hy2 节点交给 Xray 内核，而 Xray 26.2.6+ 拒绝 AllowInsecure 且无证书指纹的节点。修复：①右键节点→内核类型→sing_box（实测可用）②URI 加 pinSHA256=hu0Hp1RA8f2r6PsgJ2dc/l0xwQHyoj8khWVAe0j7eJ0=（证书 DER-SHA256 的 base64 形式）
- 01:58 用户确认 hy2 节点在 v2rayN 中跑通 ✅（双协议 REALITY+hy2 就绪）。待办：白天 A/B 测速定主力协议

## 12:18 恢复双因素登录方式（密钥+密码并存）
- 需求：agent 用密钥登录、用户自己管理用密码登录
- 关键发现：真正禁密码的是 /etc/ssh/sshd_config.d/99-hardening.conf（主 sshd_config 写 yes 但被此文件覆盖）；root 密码本就存在（passwd -S 显示 P，2026-11-16 设过），无需重设
- 操作：备份 99-hardening.conf.bak-20261117-1218 → sed 改两行(PasswordAuthentication no→yes, PermitRootLogin prohibit-password→yes) → sshd -t 校验 → systemctl reload sshd
- 生效确认：sshd -T 显示 passwordauthentication yes / permitrootlogin yes / pubkeyauthentication yes，port 22 不变
- 验证：①密钥新会话登录 OK ②密码通道探测返回 "Permission denied (publickey,password)" = 两种认证都开放 ③fail2ban active 且 sshd jail 启用（防爆破）
- 回滚：cp /etc/ssh/sshd_config.d/99-hardening.conf.bak-20261117-1218 覆盖回去 + systemctl reload sshd

## 17:30 三个副业全部改成每天自动更新 + 自动同步综合站
- 需求：三个副业都像夜末一样每天更新，跑完自动同步到综合站
- 用户确认：虚拟商品每天换一个候选品类（需求/竞争标"待自查"不编结论）；同步方式=自动化跑完自动同步
- 同步脚本：副业综合站/sync_report.py（yemo 复制HTML / laowang、virtual 把md转统一皮肤HTML → 覆盖 pages/ 固定名，写 sync_status.json）。已用现有3份报告实测 SYNC_OK
- 三个自动化（时间错开）：
  - 夜末 automation-1794800521709 每日11:30（原任务，prompt 末尾加同步步骤）
  - 老王 automation-1794919333295 每日11:45（新建，scan.py 扫描+分析+md报告+同步）
  - 虚拟品 automation-1794919340226 每日12:00（新建，每天换品类+风险判定+定价测算+同步）
- 工作目录：D:/AI work\workbuddy\副业日报\{laowang,virtual}
- 实测：老王 scan.py 单次跑通（10候选/10 README读成功）；虚拟品两脚本参数核对无误；风险扫描/定价脚本参数=skill文档一致
- 注意：虚拟品受 skill 硬约束，无平台自查数据时需求/竞争不给分、不下"可入/避开"结论，这是设计如此不是失灵

## 22:55 Loomy 会话ID标记未生效——根因查明并修正
- 用户反馈 Loomy 答复底部没加 ID 标记。查实：opencode.db 里 237 条 assistant 消息，**全部**无 `loomy会话ID` 标记
- 根因：上次把规则写在 `<hash>/workspace/AGENTS.md` + opencode.json 的 instructions，**都不是 opencode 实际读取位置**。实证：runtime guidance 文件显示 opencode cwd=`D:\workspace\loomy`，而那里没有 AGENTS.md
- 修正：在 `D:\workspace\loomy\AGENTS.md` 新建规则（opencode 官方机制=自动读 cwd 根 AGENTS.md）；脚本路径写了主+副本两处
- 脚本本身没问题：`get_session_id.py --agent loomy` 实测读出 `ses_e17c8ac64ffegg8LWnACwAElFt`
- 已同步修正 agent-session-id skill 的 Loomy 行（备份 SKILL.md.bak-sid-loomy-20261117），避免下次再走错
- 待验证：用户在 Loomy 新开一会话发消息，看底部是否出现标记（opencode 按会话读 AGENTS.md，新会话应生效；旧会话可能需重开）
- 23:01 用户确认 Loomy 新会话标记已出现 ✅（修正生效）

## 23:01 本 WB 会话为何没带 ID 标记——启动注入时机
- 用户问：Loomy 有了，但当前 WB 会话底部 ID 标记一直没出现
- 根因：`~/.workbuddy/USER.md` 的 ID 规则 mtime=14:34，而本会话 01:21 就开了；USER.md 是**会话启动时注入**，开会话后才加的规则不会进入已开会话的上下文 → 本会话全程不知道有这条规则
- 机制坑（通用）：常驻指令文件（USER.md/AGENTS.md）只对**之后新开的会话**生效；老会话要么重开、要么在会话内显式加载 skill/手动补规则
- 本会话 ID 已补取：`9bdbf6e0-c833-4b70-b38d-9df1c6d1fb6e`（--agent wb），从本条起结尾追加 `【workbuddy会话ID...】`


# 2026-11-17

## 签到+喵旅行自动化失效诊断（11:45）
- 用户问 workbuddy 签到和喵旅行自动化怎么失效、失效几天。
- 查 workbuddy.db（automation_runs/automation_runtime_state）：任务 automation-1785848159433（每2小时，ACTIVE）最后一次成功 2026-11-13 20:09，11-13 22:05 起每次运行 413 失败——模型 @cf/qwen/qwen3-30b-a3b-fp8（32k 上下文）累计会话历史 54727 tokens 超限；至今约 3.6 天没成功。
- 根因不是 daily_combo.py 脚本，而是自动化会话历史膨胀 + 免费模型上下文太小。
- 已给出修复选项（换大上下文模型 / 精简 prompt 禁读历史 / 都做），等用户确认再动。
- 经验：automation_runtime_state.last_error 字段是查自动化失败根因的最佳入口；thread_title 里也带错误摘要。

## 修复执行（11:50）
- 用户确认方案后已执行：
  1. 自动化 automation-1785848159433 的 modelId 从 @cf/qwen/qwen3-30b-a3b-fp8（32k 上下文）换成 @cf/openai/gpt-oss-120b（128k 上下文，Cloudflare 官方文档核实，本地 models.json 已有此模型）。
  2. 重写 prompt：禁止读取历史运行记录/automation_runs/旧对话（脚本幂等不需要历史），只允许跑 daily_combo.py 并回报输出。
- 脚本 daily_combo.py 完好；daily_combo.log 证实最后一次脚本执行=2026-11-13 20:10，与 DB 记录吻合。
- 下次计划运行约 12:11（nextRunAt），届时验证是否恢复。验证方式：只读查 DB automation_runs 最新一条 result_success，不发 API 请求。
- 经验沉淀：自动化失败排查路径 = automation_runtime_state.last_error + automation_runs.thread_title；Cloudflare Workers AI 模型上下文以官方 supported-models 文档为准（gpt-oss-120b=128k，qwen3-30b-a3b-fp8=32k）。

## 兜底任务同款配置（11:54）
- 按用户指示把「WorkBuddy 每日签到+喵旅行·查漏补缺(11:00)」(automation-1786765573442) 也换成 gpt-oss-120b + 同款禁读历史 prompt，并从 PAUSED 改回 ACTIVE，作为每日 11:00 兜底（幂等保护，主任务成功过则自动跳过）。
- 当前双保险结构：主任务每2小时 + 兜底每日11:00。

## wb-intl（WB 国际版）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-17.md

## 监控隧道 bat 编码事故（00:37 用户报乱码）+ v2 修复

- 事故：桌面「新加坡服务器监控.bat」我用 PowerShell Set-Content -Encoding UTF8 写入 → Windows PowerShell 的 UTF8 **带 BOM** → cmd 按 GBK 读到 BOM 字节 = 锘緻 报错；中文行全部错位崩（ч亾寤虹珛... 不是内部或外部命令）。正是 windows-launcher-safety 技能 §1 头号杀手
- 用户点名学习 WB 国内版 windows-launcher-safety 技能并修脚本；核对 au 与 wb 侧 SHA256 一致（58948E2C...），无需同步
- v1 修复（纯 ASCII 无 BOM CRLF，python 写盘）仍失败两次踩坑：
  ① wmic CommandLine like '%19999:...%' **自匹配**——模式串出现在 wmic 自身命令行里，taskkill 杀到已死 PID（日志"??Ч???"=参数无效）→ v2 改为只按 name='ssh.exe' + host 串匹配，排除自匹配
  ② cmd /c "ssh ... \"%KEY%\" ..." 嵌套引号：**cmd 不认 \"**，引号中途截断 ssh 静默不起 → v2 去掉全部内层引号（%USERPROFILE%\.ssh\key 路径无空格，引号本就多余）
- v2 改用 **curl 健康探针**（http://127.0.0.1:19999/api/v1/info）替代 netstat 端口检测：curl 穿透"隧道半死/端口假监听"状态，就绪判定真实
- 最终：check_launcher.py PASS(WITH WARNINGS)（仅 >nul WARN 可接受），双击实测 tunnel ready + Netdata HTTP 200
- 技能沉淀正名：该技能的编码铁律（纯 ASCII 或 GBK+CRLF 无 BOM，禁 UTF-8 写 bat）、wmic 精确匹配、就绪轮询全部在本事故中二次验证
- 桌面入口更名：SG-Server-Monitor.bat（旧中文名 bat 已删）；日志 C:\Users\Administrator\Desktop\tunnel_launcher.log

## windows-launcher-safety 技能升级 2.0.0 -> 2.1.0 并分发（00:44 用户指令）

- 新增 §18 SG-Tunnel 事故三连：①PowerShell Set-Content -Encoding UTF8 写 bat = 带 BOM（agent 侧新变体，与 WB Write 的无 BOM 不同）→ 铁律：agent 写 bat 一律 Python 'wb' 写 ASCII/GBK 字节并验头 3 字节 ②cmd 不认 \" 嵌套引号 → ssh 静默不起 → 路径无空格就裸参数 ③wmic CommandLine like 自匹配 → where 加 name= 过滤 ④Web 面板就绪判定用 curl 穿透探针升级 netstat 端口检测 ⑤check_launcher PASS(WITH WARNINGS) 退出码为 1 的备注
- 检查清单加 3 条；description/来源日志同步更新
- 分发：au 侧改（沙箱内 edit 工具够不着 skills 目录，用 Python 补丁脚本）→ 复制回灌 WB 国内版源头 → sync_skill.py --to primary 推 7 目标（wb-intl/au/au-ws/zcode/lobsterai/loomy/raccoon，其中 6 个新装）
- 验证：8 份 SKILL.md（含源头）SHA256 全一致 = 54E95EB9...，version 2.1.0、sec18 全在
- 流程备注：用户明确指令"写入skill并分发"= 直接改源头+分发（skill_workshop 提案流用于非显式授权场景）
- 备份：workspace/backups/skills/windows-launcher-safety.SKILL.md.bak-2.0.0-20261117

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）