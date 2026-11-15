---
layout: default
title: 技术点 · 2026-11-15
date: 2026-11-15 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-15.md, D:\AI work\workbuddy\2026-11-15-10-21-36\.workbuddy\memory\2026-11-15.md

## 跨 Agent Skill 安装流程沉淀为 skill（11:19-11:25）
- 用户问"给其他 agent 装 skill 的流程总结成 skill 了吗"→ 此前没有，本轮补建。
- 实测盘点本机各 agent 的 skill 目录与格式：
  - au（AutoClaw/OpenClaw 内核）：`~/.openclau-autoclaw/skills/`（全局，~70 个）+ `workspace/skills/`（工作区级）；Anthropic SKILL.md 标准兼容，WB skill 直接复制生效；`plugin-skills/` 为宿主内置禁改；旧残留 `~/.openclaw/skills/`（4 个）。
  - dsh：`~/.dsh/skills/`（3 个：cocoloop / safe-bulk-write-guardrail / tavily-search）；同样 Anthropic 标准直接复制生效；插件（`dsh plugin add`）与 skill 是两套体系。
  - Hermes：`D:\hermes-agent\skills\<分类>\<名>`，自有扩展格式（version/author/platforms/metadata.hermes.*，description≤60 字符、工具名用 hermes 内置名），**不能直接复制**；分 skills/ 内置与 optional-skills/ 两层。
- 新建 user 级 skill：`C:\Users\Administrator\.workbuddy\skills\cross-agent-skill-install\`（SKILL.md + scripts/sync_skill.py）。
  - sync_skill.py：单向同步 WB→au/au-ws/dsh，支持 --dry-run 预览 diff、同步前自动留 .bak-sync、跳过 .bak/__pycache__，已用 safe-bulk-write-guardrail→dsh dry-run 验证通过。
- 关键结论：au/dsh 复制即用；Hermes 必须改写格式，别反复重试复制。

## 跨 Agent 盘点二轮（11:23-11:30，用户指出一轮不全后重扫）
- 全盘重扫（用户主目录全部隐藏目录 + D 盘）新增发现的 agent skill 体系：
  - **QClaw** `~/.qclaw/skills/`（59 个，OpenClaw 系，metadata.openclaw 扩展，兼容）+ 空的 skillhub-skills/
  - **ZCode** `~/.zcode/skills/`、**Trae CN** `~/.trae-cn/skills/`（另有 builtin_skills 禁改）、**Qoder** `~/.qoder/skills/`、**QoderWork** `~/.qoderwork/skills/`（12 个）、**JoyCode** `~/.joycode/skills/`、**AtomCode** `~/.atomcode/skills/`、**Office Raccoon** `~/.office-raccoon/agent/skills/`、**CodeBuddy** `~/.codebuddy/skills/`、共享标准目录 `~/.agents/skills/`——全部 Anthropic SKILL.md 兼容，直接复制生效
  - **Ego 浏览器**用 symlink 分发（ego-browser → ~/.local/share/ego/ego-skills，真身目前为空=链接失效），同步时跳过 symlink
- 三轮补充（用户点名 Loomy 和商汤小浣熊）：
  - **商汤办公小浣熊** = `.office-raccoon`（二轮已盘到目录但没认出身份）：`~/.office-raccoon/agent/skills/` Anthropic 兼容，安装包 `D:\Program Files\raccoonoffice-desktop\`；已在 SKILL.md 里改名标注
  - **Loomy**（`D:\Program Files\Loomy\` + `AppData\Roaming\Loomy\`）：asar 有技能机制但技能走**应用内技能广场（云端）**，全盘无本地 SKILL.md 落盘目录（pets 空、leveldb 无路径）→ 不能复制文件装 skill，归入"无本地 skill 体系"组
  - D:\Program Files 全量装机清点：AutoClaw/CodeBuddy/DeepSeekHarness/JoyCode/LobsterAI/Loomy/QClaw/QianwenApp/Trae CN/WorkBuddy/WorkBuddyAI/ZCode/ZCodePreview/raccoonoffice-desktop 等（QianwenApp、WorkBuddyAI、ZCodePreview 未单独验 skill 目录）
  - 无 skill 体系：LobsterAI、美团 CatPaw、CherryStudio、box-agent、sheetagent、qoder-cli、joycoder；拼写错误旧目录 .openclaw-autocaw 勿用
- 已重写 user 级 skill `cross-agent-skill-install`：SKILL.md 全量清单（A 组 13 个可直装目标 + B 组 Hermes 改写 + 无体系名单 + 禁改目录），sync_skill.py 扩到 13 个目标代号、--list-targets、symlink 跳过、symlinks=True，已 dry-run 验证（api-test-pitfalls→qclaw 已一致 0 差异）。

## 四轮：按用户指定 7 个常用 agent 重构 skill（11:32-11:38）
- 用户指定常用 7 agent：WB 国内版 / WB 国际版 / AutoClaw 1.15 / ZCode / LobsterAI / Loomy / 办公小浣熊。
- 补测落定两个未知落盘点：
  - WB 国际版 = `~/.workbuddy-ai/skills/`（29 个，Anthropic 兼容）
  - LobsterAI = 用户级 `%APPDATA%\LobsterAI\SKILLs\`（58 个，目录名大小写是 SKILLs）+ 内置 `D:/Program Files\LobsterAI\resources\SKILLs\`（30 个禁改）；OpenClaw 系；启用状态存应用 store `skills_state`，复制后可能要在应用内启用一次
- 已重构 cross-agent-skill-install：SKILL.md 以 7 agent 为主体（1 源头 + 5 可直装 + Loomy 只能应用内广场），其余 agent 降为附录；sync_skill.py 新增 --to primary（一次推 wb-intl/au/au-ws/zcode/lobsterai/raccoon 六个目标）、secondary 目标组、symlink 跳过、--list-targets，primary dry-run 全通。
- 以后"同步技能到常用 agent"默认跑 --to primary。

## 五轮：Loomy 目录纠错（11:37-11:41，用户指正）
- 用户指正：Loomy 有用户级 skill 目录 = `C:/Users/Public/Loomy/e7d3e769f3f5/opencode/skills/`（70+ 个，Anthropic 格式，Loomy 内嵌 opencode 引擎，skill 落在 Public 共享区）。此前误判"无本地目录"是因为只扫了 AppData 和用户主目录，没扫 C:/Users/Public。
- 已更新 skill：Loomy 列为第 6 个可直装目标（hash 段提示可能随安装变化，找不到先 ls C:/Users/Public/Loomy）；sync_skill.py 的 loomy 目标改为动态探测 `C:/Users/Public/Loomy/*/opencode/skills`，primary 扩为 7 个目标，--list-targets 与 loomy dry-run 验证通过。
- 教训写进 skill 踩坑记录：扫 agent 目录别漏 C:/Users/Public。

## 七轮：触发词更新与重分发（11:43-11:47）
- 用户要求触发词必含「给其他agent装」「给其他agent分发」→ 已写进 SKILL.md frontmatter description + 正文触发词清单，并重分发到 primary 7 目标。
- 踩坑+修复：首次重分发被本机 safe-bulk-write-guardrail 护栏拦下（沙箱内 shutil.rmtree 触发 SAFE_DELETE_FAIL_CLOSED，windows 回收站不可用）→ 脚本改为「已存在=原地覆盖 copytree(dirs_exist_ok=True)，不删除」，既过护栏也更安全；stale 文件只提示不删。

## 八轮：searxng-web-search（自建搜索）补全（11:48-11:51）
- 排查 7 agent：有=WB国内/国际版、au全局+工作区、LobsterAI；缺=ZCode、Loomy、小浣熊。
- 用 sync_skill.py 补装到 3 个缺失目标（该 skill 源头只有单 SKILL.md，1 文件），全部 OK，7 agent 现已齐全。

## 九轮：自建搜索查 AlwaysData 代理三仓库（11:52-11:59）
- 用 searxng-web-search skill 搜出并用 gh api 核实星数：83★=hiifeng/V2ray-for-AlwaysData（2025-08）、"19★"实为 17★=Misaka-blog/xray-for-alwaysdata（2023-04 停更，19★ 是官方 docs 仓库无关）、14★=oyz8/AlwaysData-baihu 白虎面板（2026-09）。另挖到 AppsGanin/alwaysdata-xray（4★，2026-10，XHTTP 新路线）。
- 可行性结论：原理=SSH 上传二进制+Sites 设 User program+WS+TLS 443，技术上都能跑；但 AlwaysData Free 条款限个人非营利，代理属滥用，封号风险无解→只能当防失联备用节点+CF CDN。Free 档现为 1GB SSD/256MB RAM/¼CPU（早期 100MB 已上调）。注册需境外 IP。
- 教训：alwaysdata.com/en/plans/ 是 404，正确配额页在 help.alwaysdata.com 的 public-cloud-prices。

## 十一轮：首页改版为城市卡片式（12:19-12:28，用户反馈）
- 需求：顶部搜索框 + 默认 6 城实时天气卡片（无锡/昆明/普洱/建水/惠州/杭州，坐标内置）+ 查过的城市卡片自动排到下方（「🕘 最近查询」区，去重排除默认城）。
- 实现：app.py 加 DEFAULT_CITIES / city_card / fetch_cards，view_home 重写；CSS 加 .city-card 系列并清理重复 .grid 定义。
- 踩坑修复：①style.css 被 max-age=3600 缓存导致新样式不生效→链接加 ?v=2 版本号（今后改 CSS 记得 bump）；②启动瞬间 6 城并发拉数有偶发失败→http_json 加 1 次重试+0.8s 间隔，且失败不写缓存。
- 验收：Playwright 截图（weather-home-v3.png）6 城卡片带实时温度/天气/风力，大理查询后出现在最近查询区；缓存热后首页 6ms。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-14-23-25-11\.workbuddy-ai\memory\2026-11-15.md, D:\workspace\workbuddyai\2026-11-15-11-21-53\.workbuddy-ai\memory\2026-11-15.md

## 用 WizTree CSV 分析 C 盘高频占用 + 生成清理技能

用户要求：根据昨天那份 CSV 找出最容易占 C 盘的文件/文件夹，把清理流程做成 skill，以后不发 CSV 也能快速清理。

### 数据源与结论（T0，本机快照）
- `C:\Users\Administrator\Documents\WizTree_20261114233455.csv`（11/14 23:35，895,947 文件，223 MB）与 `WizTree_20261024115155.csv`（10/24，233 MB）。UTF-8 BOM，中文表头。
- 基线：10/24 可用 21.06 GB → 11/14 可用 5.17 GB（CSV 的 FREESPACE 字段），20 天净增 16.65 GB。
- CSV 列下标：文件名称0/大小1/分配2/修改时间3/属性4/文件5/文件夹6/…/FOLDERSIZE9/FOLDERALLOCATED10/**DRIVECAPACITY11/FREESPACE12/USEDSPACE13**/RESERVEDSPACE14。取错一位会把「已用」当成「可用」。
- **目录行的「大小」是递归总大小**，类别聚合只能用文件行。
- 最容易反复占空间的 5 类（11/14 口径）：客户端调试日志 4.78 GB（单日 +2.20，DEFER-DBG 刷屏，会回涨）、`*-updater` 升级包 4.49 GB / 仅 29 文件、Service Worker/Code Cache 5.03 GB（飞书 2.20 + Tabbit 1.40）、浏览器 Cache 2.08、包管理器缓存 2.37。合计可清 18–19 GB。
- 增量最大但不是垃圾：Docker 5.56+3.95 GB（10/30 新装）、飞书本体 2.74、`.office-raccoon` 2.47、有道笔记库 2.28。单文件最大 `docker_data.vhdx` 5.449 GB。
- 解析脚本（工作区）：`analyze_wiztree.py` → `wiztree_analysis.json`。

### 交付：技能 `cdisk-quick-clean`
- 位置：`C:\Users\Administrator\.workbuddy-ai\skills\cdisk-quick-clean\`（当前生效）+ 同步一份到 `C:\Users\Administrator\.workbuddy\skills\cdisk-quick-clean\`（旧客户端，两份逐字节一致）。分发包 `cdisk-quick-clean.zip`（工作区，官方 `package_skill.py` 校验通过）。
- 结构：`SKILL.md`（agent_created: true，中文，含触发词）、`scripts/cdisk_rules.py`（共享 P0/P1/P2 规则表 + FORBIDDEN 禁区 + 自动备份开关检测 + `\\?\` 长路径/DeleteFileW）、`scripts/scan_cdisk.py`（**主力，不依赖 CSV** 的只读扫描，quick/full 两模式）、`scripts/parse_wiztree_csv.py`（可选 CSV 增长对比）、`scripts/clean_cdisk.py`（默认 dry-run，须 `--execute`）、`references/targets.md`（本机实测清单）、`references/pitfalls.md`（自指备份等踩坑）。
- 设计决策：只读扫描与删除拆成两个脚本，中间必须人类确认；删除用 ctypes `DeleteFileW` 不进回收站；执行前查自动备份开关 + 5–200 MB 探针（free 没涨或 modify_backup 变大就停手）；分批 ≤10、审计增量落盘、`--max-seconds` 提前退出可重跑续做。
- **修过一个误判**：初版把 `ms-playwright`（浏览器二进制）和 `pnpm`（node_modules 硬链接 store）当缓存，实跑 `scan_cdisk.py` 才发现 0.373 GB 的 `chromium-1234\chrome-win64` 会被删 → 已从 P1 规则移除并加进 FORBIDDEN。以后新增规则必须先 dry-run 验证命中范围。

### 验证（T0，全部实跑）
- `scan_cdisk.py --mode quick`：239,424 文件 / 24.9s，P0 0.24 GB、P1 1.43 GB、P2 0.03 GB；`env=0 / settings_enabled=False / blocking=False` → 昨天关的自动备份开关已生效。
- `parse_wiztree_csv.py` 两份 CSV 各约 8s，基线与增长数字与手工分析一致。
- `clean_cdisk.py --tier p0p1` dry-run：792 目标 / 预估 1.67 GB，未删任何文件。
- 四脚本 `py_compile` 通过；`package_skill.py` → `Skill is valid!`。
- 当前 C 盘可用 **26.05 GB**（比昨天 23.96 又涨了约 2 GB；回收站现只剩 8 个文件 ≈0 GB）。本轮**没有删除任何文件**（除技能模板示例与 `__pycache__`）。

### 交付文档
- `C盘高频占用分析与清理技能说明_2026-11-15.md`（结论、数据可信度、TOP 清单、禁区、技能用法、验证结果）。

### 未解决 / 不确定（别瞎说）
- `DEFER-DBG` 调试日志的关闭开关没找到；只能靠重启客户端缓解回涨。
- 自动备份配置改 false 后新会话是否

## 追问：自动备份是什么时候来的 / 是不是新版加的 / 会不会连垃圾也备份

脚本：`probe_backup.py`（删除探针）、`investigate_versions.py`（新旧包关键词对比）、`backup_code_detail.py`（排除表与阈值）。结论已写进技能 `references/pitfalls.md` 第 10 节并重新打包。

- **当前状态（T0 实测）**：`settings.json` = `{"enabled":false,"maxSizeMB":1000}`（11/15 00:38 改）；环境变量 `CODEBUDDY_FILE_BACKUP_ENABLED=0`（`CODEBUDDY_SAFE_DELETE_ENABLED=1` 是另一套安全删除，别混）；客户端今天 10:17 重启（`logs\update\update-20261115.log`），昨天说的「需重启/新会话才生效」已兑现。探针：删 2 MB 临时文件 → C 盘 +1.99 MB、`modify_backup` 31 文件 / 2.345 MB 不变 → **开关已关且生效**。
- **是不是新版加的：基本是**。旧版 `D:\Program Files\WorkBuddy`（国际版，app.asar 编译 2026-08-07）整包 `fileBackup`=0、`security_center_file_backup`=0、`shouldModifyBackupBeforeWrite`=0、shim 里 `CODEBUDDY_FILE_BACKUP_ENABLED`=0，只有 `safe-delete-common`；CLI 主程序 `dist\codebuddy.js` 21 MB 里 `fileBackup`/`modifyBackup`/`documentBackup` 全为 0。新版 5.9.4（install-manifest `generatedAt=2026-10-29T15:51:49Z`，10/31 落地）里 `fileBackup` app.asar 174 次 / CLI 24 次。
- **但目录名不是新的**：`~\.workbuddy\workspace\sessions\4cb7837e-...\modify_backup` 建于 **2026-07-23 14:24**，28 个文件 / 2.30 MB，全是 `1.哈希.原文件名.md` 这类**文档编辑前版本快照**；旧版 `vendor\sandbox\sandbox-cli-gc.exe` 里也有 6 次 `modify_backup`。旧版只有轻量文档回滚，不会把删掉的缓存复制一份。
- 时间线（T0 文件时间戳）：7/11 旧版装 → 7/23 最早文档快照 → 8/7 旧版最后编译 → 10/12 WorkBuddyAI 目录创建 → 10/29 5.9.4 构建 → 10/31 落地 → 11/14 备份暴涨 5.30 GB。**具体哪个版本/哪天引入没有官方变更日志，不知道**；旧包自带 `v2.93.2.md` 里那条「自动备份」是损坏文件自动备份重建，与本功能无关，已排除。
- **会连垃圾一起备份：会**。`shouldModifyBackupBeforeWrite()` 只判断平台 + 开关 + 路径是否在排除表 + 规则 modifier，不看内容。排除表 `DEFAULT_MODIFY_BACKUP_EXCLUDED_DIRS` 只放过开发工具链（`node_modules`、`.venv`、`__pycache__`、`.pnpm-store`、`.gradle` 等）和系统临时目录；日志、`*-updater`、Service Worker、浏览器 Cache、`npm-cache` 都不在表里。常量 `FILE_BACKUP_DEFAULT_MAX_SIZE_MB=3000`、`THRESHOLD_MB=100`，但实测涨到 5.30 GB 超上限，**为何没拦住不确定**。
- 本次只写文档/日志 + 删探针临时文件，未动任何用户数据。

## 把 cdisk-quick-clean 分发到其它 agent

用户说「这个skill 分发到其他agent」，按本机多套 agent 技能目录理解执行（外发到 IM/云端未做，等用户点名）。

- **盘点**：本机 5 套用户级 skills 目录 —— `.workbuddy-ai`(29 技能，当前 WorkBuddy AI)、`.workbuddy`(75，旧版)、`.codebuddy`(1)、`.agents`(6)、`.openclaw`(3)。后 3 套格式都是 `SKILL.md` + YAML frontmatter(name/description)，与技能兼容，且都无同名冲突。`D:\Program Files\WorkBuddyAI\...\workbuddy-builtin\skills` 是内置目录，不动。
- **已分发到**：`.codebuddy\skills`、`.agents\skills`、`.openclaw\skills`，加上原有的 `.workbuddy-ai` 和 `.workbuddy`，共 5 份，逐字节校验 `BYTE-IDENTICAL`（8 文件 / 56.4 KB 每份）。
- **分发脚本** `distribute_skill.py`：只新增不覆盖、目标内容不同会跳过、`copy2` 后逐文件 `filecmp` 校验、写 `skill_distribution_record.json`、支持 `--dry-run` / `--source` / `--targets`、静默无窗口。已通用化：`HOME=expanduser('~')`、`WORKSPACE=os.getcwd()`，且脚本与解压出的 `cdisk-quick-clean/` 同级时自动用它当源（方便别的机器）。
- **技能自带** `references/installation.md`（适用条件、安装、验证、安全须知）；`SKILL.md` Step 1 改成「Python 3.8+ 标准库、自动读 USERPROFILE、仅 Windows + C 盘」。
- **两个包**：`cdisk-quick-clean.zip`（纯技能，官方 `package_skill.py` 校验通过）、`cdisk-quick-clean-dist.zip`（59.9 KB / 11 条目 = 技能目录 + distribute_skill.py + `CDISK_SKILL_INSTALL.md` + 纯技能 zip）。工作区另有 `CDISK_SKILL_INSTALL.md` 说明。
- **验证**：从 `.agents\skills\cdisk-quick-clean` 直接跑 `scan_cdisk.py --mode quick --max-seconds 20` 成功（17 万文件，C 盘可用 25.99 GB，自动备份开关 blocking=False），证明脚本自包含、不依赖源目录。
- **不确定**：各 agent 何时加载新技能（通常需新开会话/重启）未实测，不打包票；`.codebuddy`/`.openclaw` 是否分别对应 ACP peer `codebuddy`/`autoclaw` 只是推测。


# 2026-11-15

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）