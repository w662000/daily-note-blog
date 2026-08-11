---
layout: default
title: 技术点 · serv00-monitor（GitHub Actions 云端常驻探测 + 邮箱自动注册）
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · serv00-monitor：GitHub Actions 定时探测 + 126 邮箱 IMAP 收码自动注册

> 对应项目轴 Handoff：`2026-07-26-handoff-serv00-monitor`
> 目的：从「Serv00 免费主机注册开放自动监控」提炼可复用技术资产——云端 cron 常驻探测、ClawBot 凭据不可达时的通道降级、GitHub Actions 空 Secret 兜底、动态表单解析。下次做「放号/补货/抢注类云端监控」直接复用。

## 一、技术选型（这个项目用了哪些技术栈 / 组件，怎么定的）

| 选型项 | 选定 | 落选 | 选型依据 |
|---|---|---|---|
| 调度 | **GitHub Actions（cron 每 10 分钟）** | 本机探测脚本 + 弹窗 | 云端常驻、不依赖本机 24h 开机；本机沙箱无外网（T1） |
| 通知通道 | **126 邮箱（SMTP_SSL + IMAP）** | 微信 ClawBot 推送 | ClawBot token 在 WorkBuddy 不落本地明文，云端 Actions 读不到；126 有标准 IMAP/SMTP 授权码（T1 实测） |
| 验证码获取 | **IMAP 轮询 126 收件箱** | 人工看邮件 | 自动提取激活链接，闭合注册流程（T1） |
| 凭据存储 | **GitHub Secrets（5 个）** | 仓库文件 / 硬编码 | Secrets 不入库、不进日志（被 `***` 打码）（T0） |
| HTTP 客户端 | **Python 标准库 `urllib`** | 第三方 requests | Actions runner 无需装依赖，启动更快（T1） |

## 二、实施要点与关键技术（落地用了哪些做法）

1. **cron 写法与抖动**：`serv00-monitor.yml` 用 `schedule: cron: "*/10 * * * *"`；注意 GitHub Actions cron **有排队延迟，不保证准点**（常见 5–15 分钟偏差，属正常）（T1）。
2. **空 Secret 兜底（致命坑）**：GitHub 引用不存在的 Secret 会**注入空字符串而非报错**；脚本崩在 `int("")`。所有环境变量读取必须做空串兜底（T1 实测）。
3. **函数返回值解包同步**：`fetch()` 从 2 元组改成 3 元组后，主流程只解包 2 个 → `ValueError: too many values to unpack`；改返回结构必须同步所有解包点（T1）。
4. **排错必展开 step 内部日志**：顶部 Annotations 摘要会把 Secret 打码成 `***`，看不到真错误，必须展开失败 step 内部日志（T1）。
5. **动态表单解析**：`extract_form` 抓注册页所有 input（含隐藏 csrf）→ `fill_payload` 自动填 username/email/password/tos → POST；硬编码字段会因 csrf 变化失效（T1）。
6. **凭据自动识别**：`@126.com` 域名自动识别 `smtp.126.com:465` / `imap.126.com:993`，减少需填 Secret 数量（MAIL_SMTP_HOST/PORT 等不填）（T1）。
7. **启动自检**：先打印配置自检（4×True）+ 实际使用的 SMTP/IMAP 主机，便于发现空 Secret（T1）。
8. **降级路径**：`AUTO_REGISTER=off` 或注册失败 → 仅发「开放提醒」邮件，人再手动处理（T1）。
9. **合规红线**：Serv00 免费版 ToS 禁代理/VPN/隧道，这个号只建站/SSH，绝不跑代理；免费号 90 天不登录会删，注册后记得偶尔 SSH 保号（T1）。

## 三、模块职责划分（系统 / 组件如何分工）

- **GitHub Actions workflow**：调度器，每 10 分钟触发 runner。
- **`monitor.py` 探测段**：GET 注册页，关键词匹配 block 文案判断开放与否。
- **`monitor.py` 注册段**：开放时解析表单 → 填值 → POST 提交。
- **`monitor.py` IMAP 段**：轮询 126 收件箱（每 30s × 最多 5 分钟）找验证邮件 → 提取激活链接 → 访问激活。
- **`monitor.py` SMTP 段**：把账户信息发到 126 邮箱通知。
- **GitHub Secrets**：凭据边界，不落库不进日志。
- **降级路径**：自动注册失败时退化为「仅提醒」，保证人仍能收到信号。

## 四、如何选型（可复用的决策方法论）

- **是否用 CI cron**：先问「能否接受 5–15 分钟抖动 + 不保证准点」。能接受就用 CI cron（零成本常驻）；要准点/高频就回本机或独立服务器。
- **通知通道优先「凭据可导出」**：封闭 App 的推送 token 若拿不到（ClawBot 不落明文），直接排除；选 SMTP/IMAP 这类标准协议、授权码可配置的方案。
- **探测与执行解耦 + 加开关**：先让探测段稳定跑（只观察），再开 `AUTO_REGISTER` 执行动作；出错时降级为提醒而非硬失败。
- **CI 脚本把一切外部输入当「可能为空串」**：引用 Secret / 环境变量都要兜底，避免漏填一个就崩。
- **动态解析而非硬编码**：目标站表单字段（csrf 等）会变，解析页面动态填充比硬编码健壮。

## 五、深化学习指引（想深入看这些）

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| GitHub Actions `schedule` / cron 语法与延迟 | docs.github.com/actions | 官方文档 | T0 |
| GitHub Actions Secrets（空串注入行为） | docs.github.com/actions/security | 官方文档 | T0 |
| Python `smtplib` / `imaplib` | docs.python.org/3/library | 官方文档 | T0 |
| 126 邮箱客户端授权码获取 | 126 邮箱帮助中心 | 官方文档 | T0 |
| Serv00 免费主机 ToS（禁代理 / 90 天删号） | serv00.com 条款原文 | 官方条款 | T1 |
| ClawBot token 在 WorkBuddy 不落本地明文 | 本项目实测 + 官方文档无查看入口 | 自己实测 | T1 |
| Serv00 实际放号规律 / Actions cron 抖动实测范围 | 社区经验 | 印象级，待核实 | T2 |

## 六、技术结合点（这些技术怎么协同，1+1>2）

- **CI cron + IMAP 收码 + SMTP 通知**：三者串成「云端常驻探测 → 自动收验证码 → 完成激活 → 邮件回执」的全自动闭环，不依赖本机开机，也不依赖人工看邮件。
- **Secrets 空串兜底 + 启动自检**：空串兜底防止漏填崩溃，启动自检把「配置错误」在第一次运行就暴露，比跑到一半崩更省时间。
- **动态表单解析 + 自动填充**：让脚本对目标站小改版（csrf 轮换）有韧性，比硬编码字段寿命长。
- **AUTO_REGISTER 开关 + 邮件降级**：同一套代码既支持「全自动抢注」也支持「只提醒人来处理」，风险更可控——验证稳定前只开提醒，确认无误再开自动。

---
> 本文为技术点轴（对应 Handoff 2026-07-26-serv00-monitor）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合。每个 Handoff 都应有一篇对应技术点，与项目轴一一对应。
