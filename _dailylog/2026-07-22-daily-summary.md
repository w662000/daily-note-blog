---
layout: default
title: 每日工作总结 · 2026-07-22
date: 2026-07-22 23:30:00 +0800
---

# 每日工作总结 · 2026-07-22

> 本日跨两个会话记录（早上 7-21 延续会话 + 晚间 18:02 新会话），机器日志齐备，以下为人读提炼版。

## 一、今日完成事项

1. **清理 D 盘根异常文件夹**：查清 `D:\c`(510M)、`D:\d`(226M) 成因——昨晚 Hermes 容器重建时 compose 宿主机挂载路径漏写 `C:` 盘符，Docker 当相对路径在 D 盘根自动建了这两份副本。确认不再被任何容器挂载后删除，腾出约 736MB。
2. **全量复盘昨晚(ds v4)的失误**：整理出 6 类错误操作链（误用 `--force-recreate` 触发 1 小时重装 / 挂载路径坑 / 无效操作 / 临时文件散落 / 备份翻车 / 误以为改配置要重启容器），写成防再犯档案。
3. **全量清理遗留临时产物**：删除 C 盘根误建的 docker-compose.yml、4 个临时脚本、`C:\tmp`、`D:\tmp`、6 个 Hermes 构建日志（保留了 `bootstrap.py` 源码与 `config.yaml.bak` 安全网）。
4. **跨工具护栏部署**：把"最小动作 + 后果预判 + 不确定先问"护栏铺到 WorkBuddy / Hermes / Trae / Qoder 全部在用工具（master 文件 `AGENT_GUARDRAILS.md` + 各工具注入点），防止事故复发。
5. **Hermes SOUL.md 强制句生效验证**：确认 Hermes 的 SOUL.md 在 agent 构造时缓存（非实时读盘），用 `docker compose restart`（非 recreate）重启后实测 `/api/memory` 已含强制句、编辑时间与缓存吻合，确认生效。
6. **WorkBuddy 对齐 Hermes 的 GLM 模型**：WorkBuddy 原本只能接 3 个 GLM（漏了赠送的 6 个）。实测同一把 key 在三个端点 9 个模型均可聊，根因是 `models.json` 名单漏列；已补齐为 9 个（沿用原 url + key）。
7. **GLM 9 模型速度测试**：流式测速（双字段解析推理模型），结论——`glm-4.5-air` 最快最稳（首字 430ms / 总 7s / 42.8 字每秒）为干活首选；`glm-4.6v` 首字最快且支持看图；其余 turbo/flash 重思考 + 限流，体验差。报告 + 脚本已归档。
8. **建立每日工作总结机制**（本报告本身）：把机器日志转成人读总结，归档到当天文件夹（并建了每天 23:30 自动生成的定时任务）。
9. **5 份每日工作总结（7-18~7-22）三端同步发布**：分别发到 flomo（PRO webhook）、Gridea Pro（静态博客）、说说(Ech0 本地)、语雀（知识库）四个端，全流程打通。
10. **说说(Ech0)本地备份部署**：把 Ech0 笔记平台作为语雀内容的本地备份库部署好（端口 6277 Web UI / 6278 SSH 查看，数据存 `D:\shuoshuo\data`，容器自动重启已设）。
11. **修复说说 5 篇乱序**：发现 5 篇按 `created_at` 同秒回退 rowid 导致错位；改为发布时显式赋各篇内容日期的真实时间戳，重新发布后顺序正确（最新置顶）。
12. **说说界面加宽**：通过官方 `custom_css` 入口覆盖 Ech0 自己的 `--home-main-max` 布局变量（约 448px → 800px），无需改容器源码，硬刷新即生效。
13. **每日三端发布流程文档化**：写成所有 Agent 都能看懂的 `DAILY_PUBLISH_WORKFLOW.md`（master + 同步到 4 个工具目录）+ 一份用户教程。
14. **AtomCode 接入三端发布**：因 AtomCode 跑在宿主机（非 Docker），能完整执行三端脚本；部署全局指令 `ATOMCODE.md` + 一个 skill，使其也能一键三端发布。
15. **排查并修复 Gridea "你好"故障**：Gridea 把测试稿件当成 `published:false` 草稿（缺标准 frontmatter），修复为标准格式 + `published:true`；并修正排序规则——每日总结用内容日期 `00:00:00` 保证日期顺序，普通文章用真实发布时间保证新文章置顶。
16. **三端发布改为定时自动化**：新建 23:59:20「每日三端自动发布（WB 主执行）」+ 次日 00:15「failover 巡检（AtomCode 兜底）」两个定时任务，形成"生成 → 主发 → 巡检兜底"闭环。
17. **主备容错协议**：写成 `FAILOVER_PUBLISH_PROTOCOL.md`，明确 WB 主执行、其他 agent 检测、失败由同源脚本补发（因 WB 无法从外部注入命令到 AtomCode 运行会话，failover 由 WB 代跑同款脚本，效果等同）。
18. **语雀改为 GitHub Actions 云端发布（关机免疫）**：担心本机 23:35 关机漏发，新建私有仓库 `workbuddy-daily-note` + Actions 工作流（北京 23:59 触发），由云端调语雀 API，断电也能发。
19. **新增 Jekyll 博客仓库**：新建公开仓库 `daily-note-blog`（GitHub Pages 自动渲染），彻底干掉 Gridea 手动"同步"按钮——23:30 同步脚本生成 `_posts` 文章并 push，Pages 云端自动渲染成博客。
20. **安装 GitHub CLI（gh）**：机器无 winget，改用免安装 zip 版（gh 2.96.0）解压到用户目录并写入用户 PATH，无权限问题。用户已完成 `gh auth login` + `gh auth setup-git`。
21. **GitHub 双仓落地 + 补推历史**：`workbuddy-daily-note`（语雀源）与 `daily-note-blog`（博客源）均已建仓、配 secret、push 成功；把 7-18~7-21 补推到两仓库，博客端 18-22 已全自动化上线。

## 二、关键决策 / 注意事项

- **命名卷保持现状**：hermes-agent-src / webui-venv / webui-uvcache 三卷已有真实数据（那次 recreate 的副产品），无需为"让卷生效"再去 recreate（重蹈覆辙）。
- **每日总结时间语义**：Gridea 排序用 `createdAt` 降序，故每日总结固定内容日期 `00:00:00`（保证日期顺序），普通/测试文章用真实发布时间（保证新文章在当天总结之上）；改完必须退出 Gridea 重开再同步。
- **GitHub 博客 `future: true`**：博客文章 date 写当天 23:30 会被 Jekyll 当"未来文章"默认排除，已在 `_config.yml` 加 `future: true` 解决。
- **语雀 API 坑**：响应用 `status` 字段（200=成功）而非 `code`；代理环境下用裸 `requests.post` 直发（用 `Session` 会被吞请求返回空）；删文档用 `DELETE /repos/{id}/docs/{doc_id}`。
- **Gridea 稿件规范**：必须直接产出标准 frontmatter 且 `published: true`，否则被当草稿永不发布。
- **说说(Ech0) 批量发历史内容**：必须显式传 `created_at`（内容日期时间戳），否则同秒乱序；删单篇用 `DELETE /api/echo/{id}`；Echo 无 title 字段，标题作正文首行。
- **云端 Actions 的边界**：GitHub Actions 跑云端，能调语雀云 API，但碰不到本机 `localhost:6277`(Ech0) 和本地 Gridea 文件 → 所以 GitHub 路径只覆盖语雀 + 博客两端；Ech0说说 + Gridea 仍由本机 23:59:20 任务发（关机则漏，未改）。
- **跨 agent 定时约束**：Qoder/Trae/AtomCode 自身无外部可写定时器，"定时触发"只能由 WB 自动化承担；角色写进各自 rules 使其被调用时参与容错。
- **WorkBuddy `models.json` 改动**需重启桌面端才生效（启动加载）。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 每日工作总结（本报告） | `D:\AI work\workbuddy\2026-07-22\2026-07-22_每日工作总结.md` | 当日人读复盘 + 有用文件清单 |
| 护栏 master | `D:\AI work\AGENT_GUARDRAILS.md` | 跨工具通用护栏（已部署到 4 工具） |
| GLM 测速报告 | `D:\AI work\workbuddy\2026-07-22\GLM_speed_test_report.md` | 9 模型速度对比与切换建议 |
| GLM 测速脚本 | `D:\AI work\workbuddy\2026-07-22\test_glm_speed.py` | 可复用，含 7 条测速逻辑要点注释 |
| 三端发布主脚本 | `D:\AI work\workbuddy\publish_daily_summary.py` | 语雀 API + 说说 API + Gridea 写文件，幂等可重跑（自动化专用稳定入口） |
| GitHub 双推脚本 | `D:\AI work\workbuddy\sync_logs_to_github.py` | 复制总结进语雀源仓库 + 生成博客文章并 git push |
| 三端发布流程文档 | `D:\AI work\DAILY_PUBLISH_WORKFLOW.md` | 所有 Agent 可看懂的发布流程（master，已同步 4 目录） |
| 主备容错协议 | `D:\AI work\FAILOVER_PUBLISH_PROTOCOL.md` | WB 主发 + 巡检兜底协议（已同步 4 目录） |
| 用户发布教程 | `D:\AI work\workbuddy\2026-07-22\每日发布流程教程.md` | 给本人的三端发布操作说明 |
| flomo 发布脚本 | `D:\AI work\workbuddy\2026-07-22\publish_to_flomo.py` | POST webhook 发 flomo |
| 语雀云端发布脚本 | `D:\AI work\workbuddy-daily-note\publish_to_yuque.py` | GitHub Actions 云端运行，遍历 summaries 发语雀（12 次重试/120s 封顶） |
| 博客仓库 | `D:\AI work\daily-note-blog\` | Jekyll 源，push 后 Pages 自动渲染 |
| 语雀源仓库 | `D:\AI work\workbuddy-daily-note\` | 存放 summaries，供 23:59 Actions 发语雀 |
| 安全网(保留) | `C:\Users\Administrator\.hermes\config.yaml.bak-20260721T013122Z` | Hermes 配置改前留底 |

## 四、待办 / 风险

- **语雀 18-21 待最终确认**：7-18~7-21 四篇因语雀 token 限流（连续 429）尚未最终验证成功，待限流窗口恢复后由 23:59 Actions 重试；若仍失败，明早手动 `gh workflow run` 补发。7-22 语雀由 23:59 Actions 发（summaries 已在 23:30 重新加入）。
- **Gridea 仍需手动点"同步"**：GitHub 路径只干掉了"博客"的手动按钮；Gridea Pro（旧路径）仍由本机 23:59:20 任务写稿件，需用户在 Gridea 客户端点同步才实际上线。
- **Ech0说说 + Gridea 本机发布关机则漏**：GitHub 仅覆盖语雀 + 博客两端，这两端未做云端容错（用户暂未要求改）。
- **维护提示**：`publish_daily_summary.py` 改动后，除同步 4 个 agent 副本（memory/rules/memories/skill），还需同步 `D:\AI work\workbuddy\publish_daily_summary.py` 这份自动化专用副本，以及 GitHub 仓库内的同源脚本。
- **WorkBuddy 9 GLM 模型**：models.json 已补齐，需重启桌面端生效（今日早间事项，若尚未重启则仍未生效）。
- **Hermes 未声明匿名卷**：`/opt/data` recreate 时不复用，为缓存数据，丢了通常无害。
