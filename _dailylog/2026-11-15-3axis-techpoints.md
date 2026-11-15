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

## 修复增删 BUG + 故障退避（2026-11-15 14:25）
用户报障：① 点+后输"贵阳"敲回车没添加；② 点红叉没删除。根因：搜索框没绑 Enter 键事件（真 bug）；用户看的是静态 preview.html，/api 请求无人接（预览本来就不能增删）。
修复：
- views.py JS 补 keydown Enter：添加模式=加第一个候选（无候选转 /api/search 在线搜）；普通模式=切换到第一个候选；增删模式加 mode-hint 醒目提示条（不再只闪 placeholder）；focus({preventScroll:true}) 防页面跳动
- 新增 run_server.py（wsgiref，127.0.0.1:8734，PORT 环境变量，日志静默）本地真实联调
- weather.py 加上游故障退避 _last_upstream_fail + config.FAILURE_BACKOFF=120s：直连失败后 N 秒内不再试上游（实测首请求 8.3s→后续 0.01s），避免每个请求干等超时，对 256M 机器和上游宕机场景都关键
- _fill_missing 细化：页面来源为 demo 时缺城补 mock（顶栏已标注演示，不算冒充）；live/cache/stale 来源缺城走 fetch_detail，失败留空记 error
- 实测通过：add guiyang/dali → 首页 8 城卡片+面板齐全；remove dali → 面板消失；sqlite 持久化跨重启生效
- 当前本地关注列表：6城+贵阳+大理（留给用户测删除）

## 修复"127.0.0.1:8734 无限转圈"（2026-11-15 14:30）
根因：wsgiref 默认单线程，本机连不上 api.open-meteo.com 时 urlopen 的 timeout 管不住 DNS/握手等待（8~30s），一个慢请求把所有后续请求全部阻塞 → 浏览器无限转圈（curl health 正常造成"服务活着"的假象）。
修复三件套（run_server.py + weather.py）：
- ThreadingWSGIServer（daemon_threads）：实测首页卡 8s 期间 health/search/css 全部 4ms 秒回
- 指数退避：window=FAILURE_BACKOFF(120s)×2^连续失败次数(封顶16倍→32min)，连续失败不再每个窗口到期都重卡一次
- 启动预热线程 _warmup()：后台先探测一次上游（连通预热缓存/不通立即进退避），用户第一发请求实测 0.010s 秒开
注意：后台 bash 任务可能在会话轮次间被回收，服务死时重启 python run_server.py 即可。

## 修复"点下拉候选不能加入关注"（2026-11-15 14:40）
真正根因：catalog.catalog_payload() 输出的城市 JSON 漏了 id 字段（只有 name/province/lat/lon/py）！前端下拉候选项因此没有 data-city-id，添加模式点候选拿到空 id → 走"在线乡镇不可加入"提示分支；回车添加则把 undefined 当 id 发请求被服务器 400 拒。之前"输贵阳回车没反应"同根因。
修复：catalog_payload 补 "id"；新增回归测试 test_02b（目录必须带 id、天津专门盯住）；
服务器端 city=undefined 已被 400 拒（验证过）。
实测：页面内嵌目录含 "id":"tianjin"；XHR add?city=tianjin → ok；首页出现天津卡片。
附带发现：用户之前点红叉时 API 其实删成功过（贵阳/大理被删，UI 反馈坏了导致误判"没删成"）；当前列表=6城+天津。
用户提的备用方案（两栏输入框+查询/增加按钮）暂不需要——根因已修；若用户仍不满意交互再做。

## 预报表加日出/日落列 + 列宽收窄（2026-11-15 14:50）
用户要求：表格"最低/区间/最高"变窄，末尾加日出日落。
- config.DAILY_FIELDS 加 sunrise,sunset（批量接口原先没有）；weather.parse() 每日加 sunrise/sunset（[-5:] 截 HH:MM）
- views._forecast/_MAIN_JS renderDynamic 两处同步加 d-sun 列（合并为一列"日出/日落"显示 "07:10 / 17:20"）
- CSS：table-layout:fixed，.d-lo/.d-hi 7%、.d-bar 42%→17%、.d-sun 15%；≤640px 隐藏降水列和日出日落列、加宽剩余列
- fixtures 补 sunrise/sunset 数组（注意必须零填充 HH:MM，否则 [-5:] 会截出"T"）
- 21/21 测试全绿（test_04 加了批量日出日落断言）

## 卡顿修复：load_weather 改 stale-while-revalidate（后台刷新+有界等待）
- 用户报"刷新后转圈5-10圈才出新页面"：根因是退避窗口到期后每个请求都同步卡 8-11s 等上游
- weather.py：load_weather 重写为 SWR——起后台线程刷上游，请求最多等 config.REFRESH_WAIT(1.5s)，
  等不到就用缓存/演示先渲染；_fill_missing 在 _refresh_lock.locked() 时跳过网络
- **坑1（测试失败根因）**：worker() 内 `_consecutive_upstream_fails += 1` 缺 global 声明 →
  UnboundLocalError，失败路径全崩。抽成模块级 `_note_upstream_ok/_note_upstream_fail` 两个 helper
- **坑2（并发缺陷）**：_refresh_done 只在启动新 worker 时 clear，刷新进行中第二个请求会立刻读到
  上一轮旧结果。加 `_refresh_seq` 代数号，worker finally 里写回 gen，读者校验 gen 匹配才采信
- worker 改 try/finally：任何异常都保证 set 事件 + release 锁
- 新增 test_20b（live→cache→stale+退避→退避内不碰网络→demo 链路）、
  test_20c（上游 sleep 模拟卡死，断言请求 ≤ REFRESH_WAIT+1s；注意断言退避前要先等锁释放）
- 23/23 测试全绿；实测：有缓存 ~10ms，无缓存首屏最多 1.5s（后台刷完后恢复毫秒级）

## 全球主要城市支持（用户问能否查纽约）
- 实测：Open-Meteo 地理编码中文支持不完整（纽约 0 结果，北京/东京/伦敦正常）→ 不可靠
- 方案：catalog.py 内置 WORLD_CITIES 90 个国际主要城市（中文名+国家+坐标+英文标识+中文别名
  如 三藩市/雪梨/西贡/火奴鲁鲁），region="国际"，与国内城市同构（id=英文标识）
- 搜索支持：中文名/别名包含、英文标识（忽略大小写和空格，"New York"→newyork）
- catalog_payload 增加 alias 字段；前端 findCatalog 同步支持别名+去空格匹配
- 国际城市也可加入关注卡片（走 by_id 校验，批量天气/AQI 接口全球坐标都支持）
- 总目录 451 城（361 中国 + 90 国际）；test_01 坐标断言按 region 分流；新增 test_02c
- 25/25 测试全绿；实测纽约 3.4°C 阴、西北风；已上传（需重启 uWSGI）

## 内存监控页 /_mem.html（参考 searxng-render 的 mem_reporter.py）
- 新增 mem.py：cgroup v2/v1 内存（current/limit/peak）+ 全进程 RSS 合计 + 本进程 VmRSS/VmPeak/线程
  + 应用缓存（LRU 条目数、cache.json/hits.sqlite3 大小、目录 643 城、gc 对象数、运行时长）
- app.py 注册 /_mem.html（卡片式页面，10 秒 meta 刷新，75%/90% 告警分级）和 /_mem.json
- 纯标准库、读不到的指标优雅置 None（Windows 本地验证过降级）；Linux 上才有 cgroup 数据
- deploy.sh FILES 增加 mem.py；26/26 测试全绿；已上传（需重启 uWSGI）

## 机票数据源查证结论
- **飞猪 TOP 对个人不可行**（官方文档 2026-08：公司身份+天猫卖家+软著+聚石塔+5-10天审核）——豆包"注册就能用"是错的
- **jisuapi 可行但收费**（约几元/月起；flight/query 返回全舱位价目表+minprice，已核实文档）
- 机票部分改为双源降级：jisuapi（主力）→ Amadeus（免费，中国国内航线覆盖待实测）；query_flight 返回 (price, source)
- 双源版已上传服务器实跑通过（未配 key 时优雅跳过）

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）