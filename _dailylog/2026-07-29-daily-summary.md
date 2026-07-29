---
layout: default
title: 每日工作总结 · 2026-07-29
date: 2026-07-29 23:30:00 +0800
---

# 每日工作总结 · 2026-07-29

> 数据来源：合并当天 3 份会话级机器日志（2026-07-29-17-12-59 主任务、2026-07-29-22-32-36 GLM 密钥轮换、2026-07-29-23-09-10 发布链路排查）+ 根 `.workbuddy/memory/2026-07-29.md`（00:15 Failover 巡检，无操作）。

## 一、今日完成事项

1. **DNSHE 免费域名平台梳理**：把该平台 7 个可注册后缀（cc.cd / de5.net / bot.cd / ccwu.cc / bbroot.com / ddns.ge / l.cd）在 Cloudflare 托管兼容性与国内访问速度上的差异逐一理清，给出首选推荐 **de5.net**（.net 国内天然顺畅且已验证可托管 CF）。
2. **de5.net 三位数字子域名（001–999）可注册扫描**：先走了弯路——用 DNS 解析判定可注册，发现完全不可信；改用 DNSHE 官方 WHOIS API 正确判定。中途一次「5 个 agent 并行后台扫描」因脚本只把结果打到控制台、没落盘而全丢，重跑并改为写文件，最终扫完 999 个：**305 个可注册、694 个已占用、0 个待定**，并整理出连续可注册区间（如 489-498、834-850、971-975 等）。
3. **NVIDIA NIM 预览模型实测**：确认 NIM 预览分类下共 **24 个模型全部带免费端点**（且无文生图模型）；实测 12 个聊天模型的首字响应延迟——最快 Nemotron-3-Super-120B 仅 0.28s；并确认 Kimi-K2.6 已于 2026-07-07 正式下线（返回 404 属正常）。
4. **WorkBuddy 模型列表扩充与校正**：把 NIM 速度 Top5 模型直连加入 `~/.workbuddy/models.json`（总模型数 25→30）；随后更正了其中 5 个 NVIDIA 模型 ID 的拼写错误（当初写错导致 404）。
5. **slg-china 项目改造并上线**：将模型梯队从三层降为两层、删除全部 GLM 直连模型（只保留 Cloudflare 自带模型 + OpenRouter 免费），重新部署到 `https://slg-china.pages.dev`。
6. **WorkBuddy 30 模型基准测试**：用一道约束推理题评测 30 个模型，过程中发现并修复两个坑（max_tokens 太小截断深度推理答案、重测脚本把非 NVIDIA 模型的真实回复覆盖损坏），评分脚本最终产出报告。
7. **GLM API Key 轮换**：把 WorkBuddy `models.json` 里 9 个 GLM 模型 + Hermes `.env` 的 `GLM_API_KEY` 从旧 key 换成新 key。
8. **论坛 / 博客发布链路排查与补发**：定位 28 号「每日工作日志论坛帖子」缺失的根因（当晚本地代理离线导致自动化被拒、一行没跑），手动补发到 bbs1org（topic=21）/ phpBB（topic=38）；同时排查并修复博客 28 号未推送的问题，并发现博客 URL 互相覆盖的结构性 bug。

## 二、关键决策 / 注意事项

- **DNS 解析状态 ≠ 注册状态**：判定域名能否注册必须用注册商官方 WHOIS API，绝不能用 DNS 查询。铁证：222.de5.net 在面板显示「已注册」，但 DNS 返回 NXDOMAIN（保留/已注册但未挂记录的域名在权威 NS 上无 SOA，DNS 完全看不到）。
- **批量检测脚本必须写文件**：派 agent / 后台任务做批量检测时，脚本要把进度与结论写入文件，不能只 `print` 到 stdout——进程一结束结果即不可恢复（本次已丢一次、重跑约 40 分钟）。
- **Git Bash 路径坑**：在 Git Bash 里把 `/d/...` 传给 Windows `python.exe` 会被错误转义成 `D:\d\...`；必须用 `D:/...`（Windows 原生盘符 + 正斜杠）。
- **Kimi-K2.6 的 404 是模型下线，非权限问题**：已给出 3 条迁移路径（Moonshot 官方 API / OpenRouter / 自托管 NIM）。
- **基准测试两坑（下次必避）**：① `max_tokens=2000` 会截断深度推理模型的答案、导致判分偏低，改用 4096；② 重测脚本硬编码 NVIDIA URL，会把 7 个非 NVIDIA 模型（Gemini / Lagua / OR 免费）的原始真实回复**覆盖成 404 数据损坏**，必须改回「按各模型自己 url 重测」。
- **代理陷阱**：本机并存两个代理地址——`127.0.0.1:10808`（离线）与 `127.0.0.1:7897`（在线）。自动化若误走离线那个会被拒（这正是 28 号论坛自动发布失败的直接原因）。
- **密钥安全**：DNSHE API Key 与 NVIDIA Key 仅经进程级环境变量传入，绝未写入文件 / 日志 / memory 明文；已提醒用户去后台吊销。models.json / .env 的 key 改动需重启对应进程（WorkBuddy / Hermes）才生效。

## 三、生成的有用文件

| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| de5_available.txt | `D:\AI work\workbuddy\2026-07-29-17-12-59\de5_available.txt` | 可注册的 305 个纯数字子域名清单 |
| de5_available_full.txt | `D:\AI work\workbuddy\2026-07-29-17-12-59\de5_available_full.txt` | 同上，带 `.de5.net` 后缀，便于直接注册 |
| de5_taken.txt | `D:\AI work\workbuddy\2026-07-29-17-12-59\de5_taken.txt` | 已占用的 694 个子域名 |
| de5_progress.txt | `D:\AI work\workbuddy\2026-07-29-17-12-59\de5_progress.txt` | 扫描全程日志（999/999 已完成） |
| de5_uncertain.txt | `D:\AI work\workbuddy\2026-07-29-17-12-59\de5_uncertain.txt` | 待定清单（本次为空） |
| format_ranges.py | `D:\AI work\workbuddy\2026-07-29-17-12-59\format_ranges.py` | 把纯数字列表转连续区间紧凑版，便于批量注册 |
| check_de5_persist.py | `D:\AI work\workbuddy\2026-07-29-17-12-59\check_de5_persist.py` | 官方 API 法 + 落盘（最终正确版，读 DNSHE_API_KEY/SECRET 环境变量） |
| check_de5_api.py / check_de5.py / probe_dnshe.py / probe_dnshe2.py | `D:\AI work\workbuddy\2026-07-29-17-12-59\` | 早期探针 / DNS 法 / API 法脚本（均已弃用，仅留作方法对比） |
| nim_models_report.html | `D:\AI work\workbuddy\2026-07-29-17-12-59\nim_models_report.html` | NIM 24 个预览模型交互式总表 |
| nim_speed_results.json | `D:\AI work\workbuddy\2026-07-29-17-12-59\nim_speed_results.json` | 12 个聊天模型延迟实测结果 |
| speed_test_nim.py | `D:\AI work\workbuddy\2026-07-29-17-12-59\speed_test_nim.py` | NIM 速度测试脚本（v2，流式测 TTFT） |
| benchmark_report.html | `D:\AI work\workbuddy\2026-07-29-17-12-59\benchmark_report.html` | 30 模型基准测试报告（retest 前版本，待重生成） |
| benchmark_report.py | `D:\AI work\workbuddy\2026-07-29-17-12-59\benchmark_report.py` | 评分脚本（正确性+推理完整度+格式） |
| models.json | `C:\Users\Administrator\.workbuddy\models.json` | WorkBuddy 模型列表（30 个，含 NIM Top5 + 9 个 GLM 新 key） |
| .hermes/.env | `C:\Users\Administrator\.hermes\.env` | Hermes 的 GLM_API_KEY 已换为新 key |
| slg-hub-cf（functions/api/chat.js 等） | `D:\AI work\workbuddy\2026-07-27-11-25-53\slg-hub-cf` | slg-china 改造后代码（两层梯队、去 GLM 直连），已部署 |
| publish_worklog_log.txt.bak_0729 | `D:\AI work\bbs1org-deploy\publish_worklog_log.txt.bak_0729` | 论坛发布日志备份（补发 28 号前） |

## 四、待办 / 风险

- **博客 URL 互相覆盖（结构性 bug，待用户拍板）**：`daily-note-blog/_config.yml` 的 `permalink: /dailylog/:slug/` 会把文件名前缀 `2026-07-28-` 日期剥掉，导致所有「每日工作总结」共用同一地址 `/dailylog/daily-summary/`，每天互相覆盖——首页把每天都链到同一处，点进去永远是「最新构建那天」，27 号及更早已不可单独访问。建议改成 `permalink: /dailylog/:year-:month-:day/:slug/`，但会改变已发布 URL，需用户确认。语雀不受影响（走另一仓库 + Action）。
- **论坛工作日志无离线兜底**：现有「离线兜底·补发缺失总结」自动化只补 summary，不补论坛原始工作日志帖子。若 23:40 当晚代理再离线，论坛工作日志会再次静默缺失。建议给论坛也加 09:30/10:00 兜底（复用 `publish_worklog_to_forums.py --date <缺失日>`），或确保 `127.0.0.1:10808` 常驻。
- **de5 子域名待批量注册**：连续可注册区间（489-498、834-850、971-975、459-465、538-549、634-649、679-695、729-746、759-785 等）已导出，等用户去 DNSHE 批量抢注。
- **NIM 慢模型未 warm-up 复测**：MiniMax-M3 / Mistral-Medium-3.5 / GLM-5.2 首调冷启动 36-108s，多为共享免费端点冷启动而非真实推理慢，本次未复测，结论仅供参考。
- **benchmark_report.html 待重生成**：当前为 retest_6 修复数据前的版本，建议修复后重生成以获得准确评分。
- **GLM 新 key 生效前提**：WorkBuddy / Hermes 重启前新 key 不生效；`models.json.bak` / `.backup-20260725` 历史备份仍含旧 key 未改动，若对外分发需注意。
- **GitHub 同步**：本机 `gh` 若未登录或代理不通，push 会失败（预期内）——总结已复制到本地仓库（语雀源 `workbuddy-daily-note/summaries/` + 博客源 `daily-note-blog/_dailylog/`），配好 `gh` 后下次即生效。
