---
layout: default
title: 技术点 · 2026-11-27
date: 2026-11-27 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-27-10-33-05\.workbuddy\memory\2026-11-27.md

## 11:10 X 活动发帖文案
- 用户在做一个 AutoClaw 推广任务：关注 @AutoClawAler + 发公开帖 @它 + 提交链接和截图，承诺 10M tokens/1000 credits（来源：用户贴的活动页截图，未独立核实）。
- 给用户写了 3 版发帖文案（英文通用/中文/技术向短版），并提醒活动明确排除 "AI-generated filler"，最好按真实体验改一两句再发。
- 11:17 用户看到奖励 7 天过期，决定放弃活动。

## 11:23 hy4 flash 免费额度查询
- 用户抱怨 WorkBuddy 的 hy4 flash 每天额度动不动用完，问具体多少。
- 查证结论：**官方从未公布具体数值**。多来源一致口径为「每日赠送免费额度，订阅用户享更高配额」「触及限额后可消耗积分继续，页面提示重置时间」，均无具体数字。
- 来源分级：T1=官方客户端模型卡说明（0.00x、每日赠送、订阅更高、11/16–11/30 限免）；T2=腾讯云开发者社区文章 2026-11-17（hollyx，二次转述官方口径，非公告原文）、微信公众号多篇（自媒体，明确写「每日额度数值官方未公布」）。官方活动页 cloud.tencent.com.cn/act/pro/workbuddy 也未列具体额度。
- 已告知用户：网上流传的具体数字不作数；额度用完不是停服而是转积分；生图/生视频不占该额度、照常扣积分；限免 11/30 23:59 止。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-26-20-58-07\.workbuddy-ai\memory\2026-11-27.md, D:\workspace\workbuddyai\2026-11-27-15-01-30\.workbuddy-ai\memory\2026-11-27.md

## custom-model-onboarding-v2 全量分发 + 旧加模型 skill 全量停用（10:10）

**背景**：11-26 建的新 skill 本地试用通过，用户拍板分发到全部 agent，并停用所有旧的"新增模型"skill，
以后各 agent 加模型统一用 v2。用户 AskUserQuestion 确认两点：①分发范围=全部 8 个 agent；
②旧 skill 停用范围=所有 agent 上的全部旧加模型 skill（归档可恢复，不硬删）。

**现状盘点**（分发前）：
- WB 国内版 4 个：`autoclaw-add-model`、`custom-model-onboarding`、`lobsterai-batch-model-import`、`zcode-batch-model-import`
- WB 国际版（源头）2 个：lobsterai/zcode-batch-model-import
- au / au-intl / zcode / lobsterai / loomy / raccoon 各 2 个：lobsterai/zcode-batch-model-import
- 共 18 个；`model-radar-topn` / `model-rate-limit-radar` 是额度监控，保留不动。

**执行**（全部按红线先备份后动工）：
1. **备份**：18 个目录整体复制到 `skill_archive_model_20261127_100849/`，`diff -r` 逐字节校验 18/18 一致，
   `manifest.tsv` 记录原路径（tag/skill/src）便于回滚。
2. **分发**：`sync_skill.py custom-model-onboarding-v2 --source <wb-intl 路径> --to au au-intl zcode lobsterai loomy raccoon`
   （source 必须覆盖，因为默认源头是 WB 国内版；wb-intl 自己是源头无需推）。
   WB 国内版不在脚本 target 列表，单独 `cp -r` + diff 校验。
3. **停用**：按 manifest 路径逐个 `shutil.rmtree`，删前校验归档副本存在 + 路径合法性，分 3 批（9/6/3），
   每批后确认归档副本仍在。
4. **验证**：冒烟测试 8/8 GREEN（脚本编译通过、无漂移）；8 端旧 skill 全 CLEAN；
   归档 18/18 SKILL.md 完整；model-radar 类保留完好。

**踩坑**：
- 分发脚本绿灯闸（smoke_common_skills.py）检查 8 端，WB 国内版（wb-cn）不在 `--to primary` 里，
  只推 6 个目标会报红灯"缺失端 wb-cn"——必须先单独复制到 wb-cn 再重跑冒烟才全绿。
- 删除脚本安全闸 `("skills" in src.parts)` 大小写敏感，LobsterAI 目录名是 `SKILLs`（大写 S），误报
  "suspicious src path" 中断；改为 `any(p.lower()=="skills")`。数据无损，重跑即可。

**回滚方法**：按 `manifest.tsv` 第 3 列原路径，从 `skill_archive_model_20261127_100849/<tag>/<skill>/` 复制回去。

**脚本**：本工作区 `remove_old_skills.py`（按 manifest 安全删除，支持切片分批）。
分发脚本：`C:\Users\Administrator\.workbuddy-ai\skills\cross-agent-skill-install\scripts\sync_skill.py`。

## 三层分离检查 + 国内版 2.0 残留清理（10:35）

**三层分离全 agent 检查结论**：8 个 agent 中唯一不符合的是 AutoClaw 2.0 国内版 103 条
（model 带 `[平台名]` 前缀 + base_url 全走网关 18901 + 凭证全 `wb-bridge` 占位）。其余 7 个
（WB 国内/国际、AutoClaw1.x、国际版、ZCode、LobsterAI、DSH、Hermes）全部符合——id 真实、
前缀在显示字段（name/alias）。检查脚本 `check_three_layer.py`（本工作区）。

**关键判断**：国内版早于 11-25 被国际版覆盖，是遗留数据——4 个 AutoClaw2.exe 进程全是国际版
（`--user-data-dir=...AutoClaw-oversea-official`），国内版 0 进程；国内版数据停在 11-25 12:15。
故国内版 103 条不需改写（没人用），正在用的国际版 11 条昨天已修成三层分离、全绿。

**清理执行**（用户授权"网关孤儿进程 + 国内版 2.0 残留都清理"）：
1. 停网关孤儿进程 node PID 11444（`wb-model-bridge.mjs`），18901 端口释放。
   停前确认国际版 11 条 0 条依赖网关（全是真实上游 base_url），安全。
2. 归档目录 `cleanup_autoclaw2cn_archive_20261127_103004/`，manifest 22 行。
   - 网关自启动 `Startup\WBModelBridge-AutoStart.vbs`（不移除会重启复活）
   - `free-model-proxy/` 下网关+2.0 导入残留（脚本/日志/backup/oskey/connections_map 等）
     **保留原地**：`dsh-our-free-model/`（DSH git 仓库）、`verify_radars.mjs`、`add_intern_ai_to_autoclaw1x.cjs`（1.x）
   - 国内版数据 `AutoClaw-official/`（206M，10433 文件）
3. 大目录移动：`shutil.move` 跨盘符在长路径上报 WinError 3（移到一半 131M/206M，数据未丢），
   改用 **robocopy /MIR**（PowerShell 调用，Git Bash 会把 /MIR 当路径转换），1833 目录/10433 文件全同步。
   校验：两边文件数 10433、字节 303694872 一致；runtime.sqlite 与 credentials.enc SHA256 匹配。
   闸校验通过后删源目录。
4. 最终验证：18901 无监听、PID 消失、自启动项移走、国内版目录删除、保留项完好、
   `autoclaw`(1.x) 与 `.openclaw-autoclaw` 未动、归档 335M 完整；国际版 11 条诊断 route_ok 11/11、
   真实凭证 11、占位 0。

**明确不动**：`autoclaw`(小写,1.x)、`.openclaw-autoclaw`（skill 绿灯闸脚本在此）、国际版、model-radar 类。
**恢复方法**：按归档 manifest.tsv 把各项移回原路径。
**脚本**：本工作区 `check_three_layer.py`（全 agent 检查）、`do_cleanup.py`（清理移动）、`diag_cn_creds.cjs`（国内版凭证诊断）。
国内版 AES key 从 `AutoClaw-official\Local State` 导出（不是 `AutoClaw\`），hex 存 `oskey_cn.hex`。

**归档最终删除（10:45，用户二次确认"连归档也删掉释放 335M"）**：
- 删 `cleanup_autoclaw2cn_archive_20261127_103004/`（335M、10458 文件），不可恢复。
- 坑：`Remove-Item` 在本环境把目录移进回收站（`D:\$RECYCLE.BIN\...\$RZSZTR7`），空间没释放；
  再永久删回收站那份才真正释放。D 盘可用 265.82 → 266.14 GB（+0.32G≈335M）。
- 删后复核：归档与回收站均无残留；保留项（dsh-our-free-model、autoclaw 1.x）完好；
  国际版 11 条 route_ok 11/11、真实凭证 11、占位 0，未受影响。

## 用 v2 skill 接入 dots.ai 模型到全部 agent（11:35）

**用户给**：dots.ai 平台，`dots3-note-prev`，key `ak_UDSjyzR4aC6C9aRt0kM1UK9oB9GbB`，
文档 https://dots.ai/platform/docs#chat-completions。要求用新 skill 加到全部常用 agent。

**接入参数（官方文档 T0 + 实测）**：base_url `https://note3-prev-api.askdiandian.com`，
路径 `/v1/chat/completions`，官方用 `api-key` 头但**实测 `Authorization: Bearer` 也 200**（所以全部
标准 OpenAI-completions agent 可直连，无需网关）；上下文 512K=524288；响应 `model=dots3_note`（下划线，
请求用 dots3-note-prev 正常）。显示名 `[dots.ai] dots3-note-prev`，真实 id `dots3-note-prev`。

**⚠️ 关键教训：用户批评"重复造轮子"——老 skill 里有跑通的脚本，应先照搬再改**：
归档 `skill_archive_model_20261127_100849/wb-cn/` 里 4 个老 SKILL.md + 脚本是本轮关键参考：
- `custom-model-onboarding/SKILL.md`（425 行，8 agent 全落点 + 所有坑）
- `custom-model-onboarding/scripts/lobster_inject.py`（追加式，下一空槽 custom_N）
- `zcode-batch-model-import/scripts/import_models_to_zcode.py`（url 分组+备份+模板自带模型禁用）
- `autoclaw-add-model/SKILL.md`（1.x apiKey 明文直写 app 自动重加密；2.x SQLite 公式）
我一开始自己瞎摸 Loomy/小浣熊落点、想解 AutoClaw1.x 的 enc: key，全是老 skill 早写明的事。
**以后加模型先读这 4 份老文档**（在归档目录，或恢复回 skill），别再重复研究。

**执行结果（12/12 验证通过，脚本都在本工作区）**：
- 备份 `backup_dots_20261127_111850/`，14 个配置 SHA256 一致
- WB 双版本：`add_dots_wb.py`，54→55 / 51→52
- AutoClaw 国际版：`add_dots_au_intl.cjs`，直连三层（真实 id+真实 base_url+真实 key+route 新公式），
  11→12 条，diagnose route_ok 12/12 真实凭证 12 占位 0（**走昨天修好的直连路径，不是老 skill 的网关方案**）
- AutoClaw 1.x：`add_dots_autoclaw1x.cjs`（照搬 add_intern_ai 脚本），catalog 60→61，明文 key 待 app 启动重加密
- ZCode：`import_models_to_zcode.py`，provider 10→11（custom-note3prevapi，templateId=openai），
  13 条模板自带模型禁用，manual 规则空
- LobsterAI：`lobster_inject.py`，进程已退出（无需用户关），追加 custom_13（不覆盖 0-12）
- Loomy：`add_dots_loomy.py`，provider dotsai（源码 addCustomProvider 写法：明文 apiKey、
  不设 useSessionAuth，否则被登录 token 覆盖），默认模型未改
- 小浣熊：`add_dots_raccoon.py`，真正落点是 `config.yaml` 的 `saved_models_json`（JSON 字符串数组），
  **不是 model-profiles.json**（那是程序生成的注册表，手改无效）；schema 从 asar 挖到
- DSH：`add_dots_dsh.py`，key 放 `.credentials.yaml` 的 WB_KEY_16，cordis.patch.yml 用 apiKeyEnv 占位，
  插入点=providers 段末尾（老 skill 坑：插错会吞掉上一个 provider 的 models）
- Hermes：`add_dots_hermes.py`，config.yaml custom_providers 末尾 + Studio 的 modelVisibility/customModels 两处
- 验证 `verify_dots.py` 12/12；上游实测 HTTP 200（Bearer + api-key 都通）

**待用户操作**：重启 WB/AutoClaw国际版/ZCode/小浣熊/Loomy/Hermes 生效（LobsterAI 已退出，下次启动即生效）；
1.x 启动后明文 key 会自动重加密为 enc:（铁证）。校验脚本有个双层 JSON 坑：小浣熊 config.yaml 的
saved_models_json 是 YAML 双引号标量，需 `json.loads(json.loads(raw))`，raw 不能 strip 掉外层引号。

**v2 skill 教训回写并同步全端（11:36，用户"同步"指令）**：
- 源头（wb-intl）新增 `references/reuse-te

## dots.ai 404 修复：base_url 漏 /v1，10808 只是系统代理（11:50）

**用户反馈**：WB 国内版 dots 调用失败，截图请求经 `127.0.0.1:10808`，用户问"不是直连吗 怎么有个10808的网关?修复"。

**定位结论**：
- 10808 = v2rayN `xray.exe`，Windows 系统代理 `ProxyEnable=1 / ProxyServer=127.0.0.1:10808`。
  对照实测 `--noproxy '*'` 与显式走 10808 都 HTTP 200 → 代理不是病根，也不是我们搭的网关，未改动它。
- 真因：源 `url` 写成 `https://note3-prev-api.askdiandian.com`，WB 拼 `<url>/chat/completions` → 404；
  正确应为 `https://note3-prev-api.askdiandian.com/v1`，实际请求 `/v1/chat/completions` → 200。

**执行**（先备份 `backup_dots_urlfix_20261127_114445/`，11 文件）：
- 本工作区 `fix_dots_url.py` 改成幂等版，统一改 9 类落点：WB 国内/国际、AutoClaw1.x、ZCode、
  LobsterAI、Loomy、小浣熊、DSH、Hermes、**AutoClaw 国际版 SQLite**。
- AutoClaw 国际版必须同时改 `base_url` 和按新公式重算 `route_revision`（凭证 key 不含 base_url，无需改凭证）。
- 修复结果 10/10；严格版 `verify_dots.py` 12/12 通过（URL 必须含 /v1 + route MATCH）；
  diagnose 带 keyfile 复核 route_ok 12/12、真实凭证 12、占位 0。临时 key `oskey_au_intl.hex` 已删除。
- 上游实测：`/v1/chat/completions` 直连与走 10808 均 HTTP 200，响应 `model=dots3_note`。

**skill 回写 + 分发**：源头（wb-intl）SKILL.md 与 `references/agent-endpoints.md` 新增两条红线：
base_url 漏平台路径前缀（dots 必须 /v1）；见 10808 先用 `--noproxy '*'` 证伪，别误判自建网关。
同步 6 端 + 单独复制 wb-cn，冒烟 8/8 GREEN、无漂移。
**注意**：`sync_skill.py --to primary` 在 source=wb-intl 时会尝试把源头复制到自身，
本会话占用文件导致 WinError 32；正确用法是显式列 `--to au au-intl zcode lobsterai loomy raccoon`，再单独补 wb-cn。

**待用户**：重启 WB 后复测 dots；Hermes 当时在运行，也需重启才读新配置。

## WB dots 二次病根：双鉴权头 404 `provider.client_bad_request`（12:25）

用户重启后仍报错，截图文案从 `404 page not found` 变成
`404 {"title":"Invalid provider request","error_type":"provider.client_bad_request"}`
（traceId `9422709e...`，proxy 仍显示 10808）。

**定位链**：
- 旧日志证明 WB `normalizeChatCompletionsUrl()` 会把源 `url` 补成 `<url>/chat/completions`；
  读安装代码 `codebuddy.js` 确认：raw 带 `/v1` 时结果正确为 `/v1/chat/completions`（已实测 200）。
- `/v1/v1/chat/completions` 与 `/chat/completions` 都返回纯文本 404，不是截图的 JSON 错误。
- 复现实验锁定：**同时发 `Authorization: Bearer <key>` + `api-key: <key>` 时**，
  dots 网关返回与截图完全一致的 404 `Invalid provider request / provider.client_bad_request`
  （同样组合有时其他后端 200，故表现为间歇性失败）。单独 X-API-Key / api-key / Authorization 均 200。
- WB `getCustomHeaders()` 给自定义模型同时注入 `X-API-Key`（`eS.API_KEY_HEADER`）和
  `Authorization: Bearer`；`axiosToFetchAdapter` 里只 `delete em.authorization`（小写），
  大写 `Authorization` 没删掉 → 双头到达上游。

**修复**：最小补丁 `D:\Program Files\WorkBuddy\resources\app.asar.unpacked\cli\dist\codebuddy.js`
```
if(delete em.authorization,delete em["user-agent"],...)
→ if(delete em.authorization,delete em.Authorization,delete em["user-agent"],...)
```
只删大写 Authorization，保留 X-API-Key（单头实测 200）。
备份 `backup_wb_codebuddy_20261127_1220/codebuddy.js`（SHA256 6255dad0...），
`node --check` 通过，语法无误。未杀任何用户进程。

**skill 回写 + 同步**：SKILL.md 红线 + `references/agent-endpoints.md` WB 节新增双鉴权头坑和补丁位置，
6 端同步 + wb-cn 单独复制，冒烟 8/8 GREEN、无漂移。

**待用户**：必须**完全退出并重启 WB**（旧 CLI host 仍加载旧 codebuddy.js），再开新会话复测 dots；
WB 升级会覆盖此补丁，skill 里已写明需重打。

## WB dots 第三层病根：认证拦截器回填会话 token（13:05，已端到端验证修复）

用户重启后错误变为 `400 governance.dots_platform_invalid_request`（错误类型在变=每层修复都生效了一层）。
WB 日志确认 URL 已是 `/v1/chat/completions`、补丁已加载，但治理层仍拒。

**抓真实请求（决定性证据）**：把双份 models.json 的 dots url 临时指到本地捕获服务器（127.0.0.1:18999），
用 `node <WB>/cli/bin/codebuddy -p hi --model custom-local:dots3-note-prev` 触发，抓到完整请求头：
`X-API-Key: ak_UDS...` + **`Authorization: Bearer [object Object]`**（CLI 无登录态）；
GUI 登录态下则是 WB 自己的 token。dots 治理层校验 Authorization 不是 dots key → 400/403。

**完整病根链**：OpenAI SDK（x-stainless 头证实）按 `buildOpenAIClientOptions` 自带
`Authorization: Bearer <dotsKey>` → 上一版补丁在 `axiosToFetchAdapter` 删掉它 →
**axios 认证拦截器（`AuthenticationHttpInterceptor`）发现 Authorization 缺失，用
`authenticationManager` 的会话 accessToken 补回**（这正是拦截器职责）。删了会再补，白删。

**最终修复（第二版补丁）**：利用 WB 拦截器自带的逃生头 `X-No-Authorization`（见即跳过）：
```
if(delete em.authorization,delete em.Authorization,em["X-No-Authorization"]="true",delete em["user-agent"],this.isCustomModelRequest(ec,eu)){
```
备份 `backup_wb_codebuddy_20261127_1300/`（第一版补丁态，4175816e...），
改后 sha e8fb90c3...，`node --check` 通过。

**端到端验证**：还原两份 models.json（干净 /v1）→ 停捕获服务器 →
同一 CLI 命令直连真实 dots：之前 `403 key_not_allowed` → 现在返回 **`pong`**。修复确认。
坑：第二轮备份脚本在 domestic 已指向捕获地址后才复制 `cn_models.json`，恢复断言拦住了，
改用第一份 `models.json` 备份恢复。GUI 当前会话（12:49 CLI host）仍持第一版补丁代码，
**需再次完全重启 WB** 才加载第二版。

**skill 已更新同步**：SKILL.md 红线 + agent-endpoints WB 节改为两段式补丁完整说明（含捕获调试法），
8/8 GREEN 无漂移。

## au 国际版 dots 报错：max_tokens=524288 被上游拒（13:20）

用户报 au 国际版有报错（未给截图）。自查：diagnose route_ok 12/12、真实凭证 12、DB 三层全绿，
App 12:51 重启晚于配置修复——DB 层没有问题。挖 au 主日志
`zwork-main-2026-11-27.log`：13:06:44 dots 请求 `outcome:failed`（260ms 快速失败）。
查 DB 行发现 `max_tokens=524288`——加模型时把 512K **上下文**错填进了**输出上限**字段。
此前实测 dots 对 max_tokens=524288 直接 400 `provider.client_bad_request`，32768 正常
（dots 官方 output limit=32768，Loomy/小浣熊当时就配的 32768）。

**修复**：备份 `backup_au_dots_maxtok_20261127_1315/`（sqlite+wal+shm），
`UPDATE model_connections SET max_tokens=32768`（route_revision 哈希不含 max_tokens，无需重算），
复核 route_ok 12/12。用 32768+tools+stream 模拟 au 请求形态实测 200。
**教训**：加模型时 max_tokens 字段填的是"最大输出"，不要把 contextWindow 抄进去；
以后 onboarding 脚本应对 maxTokens 做 output 上限校验。

**待用户**：重启 au 国际版后复测 dots。

## au 主库页级损坏 + 完整恢复（13:31，重要教训）

max_tokens 修复后用户复测仍失败（`400 governance.dots_platform_invalid_request`）。为抓真实请求把
au 库 base_url 临时指向本地捕获服务器，用户重启后发消息触发（回复"okokok"=假流式响应），**抓包成功**。

**根因（抓包实锤）**：au 同时发 `reasoning:{"effort":"high"}` + `reasoning_effort:"high"` +
`thinking` + `enable_thinking` 四个推理参数；逐项剔除实验证明**单独发任意一个都 200，
`reasoning` 与 `reasoning_effort` 并存即 400**。

**事故**：我在 au 运行期间反复外部读写其 SQLite + 用户快速重启，导致 WAL 损坏（NOTADB）
→ 用户重启出现"本地数据出现异常/ledger_integrity_failed"→ 主库出现真实页级损坏
（integrity_check 多个 btree 页报错）。主库 13:25 前的备份是干净的。

**恢复**：用户退出 au → 损坏文件隔离（`quarantine_au_corrupt_20261127_1331/`，未删）→
从 `backup_au_capture_20261127_1325/runtime.sqlite`（quick_check=ok、含真实 URL+32768）恢复主库、
删 WAL/SHM 重建 → `supports_reasoning=0`（根治：au 不再发推理参数组合）→ 删除
`runtime.sqlite.corruption-observed.json` 标记 → quick_check ok、route_ok 12/12、18 条连接完好。
丢失：仅 13:25 后 au 内的新会话数据。

**教训（必须遵守）**：
1. **绝不.au 运行期间外部写它的 runtime.sqlite**——写前必须让用户完全退出应用（连报错窗口）。
2. 快速失败+错误类型变化=多层病根叠加，要用本地捕获服务器抓真实请求体，别猜。
3. 每次改库前 quick_check 备份，备份本身也要验证 quick_check。

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

## - 当日会话 2 个，消息 20 条：
  - [10 条] 你是（session sess_ae494406-08…）
  - [10 条] 你是哪个模型（session sess_d4ccbec0-d5…）