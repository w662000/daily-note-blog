---
layout: default
title: 每日工作总结 · 2026-07-19
date: 2026-07-19 23:30:00 +0800
---

# 每日工作总结 · 2026-07-19

## 一、今日完成事项
**云南旅居房分析系统（yunnan-housing）一期 MVP 从 0 到全链路跑通**，全天高密度迭代：
1. **项目搭建**：CF Workers（爬虫+API）+ D1(SQLite) + KV(缓存) + CF Pages(Dashboard)，12 个基础文件。
2. **数据源攻坚**：CF Workers 直爬被贝壳/安居客/58 全部封锁 → 改为「本地爬虫(住宅IP) + CF 存储」。诊断后锁定 **58同城**为可用源（解析器针对 58 结构，70 条/页解析率近 100%）。
3. **数据链路打通**：因 workers.dev 国内 POST 被拦截，绕过 HTTP 改用 `wrangler d1 execute` 直连 D1，导入 175 条验证通过；Dashboard 用 Static Assets 直接部署到 Worker。
4. **仪表板增强**：cities 扩到云南 16 城；顶部数据源下拉筛选；"在售房源"可点击展开全部房源列表（含排序/分页/小区名点击）；区级联动 + 小区均价显示。
5. **爬虫工程化**：安全模式（UA 池/随机延迟/500 条上限）、定时任务（schedule_crawler.ps1，默认 22:30）、桌面完成通知（toast）、输入校验修复、PowerShell 变量名大小写陷阱修复。
6. **Cookie 登录墙对抗**：load_cookies 支持 json/txt/env；会话级风控用 Referer 链条 + 撞墙刷新重试 + 早退；cookies.env 自动备份防护。
7. **数据模型修正（重要）**：从"全局去重→580 唯一房源"**纠正为"快照累积"**——房价走势需要同源多行（不同 crawled_at），原 17500+ 快照是真实数据非垃圾；migrate 改为只加列不删数据。衍生贝壳(ke.com)爬虫三件套。

## 二、关键决策 / 注意事项
- **bat 必须纯 ASCII**（中文会 GBK 乱码炸脚本）；PowerShell 带 `[ValidateSet]` 的参数禁止同名（任何大小写）局部变量。
- **workers.dev 国内 POST 被拦截** → 用 wrangler 直连 D1 才是稳路；长期方案绑自定义域名。
- **走势数据 ≠ 重复**：每套房源每次爬到都存一条价格快照，跨次保留。
- 用户本地 `python` 不在 PATH，命令一律用 `.bat` 包装或托管 python 绝对路径。

## 三、生成的有用文件
| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 项目根 | `2026-07-19-09-49-20\yunnan-housing\` | 完整 MVP（wrangler.toml / schema.sql / README.md / src/ / dashboard/） |
| 本地爬虫 | `yunnan-housing\local-crawler\` | crawler.py、backup_to_sql.py、run_daily.bat、check_cookies.bat、notify_complete.ps1 等 |
| 定时任务 | `yunnan-housing\schedule_crawler.ps1` + `install_schedule.bat` | 注册/查看/触发/卸载每日爬取 |
| 种子数据 | `yunnan-housing\patch_cities.sql` + `schema.sql` | 16 城补丁 + 表结构 |
| 备份防护 | `local-crawler\backup_files.bat` | 重要文件一键快照 |

## 四、待办 / 风险
- 用户需浏览器导出 `cookies.env`（58 登录态）爬虫才出数据；IP 被风控时换网络/冷却。
- 呈贡分页器解析局限（实测 557 vs 预估 3500），待修 parse_58_max_page。
- 长期建议绑定自定义域名，彻底绕开 workers.dev POST 拦截。
