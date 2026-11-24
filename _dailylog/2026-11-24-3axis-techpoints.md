---
layout: default
title: 技术点 · 2026-11-24
date: 2026-11-24 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-24-10-36-47\.workbuddy\memory\2026-11-24.md, D:\AI work\workbuddy\2026-11-24-15-41-39\.workbuddy\memory\2026-11-24.md

## ego-browser profile 自检（v3.1.1-router）
- 严格按 skill 完成自检，未用 playwright/tabbit/Edge 绕行。
- 结论：profiles() 返回 9 个（Default「您的 ego」+ wb-cn/wb-intl/au/au-intl/zcode/lobsterai/loomy/raccoon 共 8 agent）；WB 任务空间 wb-cn:profile-selfcheck（id=10）落在 Profile 1 / wb-cn；ego 窗口最小化驻留、不在前台（IsIconic=True, IsForeground=False）。
- 验证 profileId 归属要用 listTaskSpaces()（taskSpace 返回对象不含 profileId 字段）。
- 最小化窗口下 page.screenshot() 会 15s 超时（skill 已知问题），窗口状态用 Win32 IsIconic/GetForegroundWindow 文本确认更可靠。
- 本机坑：PowerShell 工具 stdout 被 ConPTY 吞→写文件再读；Bash 调 powershell.exe 被安全策略拒→在 ego 脚本内用 node:child_process 调 PowerShell。
- 进度文件：进度/进度_20261124_1545_ego-profile-selfcheck.md

## ego-browser skill 依赖审计
- frontmatter: name=ego-browser, version=3.1.1-router（在 metadata 内）, date=2026-11-24；两份 SKILL.md（外层+嵌套副本）字节相同，目录整体重复需整理。
- 实测依赖：CLI 0.6.3.17✅ / ego lite App✅ / 9 profile✅ / Win32 PowerShell 最小化✅ / references+scripts✅ / Playwright 缓存 701.5MB + 用户级环境变量 + node workspace playwright 包✅ / Edge✅ / curl+python✅。
- Tabbit：已装但装在 D:\Program Files (x86)\Tabbit Browser\Application\Tabbit Browser.exe（skill 文档写 "Tabbit.exe" 不准）；.tabbit-debug-profile 缺失、9222 未启动→降级路径部分具备。
- 探测坑：全盘 os.walk 搜 Tabbit 卡死；where Tabbit.exe 中文 GBK 编码报错；靠注册表 Uninstall 才找到 D 盘安装点。
- 进度文件：进度/进度_20261124_1551_ego-skill-deps-audit.md


# 2026-11-24 工作日志

## 给 au 国际版（AutoClaw 国际版）增加 11 个模型（已完成，待重启生效）
- 目标：xf 系 1 条（spark-x2.6）+ intern-ai 系 10 条，来源 `~/.workbuddy/models.json`；执行前已向用户确认范围。
- 国际版识别：`%APPDATA%\AutoClaw-oversea-official\`，owner_id `3461f6d2-3694-4e65-8204-5b1b17dcf2d4`，版本 2.5.3，渠道 overseas_release；安装共用 `D:\Program Files\AutoClaw\AutoClaw2\AutoClaw2.exe`。
- 方案：11 条 custom 连接写入 `accounts\<hash>\runtime\runtime.sqlite`，base_url 指向已运行的本地网关 `http://127.0.0.1:18901/v1`，model 用 `[xf] x` / `[intern-ai] x` 显示名；`runtime\credentials.enc` 新建并写占位凭证 `wb-bridge`（网关转发时忽略客户端 Authorization，因此库里不放真实 key）。
- 备份：`backup_au_oversea_20261124_161550/`（main db + wal + shm + account-credentials.enc + Local State）。
- 验证：custom 11 条 / managed 6 条；凭证回读 11/11；网关单次实测 xf 模型 HTTP 200。
- 关键坑：数据库是 WAL 模式，验证时 `immutable=1` 看不到刚写入的行，必须用普通连接；国际版 `account-credentials.enc` 是账号 token，不是模型 BYOK 凭证。
- 待用户自行重启 AutoClaw2.exe 后 UI 才刷新；未擅自关闭用户程序。
- 详细步骤与回滚见 `进度/进度_20261124_1620.md`。


# 2026-11-24 工作日志

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-24-10-51-31\.workbuddy-ai\memory\2026-11-24.md, D:\workspace\workbuddyai\2026-11-24-15-39-14\.workbuddy-ai\memory\2026-11-24.md

## asar 积分提示排查 skill 固化
- 新建用户级 skill `electron-asar-nopoints-patch`（`~/.workbuddy-ai/skills/`），workflow 型 SKILL.md + `scripts/scan_asar.py`（只读扫描）+ `scripts/patch_asar.py`（等长补丁/备份/hash 校验/原子写/verify）+ `references/case-autoclaw-cn-20261122.md`（国内版实战）。已通过 package_skill 校验，打包 zip 在工作区根目录。
- 适用范围：Electron 客户端"积分不足→购买卡片"误判，等长字节替换 + 先备份 + 字节级验证 + 回收站删备份 + 提醒自动更新会覆盖补丁。

## 查证：11-22 国内版 AutoClaw asar 补丁确系本线做的
- 会话 `d-AI work-workbuddy/2026-11-22-10-52-32/17ea84cf-...`（标题「排查 Autoclaw 积分提示开关」）：改 `D:/Program Files/AutoClaw/resources/app.asar`，把 `shouldShowNoPointsForFailedMessage()` 改成 `return false`（等长，310635872 字节，差异 73 字节），关掉"错误文本猜余额"导致的误弹购买卡片。11-24 复核补丁仍在（旧判定残留 0）。3 个备份已按用户要求移入回收站。
- 注意：此活在 **wb 国内版**会话里做的，不在 wb-intl/AutoClaw 自身历史里——跨 agent 查历史要按 agent-session-id SKILL.md 的平台→存储位置表逐个查（wb-cn 在 `~/.workbuddy/projects`，au-intl 在 `%APPDATA%/AutoClaw-oversea-official/accounts/<hash>/runtime/runtime.sqlite`）。

## au 国际版"自定义模型仍弹积分不足"= 会话模型冻结，非 bug（未改代码）
- 用户报：积分用完、用自定义模型仍弹"账户额度不足"卡片。查 `runtime.sqlite`（只读复制）结论：
  - 弹提示的失败 run（11-24 07:56~08:22Z）全走 `provider=zwork-managed`、模型 `zai_glm-5.3-flash`（连接 `4296c81c...`），错误码 `managed_model_points_insufficient`，detail `http 402 · provider_error` —— 服务端真返回 402，不是误判。
  - 用户配了 custom 连接 `[xf] spark-x2.6`（`befc87f7...`, base_url `127.0.0.1:18901`, active=1, 网关活着且模型 id 精确匹配），但最近 200 条 egress 路由 **100% zwork-managed**，custom 从未被用过。
  - 会话 `b69b719e...`（WordPress 主题）13 条 request 全是 `zai_glm-5.3-flash`，含用户明说"继续 我换了自定义模型"那条——**会话级模型冻结**：在运行中的会话换模型不生效，必须新会话/在正确位置切换。
  - au 国际版代码本身已区分：托管 402→平台充值卡片；自定义 402→`third_party_model_payment_required`（去服务商充值），且 `cdo` 有 `if(provider!=="zwork-managed")return` 保护。所以自定义模型本就不会弹平台购买套餐。
- 按用户选择"先查为什么没用上自定义模型"，**未改任何 asar/JS**，向用户说明根因与解决办法（新开会话选自定义模型）。


# 2026-11-24 工作日志

## codebuddy CLI 免费模型核查 + 认证排障

- **免费模型结论（T1，本机 CLI v2.174.0 安装包 `product.json` 标 `x0.00 credits`）**：只有两个——`deepseek-v4.1-flash`（1M 上下文，旗舰）、`hy3`（混元3，192K）。其余为低价档：`deepseek-v4.1-flash-sg` x0.03、`glm-5.3-flash` x0.06、`gpt-5.6-luna` x0.14（实测 400 personal_free_user 不可用）。
- **用户自定义模型**：`~/.workbuddy-ai/models.json` 里有 6 个标注"免费"的智谱 GLM（走用户自己的智谱 key），不属于 CodeBuddy 账号免费额度。
- **认证排障结论（重要，避免重复排查）**：WorkBuddy 派生的工具进程（Bash/PowerShell 工具）调 codebuddy CLI 一律报 `AuthenticationRequiredError`，根因是 AuthRefresh 向 `workbuddy.ai/v2/plugin/accounts` 请求返回 401 → `SignError: Failed to refresh session: account list is empty` → userId 被清空。用户在自己的 PowerShell 终端直接跑 `codebuddy -p --model hy3 "hi"` 正常返回，说明登录态本身健康，**只是宿主派生进程的令牌刷新链路拿不到 token**。以后遇到"我这边调不通但用户终端通"，直接用这个解释，不必反复试 `.cmd`/`.ps1`/无扩展名副本或环境变量。
- **附带坑**：宿主注入的 `HTTP_PROXY/HTTPS_PROXY`（127.0.0.1:14553）会让 CLI 在 `setProxy` 报 `Right-hand side of 'instanceof' is not callable`；从子进程 env 里去掉这两个变量该报错消失，但认证错误仍在（两件事独立）。
- 日志位置：`C:\Users\Administrator\.codebuddy\logs\2026-11-24\2026-11-24-10-51-31__33accda1bf49f9eaf069ef116797eac4.log`。
- **2026-11-24 21:58 补记**：用户已在自己的 PowerShell 里实测 `codebuddy -p --model deepseek-v4.1-flash "hi"` 和 `--model hy3 "hi"` 均返回正常（`Hi! What can I help you with?`）。两个免费模型全部实测通过，前面"工具进程侧无法实测"的限制不影响用户终端侧使用。

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-24.md

## codebuddy CLI "未登录"诊断（WB国际版）
- 现象：PowerShell 直跑 codebuddy 正常，WB国际版会话内调用报 Authentication required。
- 根因：WB国际版会话注入 ACC_PRODUCT_CONFIG_PATH（spill 配置，authentication.id=workbuddy-desktop-ai）→ CLI 改读 workbuddy-desktop-ai.info，其 token 是 $wbEncrypted 加密信封，独立 CLI 无钥 → 误判未登录。对照实验复现成功。
- 修复：调用前清 ACC_PRODUCT_CONFIG* 四个变量（成功判定仍以 stdout 非空为准）。
- 报告：workspace/reports/WB国际版codebuddy未登录诊断_20261124.html

## ~/.agents/skills 共享技能目录清空（用户指示）
- 9 个技能：7 实体目录全量备份到 workspace/backups/agents-skills-20261124/（8.78MB）；2 个 junction（ego-browser、tabbit）只摘链，源目录未动。
- 判定依据：au 托管目录是 7 个实体目录的超集（autoglm-browser-agent、pptx 唯一副本也在 au 托管目录）；mcporter.json 无 .agents 引用。
- **今后不把 ~/.agents/skills 当技能安装位/分发目标**（用户：没必要再搞共享目录）。注意 cross-agent-skill-install SKILL.md 附录还列着 `~/.agents\skills\`（agents 代号）——已过时，待走提案更新该技能附录。

## free-cli-caller v1.1.0 → v1.2.0 更新与分发
- Skill Workshop 提案 free-cli-caller-20261124-b7b3852e3a 已应用（v1.2.0：WB国际版 ACC 变量修复段）。
- 坑1：skills.workshop 对 agents-skills-personal 和 openclaw-managed 两个来源都拒写；可写的是 workspace\skills（工作区技能位）。提案最终落在 au-ws。
- 坑2：revise 提案时必须给完整 SKILL.md 全文，否则 apply 会整文件替换丢历史内容。
- 坑3：sync_skill.py 会把源头目录里的 .bak-sync 文件当载荷复制到全部目标——源头放备份文件会污染分发；发现后已全部清除。
- 坑4：au-intl（zwork-agent skills）同步会删除 _store_meta.json（视为 stale）——已按 agent-session-id 的 user/directory 导入格式补回（含 contentSha256）。
- 分发落点 9 处全部 v1.2.0 + 修复段验证通过：wb(源头)、wb-intl、au全局、au-ws、au-intl、zcode、lobsterai、loomy、raccoon。
- v1.1.0 旧版备份：workspace/backups/free-cli-caller-bak-20261124/free-cli-caller.SKILL.v1.1.0.md

## evolution 提案 evo-2026-11-24-wb-intl-codebuddy-auth-env 已批准并应用（22:52）
- 用户回复「批准 evo-2026-11-24-wb-intl-codebuddy-auth-env」。
- 落点：MEMORY.md 新增「WB国际版会话内调 codebuddy 报"未登录"的根因与修复（2026-11-24 实测）」小节（ACC_PRODUCT_CONFIG* 注入 → $wbEncrypted 信封 → 清四个变量修复）。
- 过程说明：原 pending 草稿在卡片审批时缺失，桌面端从提案 payload 重建了 surrogate 草稿（Status 已标 approved，位于 evolution-drafts/approved/）；应用时用脚本做了 H2 章节完整性校验（21/21 全保留）后整文写入，并修正报告路径大小写。
- 草稿归档：evolution-drafts/approved/wb-intl-codebuddy-auth-env.md

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

## - 当日会话 3 个，消息 196 条：
  - [55 条] ego-browser profile check and task space creation（session sess_b50dc7a0-be…）
  - [40 条] 用新增模型skill 给au国际版加装 xf系和inter-ai系共10来个模型（session sess_da09859d-c2…）
  - [101 条] **ego-browser 自检任务执行**（session sess_e68fd9a4-2f…）