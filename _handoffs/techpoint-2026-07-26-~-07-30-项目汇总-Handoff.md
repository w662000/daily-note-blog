---
layout: default
title: 技术点 · 2026-07-26 ~ 07-30 项目汇总 Handoff
date: 2026-07-29 23:30:00 +0800
---

# 技术点 · 2026-07-26 ~ 07-30 项目汇总 Handoff

> 来源：260729_2026-07-26 ~ 07-30 项目汇总 Handoff_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260729_2026-07-26 ~ 07-30 项目汇总 Handoff_handoff.md（编码探测：utf-8）
- > ⚠️ 本件为「时间轴打包」退化件（多天多项目汇总），按 2026-08-02 裁定 A 预置 bak 以堵幂等缺口，不作项目 handoff 外发。
- | 2 | Hermes WebUI 本地 Docker 两容器部署 | `260721_hermes-webui本地Docker两容器部署_handoff.md` |
- | 4 | Hermes Windows 原生部署迁移 | `260723_Hermes_Windows原生部署迁移_handoff.md` |
- | 6 | 免费 VPS 代理 Wispbyte + gost 跑通 | `260725_免费VPS代理Wispbyte_gost跑通_handoff.md` |
- | 7 | Gaming4Free sing-box 注入部署 | `260726_Gaming4Free_sing-box注入部署_handoff.md` |
- **博客永久链接撞车 BUG 修复**：`daily-note-blog/_config.yml` 的 `dailylog`/`handoffs` 的 `permalink` 由 `/dailylog/:slug/` 改为 `/dailylog/:name/`，解决"所有每日总结共用 slug=daily-summary 互相覆盖"问题。改后 `/dailylog/2026-07-28-daily-summary/` 返回 200、旧撞车地址 404。
- **Gridea Pro 白屏修复**：`config/posts.json` 索引停留在 07-27，未登记 260727/728/729 文章 → 列表白屏。重建索引（26 篇）+ 清理 `EBWebView` 缓存目录后正常。补写 `260728工作总结.md`（published:true）。
- **每日发布拓扑澄清**：自动 4 端（bbs1org 论坛原始日志 / phpBB 论坛原始日志 / 博客 _dailylog / 语雀工作总结）+ 手动 1 端（Gridea 浓缩版需点同步）。对应脚本 `publish_worklog_to_forums.py`、`sync_logs_to_github.py`。
- **7-28 论坛发布缺失补发**：当晚代理 `127.0.0.1:10808` 离线导致自动化被拒未跑，已手动补发（bbs1org topic=21 / phpBB topic=38）。
- 安装包自带 `better-sqlite3` 原生模块 ABI 错配 → GUI 全黑/端口 20128 起不来。最终有效实例：`D:\Program Files\OmniRoute\OmniRoute.exe`（用户桌面双击启动），本地 OpenAI 网关 `http://localhost:20128/v1`。
- 启动脚本 `D:\omniroute\start-omniroute.bat`：设 `DATA_DIR`（**必须无空格路径**，曾有 `D:\AI work\omniroute-data` 触发全新身份 bug）+ 出口代理三变量 + `/D` 显式工作目录。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 安装包自带 `better-sqlite3` 原生模块 ABI 错配 → GUI 全黑/端口 20128 起不来。最终有效实例：`D:\Program Files\OmniRoute\OmniRoute.exe`（用户桌面双击启动），本地 OpenAI 网关 `http://localhost:20128/v1`。
- 启动脚本 `D:\omniroute\start-omniroute.bat`：设 `DATA_DIR`（**必须无空格路径**，曾有 `D:\AI work\omniroute-data` 触发全新身份 bug）+ 出口代理三变量 + `/D` 显式工作目录。
- 数据/配置目录：`C:\Users\Administrator\AppData\Roaming\omniroute\`（`server.env` 存密钥、`storage.sqlite` 存 provider 连接，API key 为 `enc:v1:` 加密）。
- **铁律**：OmniRoute 是 Electron GUI 应用，必须在交互式桌面会话启动；agent/无头 shell 里启动即退出，端口起不来——"启动网关"这一步只能用户双击完成。
