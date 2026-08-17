---
layout: default
title: 每日工作总结 · 2026-08-17
date: 2026-08-17 23:30:00 +0800
---

# 每日工作总结 · 2026-08-17

> 来源：本机机器日志（会话目录 `2026-08-17-00-05-49/.workbuddy/memory/2026-08-17.md`）+ workspace 根 `.workbuddy/memory/2026-08-17.md`。今日主线 = 发布链路事故修复与固化 + 有道龙虾（LobsterAI）活清单模型导入 + 雷达轮询调优。

## 一、今日完成事项（分点，通俗语言）

1. **锁定 14 个自动化 tasks 的模型为 hy3**：此前 modelId 为空，调度器走自动路由会冒出 glm-5.2 / minimax-m3 等模型；用户要求 8/31 前只用 HY3，已用 `automation_update` 逐个显式写死 modelId=hy3。
2. **固化两条发布链路铁保证（等同红线）**：①「有交接文档必有技术点」——技术点生成不再被「本顿是否已发新 handoff」卡住；②「Gridea 不漏稿」——渲染+push 必须是 23:07 主链最末棒（已删独立 23:12 Gridea 任务，避免抢 git / 早于稿件落盘的竞态）。两保证写入跨项目记忆 `~/.workbuddy/MEMORY.md` 与项目 MEMORY.md，并更正过期排程记录。
3. **修复 260816 夜间 5 端发布事故**：根因有二——技术点生成被「已发过的 handoff 判为已发布→跳过」卡掉；Gridea 渲染竞态（handoff 稿件 23:28 才落盘，23:12 同步早跑完）。已补生成并推送 14 篇缺失技术点、重渲染 Gridea、清 20 篇积压、改造 23:07 自动化（技术点无条件 + 末尾渲染 Gridea）。遗留：有道云第 5 端 upload_youdao 退出码 1 待另查。
4. **核查并根除「老技术点脚本重复发」风险**：实测查证旧第三轴任务 `automation-1785648241323/1785648241459` **根本不存在**（view 报 not found，此前记忆误判已更正）；老脚本只认带日期的 `YYYY-MM-DD-techpoint-<slug>.md`，新链产 `techpoint-<slug>.md`（无日期）→ 命名不兼容，老脚本捞不到、不会重发。清理了 10 篇真重复（老+新各一篇），老格式移出集合目录 / 剩余 40 篇建占位冻结。
5. **老脚本「暂停不删、隔离不干扰」**：把 4 个老技术点脚本 + `gen_autoclaw_docs.py`（一次性硬编码 260812 的老格式生成器）移入 `handoff/_deprecated_old_techpoint/` 隔离暂停；DB 只读核查确认 14 个自动化无任何任务实际 subprocess 调老脚本，新链已彻底独立。
6. **技术点扩为全端发布**：用户拍板选项 A，把技术点从「刻意只发 2 端（避 spam）」扩为全端；因语雀会员到期 API 不可用，实际落 **4 端**（Gridea + 博客源 + 论坛 bbs1org#3/phpBB#11 + 有道云第 5 端）。落地点：`handoff_flow.py` 加 `YUQUE_ENABLED=False` 守卫；`techpoint_flow.py` publish 新增 Gridea 写稿 + 论坛发帖（标题去重）。⚠️ 发现 `techpoint/update/` 现存 **76 篇待发布技术点**积压，当晚 23:07 会一次性发 4 端。
7. **有道龙虾（LobsterAI）活清单模型导入（含纠错）**：
   - 初判（21:51，后证错）：以为落点是 `openclaw.json` 的 `models.providers`，按此注入 9 个 `wb-<vendor>` provider。
   - 更正（22:08）：扒 asar + sqlite 核实——真正落点是 `AppData\Roaming\LobsterAI\lobsterai.sqlite` 的 `kv.app_config.providers`（字典，按供应商名做 key）；APP 自带「导入供应商」JSON 功能只能改已有 key、加不了新 vendor。唯一可靠路子 = 直接写 sqlite，用自定义 key `custom_0`..`custom_8`（`isCustomProvider` 约定）。
   - 落地（22:12–22:19）：关 APP → 备份 sqlite → 把 `~/.workbuddy/models.json`（28 模型 / 9 vendor）按 vendor 注入 `custom_0..8`（apiFormat 全 openai，displayName=供应商名），原内置 18 provider 保留；回读校验通过（新增 custom=9 / 模型=28）。用户重启 LobsterAI 即可在设置→供应商看到。
8. **存可复用 skill**：把龙虾批量导入流程固化为用户级 skill `~/.workbuddy/skills/lobsterai-batch-model-import/SKILL.md`（根因 + 落点 + custom_N 约定 + schema + 注入脚本 + 踩坑）。
9. **雷达轮询间隔调优**：测速(speed) 改 **2 小时(7200s)**、测限流(ratelimit) 改 **8 小时(28800s)**。用 `radar-interval-tune` 脚本 `set_radar_interval.py --radar both --hours 2 8`：自动备份 config.json → 停旧进程(PID 10060/10148) → 起新 daemon(PID 12032/2008) → 日志实证新间隔生效。安全下限未触发。
10. **10:16 离线兜底补发巡检（11:00 检查点链路）**：自动化 `1784739275903` 核验 08-14/15/16 三日的总结已落盘（mtime 均在当晚 22:57–23:01），无缺失→跳过补发，未触发 publish-yuque.yml。

## 二、关键决策 / 注意事项

- **模型锁 hy3**：8/31 前全部自动化只用 HY3，已显式写死 modelId，杜绝自动路由换模型。
- **语雀会员到期**：handoff / 技术点发布链路的语雀端（API）已禁用（`YUQUE_ENABLED=False`），跳过不计失败；冗余发布由云端 `publish-yuque.yml` Action 兜底（限流红线：不手动重发语雀）。
- **老脚本红线**：暂停隔离即可、不删除；任何情况下不得让老脚本往论坛/语雀/Gridea 重发技术点、或往 `_handoffs` 写老格式干扰新链。
- **龙虾导入唯一正确落点**：`lobsterai.sqlite` 的 `kv.app_config.providers` + `custom_N` key；必须关 APP 再写（否则内存态覆盖回滚）；勿动 `openclaw.json` / `app.asar`。某 vendor 报 404 多为 base 缺 `/v1` 后缀（如 DeepSeek 已修正为 `https://api.deepseek.com/v1`）。

## 三、生成的有用文件（表格）

| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| 今日工作总结（本文件） | `D:\AI work\workbuddy\2026-08-17-00-05-49\2026-08-17_每日工作总结.md` | 4 端发布源 + 归档 |
| 进度留痕（8 份） | `D:\AI work\workbuddy\2026-08-17-00-05-49\进度_20260817_*.md` | 各阶段进度备查 |
| 龙虾活清单导入文件 | `D:\AI work\workbuddy\handoff\lobsterai_models_import.json` | 28 模型 / 9 vendor 的 JSON 导入包 |
| 龙虾批量导入 skill | `C:\Users\Administrator\.workbuddy\skills\lobsterai-batch-model-import\SKILL.md` | 复用导入流程 |
| 龙虾 sqlite 备份 | `AppData\Roaming\LobsterAI\lobsterai.sqlite.bak_20260817_221235` | 注入前备份，可回滚 |
| 雷达 config 备份 | （由各 `config.json` 的 `set_radar_interval.py` 自动备份） | 间隔调整前备份 |
| 老脚本隔离目录 | `D:\AI work\workbuddy\handoff\_deprecated_old_techpoint\` | 暂停不删、防干扰新链 |

## 四、待办 / 风险

- **P1 有道云第 5 端 `upload_youdao.py` 退出码 1**：260816 修复遗留，今日未深入；由 23:07 主链步骤④统一跑，退出码 1 待查（三轴镜像是否真失败）。
- **P1 技术点 76 篇积压**：`techpoint/update/` 现存 76 篇待发，今晚 23:07 一次性发 4 端（含论坛 76 帖），量偏大但按设计在夜间跑、避免白天打爆限流。
- **P2 龙虾连通未实测**：沙箱无网，sqlite 注入已校验结构但未实测各 vendor 真实通；需用户重启龙虾并自测，404 多查 `/v1` 后缀。
- **P2 雷达 daemon 常驻状态**：新 daemon(PID 12032/2008) 已起、日志实证新间隔；看门狗覆盖情况待下个会话确认。
- **跨项目**：发布链路两条铁保证已固化进 `~/.workbuddy/MEMORY.md`（每次会话自动注入），需后续自动化严格遵守。
