---
layout: default
title: 每日工作总结 · 2026-08-13
date: 2026-08-13 23:30:00 +0800
---

# 每日工作总结 · 2026-08-13

> 来源：会话级机器日志 `D:\AI work\workbuddy\2026-08-13-11-01-50\.workbuddy\memory\2026-08-13.md`（11,179 字节，全天主线）。当前自动化会话 `2026-08-13-22-40-58` 无独立日志，以该会话日志为准。

## 一、今日完成事项（分点，通俗语言）

1. **通达信分时预警公式「股价由绿翻红」**
   - 先理清通达信分时线红绿判定规则：现价 > 昨收 = 红，< 昨收 = 绿，相等 = 白。由此推出「由绿翻红」在数学上等价于「分时价上穿昨收价」。
   - 交付两套公式：方案 A 技术指标公式（主图叠加，分时主图看 DRAWICON/DRAWTEXT 信号）+ 方案 B 条件选股公式（配合「功能 → 预警系统 → 条件预警」自动弹窗+声音）。另附严格版 `CROSS(C, DYNAINFO(3))`（不算「刚好等于昨收」的白线瞬间）。
   - 配了 SVG 示意图说明红区/绿区/昨收虚线/上穿信号点。

2. **ser00（serv00 监控）项目 126 邮箱配置定位**
   - 厘清「ser00」= serv00 免费主机监控项目，目录 `D:\AI work\workbuddy\2026-07-25-12-10-12\`。
   - 找到邮箱 `w662000@126.com`、IMAP `imap.126.com:993` / SMTP `smtp.126.com:465`；确认授权码 `MAIL_AUTH`/`SERV00_USER`/`SERV00_PASS` 的真值当年存进了 **GitHub Actions Secrets**，本地文件只有变量名无明文。
   - 交付本地 imaplib 脚本 `126_imap_read.py`（放当日会话目录），用授权码登录 IMAP 轮询收件箱抽验证码链接；云端版在 `daily-note-blog/serv00-monitor/`。

3. **conversation_search 检索能力实测（纠正「对话不能查」误解）**
   - 用户质疑「授权码搜不到 = 对话记录不能查」，实测澄清：能查历史对话，但有 3 个局限 ≠ 不能查——① 默认只搜最近 7 天；② 语义 top-N 排序非精确匹配（对 16 位随机串检索极弱）；③ 归档对话不进索引。

4. **workbuddy.db 结构实测 + serv00 起源会话精准定位**
   - 确认 `sessions` 表只存会话元数据（id/title/status/cwd/时间戳），**不含对话正文**；正文在 conversation_search 服务端索引。
   - 定位 serv00 起源会话 `id=c493ad8b-c442-4021-9859-0e296d9f22ad`、`cwd=2026-07-25-12-10-12`、`status=archived`、标题「解决phpbb中markdown未渲染问题」（标题不含 serv00 → 标题搜也漏）。全库 65 条 archived 被 conversation_search 排除，这才是搜不到的根因。
   - 14:11 按用户确认**解除归档**（`archived → completed`，备份 `workbuddy.db.bak_unarchive_20260813_141117`），解除后 conversation_search 成功召回该会话，验证「归档=检索盲区」假设成立。

5. **密钥管理红线新增（14:14）**
   - 用户明确：密钥绝不只存在聊天里。确认本次授权码没丢是因为当年存进了正经保密库 GitHub Secrets，不是聊天靠谱。
   - 今后处理任何密钥/凭证：主动建议落正经保密库（GitHub Secrets / 密码管理器 / 本地 gitignored `.env`），绝不只留聊天里；已记入跨项目 `MEMORY.md`「密钥/凭证管理铁律」。

6. **拆除 serv00 监控项目（15:13–15:20，用户下令停用+删除）**
   - 按红线先只读侦察，再 AskUserQuestion 逐条确认（4 项全选推荐），后执行，全成功：
     - GitHub Secrets：`gh secret delete` 删光 `w662000/daily-note-blog` 的 5 个相关 Secret（MAIL_AUTH/MAIL_USER/SERV00_PASS/SERV00_USER/AUTO_REGISTER），复核空列表。
     - 本地会话目录 `2026-07-25-12-10-12`：只删 `serv00_monitor.py`/`.bat`（精准，不误伤同目录 Gaming4Free/Discord/子域名），备份留 `.serv00_deleted_20260813/`。
     - WB 自动化 `automation-1785033795089`「Serv00 注册开放探测(HOURLY后备)」软删。
     - 仓库 `D:\AI work\daily-note-blog`：`git rm` 移除 `serv00-monitor/`+`.github/workflows/serv00-monitor.yml`，commit `6c9ab28` push 到 master（`deploy.yml` 保留）。

7. **AutoClaw 启动修复（20:30，用户截图 SyntaxError 崩溃）**
   - 症状：导入新模型后重启失败，弹窗 `SyntaxError: Unexpected token ')'` at `app.asar/out/main/index.js:158408`（实为多余的 `}`）。
   - 根因：`index.js` 第 158408 行多了一个孤立的 `}`（158407 行的函数已闭合）；三个 asar 文件大小完全相同 → 内部发生等长字节替换，怀疑导入模型时写坏了包内代码。
   - 修复：`npx asar extract` → `node --check` 定位 → Python 删掉第 158408 行多余 `}` → 再 `node --check` 通过 → `npx asar pack` 重打包 → 备份损坏版为 `app.asar.broken_20260813_2033` 并覆盖 `D:/Program Files/AutoClaw/resources/app.asar`。
   - 验证：`node --check` 通过；启动后 AutoClaw 数据目录日志 20:38 有活动更新、无致命错误（无头环境「退出码0立即退出」非崩溃，用户有头环境正常）。

8. **火山引擎方舟 API 403 诊断（21:05）**
   - 用户调 GLM-5-2（endpoint `ep-20260813201925-sn47j`）连续 `403 ... your account has an overdue balance` → **账户现金余额为负（欠费）**，不是 token 耗尽。
   - 厘清火山方舟三桶计费互不通用：①现金余额 ②代金券 ③赠送资源包（如活动送 200 万 token）。赠送 token 无现金属性、不能还欠费；账户一旦现金欠费即全账号锁死，所有 API 返回 403。

9. **Hermes Studio(:8650) vs WebUI(:8787) 模型数不一致根因（22:15）**
   - 答：否，两个前端读不同文件。
   - WebUI → `C:/Users/Administrator/.hermes/webui/models_cache.json`：108 条唯一模型，UI 显示 66 = 自身过滤视图（启用中/dedup）。
   - Studio → `C:/Users/Administrator/.hermes/cache/model_catalog.json`（openrouter39+nous30=69）+ `cache/openrouter_model_metadata.json`（**1194** 条 OpenRouter 全量）→ 展示「可添加的模型宇宙」100+。
   - 真相源 `config.yaml`：实际配置 79 模型。不同步诱因：两缓存重建时间不同（webui 22:11 / studio 22:03），且 22:03 `config.yaml` 曾检测损坏（加 GLM-5.2/volcengine 那阵），目录按损坏态重建、WebUI 按修复态重建 → 对不上。

## 二、关键决策 / 注意事项

- **通达信预警**：条件预警周期必须选「1 分钟或分时」，选日线 `REF(C,1)==DYNAINFO(3)` 恒假永不触发；`DYNAINFO` 系列是实时行情函数，盘后/停牌不预警；信号天然只响一次（翻红后下一分钟 `REF(C,1)` 已在昨收上方，条件自动失效）。
- **GitHub Secrets**：引用不存在的 Secret 会注入空串，需代码兜底。
- **检索边界**：`completed`/`working` 会话可正常检索，`archived` 65 条是盲区；要找项目配置最靠谱是**直接翻磁盘目录**（如 `2026-07-25-12-10-12/HANDOFF.md`），而非搜聊天原文。
- **高危删除铁律**：一律先只读侦察 + AskUserQuestion 弹框逐项确认，不擅自执行（本次 4 项全部确认后落地）。
- **AutoClaw 修复副作用**：改变了 asar 大小（341MB 含 node_modules，原 280MB 外挂 unpacked）；原 `app.asar.bak-20260807/20260813` 提取不完整，**不推荐直接回退覆盖**。
- **火山方舟**：赠送 token 是「消费抵扣券/资源包」无现金属性，不能还欠费；欠费需充现金抹平（1–5 分钟恢复），否则 GLM-5-2 持续 403（且会连累依赖该账号的 WebSearch 等联网调用）。
- **Hermes 缓存对齐**：需重启 Hermes gateway 按当前 config.yaml 重建两份缓存，属高危动作，**未擅自执行**，待用户确认。

## 三、生成的有用文件（表格）

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 126 邮箱自动读取脚本 | `D:\AI work\workbuddy\2026-08-13-11-01-50\126_imap_read.py` | 本地 imaplib 登录 126 IMAP 轮询收件箱抽验证码链接 |
| 通达信「由绿翻红」公式（A/B/严格版） | 会话内交付（未落独立文件） | 分时主图信号 + 条件预警弹窗声音；严格版用 CROSS 不算白线瞬间 |
| 分时红绿区 SVG 示意图 | 会话内配图 | 说明红区/绿区/昨收虚线/上穿信号点 |
| 解除归档备份 | `C:\Users\Administrator\.workbuddy\workbuddy.db.bak_unarchive_20260813_141117` | 解除 serv00 会话归档前的 workbuddy.db 备份 |
| AutoClaw 损坏版备份 | `D:\Program Files\AutoClaw\resources\app.asar.broken_20260813_2033` | 修复前的损坏 asar，供回退参考 |
| serv00 本地删除备份 | `D:\AI work\workbuddy\2026-07-25-12-10-12\.serv00_deleted_20260813\` | 删除 serv00 监控脚本前的本地备份 |
| daily-note-blog 提交 | `D:\AI work\daily-note-blog`（commit `6c9ab28`） | 移除 serv00-monitor/ 与 workflow，push 到 master |
| 跨项目密钥铁律 | `~/.workbuddy/MEMORY.md` | 新增「密钥/凭证管理铁律」：绝不只存聊天里 |

## 四、待办 / 风险

- **P0 火山方舟欠费**：用户在控制台查欠费金额/来源 + 看资源包绑定哪个 model + 充现金抹平；否则 GLM-5-2 持续 403，且本机任何依赖该账号的联网调用（如 WebSearch）也锁死。
- **P0 126 授权码停用**：需用户去 mail.126.com 网页「客户端授权密码」手动关闭（网易无公开 API）；因 4 处已删光，即便不禁用也无任何东西在用该授权码。
- **P1 AutoClaw 根因**：导入模型为何写坏包内 `index.js` 代码未查，本次先保能启动，后续观察是否复现。
- **P1 Hermes 缓存对齐**：Studio/WebUI 模型数仍对不上，需重启 gateway 重建缓存（高危，待用户确认）；当前配置真相源 config.yaml=79 模型可用。
- **P2 目录混放风险**：`2026-07-25-12-10-12` 是「大杂烩」目录（多项目混放），后续任何删除须再确认范围，避免整删误伤。
- **P2 归档检索盲区**：65 条 archived 会话在 conversation_search 中不可见，若要恢复历史会话需手动改 status（可逆）后再搜，但只回摘要、不含正文。
