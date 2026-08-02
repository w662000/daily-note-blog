---
layout: default
title: SkillHub 9.8 万技能市场调研与 Cloudflare 部署上线 · 交接文档
date: 2026-08-03 23:30:00 +0800
---

> 来源：项目文档 `2026-08-02-19-29-10\HANDOFF_SkillHub技能市场调研与Cloudflare部署.md`
> 由 handoff_flow.py（scan 阶段）自动收集，标题取自文档 H1（即主要干的活），待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# SkillHub 9.8 万技能市场调研与 Cloudflare 部署上线

## 1. 这个项目是什么
把公开技能社区 **skillhub.cn（约 10.2 万用户创作、免费下载的 AI Skills）** 全站数据抓下来，做成一个**公网可检索的中文 AI 技能大全交互看板**，并配套产出 14 个分类维度的市场调研素材，作为后续「用 AI 赚钱」商业机会设计的数据底座。

## 2. 做了什么 / 关键产出
- **全量数据采集**：`skillhub_all.json`（154 MB，全字段，98,824 个去重 skill，12 个一级分类；最多 ai-agent 16,102、dev-programming 12,286）。前端精简版 `skillhub_min.js`（window.SKILLS）。
- **市场调研**：14 个分类调研文档 `skillhub_*.md`（knowledge-management / dev-programming / it-ops-security / data-analysis / content-creation / design-media / business-ops / education / office-efficiency / professional / life-service / ai-agent 等），覆盖安装量、头部技能、可商业化切口。
- **公网部署（已完成上线）**：复用 slg-china 的 Pages + D1 + Functions 模式。
  - 生产站：**https://skillhub-cn.pages.dev**
  - 架构：静态前端 `public/index.html` + `functions/api/skills.js`（分页/分类/搜索/排序）+ `functions/api/stats.js`；数据库 Cloudflare D1 `skillhub-db`（APAC 区，绑定名 `DB`）。
  - 配置：`wrangler.toml`（`pages_build_output_dir="public"` + `[[d1_databases]]`）。
- **发布方案文档**：`skillhub_pages_d1_plan.md`（从本地单文件看板演进到 Pages+D1 的完整方案，含 schema.sql）。

## 3. 验证（curl 实测，全 200）
| 检查项 | 结果 |
|---|---|
| 首页 HTTP | 200 ✅ |
| /api/stats（total/verified/分类计数） | 200，total=98824 ✅ |
| /api/skills（分页） | 200，返回真实 items ✅ |
| /api/skills?category=ai-agent&sort=stars | 200，按星排序正确 ✅ |
| /api/skills?q=PPT（搜索） | 200，关键词命中 ✅ |

> 注：首访 `/api/skills` 偶发 522（Pages Function 冷启动），重试即 200，属正常冷启动，非故障。

## 4. 可复用技术点（后续灌库必看）
- wrangler `d1 execute --file` 大文件会被当单条语句 → `SQLITE_TOOBIG`；改用 **D1 REST API `{"batch":[...]}` 分批提交**。
- D1 单条 SQL 硬上限 = **100,000 字节**；按字节切分（<80KB/条）。
- `INSERT OR IGNORE` 幂等 + `import.ckpt` 断点续传。

## 5. 如何继续
- 把 skillhub-cn.pages.dev 定位为**免费流量入口**（不自身营收），在各商业落地页加「更多 AI 工具测评」交叉引流。
- 如需迭代：前端加「为我推荐 / 对比 / 收藏 / 提交技能」；后端可接 FTS5 全文检索（schema 已预留）。
- 源数据 `skillhub_all.json` 154MB 在本会话根目录，灌库脚本与断点文件 `import.ckpt` 在 skillhub-cf/。

## 6. 合规要点（贯穿后续商业项目）
- skillhub 是**用户创作、免费下载**社区站；商业化只做「索引 / 评论 / 推荐 + 跳转链接」与「基于技能思路自建自有产品」，**不转售他人 skill 文件**（侵犯创作者权益 + 违反平台 ToS）。
- 含「微信小程序 AI 开发专区·官方出品」，内容敏感度更高，转售/SEO 重写搬运即越界。

