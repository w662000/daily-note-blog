---
layout: default
title: 每日工作总结 · 2026-07-27
date: 2026-07-27 23:30:00 +0800
---

# 每日工作总结 · 2026-07-27

> 本总结由「每日工作总结生成」自动化任务，依据两个会话目录下的机器日志（`.workbuddy/memory/2026-07-27.md`）提炼而成：
> - `2026-07-27-11-25-53`（全天主任务：免费云资源盘点、free-resource-hub 项目、Replit 排障）
> - `2026-07-27-20-35-25`（晚间：豆包 AI Skill 调研/安装、Replit+Cloudflare 域名排障）
>
> 当天无纯日期文件夹，故产物落于主工作会话目录 `2026-07-27-11-25-53`。

## 一、今日完成事项

### 1. 免费云资源大盘点（free-for-dev 深度核实）
- 系统梳理了开源清单 `ripienaar/free-for-dev`（"不绑信用卡就能申请的云/VPS 资源"），产出一份主报告和十余份单条目分析。
- 逐项核实 30+ 个免费条目是否**真的免信用卡**、是不是**真服务器**，纠正了大量 README 过时/错误数字（如 Crystallize 目录项差 10 倍、Fibery 用户数/存储过时、Seafile 1GB 实为 30 天试用、Solo/Squash 疑似已停服）。
- 把资源归成四层：① 真·免卡服务器 ② 免卡 SaaS（非服务器）③ 工具型坑（面板/部署工具，机器另算+底层要卡）④ 开源可自建（Seafile 可拼回免卡服务器主线）。
- 额外跑了两个大段分析：**Generative AI 段**（20 家送免费 AI 模型/tokens，存报告）、**Web Hosting 段**（23 家，筛出 19 家真免卡）。
- 对 19 家免卡 Web Hosting **实测国内直连可达性 + 延迟**，筛出"配置好/国内快/不需代理"的子集（Vercel/Netlify/PandaStack 等直连可达；render/Neocities 需代理被墙）。
- 把核实过的真实免卡 OpenRouter 模型 `inclusionai/ling-3.0-flash:free` 加进 WorkBuddy 模型列表（现共 25 模型/13 个 OpenRouter）；`tencent/hy3:free` 核实并无免费版，按用户选择跳过。

### 2. "免卡"真相澄清（Alwaysdata / Serv00 / Zoho）
- **Alwaysdata**：原本以为免信用卡，用户实测注册要卡验证。经源码分析确认表单路径是硬门槛（Payzen 网关），且 Google OAuth 路径也按 IP 风控。已诚实致歉，并修正 Alwaysdata 指南、skill、主报告三处。推荐走 Serv00 作为真正免卡+SSH 的替代。
- **Serv00**：真正免卡+SSH，但当前注册通道满员关闭。其实昨天（07-26）已搭好**云端自动监控系统**（GitHub Actions 每 10 分钟探测放位→自动抢注→126 邮箱收验证码→通知），今天的"重新验证要不要卡"属重复劳动，已记入教训。
- **Zoho Mail**：免费版免卡但需手机号、且无 IMAP，不适合当程序收信通道（对比 DNSExit 免费档带 IMAP 更对口）。

### 3. 豆包视频 11 个 AI Skill 调研 + 安装
- 用户转发豆包视频，问那 11 个高频 AI Skill 能不能装到 WorkBuddy。
- 结论：7 个能装**等价** Skill（notebooklm-studio / playwright-browser-automation / impeccable / humanizer / skill-creator 等），1 个原生内置（Find Skills），3 个市场无同名需自建（Agent Reach / Gstack / Superpowers）。
- 实际安装 5 个等价 Skill + **自建 `agent-reach`** Skill（跨平台搜资料免 API，含工作流 + 平台选型参考）。
- 把昨天(07-26)的 serv00 注册监控脚本从 GitHub Actions **迁到 Apify Actor**（默认暂停，避免与云端版双跑冲突）。

### 4. free-resource-hub 项目（AI 免费资源中心，五合一）
- 从 `kb-assistant`（AI 知识助手，先试 PandaStack/Zeabur 都因要卡放弃，后上 Replit）演进到 `free-resource-hub`（用户认为 2C4G 只跑问答大材小用，改做功能更全的"AI 免费资源中心"）。
- 五大模块全部落地并本地验证：① 可浏览目录（39→63→64 条）② AI 问答助手（OpenRouter 免费模型检索增强）③ 资源存活监控 ④ 自动采集 ⑤ 跨平台搜索聚合（先 Agent 驱动，后改**搜索 API 驱动** Tavily/Exa/Perplexity，部署后 app 每日自动跑）。
- 部署到 **Replit Starter**（免卡、国内直连 0.31s、公开 URL），设 UptimeRobot 每 15min 保活；用户截图确认线上 **64 条卡片 + AI 问答正常**。
- 修复线上 unicode 乱码 bug（分类名半截字），新增 `POST /api/reseed` 端点让用户线上一键重建干净数据。

### 5. Replit 自动续期方案（绕开已死的 API token）
- 发现 Replit 已砍掉 `replit.com/account/tokens` 生成入口，原 `.github/workflows/republish.yml` 靠 API token 的路线已不可行。
- 改用**方案 B：Playwright 驱动 Replit UI + 会话 cookie 注入 Republish**，每周一自动跑；退出码分级 + 诊断截图产物兜底。用户导出 replit.com 会话 cookie 填入 Secret 即可闭环。

### 6. Replit + Cloudflare 自定义域名排障
- 用户 `ai.w662000.cc.cd` 访问报 525（SSL 握手失败）+ replshield 强制登录。
- 根因：Replit Starter **无自定义域名权限**（不签证书、CF 回源 SNI 不匹配）+ 默认 **Password protected**。
- 正解：Publishing → Visibility 改 **Public** + 点 **Republish**，DNS 直连 Public 部署即通；Worker 反代留作冗余兜底。

## 二、关键决策 / 注意事项

- **动手前先读记忆**：今天因没先读 handoff + 跨项目 MEMORY.md，把 Serv00 当"新发现"重复验证了一遍（其实 07-26 已建好云端自动注册系统）。教训：先读 `HANDOFF.md` 与 `~/.workbuddy/MEMORY.md` 再进对话；`conversation_search` 不能替代直接读记忆文件。
- **诚实纠偏**：Alwaysdata "免信用卡" 判断不够准（依据 README/社区而非实际注册末步），以用户截图 + 源码分析证伪后已致歉并修正三处文件。
- **安全红线**：明确拒绝伪造支付卡 token / 攻击支付接口（绕过金融反欺诈控制，越线）；`tencent/hy3:free` 核实无免费版，按用户选择不加进模型列表。
- **Replit 免费 Starter 硬限**：只能发 **1 个 app**，且代码公开（handoff 内容会可见）→ 用 free-resource-hub 轮换下线 kb-assistant 释放发布槽。
- **UptimeRobot ≠ 防过期**：保活只防"休眠"（让调度器每日跑），**不重置 30 天发布过期**，仍需每月手动 Publish 或方案 B 自动 Republish。
- **部署平台筛选结论**：PandaStack/Zeabur 都要绑卡 → Render 免卡但被墙（直连 http=000）→ 最终锁定 **Replit Starter**（免卡+国内直连+Secrets 环境变量）。
- **环境坑**：本沙箱代理做 TLS 拦截，`curl` 必须 `-k`；`/c/...` 当参数传给程序会被误解成 D: 盘相对路径，必须用 `C:/...` 绝对写法；pip 装包需放开沙箱联网。
- **OpenRouter `ling-3.0-flash:free` 是 reasoning 模型**：会烧光 `max_tokens` 在 reasoning 字段导致 `content:null` → 提到 2000 + 加回退免费模型链 + 3s 重试防限流。

## 三、生成的有用文件

| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| 主报告（无信用卡云资源分析） | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-for-dev-无信用卡云资源分析.md` | free-for-dev 全量核实：服务器向资源 + 非服务器逐项核实 + 过时纠正 + 停服标记 |
| Alwaysdata 注册与 SSH 上手 | `D:\AI work\workbuddy\2026-07-27-11-25-53\Alwaysdata-注册与SSH上手.md` | Alwaysdata 注册（OAuth 优先）+ 开 SSH + 最小 Flask 部署 + 保号雷区 |
| AI 免费模型与 tokens 分析 | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-for-dev-AI免费模型与tokens分析.md` | Generative AI 段 20 家送免费模型/tokens 核实（A 类真送 / B 类 BYOK） |
| Web Hosting 免卡分析 | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-for-dev-WebHosting免卡分析.md` | Web Hosting 段 23 家筛选：19 家真免卡 / 2 家存疑 / 3 家过时 |
| Web Hosting 配置与国内访问筛选 | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-for-dev-WebHosting-配置与国内访问筛选.md` | 19 家实测直连可达 + 延迟 + 配置评级 |
| 单条目详细分析（合集） | `D:\AI work\workbuddy\2026-07-27-11-25-53\{Solo,SquashLabs,Bonsai,WPJack,DNSExit,Crystallize}-详细分析.md` | 各条目核实留档（含 Solo/Squash 疑似停服、Bonsai/DNSExit 正面命中免卡） |
| 免卡部署平台对比 | `D:\AI work\workbuddy\2026-07-27-11-25-53\免卡部署平台对比-Zeabur推荐.md` | PandaStack/Zeabur/Koyeb/Northflank/Render/Replit 实测对比，最终推 Replit |
| kb-assistant 部署指南 | `D:\AI work\workbuddy\2026-07-27-11-25-53\kb-assistant-Replit部署指南.md` | kb-assistant 的 Replit 部署步骤（项目已轮换下线，留档） |
| free-resource-hub 主项目 | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-resource-hub\` | AI 免费资源中心五合一：app.py/db.py/reach.py/monitor.py/collect.py/retrieval.py/templates/ |
| Replit 自动 Republish 机器人 | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-resource-hub\republish_bot.py` | Playwright 驱动 Replit UI + cookie 注入 Republish（绕开已死 API token） |
| 自动续期工作流 | `D:\AI work\workbuddy\2026-07-27-11-25-53\free-resource-hub\.github\workflows\republish.yml` | 每周一自动 Republish + 诊断产物兜底 |
| serv00 监控 Apify 版 | `D:\AI work\workbuddy\2026-07-27-11-25-53\serv00-apify-monitor\` | serv00 注册监控迁到 Apify Actor（默认暂停，避免与 GitHub Actions 版双跑） |
| kb-assistant（已弃，留档） | `D:\AI work\workbuddy\2026-07-27-11-25-53\pandastack-kb-assistant\` | 早期 AI 知识助手版，已被 free-resource-hub 轮换替代 |
| 自建 agent-reach Skill | `C:\Users\Administrator\.workbuddy\skills\agent-reach\` | 跨平台搜资料免 API（SKILL.md + references/platforms.md） |
| WorkBuddy 模型列表（已更新） | `C:\Users\Administrator\.workbuddy\models.json` | 新增 `inclusionai/ling-3.0-flash:free`（OpenRouter 真免费，现共 25 模型/13 个 OpenRouter） |
| GitHub 私有仓库 free-resource-hub | `https://github.com/w662000/free-resource-hub` | 已 push（含 republish.yml 自动续期） |
| GitHub 私有仓库 kb-assistant | `https://github.com/w662000/kb-assistant` | 已 push；自动续期 workflow 已删除停用（项目即将下线） |

## 四、待办 / 风险

- **free-resource-hub 上线后需用户手动闭环**：
  - Replit 后台 Secrets 加 `OPENROUTER_API_KEY`（用户 key 已给，本地验证通过）；加 `SEARCH_PROVIDER`=tavily/exa/perplexity + 对应 key 开启每日自动聚合。
  - 浏览器导出 replit.com 会话 cookie（JSON）→ 在 free-resource-hub 仓库 Secrets 设 `REPLIT_COOKIE`（已设 `REPLIT_USERNAME=wxatp2022`，API token 路线已死不再需要）。
  - 发布后**删 kb-assistant 释放 Replit 唯一发布槽**（kb-assistant 仍占槽、线上仍可达、30 天过期）。
  - 等 Replit 拉取最新代码后，调一次 `POST /api/reseed` 修复线上分类乱码（已加端点，无需重部署）。
- **方案 B 风险**：Cloudflare bot 检测可能拦无头浏览器；Replit UI 改版可能使按钮没匹配上（退出码 3，看 buttons_dump 微调）；cookie 过期（退出码 2，重导）。均靠诊断产物兜底，不阻塞手动 Publish 兜底。
- **Alwaysdata 指南待改**：第 10 节"SERV00 作为替代"属冗余误导，应改为"指向已建云端监控系统"的引用（用户尚未确认）。
- **Apify 版 serv00 监控未实际部署**：默认暂停，需用户本地有 apify-cli + 登录 + 填 Input（serv00User/serv00Pass/mailUser/mailAuth）后才生效。
- **环境限制**：本沙箱出网受限（代理 TLS 拦截，curl 需 `-k`），且 WebSearch 本会话多次故障，全程靠 curl -k + WebFetch + Wayback 核查。本地直连路由异常好**不代表中国普通家宽**——Vercel/Netlify/Kinsta 系在家宽常被限速/重置，需用户本地自测。
- **Serv00 注册放位靠云端**：GitHub Actions 自 07-26 起每 10 分钟候着，开放自动抢注并邮件通知 w662000@126.com，用户查该邮箱即可，无需手动蹲。
