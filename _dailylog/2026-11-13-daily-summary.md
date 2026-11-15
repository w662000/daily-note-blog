---
layout: default
title: 每日工作总结 · 2026-11-13
date: 2026-11-13 23:30:00 +0800
---

# 每日工作总结 · 2026-11-13

## 一、今日完成事项（分点，通俗语言）

- **修好托管 Python 解释器，所有自动化恢复运行**：早上发现每日合并自动化报 `No module named 'encodings'` / `Could not find platform independent libraries`。查明是 `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/` 下的 `Lib` 标准库目录在今天 10:18 被清掉了（目录修改时间可印证），而这个目录被多个自动化脚本共用，缺了就会全部失效。已从本机 `Loomy/python-runtime/3.13.13-09efd5c6/Lib` 复制完整的 3.13 标准库回去（同 ABI、同 pyc 魔数，兼容）。修复后 `daily_combo.py` 恢复正常。
- **今日日合并脚本跑通**：阶段1 喵旅行 idle 未达上限，自动出发（商场店铺，location_id=2，轮换 2/4）；阶段2 签到成功，连续天数 45 天，msg=OK。
- **查清 4 端发布停更约 1 个月的两层原因**：一是 gh 令牌失效，`gh auth status` 报 token invalid，导致 git push 无法认证，daily-note-blog 积压 156 个 commit 推不出去，线上博客停在 10-12；二是发布链自动化从 11-02 起连续 12 天全灭，统一报 `refusal -32003 Quota exceeded: 429 请登录platform进行实名认证以获取更高rpm`（免费档 RPM 上限）。脚本型自动化（签到/SkillHub/Gridea sync）同期正常，说明不是调度器问题，是 LLM 调用被限流拒答。
- **推送积压清零、线上博客恢复**：用户 21:05 完成 `gh auth login`（device flow，凭证存 keyring）；21:10 把 156 个积压 commit 一次推上 GitHub（5372264..d4da4a3 → master），GitHub Pages 自动重部署，线上博客恢复至 11-13。
- **发布链架构重构方案落地**：新建 `D:\AI work\workbuddy\publish_train.py`，把搬运环节固化成 7 步串行脚本（handoff publish → techpoint publish → youdao → sync_logs 今日+昨日 → 博客 git push → 论坛补发 3 天 → gridea_auto_sync），全幂等、单步失败不中断，日志写到 `logs/publish_train_YYYYMMDD.log` 并带 SUMMARY 行。
- **注册系统级定时**：Windows 任务计划新增 `WB_publish_train_2315`（每日 23:15）和 `WB_publish_train_retry_1020`（每日 10:20 晨检重试），带 StartWhenAvailable 补跑、30 分钟超时，命令使用受管 venv python。
- **8 个自动化切换模型**：23:00/23:05/23:07 → gemma；10:00/10:05/10:10/10:15/11:00/23:15 → qwen3。切换时 23:00 任务曾产生重复行（1784700756809），已删除，保留原 `automation-1784700756809`。
- **剩余自动化全量切换完成**：美团领券/签到合并(hourly)/签到查漏补缺/Replit 续期提醒/SLG 抓取/SLG cookie 提醒/Replit 到期提醒×2 → qwen3；SkillHub 看板 → gemma。终验 18/18 自动化全部在 CF 双模型上（gemma 主 5 个、qwen3 垫 13 个），hy3/agnes/glm-5.3-flash 清零。
- **产出最靠谱模型 TOP20 报告**：数据源为限速雷达 latest.json（2026-11-13 19:55 实测，92 模型×15 连发）+ 活清单基准分（2026-10-13 综合分排行）。分布：满分 15/15 仅 18 个 + 93% 的 2 个；不可靠(<50%) 53 个；untestable 19 个。T1 主力：deepseek-v4-pro(62.9)/deepseek-flash(62.7，官方直连)/@cf/gemma-4-26b(64.7)/@cf/qwen3-30b(62.4)/@cf/gpt-oss-120b(59.7)/nemotron-3-ultra-550b/@cf/qwq-32b。

## 二、关键决策 / 注意事项

- **模型选型决策（用户拍板）**：生成环节弃用 GLM，改用 CF Workers AI 模型（免实名认证）；搬运环节固化成 py 脚本走系统级定时。主模型 = `@cf/google/gemma-4-26b-a4b-it`（综合分 64.7，CF 第一），垫底 = `@cf/qwen/qwen3-30b-a3b-fp8`（62.4，CF 第二）；双模型隔离，晚主链走 gemma、早兜底走 qwen3。
- **更正此前误判**：旧发布链并非"未指定模型"——23:00 用 agnes-2.5-flash、兜底任务用 glm-4-flash-250414，只是底层都打到智谱后端被 429。此前说 model_id 全空，是读错列名（model_id 误判为 modelId）。
- **限流元凶实锤**：agnes-2.5-flash 15 次中 13 次被限流；glm-5.2 分高(64.8)但 8/15 限流；deepseek-v4-flash 走 Loomy 中转 14/15 限流，而官方直连 15/15 全通；Gemini/Loomy/b.ai 通道网络层全挂。选模型要看实测限流，不能只看基准分。
- **运行时必须 `env -u PYTHONPATH`**：WorkBuddy 自身把 `PYTHONPATH` 设为 `D:\Program Files\WorkBuddy\resources\app.asar.unpacked\cli\vendor\shim`，会污染托管解释器导入。
- **首跑安排**：今晚 23:15 列车首次实跑（此时 261010 handoff 积压 + 3 天论坛补发会真实发出）；未手动提前跑，等用户知情。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
| --- | --- | --- |
| 搬运列车脚本 publish_train.py | `D:\AI work\workbuddy\publish_train.py` | 7 步串行发布搬运，全幂等、单步失败不中断 |
| 列车运行日志 | `logs/publish_train_YYYYMMDD.log` | 每次列车运行记录，带 SUMMARY 行 |
| 最靠谱模型 TOP20 报告 | `model-speed-radar/最靠谱模型TOP20_2026-11-13.md` | 92 模型限流实测 + 基准分综合排行，供选型参考 |
| 恢复后的宿主 Python 标准库 | `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/Lib` | 供所有自动化脚本共用的 3.13 标准库（含 encodings） |
| 标准库复制来源目录 | `C:/Users/Administrator/AppData/Local/Loomy/python-runtime/3.13.13-09efd5c6/Lib` | 本次修复的 Lib 来源 |

## 四、待办 / 风险

- **P0：完成模型平台实名认证**，解除 429，恢复 23:00 发布链；之后可考虑把 23:00 档 6 个任务错峰串行，进一步降低 RPM。
- **首次列车实跑待观察**：今晚 23:15 首跑，会真实发出 261010 handoff 积压和 3 天论坛补发，需确认结果与 SUMMARY 行。
- **Lib 被清原因未查明**：标准库目录今日 10:18 被清掉，来源不明，存在再次被清、导致全部自动化挂掉的风险。
- **两个已过期的 once 提醒待清理**：Replit 到期提醒（8/23、8/25）早已过期不会再触发，建议下次清理时删除。
- **历史记录缺口**：automation_runs 仅保留 11-02 之后记录，10-12~11-01 的失败情况无法考证。
- **gh 令牌长效性**：本次靠用户重新 `gh auth login` 恢复，需关注令牌后续是否再次失效导致 push 积压。