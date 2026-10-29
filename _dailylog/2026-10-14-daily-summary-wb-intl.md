---
layout: default
title: 每日归纳 · WB 国际版 · 2026-10-14
date: 2026-10-14 23:30:00 +0800
---

# WB 国际版 · 每日归纳 · 2026-10-14

> 数据源：D:/workspace/workbuddyai  （agent id = `wb-intl`）

## 一、工作日志

### 工作日志文件：`.workbuddy-ai/memory/2026-10-14.md`

# 2026-10-14

## 保住 Phase 4 成果：MCP 注册 + skill 固化（用户指令："该注册就注册 该做成skill就做"）

1. **MCP 注册**：`C:/Users/Administrator/.workbuddy-ai/mcp.json` 新增 `agent-teams` 条目
   （node 22.22.2-6 → `D:/workspace/workbuddyai/agent-teams/mcp-server.mjs`，
   env `AGENT_TEAMS_WORKSPACE=D:/workspace/workbuddyai`）。
   验证：JSON 合法；stdio 握手 `initialize → tools/list` 返回 **14 个 captain 工具**。
   注意：新 server 不会自动生效，需用户在连接器管理页对 `agent-teams` 点"信任/启用"。

2. **Skill 固化**：`C:/Users/Administrator/.workbuddy-ai/skills/agent-teams/SKILL.md`
   （用户级，quick_validate 通过，`agent_created: true`）。
   内容：触发/不触发、前置检查（judge peer 启动命令）、8 步标准工作流、
   escalated vs halted 处置、14+4 工具速查、P0 硬规则（无窗口/多行走文件/不替成员改代码）、
   环境变量表。示例 scripts/references/assets 已删。

Phase 4 成果至此双通道保住：MCP（运行时）+ skill（触发与知识层）。

---

## 【00:15-00:45】Phase 5 全部完成（159/159 测试）

**5.1 交付审计**：`quality.mjs` 新增 `gitStatus`（异步 git status --porcelain=v1，
windowsHide，非仓库优雅降级）/`auditFromStatusText`（复用 Phase 4 分类原语，
in_scope/undeclared/out_of_scope + rename 取新路径）/`describeAuditSection`/
`runDeliveryAudit`（每轮落 `review/<task>/r<n>/audit.json`）。judge 与 pipeline
两条评审路都先审计后评审，审计节进评审 prompt；`reviewHistory.auditSummary` +
`t.audit` + task schema 补字段。沙箱注意：execFileSync EBUSY → 测试用异步 spawn；
porcelain v1 未跟踪目录折叠为 `src/`，测试用暂存文件拿文件级条目。

**5.2 活动面板**：`activity.mjs`（buildActivityData / renderActivityHtml /
writeActivityReport）—— 静态单文件 HTML、服务端渲染、HTML 转义、prefers-color-scheme。
队长每次 `agent_teams_status` 重新生成 `<stateDir>/activity.html` 并返回
`activityPath`；成员调用不写盘。示例：`examples/gen-activity-demo.mjs`
→ activity-demo-zh/en.html。

**5.3 i18n**：`mcp/locales/zh-CN.json` + `en-US.json`，`loadLocale(tag)`
（默认 zh-CN，未知 tag 回退 zh-CN），`AGENT_TEAMS_LOCALE` 选语言。
服务端协议字符串/事件名/状态名保持英文键（面向程序，不翻译）。

**5.4 触发层核对**：SKILL.md 补 活动面板/交付审计/audit 触发词 + Phase 5 小节，
quick_validate 通过。

**回归**：159/159（148 原有 + 6 审计 + 5 面板/i18n）。Phase 5 完结，待 Phase 6
（PreToolUse 兜底、孤儿回收、注册 ~/.workbuddy-ai/mcp.json ✅已提前做、全量回归）。

## 【01:00-01:10】per-member 模型 + 随时人工改（用户需求）

- `agent_teams_add_member` 升级为 **upsert**：对已有成员传 model/provider 即重排路由
  （优先级 request > team config > captain，与创建时一致），下次 spawn 生效
  （spawn 在 run 时读 member.route.model）；只传 persona 不动模型；
  provider 无 model 拒绝且保留旧路由；fire member:updated 事件。
- 免费三模型：deepseek-v4.1-flash（默认/队长） / step-5-preview / hy3，
  `AGENT_TEAMS_MEMBER_MODEL` 是团队默认，成员可各自覆盖。
- 测试 tests/member-model.test.mjs 4/4；全量 **163/163**。
- 注意：st.members 里队长本身占一行 role='captain'，计数要过滤。
- demo 面板已按用户指派重生成（w1=step-5-preview, w2=hy3, w3=dsv4.1-flash）；
  SKILL.md 已补 upsert 用法，校验通过。

## 【01:07-01:15】Phase 6 全部完成（168/168 测试）—— 六阶段移植收官

**6.1 孤儿回收验收**：机制 Phase 3 已有（claims/<taskId>.claim 带 pid，
scheduleTick 对死 pid/过期 claim 回收：recovered=true + round+1 + attemptId=null；
updateTask 的 E_STALE_ATTEMPT 拒绝旧 attempt；agent_teams_resume 按需跑同一恢复）。
本阶段补齐计划验收测试 tests/recovery.test.mjs 2/2：
强杀队长（claim marker 换死 pid）→ 重入冷恢复 → 旧 attempt 报 done 被拒 →
新 claim 拿新 attempt；resume 按需回收同样通过。

**6.2 PreToolUse 兜底**：`hooks/pre-tool-use.mjs`（成员 CLI 的 PreToolUse hook）。
拦截成员对 captain-only `agent_teams_*` 的调用：exit 2 + stderr 拒绝理由，
并追加一行到 `<stateDir>/hook-blocks.log`；成员 4 工具与非 agent-teams 工具放行；
stdin 不可解析 fail-open（绝不卡死会话）；无子进程无窗口（P0）。
安装：成员 settings.json hooks.PreToolUse → node .../pre-tool-use.mjs。
测试 tests/hook.test.mjs 3/3（create_task 拦截并记录 / 放行路径 / 全家族拒绝）。

**6.3 Automation 定时 tick**：仓库定义 `automations/agent-teams-tick.json`（含
prompt/rrule/guardrails）；环境注册表已创建同名自动化（每小时，ACTIVE，
id 72d9f308...，cwd=D:/workspace/workbuddyai）。用途：队长空闲时兜底 tick
（依赖晋升、孤儿回收、面板刷新）。约束：绝不创建/改动团队状态。

**6.4 注册 MCP + 全量回归**：mcp.json 注册早已完成（00:10）；本次全量
**168/168**（163 + 2 recovery + 3 hook）。

**六阶段全部完成。** 移植状态：Phase 0-6 ✅；评审 judge 模式真实验证 LIVE；
pipeline 模式遗留（produce>600s，另案）。

---

## 【10:00-10:30】评审 peer 惰性自动拉起（ensurePeer）完成（172/172 测试）

**需求**（用户拍板选 A）：skill/MCP 触发时自动拉起 judge peer，不进自启动菜单。

**交付**：
- `mcp/lib/peer.mjs`：`ensurePeer()` 复用 start-review-peer.mjs 的已验证引导路径
  （peers.json 驱动：clearEnvPrefixes + setEnv + 网关密码 + 账号 token）。
  就绪探针用正确头（x-codebuddy-request + x-access-token）。
  单例 inflight **同步赋值**（修复并发窗口双 spawn 竞态，测试抓到）；
  windowsHide + detached:false（P0），子进程随 MCP server 存活，无僵尸。
- 门禁接线：`checkReviewBackend` 发现所需 peer 挂了 → ensurePeer 一次 → 重检，
  仍挂才 fail-closed（reason 注明 auto-start 已尝试）。`AGENT_TEAMS_PEER_AUTOSTART=0` 可关。
- 预热：建队/建任务时 fire-and-forget `prewarmPeer()`，评审触发时 peer 早已就绪。
- 测试 `tests/peer.test.mjs` 4/4：已起采纳不重生 / 冷启动+env 契约（strip CODEBUDDY_*、
  密码、token、setEnv 全断言）/ 并发共享一次 spawn / 启动即崩报 ready:false。
- 实机验证：真实 peers.json，桌面宿主 peer 在跑 → 66ms 采纳 `started:false`。

**事故与修复（重要教训）**：首轮全量回归卡死 14 分钟——tools.test.mjs 的
`loadConfig` 解析出**真实** orchestratorPath → prewarmPeer 在单测里拉起了真 CLI
（每次建队重试 240s）。修复双重保险：
1) 7 个测试文件的 tmpCfg 一律 `peerAutoStart: false`（hermetic）；
2) `prewarmPeer` 加 `fs.existsSync(cfg.peersFile)` 守卫（路径不对绝不后台 spawn）。
修后 tools.test.mjs 22/22 仅 6s；全量 **172/172，16 秒**。
SKILL.md 已把"手动最小化终端拉起"改为"自动惰性拉起 + 手动兜底"。

## 【10:30】文档落地：新建 agent-teams/README.md + SKILL.md 补 peer 开关

- ensurePeer 属 Phase 4 评审后端接入的收尾补强（闭环当时遗留的"peer 生命周期"注意事项）。
- 新建 `agent-teams/README.md`：六阶段状态表、目录结构、评审后端（judge/pipeline、
  退出码契约）、**评审 peer 生命周期（惰性自动拉起 5 条机制）**、审计/面板、
  per-member 模型 upsert、注册激活、测试守卫（no-window + peerAutoStart 密封）。
- SKILL.md 环境变量表补 `AGENT_TEAMS_PEER_AUTOSTART` / `AGENT_TEAMS_PEER_READY_TIMEOUT_MS`，
  quick_validate 通过。

## 【11:00-11:25】成员扩容/自定义模型 + 面板模型下拉（用户两问落地）

**Q1 结论（实测 CLI --help）**：成员上限默认 8（AGENT_TEAMS_MAX_MEMBERS / create 传
maxMembers），无"默认 3 人"限制；CLI --model 除内置 0 积分三模型外，还内置
~100 个 `custom-local:*`（wb-model-bridge 聚合的自定义模型）与账号计费模型
（gpt-6/glm-5.3/kimi-k3…）——`add_member({model:'custom-local:xxx'})` 零配置即用；
0 积分保证仅内置三模型。

**Q2 实现**：活动面板成员表模型格升级为 input+datalist（可下拉可手输任意模型 ID）；
选中即时生成可复制的 `agent_teams_add_member {"teamId","id","model"}` 命令（点击复制），
交队长执行、下次 spawn 生效。目录来源零子进程：缓存后端预检 0 积分表
（quality.mjs 新增 cachedBackendInfo()）+ AGENT_TEAMS_MEMBER_MODELS + 内置三模型。
无目录时回退纯文本、零 JS（向后兼容）。locales 增 modelHint（中英）。

**测试**：activity 6/6（新增下拉/datalist/命令回显/无目录回退断言）；全量绿。
**排查记录**：peer 崩溃测试在并行负载下 5s deadline 先于退出检测 → 测试超时放宽 30s；
quality.test.mjs 全量并发偶发文件级超时（45s 单跑 vs 60s 限）→ 全量命令用
--test-timeout=180000。两处均为负载时序问题，非代码回归（失败集合逐轮漂移、
单跑全绿）。README 已更新成员扩容/自定义模型/面板下拉三节。

## 【12:15】修面板下拉"只有一个模型"——datalist 过滤陷阱 → 自绘下拉

**用户报告**：下拉框出现但里面只有原来的一个模型。根因：原生 `<input list>` 的
浏览器行为——输入框**预填了当前模型值**时，选项列表按输入文本**前缀过滤**，
目录里其余条目全被隐藏。

**修复**：弃用 datalist，改自绘下拉（`.mwrap/.mbtn/.mlist`）：
- 点击按钮展开**全量**目录（当前项打 ✓），点选即生成命令；
- 顶部"输入自定义模型 ID…"自由输入行：输入即过滤高亮、Enter 提交（Esc 关闭），
  任意 CLI 模型 ID（含 custom-local:*、账号模型）都能填；
- 点击面板其他处自动收起；点击命令框全选+写剪贴板；
- 暗色主题适配；无目录时无样式无 JS（CSS 也按需注入）。
- locales 增 modelCustom（中英）。测试 6/6；全量 173/173。

**提醒**：真实 activity.html 由**运行中的** MCP server 进程生成——旧进程跑的
是旧代码，需重启 agent-teams 连接器/新会话后才出下拉。

## 【12:50】解决"下拉只有几个模型"——接 CLI 全量模型目录（119 个）

**根因**：面板目录此前只有两个来源：内置 0 积分三模型 + 后端预检缓存的 free 表
（该表当时因 peer 认证挂掉返回空）+ AGENT_TEAMS_MEMBER_MODELS。脚本演示里
写死的 4 个 custom-local 也被误带进用户真实观感 → 用户截图中只有 7 个。

**修复（member-models.mjs）**：从 `codebuddy --help` 的
"--model … Currently supported: (…)" 解析 CLI 真实接受的全部 ID（实测 119：
内置/账号模型 + 99 个 custom-local:* 桥接自定义模型），写 `<stateDir>/
model-catalog.json` 磁盘缓存（TTL 7 天），合并优先级：内置免费 < CLI 缓存 <
后端 0 积分表 < env。server 启动时 fire-and-forget 预热（冷探 10-20s，
之后 status 0 开销）。probe 用 `spawn(node, [cliPath, '--help'])`——
bin/codebuddy 是 shebang 无扩展名脚本，Windows 直 exec ENOENT（与成员
spawn 同型）；空输出偶发时一次 retry 兜底。`AGENT_TEAMS_MODEL_CATALOG_REFRESH=0`
关闭冷探。测试 hermetic：7 个测试 cfg 加 modelCatalogRefresh:false。
新增 tests/member-models.test.mjs 3/3；activity 6/6；全量 **176/176**。
README「活动面板的模型下拉」节已重写（含"为什么不是只有 3 个"）。

## 【13:58】工作区动态解析（用户建议落地）

问题：mcp.json 注册时用 env 把 AGENT_TEAMS_WORKSPACE 全局钉死 D:/workspace/
workbuddyai → 任何会话的 agent_teams 工具都操作同一个 state dir。

修复：
- `mcp-server.mjs` 新增 `resolveWorkspace()`，解析链：
  `--workspace` 参数 > `AGENT_TEAMS_WORKSPACE` > **安全的 cwd** > 安装目录。
  原理：host 每会话起独立 server 进程，各带自己的 cwd → 不钉环境变量即动态。
- 安全过滤：cwd 命中系统/应用目录（Program Files、AppData、System32、
  node_modules、.codebuddy、.hermes、.workbuddy、install 名录）时回落，绝不
  把团队状态写进系统目录。loadConfig 加 cwd 形参便于测试。
- `~/.workbuddy-ai/mcp.json` 的 agent-teams 条目**删除 env 块**（验证 JSON OK）。
- 新增 tests/workspace.test.mjs 6/6（优先链/动态 cwd/系统目录回落/主目录放行/
  loadConfig 形参）。启动日志新增 `[boot] workspace=... stateDir=...`。
- README「注册与激活」重写工作区动态解析一节；SKILL.md env 表同步。
- 全量 **182/182**。注意：当前会话的 server 是旧 env 形态启动的，用户需再
  reconnect 一次让新注册形态生效（本会话 workspace 没变，行为一致）。

## 【17:30】外部审计报告核实 + Phase 7 加固（205/205）

用户贴来一份 agent-teams 审计报告（4 项 P0 + 若干 P1/P2），要求"分析下，确有必要就改进"。
**逐条实测核实后**只做真问题，并在报告里指出不成立的几条。

### 实测结论（取证方法 + 结果）
- **P0.1 部分成立**：`POST /api/v1/acp/connect` 在**不带 token / 带错 token** 时
  都返回 200（只校验 `x-codebuddy-request: 1`）。所以 `isPeerReady()` 只能证明
  "端口活着"，不能证明"这个 peer 能用"——但它**确实**会让错密码的实例也通过，
  因此"未校验密码"的表述不准确，"探针不具备区分能力"才是准确的。
  现场证据：当前 15999 是**外部实例**（`spawnedServers: []`），且
  `orchestrator health` 的 `judge.ok=false`（session/new 报 Authentication required），
  `orchestrator models` 直接失败 → 门禁此刻是 fail-closed 的。
- **P0.2 部分成立**：`checkReviewBackend` **已有**"信用表必须有 x0.00 模型"的守卫；
  缺的是"评审实际用的模型是不是免费"（judge 模式用 peer 启动时的 `--model`，
  `orchestrator prompt` 不会重新钉定）。
- **P0.3 **成立且严重****（真 bug）：`Number(env.X ?? def)` 对 `'abc'` 得 NaN。
  实测：`PEER_READY_TIMEOUT_MS=abc` → `deadline=NaN` → `Date.now()>NaN` **恒 false**
  → 就绪循环永不退出（挂死）；`MAX_MEMBERS=NaN` → 上限失效；
  `MEMBER_TIMEOUT_MS=NaN` → `setTimeout(fn,NaN)` 成员刚起就被杀；
  `JUDGE_TIMEOUT_MS=''` → `Number('')=0`，`??` 拦不住 0 → 评审秒超时。
- **P0.4 不成立**：pipeline 模式**已实现**且 `runAsync` 有独立超时
  （`reviewTimeoutMs` 默认 10min）→ 不会"卡死"，只会超时后 escalate。
  故改为启动 WARN + 文档说明，而非硬报错删功能。
- **P1.3 不成立**：judge 已有独立超时（`judgeTimeoutMs`），且 `quality.test.mjs:393`
  早有"hung judge 被超时切断"的用例。
- **P1.7 不成立**：工作区黑名单正则里已含 `windows`，`C:\Windows` 本来就被拦。

### 意外发现的真 bug（审计没提，最值钱）
- **`writeActivityReport()` 的解构漏了 `availableModels`** → `buildActivityData`
  收到 undefined → `hasCatalog=false` → **队长看到的真实面板根本没有模型下拉**，
  而手工生成的 `activity-demo-*.html`（直接调 `buildActivityData`）却有。
  这正是"面板看起来是坏的、demo 却是好的"的根因。实测复现：`has mbtn=false`。
- **`tests/audit.test.mjs:189` 是坏的**：读 `process.env.FAKE_ORCH_LOG` 但从未设置
  → `readFileSync(undefined)`。基线 181/182 就是它。已修。

### 落地改动（Phase 7）
1. `mcp-server.mjs`：新增 `envNumber/envBool/envChoice`。缺失或空白=未设置（用默认
   值，不告警）；有值但非法/越界=默认值+warning，启动打 `[config] WARN`，
   并从 `loadConfig().warnings` 可读。`REVIEW_MODE` 做枚举校验。数值键全部加范围。
2. `mcp/lib/peer.mjs`：`SPAWNED` pid 集合 + `listenerPid()`（win32 `netstat -ano -p tcp`
   / 其它 `lsof`，均 `windowsHide:true`，**异步 execFile**）+ `peerProvenance()`
   / `peerProvenanceFromFile()` / `peerModelFromConfig()`。`ensurePeer` 返回
   `provenance: ours|foreign|unknown`，复用外部实例时打 WARN；deadline 加了
   `Number.isFinite` 兜底（不依赖调用方校验）。
3. `mcp/lib/quality.mjs`：`billedModels` 从"只计数"改为收全名单；
   judge 模式新增**计费护栏**——解析 peers.json（跟 cloneOf）取 `--model`，
   命中 billed 名单就 fail-closed 并写明"会消耗账号积分"；无 `--model` 不误报。
   `checkReviewBackend` 返回值新增 `peer`（来源）与 `billedModels`。
4. `mcp/lib/tools.mjs`：`isBilledModel/billedWarning`；`add_member` 返回值带
   `warning`；`status` 返回 `modelWarnings` + `reviewBackend`，并把
   `billedModels`/`peer` 透传进面板；新增 `reviewPeerInfo()`（无缓存时直接探一次，
   TTL 30s，**peers.json 不存在则跳过** → 测试零影响）。
5. `mcp/lib/spawn.mjs`：新增 `reapDead()`（`process.kill(pid,0)` 判定，
   **只删记录不杀进程**；EPERM 视为存活）。
6. `mcp/lib/constants.mjs` + tools：新增 `agent_teams_reclaim_orphans`
   （第 15 个 captain 工具，复用同一个 `scheduleTick()`）。hook 是
   deny-by-default 所以成员自动被拦。
7. `mcp/lib/activity.mjs`：**修 writeActivityReport 签名**；`buildActivityData`
   支持 `billedModels`/`peer`；渲染 ⚠️计费徽标、`tr.warn` 高亮、peer 来源行、
   配额横幅；locale 加 `peer/peerProvenance/billedModelShort/billedModelWarn/quotaNotice`。
8. 测试：新增 `config.test.mjs`(10) / `review-guard.test.mjs`(3) /
   `reclaim.test.mjs`(3)；扩 `activity.test.mjs`(+3) / `peer.test.mjs`(+4)；
   修 `audit.test.mjs` 与 `tools.test.mjs`（工具数改为从 `TEAM_TOOL_NAMES` 派生）。
9. 文档：README 新增「peer 来源识别 / 评审计费护栏 / 环境变量与配置校验 /
   手动孤儿回收」四节 + 面板告警 + 测试守卫；SKILL.md **修正了原本错误的工具入参**
   （原来写 `{teamId, title}` 等，真实是 `{subject, id}`、`create{name,goal,plan}`、
   `resume{requeue}`、无 `teamId` 参数），并加 15 工具速查表 + 两条 fail-closed 护栏。

### 关键教训（踩坑记录）
- **不要把 `process.pid` 塞进 `spawner.live`**：`handle.close() → reapAll()` 会在
  Windows 上对本进程 `taskkill /T /F`，表现为"测试文件静默退出 1、无任何输出、
  没有子测试"。写测试时用真实子进程。
- `execFileSync` 在本沙箱 EBUSY，`netstat`/`lsof` 探测必须用异步 `execFile`。
- 审计报告要**逐条取证**：8 条里 4 条不成立或表述错误，直接照做会白改甚至删功能。

最终全量：**205/205 通过**（约 20s，命令 `node --test --test-timeout=180000 "tests/*.test.mjs"`）。

---

## 【10:30】用户"后续测试建议"执行：烟测 / 护栏专项 / 回归

### 1. 烟测（19 项，全绿）
- 新写 `examples/smoke-peer-guards.mjs`：**不碰 15999**（那是 codebuddy-a2a 的
  开机自启服务，不是孤儿进程），改用 15998 副本 + `--config`。19 项检查全 PASS，
  跑完把**真实信用表**落盘 `tests/fixtures/models-real.txt`。
- 15999 归属实测确认：`peerProvenanceFromFile(real peers.json)` → `foreign`、
  `pid=11368`（OS 判定，`netstat -ano`）。**杀它无效且有害**（登录后自动回来，
  且不继承我们的网关密码 → 探针过、`session/new` 报 Authentication required）。

### 2. 护栏专项
① 计费模型 fail-closed：`tests/review-guard.test.mjs` 已覆盖（fake orchestrator）；
   本轮补 **`parseCreditTable` 对真实信用表**的解析测试（防 CLI 输出格式漂移）。
② 非法 env：单测已覆盖；本轮补**运行时**验证 —— `config.test.mjs` 新增
   "boot: rejected env values are logged loudly as [config] WARN"（真启动 server 抓
   log 行），`peer.test.mjs` 新增 "NaN readyTimeoutMs 回退到配置预算、不挂死"。
③ 复用外部 foreign peer：日志 WARN + 面板标注已验证；本轮**补上"可手动选择是否
   继续"的机制** —— 新增 `AGENT_TEAMS_PEER_ALLOW_FOREIGN`（默认 `1`=告警放行；
   `0`=**拒绝复用**并 fail-closed，原因带占用 pid 与解法）。

### 3. 真 bug（烟测抓出，单测没抓到）
**就绪探针会瞬时抖动**：一个确认存活（`listenerPid` = 我们的 pid、
`process.kill(pid,0)` OK）的 `codebuddy --serve`，在 24 秒 6 次探针中**失败过 1 次**，
下一次又恢复 200。
- 危害：`ensurePeer` 快通道用单次探针判"peer 不存在" → 会**在已占用端口再 spawn
  一个**（新进程无法监听、`hosted` 槽位被覆盖、provenance pid 指向马上退出的进程）。
- 修法：`probeReady()` 重试 3 次（1.5s 间隔）；spawn 前**最后一道闸**用
  `listenerPid` 问 OS 端口占用 —— 被占 = peer 存在 → **采纳，绝不重复 spawn**。
- 关键细节：**连接被拒（ECONNREFUSED）是确定性结论，不重试**，否则每次"peer down"
  诊断白等 3 秒。`probeOnce()` 区分 refused / 其它（undici 把 socket 错误包在
  `cause`，还要看 AggregateError 的 `.errors[]`）。
- 回归：`tests/peer.test.mjs` 4 条新用例（抖动重试 / 拒绝不重试 / 端口被占只采纳 /
  allowForeign 拒绝）。

### 4. 新增 `--orchestrator-config`（绕开被占用的 15999）
端到端接线：`loadConfig().orchestratorConfig`（`--orchestrator-config` /
`AGENT_TEAMS_ORCHESTRATOR_CONFIG`，flag 优先）→ `peersFile` 派生自它 →
`orchestratorConfigArgs(cfg)` 接到 `models` / `health` / `prompt` / `run` **四条命令**
（此前只接了 models/health 两条）。

### 5. 修掉一个 tripwire 误报
`tests/no-window.test.mjs` 的第二个断言**不剥离注释**，我在 `probeReady` 文档注释里
写了 "`spawn()`" 就被当成真实调用。→ 该断言改为先剥离纯注释行（与第一个断言一致）。

### 6. 第二个真 bug：信用表有**第三个区块**（真实抓取 fixture 当场暴露）
把真实 `orchestrator models` 输出落盘成 `tests/fixtures/models-real.txt` 后立刻发现：
真实表是三段，不是两段 ——

```
--- credits = x0.00 (0 积分) ---           ← free（3）
--- billed models (x>0) ---                ← billed（20）
--- unlabeled credits=null (100, bridge custom providers) ---   ← 第三段（100 个）
```

`parseCreditTable` 只认前两个 banner，于是第三段开始时 `section` 仍是 `'billed'`，
100 个 `custom-local:*` / `default-model` **全部漏进 `billedModels`**：
- billed 计数 20 → **123**（面板计数虚高）；
- **计费护栏会误拒**钉在"积分未知"自定义模型上的 judge peer（fail-closed 打错方向）。
修法：**任何未被识别的 `--- … ---` banner 关闭当前区块**（未来 CLI 加段也不会泄漏）。
回归断言：`custom-local:*` 不得出现在 billed、billed < 60。
烟测同步加"实时信用表解析"检查 → **20/20**。
**教训：解析外部 CLI 输出，必须用真实抓取做 fixture，不能只靠自造的假样本。**

### 7. 全量
**216/216 通过**（`node --test --test-timeout=180000 "tests/*.test.mjs"`）。
曾出现一次 216（1 fail / 1 cancelled），根因见 §9。

### 8. 默认 config 的真实现状（重要，给用户交代）
- `orchestrator health` → peers **全 ok:true**（探针只看端口活着）；
- `orchestrator models` → **失败**：`codebuddy: session/new rpc error: Authentication required`；
- `judge.ok` → false。
即**"health 全绿"≠"peer 能用"**。用户验收点里的"`models` 正常返回"在默认 peers.json
（15999 = 外部 a2a 服务）上**做不到**，只能指向干净 peer（`--orchestrator-config`
换端口）—— 这正是本轮把该开关端到端接线的原因。

### 9. 第三个 bug：偶发失败用例的真根因 = `taskkill` 同步且慢
偶发 `not ok 167 - a timeout is flagged and the process is reaped`
（`tests/spawn.test.mjs`，等待 26.8 s，断言 `< 25 s` 失败）。
**根因不是测试写错，是产品代码**：`killTree()` 用
`execFileSync('taskkill',['/PID',pid,'/T','/F'])`，而 `execFileSync` **阻塞事件循环**。
实测本机：
- 空闲：**3251 ms**
- 全量并行负载：**~25 s**
→ 生产后果：成员超时 / `reapAll` 时 **MCP server 事件循环被卡住**（HTTP、scheduler tick 全停）。
修法：`execFileSync` 加 **`timeout: 8000`** 硬上限（超时则回退
`process.kill(SIGKILL)` 杀直接子进程）。测试判据同时改为"子进程睡 60 s、上界 30 s"
（原 30 s / 25 s 太贴近真实开销）。单跑该用例：6.8 s（1.2 s 定时器 + 3.2 s taskkill）。

### 10. 最终全量
**216/216 通过**（`node --test --test-timeout=180000 "tests/*.test.mjs"`）。

---

## 【21:15】第二轮审计（README+代码整体复盘）逐条取证 → 只做真需要的

用户贴来第二份审计（P1×6 / P2×4 / 文档 3 处），指令"看下这次审计是否有改进必要"。
**逐条取证结论：1 条前提不成立、1 条已实现、4 条确有必要。**

### 不成立 / 已实现（不改）
- **P1.2「坏 `--orchestrator-config` 会让 MCP server 崩溃」→ 前提不成立。**
  实测（`examples/_probe-bad-config.mjs`，已删）：`loadConfig` 不做 I/O；
  `loadPeerConfig` 读/解析失败 try-catch 返回 null；`runAsync` 只 resolve 不 throw；
  `startServer` **正常启动并干净关闭**。全链路无一处 THREW。
- **P1.4「git stderr 被丢弃」→ 已实现。** `gitStatus()` 已把 stderr 首行写进
  `reason`（exit!=0 分支），`runDeliveryAudit` 又把 `reason` 落进 `audit.json`。
  审计建议的 `gitDiagnostic` 字段与既有 `reason` 重复。
- **P1.2 的"拒绝启动"部分 → 主动不做**：评审是 best-effort，server 主职责是
  15 个团队/成员工具（不需要 peer）。为一个评审侧配置错误把整个连接器弄挂是更糟的
  失败模式；与既有 `orchestratorPath===null → gate 报 disabled` 一致。

### 确有必要（已落地）
1. **真 bug：`tail()` 只取 stderr 最后 4 行 → 错误信息被丢。**
   取证第 3/4 步暴露：真实 orchestrator 的输出是「1 行有用信息 + 一大段 ESM 堆栈」，
   旧 `tail()` 只留 `at ModuleJob.run (node:internal/…)`，**路径不见了**。
   → 改为优先保留首部非堆栈行（`^at ` / `^node:internal/` / 分隔线视为噪声）。
   现在 reason = `` `models` exited 1: [orch] FAILED: Error: cannot read peer registry: <path> ``。
2. **P1.1 探针重试日志**：`probeReady` 原来静默重试 —— "抖动后恢复"与"一次成功"
   在结果上完全一样。现在每次失败一条 `[peer-probe] WARN … n/N`、恢复时说明发生过
   抖动、`ECONNREFUSED` 单条且不重试、全败打 `treating … as down`；
   惰性拉起每 10 s 一条进度（实测就绪 23–26 s，轮询 2 s，没这条日志看着像挂死）。
3. **P1.2/P1.6 路径配置启动校验**：新增 `validateOrchestratorConfig()`（export，
   纯函数+FS），三种坏法（不存在/非 JSON/无 `peers`）→ `[config] ERROR <完整路径>`，
   并进 `loadConfig().configIssues` → `agent_teams_status.configIssues`。**不拒绝启动**。
4. **P1.5 foreign 拒绝给可复制命令**：新增 `killHint(pid)`（win32 `taskkill /PID n /T /F`，
   其它 `kill n`），peer.mjs 的 WARN 与 quality.mjs 的 fail-closed reason 共用同一份。
5. **P1.3 模型目录降级可见**：`readCache` 现在区分「没有缓存」与「缓存过期」；
   过期后冷探失败/刷新被关 → `[model-catalog] WARN` + `catalogState().degraded`
   → `agent_teams_status.modelsDegraded/modelsNote`。**过期缓存不再被当当前列表用**。
6. **文档 3 处**：① 第 49-50 行 pipeline「暂不可用（另案）」与第 54 行「可用但不可靠」
   自相矛盾 → 统一；② 测试命令补注"单测不拉真实 CLI，只有 examples/ 下的 e2e 与烟测才拉"；
   ③ 新增「MCP 重启后自己拉起的 peer 会变成 foreign」已知现象节（`SPAWNED` 是进程内存，
   属预期行为，两种应对）。

### P2 全部延后（按审计自己的建议）
配额监控（CLI 未开放信用消耗 API）、面板导出归档、状态持久化（WB 每会话独立 MCP 进程，
会话隔离复杂）、面板一键 kill（安全边界：只生成可复制命令）—— P2.4 的价值已由
P1.5 的 `killHint` 覆盖大半。

### 顺带接线（否则新诊断是死代码）
`createTools` 新增 `log` 入参（`deps.log`），并加进 `qualityCfg()`；
`mcp-server.mjs` 把 `startServer` 的 `log` 传进去。此前 `cfg.log` 在 quality.mjs 里
被读但从未被赋值。

### 测试
228/228 通过（216 → 228，+12）：config(+4：validateOrchestratorConfig 三态、
configIssues 不抛、boot `[config] ERROR`)、member-models(+4：过期/无缓存/新鲜/刷新关闭)、
peer(+3：每次失败都记日志、ECONNREFUSED 只一条且不等间隔、ensurePeer 传 log)、
review-guard(+1：真实 orchestrator 坏 config → reason 含路径且不是堆栈；foreign 拒绝含 kill 命令)。

### 踩坑
- `node -e "<脚本>" arg1 arg2`：**argv 整体左移一位**，不是"额外参数丢失"。
  实测 `node -e "…" AAA BBB` → `process.argv = [node, 'AAA', 'BBB']`，
  `slice(2) = ['BBB']`（`argv[1]` 是第一个额外参数，不是 `-e`、也不是脚本路径）。
  而 `node script.mjs AAA BBB` → `slice(2) = ['AAA','BBB']`。
  所以 stub 一律**落盘成文件**再 `node stub.mjs port`，否则参数会错位
  （我这次就是 `port='/ready'` → listen NaN → 探针 ECONNREFUSED）。
- 测"ECONNREFUSED 不重试"必须用**先 bind 再 close 拿到的空闲端口**，否则可能撞上
  同文件其它 fixture 的 403 stub → 走成重试路径。

---

## 【23:30】用户报障：agent-teams 同时开 5 个成员 → 宿主 OOM

**用户原话**：另一个对话让 agent-team 做项目可行性分析，同时开了 5 个 agent，
结果 OOM；后来改成流水线模式在跑。

### 根因（代码取证 + 实测，不是猜）
1. **成员并发完全没上限。** `scheduler.scheduleTick()` 只算 `ready`，不 spawn；
   真正派生的是队长调 `claim_task({taskId, memberId, spawn:true})` → 直接
   `spawner.run()` 立刻 spawn。`AGENT_TEAMS_MAX_MEMBERS`（默认 8）限制的是
   **团队人数**，不是**并发数** → 队长一次派 5 个 = 5 个进程同时起。
2. **每个成员 = 一个完整 `codebuddy` CLI Node 进程。** 本机 `tasklist` 实测：
   17 个 node 进程共 1.5 GB，最大单个 375 MB、次之 223 MB —— 即**单个 CLI 实例
   约 150–375 MB RSS**，且 CLI 自己还派生子进程（`killTree /T` 就是为它们准备的）。
3. **评审 peer 是额外的完整 CLI 实例**（`codebuddy --serve`），常驻。
4. **父进程缓冲无界**：`spawn.mjs` 里 `stdout += d` / `stderr += d`，一个疯狂
   输出的成员能把 MCP server 的堆撑爆。

### 落地改动
- `spawn.mjs`：
  - 新增 `DEFAULT_MAX_CONCURRENT_MEMBERS = 3`、`MAX_MEMBER_STREAM_CHARS = 4MB`。
  - 新增 `TailBuffer`（有界尾缓冲，摊还 O(1) push；只留尾部——`--output-format json`
    的 JSON 在最后，报错也在最后；`toString()` 标注丢弃了多少）。
  - `MemberSpawner`：`maxConcurrent` + FIFO 信号量 `_acquireSlot/_releaseSlot`，
    `run()` 变薄壳（拿槽 → `_runInner` → finally 释放），`_runInner` 是原 body。
    **超限派发排队，不拒绝不丢活。**
  - `reapAll()` 取消排队等待者（resolve `{cancelled:true}`）→ `run()` 返回
    `cancelledRun()`（exitCode 1 + 明确 error），走调用方既有的 failed 分支释放任务，
    不会在拆队后又偷偷 spawn。
  - stdout/stderr 改用 `TailBuffer`。
- `mcp-server.mjs`：新增 `AGENT_TEAMS_MAX_CONCURRENT_MEMBERS`（默认 3，1–64，
  走 `envNumber` → 非法值回默认+告警，**不会变成 Infinity**）；传给 spawner 的
  `maxConcurrent`；tools cfg 带 `maxConcurrentMembers`。
- `tools.mjs`：`status` 新增 `memberConcurrency: {active, queued, max}`。
- 文档：README 新增「成员并发上限与内存（防 OOM）」节（含实测数字、根因、
  已知边界）；阶段表加第 9 行；SKILL.md 的执行步骤加并发告警 + env 说明。

### 测试
236/236（228 → 236，+8）：spawn(+3：并发上限真的封顶且排队者仍跑完、reap 取消
排队、TailBuffer 边界与 JSON 保尾)、config(+1：并发上限默认 3 且垃圾值不回退成
Infinity)、NUMERIC_KEYS 加新键。

### 关键设计取舍（为什么是"排队"而不是"拒绝"）
拒绝会让队长必须实现重试循环（LLM 容易漏，任务会永远卡在 ready）；排队是
自管理的，活一定跑完。取消语义用"返回失败结果"而不是 reject，这样复用调用方
已有的 failed 分支，不用改任何调用点。
**注意**：排队中的任务状态已是 `claimed`；若队列等待超过 claim TTL（30 min），
`scheduleTick()` 可能把它判为废弃重排 → 重复劳动但状态不坏（attemptId 守卫）。

## 二、项目 / 技术点（当日 handoff 与报告）

_当日无新增 handoff / 项目报告（此 agent 当日可能没在该端干活）。_


---

生成：multi_agent_publish/collect_day.py · 2026-10-29 22:18