---
layout: default
title: 技术点 · 2026-11-18
date: 2026-11-18 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-17-22-32-26\.workbuddy\memory\2026-11-18.md, D:\AI work\workbuddy\2026-11-18-14-41-01\.workbuddy\memory\2026-11-18.md

## 14:41 查今日定时任务运行情况（只读）
- 数据源：`~/.workbuddy/workbuddy.db` 的 automations / automation_runs / automation_runtime_state（T0 系统一手记录）。
- 截至 14:41：今天 16 次运行、去重 12 个任务 → 8 成功 / 4 失败；晚间任务未到点。
- 失败 4 个：①灾变看门狗(automation-1794889378320) 3 次全败=429×2+ECONNRESET×1，今天无邮件告警保护；②签到喵旅行查漏补缺11:00(automation-1786765573442) 429；③美团领券(automation-1794562873327) missed 补跑 60s 未建 session；④有道云补发qwen垫底(automation-1787577004531) missed 补跑 60s 未建 session。
- 根因：glm-4.7-flash 被 429 限流（看门狗/查漏补缺都用它，单点风险）；网络/代理 ECONNRESET；早上约10点开机导致 missed 集中补跑并发抢资源。
- 成功亮点：签到+喵旅行合并(automation-1785848159433) 前两次 ECONNRESET、14:21 第三次成功，幂等正常（喵旅行中+已签到自动跳过）。
- 详情见 进度/进度_20261118_1441.md。

## 15:48 换模型：看门狗+查漏补缺 glm-4.7-flash → glm-4-flash-250414
- 用户要求把两个撞 429 的免费模型换成 `glm-4-flash-120414`；核对 models.json 该 ID 不存在，判断是笔误，用户确认改用真实存在的 `glm-4-flash-250414`（今天跑成功的补发/巡检任务同款，未撞限流）。
- 改前 automation_update view 读全配置；只改 modelId 一个字段，其余未动。
- 两个任务：automation-1794889378320（看门狗·每2h:30）/ automation-1786765573442（签到喵旅行查漏补缺·每日11:00）。
- 已回读数据库确认 model_id=glm-4-flash-250414、status=ACTIVE、rrule 不变。下次运行自动用新模型，效果待后续运行观察。

## 18:10 核查有道云三轴上传状态（只读，结论：没传完）
- 今天11:14 publish_train 日志：工作日志·11-18 有道云保存 OK；项目流/技术点·11-18 均 search 查询失败被 SKIP；step3_youdao FAIL 1800s 超时。
- v3 重建 PHASE3 今天11:30 重传 CRASH：upload_youdao.py timeout 3600s；闸门 .youdao_pause.json 已10:00过期。
- youdao_final_state.json 全盘不存在 → 重建未收尾（G5 对账也因此永远跳过）；dedupe_plan.json 空结果未执行。
- 三轴目录ID：worklog 7587B5CC…/projects C533B557…/techpoints 9C31CBCE…
- 详情见 进度/进度_20261118_1810.md。未改动任何文件。

## 19:43 找到删596篇的元凶BUG + 熔断
- **根因**:计划任务 `YD_Rebuild_Logon`(LogonTrigger开机自启,Enabled=true,注册11-17 11:19)每次登录跑 `pythonw collect_delete_rebuild_v3.py --delete-now`。该脚本 PHASE 2b(L188-189)逻辑:`todo2=[笔记 for 笔记 in 三目录 if id not in done_ids]`——把"ID不在历史删除清单"的笔记一律当残余删除。quick_fill 新传的笔记ID当然不在清单→被全删。昨晚21:33删644篇(含刚传596),今早10:24开机又删1篇,下次开机还会删。
- **熔断**:备份 v3(.bak-antibug-20261118)后在入口加闸门——无 `.ALLOW_YD_DELETE` 授权文件即 sys.exit(0)。实跑验证:输出[CIRCUIT-BREAK]删除未授权退出,py_compile通过。今后默认不删,授权文件不存在=安全。
- 注意:YD_Rebuild_Logon 任务本体仍在(开机触发),但脚本已熔断;schtasks/PowerShell系统工具被安全策略禁,未删任务本体。若要彻底删任务需用户放开"系统工具"策略。
- 后台直传 task NeBamN 正常(320/611零失败,LogonTrigger不重启不受影响)。

## 22:10 用户决定手动删 YD_Rebuild_Logon，已告知位置
- 任务定义文件：`C:\Windows\System32\Tasks\YD_Rebuild_Logon`（3670字节，UTF-16 XML，mtime 11-17 11:19:40）
- 注册表残留：`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\YD_Rebuild_Logon`（存在）
- 提醒用户：光删XML文件不够，注册表TaskCache也有项；推荐用任务计划程序GUI删（自动清两处）。脚本已熔断，删任务不紧急。


# 2026-11-18 工作日志

## intern-ai 10 模型同步到 WB 国际版

- 需求：把国内版已验证的 10 条 intern-ai 同步到 WB 国际版。
- **关键发现**：WB 国际版数据目录是 `~/.workbuddy-ai/`（不是国内版的 `~/.workbuddy/`），模型清单在 `~/.workbuddy-ai/models.json`；国际版进程是 `WorkBuddyAI.exe`（国内版是 `WorkBuddy.exe`），安装目录 `D:\Program Files\WorkBuddyAI`。依据 agent-session-id skill 记录。
- 数据源：直接从国内版 `~/.workbuddy/models.json` 读 10 条 intern-ai 原样复制（端点/key/模型昨天已实测验证，无需重测，避免触发限流）。
- 结果：国际版 41 条 → 51 条，10 条 intern-ai 全部回读确认，URL/key/id 唯一性校验通过；保持 indent=2 格式。
- 备份：`~/.workbuddy-ai/models.json.bak-add-intern-ai-20261118-195130`
- 脚本：`D:\AI work\workbuddy\2026-11-17-22-32-26\add_intern_ai_wb_intl.py`（幂等，检测已有则跳过）
- 待办：**需重启 WB 国际版（WorkBuddyAI.exe）** 模型选择器才显示；未擅自重启以免打断用户会话。

## 副业综合站（8870）三栏目「每日报告」子菜单对齐

- 需求：夜末/老王/虚拟三条线都要有「每日报告」历史列表，原来只有夜末左侧有，老王和虚拟只有当天最新报告（覆盖式）。
- 站点位置：`D:\AI work\workbuddy\2026-11-17-01-21-22\副业综合站\`，服务脚本 `D:\AI work\workbuddy\sidehub_serve_8870.py`（端口 8870）。
- 三个栏目：yemo(夜末) / laowang(老王) / virtual(虚拟选品，目标文件 virtualgoods.html)。

### 改造（两处文件）
1. **`sync_report.py`**：加归档 + 索引。
   - 新增 `ARCHIVE_PREFIX`/`SHORT`/`NAMES` 映射、`parse_date()`、`archive()`、`rebuild_index()`。
   - 每次同步除了覆盖固定最新文件（yemo.html/laowang.html/virtualgoods.html），再写一份带 **8 位 YYYYMMDD** 的归档 `<前缀>-YYYYMMDD.html`，并重建 `pages/index.json`。
   - 踩坑：归档日期最初用 4 位 MMDD，`rebuild_index` 里误按 `mmdd[0:4]` 当年份 → 解析成 `1118--`、label 变 `-`。**改用 8 位完整日期**后无歧义，已清理旧 4 位归档文件。
2. **`index.html`**：左侧三个栏目的子菜单改为**动态读取 `pages/index.json`** 渲染，不再硬编码 11-17；修复 `goSrc(link, src, key)` 原来硬编码 `data-k="yemo"` 的 bug（点老王/虚拟的历史链接会错误高亮到夜末）。

### 历史数据（重要事实，不要凭空补）
- yemo 源目录 `C:\Users\Administrator\.workbuddy\skills\yemo-git-radar\data\reports\` 有 11-16/17/18 三份 → 补成 3 天归档。
- 老王源目录 `D:\AI work\workbuddy\副业日报\laowang\`、virtual 源目录 `...\virtual\` **各自只有 11-18 一份 md**；两个自动化任务（automation-1794919333295 / ...340226）记忆显示 11-18 是**首次运行**，11-17 无报告产出 → 历史无法补，不是漏同步。

### 验证（Playwright MCP 实测，非推断）
- 三栏目左侧子菜单全部动态渲染：夜末 4 条（最新+11-18+11-17+11-16）、老王 2 条、虚拟 2 条。
- 每个链接 `goSrc(this,'pages/xxx-YYYYMMDD.html','栏目key')` 带正确 key。
- 跨栏目交互：在老王栏目点夜末 11-16 → 高亮切 yemo、面包屑更新、iframe 加载 `yemo-20261116.html`、子菜单正确切换。**全部通过**。
- 最新文件一致性：`yemo.html` == 源 11-18；服务 index.html/index.json/归档页 HTTP 200。

### 自动化兼容性
- 三个自动化任务都会调用 `sync_report.py`，改一处即三端生效；归档与索引在每次同步时自动完成，无需手改 index.html。

### 备份/产物
- 归档：`pages/yemo-20261116.html`、`yemo-20261117.html`、`yemo-20261118.html`、`laowang-20261118.html`、`virtualgoods-20261118.html`
- 索引：`pages/index.json`

## wb-intl（WB 国际版）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）