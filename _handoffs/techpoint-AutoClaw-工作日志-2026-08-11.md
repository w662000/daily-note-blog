---
layout: default
title: 技术点 · AutoClaw 工作日志 · 2026-08-11
date: 2026-08-12 23:30:00 +0800
---

# 技术点 · AutoClaw 工作日志 · 2026-08-11

> 来源：260812_autoclaw-工作日志-2026-08-11_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260812_autoclaw-工作日志-2026-08-11_handoff.md（编码探测：utf-8）
- 用户提供了有道云笔记 MCP API Key，完成全套接入：
- **API Key**：已写入 `C:\Users\Administrator\.youdaonote.json`（backend=mcp, server=https://open.mail.163.com/api/ynote/mcp/sse）。Key 值不要写入任何文件。
- **用法**：所有命令带 `-s ydn`；保存 Markdown 用 `save`（禁止用 create）；剪藏用 `clip URL`
- web_search 接口当天不可用（broker_unauthorized），改用 autoglm-open-link + 百度/官网页面拿信息，可行
- open-link 脚本在 PowerShell 下需 `$env:PYTHONIOENCODING="utf-8"` 否则 GBK 编码报错
- gateway 进程 PATH 是旧的：新装 CLI 要让 skill 可用，需在已存在 PATH 目录放包装器（.local\bin）
- **youdaonote MCP 服务端偶发 "Session not found"（HTTP 404）**：瞬时会话过期，重试即可，不是配置问题；批量操作时建议分小批执行
- 笔记库结构（归档后）：我的资源/收藏笔记 下 7 个分类文件夹（Hermes相关5 / 免费资源7 / AI工具5 / 股票2 / Obsidian工作流4 / 部署教程3 / 其他2），已办结 1 篇（MemOS）未动
- 用户明确不走 Docker，在 WSL Ubuntu 24.04 直接部署 TradingAgents-CN（main 分支 v1.1.0，源码 ~/TradingAgents-CN）
- systemd 服务：tacn-backend / tacn-worker / tacn-frontend（开机自启+崩溃重启）
- 踩坑记录：

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
- 用户明确不走 Docker，在 WSL Ubuntu 24.04 直接部署 TradingAgents-CN（main 分支 v1.1.0，源码 ~/TradingAgents-CN）
- 组件：MongoDB 8.0.28（apt，无认证）+ Redis（apt）+ Python 3.12 venv（pip install -e .，阿里云源）+ 后端 uvicorn:8000 + worker analysis_worker + 前端 Vite:3000（node18/npm9，npmmirror 源）
- systemd 服务：tacn-backend / tacn-worker / tacn-frontend（开机自启+崩溃重启）
- 账号：admin/admin123（写入 tradingagentscn_v0_root.users；create_default_admin.py 默认写 tradingagentscn 库，需手动复制用户）
- 踩坑记录：
  - WSL2 中 redis.asyncio + socket_keepalive_options 报 Error 22 EINVAL → 已从 app/core/redis_client.py 移除该参数
  - create_default_admin.py 硬编码带认证 MONGO_URI + DB_NAME=tradingagentscn，与后端实际库 tradingagentscn_v0_root 不一致 → 改 URI 后 mongosh 复制用户
  - PowerShell 写 shell 脚本带 CRLF 导致 systemd unit 无效 → tr -d '\r' 修复
  - WSL2 localhost 转发失效：Windows 访问需用 WSL IP 172.29.46.12（或管理员 netsh portproxy；IP 重启会变）
  - PyPI 官方源慢 → 阿里云镜像 mirrors.aliyun.com/pypi/simple；apt 锁被 unattended-upgrades 占用 → systemctl stop 后 rm 锁
- 剩余：用户提供 LLM API Key（DeepSeek/百炼/火山等）后配置模型才能真正分析；之后接 schedule-tradingagents skill（quark 网盘下载）+ OpenClaw cron 自动化
