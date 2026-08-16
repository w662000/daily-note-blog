---
layout: default
title: 技术点 · 2026-07-31 已完成项目 Handoff
date: 2026-07-31 23:30:00 +0800
---

# 技术点 · 2026-07-31 已完成项目 Handoff

> 来源：260731_每日完成项目_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260731_每日完成项目_handoff.md（编码探测：utf-8）
- 1. **跨项目记忆瘦身（方案 B）**：把 `~/.workbuddy/MEMORY.md` 从 26KB／约 2747 token 压到约 16.6KB／1770 token，**每次对话省约 977 token（36%）**。6 条强制红线一字未动，Hermes 端口/路径、服务清单、Gridea 规则全保留；压缩的是已退役的 Docker 史、已修复的 D:\c bug、冗长排障段。顺手修掉一处矛盾：MCP 配置文件统一为 `~/.workbuddy/mcp.json`（**不带点**）。
- 2. **夜间发布任务整体提前 30 分钟**：5 条夜间管道任务 23:xx → 减 30 分钟，相对顺序不变。「每日工作总结生成」一并前移，因为语雀/Gridea 发布依赖它的产出，不移会让发布跑在生成之前。
- 3. **Gridea 从"手动点同步"改为全自动**：过去每天写完浓缩版稿件，还得开 Gridea Pro GUI 手动点同步才上线。本次用 Gridea Pro 自带 MCP（`gridea-pro-mcp.exe`）驱动 `render_site` 渲染，再在 `output/`（本身是 git 仓库，远端 `w662000.github.io`）里 add/commit/push，写成 `gridea_auto_sync.py`。实测两次：首次推 63 个文件成功，第二次仅 sitemap 时间戳变化（与手动同步行为一致，非 bug）。新建「Gridea 自动同步（render+push）」自动化接管。
- `scan`：递归搜最近 5 日的 `YYYY-MM-DD_每日工作总结.md`，提取「今日完成事项」一节，写成 `YYMMDD_每日完成项目_handoff.md` 进收件箱（幂等，已存在则跳过）。
- 7. **审计并修正 Gridea 链路里 3 处过时注释**（`publish_daily_summary.py` / `gridea_auto_sync.py` / `handoff_flow.py`），只改文档不改逻辑，避免以后被"已移除""需手动点同步"这类陈旧说明误导。
- 8. **StepFun 阶跃星辰 14 款模型全量导入**：含多模态推理、文本推理、视觉、图像生成/编辑、语音 TTS/ASR，统一走 `https://api.stepfun.com/v1`，复用现有 Key。
- 10. **NVIDIA NIM 免费层全量盘点 + Tier1 九条落地**：原先只精选了 5 条，本次盘清 NIM 免费层（40 RPM 共享、**无日 token 上限、免信用卡、国内直连**、一个 Key 通吃 100+ 模型），按 Tier1/2/3 分级出清单，用户选「方案 B：Tier1 全量」，写入 9 条并**核实修正 3 个不确定 ID**（`glm-5` → `z-ai/glm-5.2`、`llama-4` → `meta/llama-4-maverick-17b-128e-instruct`、`gpt-oss-120b` → `openai/gpt-oss-120b`）。models.json 49 → **58** 条。
- 12. **models.json 四项优化全做**：vendor 命名统一（Custom → 真实厂商）、按 vendor 排序（国内→路由→国外）、name 加 `[Vendor]` 前缀、step-3.7-flash 两条端点重名做区分。`Custom` 残留归零。
- 13. **模型平台对比文档（三轮修正才定稿）**：`handoff/260731_模型平台对比_handoff.md`。最终口径 = **以实际调用的 Key 和端点归类**，而非模型原始厂商（例如 GLM-5.2 用 SenseNova Key 调，就归商汤；所有走 OpenRouter Key 的统一归 OpenRouter）。
- 14. **WorkBuddy vs Hermes 模型列表结构对比**：查明 WB 的 `models.json` 是**扁平数组**，Hermes 的 `config.yaml` 是 `provider → models` **分层结构**；官方文档确认 WB 模型选择器只展示单一自定义模型组，`vendor` 只是后端路由代号不是 UI 分组键。**结论：改配置文件做不出 Hermes 那种可折叠分组，是 WB 客户端 UI 的固有限制。**
- 17. **StepFun Key「没有权限」实测定位**：Key 完全有效（`/v1/models` 返回 29 个）。真因是 `step-2x-large` 是**图像生成专用模型**，只能走 `/v1/images/generations`；被当聊天模型打到 `/v1/chat/completions` 就返回 404 "no access"，App 显示成"没有权限"。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
