---
layout: default
title: 技术点 · SkillHub 9.8 万技能市场调研与 Cloudflare 部署上线
date: 2026-08-02 23:30:00 +0800
---

# 技术点 · SkillHub 9.8 万技能市场调研与 Cloudflare 部署上线

> 来源：260802_SkillHub 9.8 万技能市场调研与 Cloudflare 部署上线_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260802_SkillHub 9.8 万技能市场调研与 Cloudflare 部署上线_handoff.md（编码探测：utf-8）
- > 来源：项目文档 `2026-08-02-19-29-10\HANDOFF_SkillHub技能市场调研与Cloudflare部署.md`
- **公网部署（已完成上线）**：复用 slg-china 的 Pages + D1 + Functions 模式。
- 架构：静态前端 `public/index.html` + `functions/api/skills.js`（分页/分类/搜索/排序）+ `functions/api/stats.js`；数据库 Cloudflare D1 `skillhub-db`（APAC 区，绑定名 `DB`）。
- 配置：`wrangler.toml`（`pages_build_output_dir="public"` + `[[d1_databases]]`）。
- **发布方案文档**：`skillhub_pages_d1_plan.md`（从本地单文件看板演进到 Pages+D1 的完整方案，含 schema.sql）。
- | /api/stats（total/verified/分类计数） | 200，total=98824 ✅ |
- | /api/skills（分页） | 200，返回真实 items ✅ |
- | /api/skills?category=ai-agent&sort=stars | 200，按星排序正确 ✅ |
- | /api/skills?q=PPT（搜索） | 200，关键词命中 ✅ |
- > 注：首访 `/api/skills` 偶发 522（Pages Function 冷启动），重试即 200，属正常冷启动，非故障。
- wrangler `d1 execute --file` 大文件会被当单条语句 → `SQLITE_TOOBIG`；改用 **D1 REST API `{"batch":[...]}` 分批提交**。

## 三、关键产物与命令
- **全量数据采集**：`skillhub_all.json`（154 MB，全字段，98,824 个去重 skill，12 个一级分类；最多 ai-agent 16,102、dev-programming 12,286）。前端精简版 `skillhub_min.js`（window.SKILLS）。
- **市场调研**：14 个分类调研文档 `skillhub_*.md`（knowledge-management / dev-programming / it-ops-security / data-analysis / content-creation / design-media / business-ops / education / office-efficiency / professional / life-service / ai-agent 等），覆盖安装量、头部技能、可商业化切口。
- **公网部署（已完成上线）**：复用 slg-china 的 Pages + D1 + Functions 模式。
  - 生产站：**https://skillhub-cn.pages.dev**
  - 架构：静态前端 `public/index.html` + `functions/api/skills.js`（分页/分类/搜索/排序）+ `functions/api/stats.js`；数据库 Cloudflare D1 `skillhub-db`（APAC 区，绑定名 `DB`）。
  - 配置：`wrangler.toml`（`pages_build_output_dir="public"` + `[[d1_databases]]`）。
- **发布方案文档**：`skillhub_pages_d1_plan.md`（从本地单文件看板演进到 Pages+D1 的完整方案，含 schema.sql）。

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
