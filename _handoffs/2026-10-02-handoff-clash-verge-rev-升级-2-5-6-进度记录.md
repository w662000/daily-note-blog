---
layout: default
title: 交接文档 · Clash Verge Rev 升级 2.5.6 进度记录
date: 2026-10-02 23:30:00 +0800
---

# Clash Verge Rev 升级 2.5.6 进度记录

- **日期**：2026-10-02
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-02-09-38-27\进度_clash_verge_2.5.6.md

- 时间：2026-10-02
- 现象：客户端弹出「2.5.6 已下载，提示安装」，点击「安装」后无任何反应。

## 排查（根因）
- 运行中进程：`clash-verge.exe`、`verge-mihomo.exe`
- Temp 目录仅残留 `Clash Verge-2.5.5-updater-iTnSzk`（上次 2.5.5 的升级缓存），**全盘搜不到任何 2.5.6 安装包** → 结论：UI 假报「已下载」，2.5.6 安装包根本没真下到磁盘，所以点安装拿不到包可跑 → 无反应。
- 系统架构：AMD64（x64）→ 应选 `x64-setup.exe`。

## 修复动作
- 来源：GitHub Releases API（T1 官方源）确认 v2.5.6 资产名
  - `Clash.Verge_2.5.6_x64-setup.exe`（NSIS 安装包）
- 下载：`https://github.com/clash-verge-rev/clash-verge-rev/releases/download/v2.5.6/Clash.Verge_2.5.6_x64-setup.exe`
- 落盘：`C:\Users\Administrator\Downloads\Clash.Verge_2.5.6_x64-setup.exe`（59,572,259 字节 ≈56.8MB）
- 完整性校验：文件头 `MZ` / `PE32 Nullsoft Installer self-extracting archive` ✓
- 安装：先 `Stop-Process` 退旧进程 → 静默 `setup.exe /S` → 退出码 **0**

## 结果
- 已升级到 **2.5.6**（用户肉眼确认），更新提示应不再弹出。
- 安装后 clash-verge 未自动启动（NSIS 默认行为），需手动打开或重启。

## 残留待清理（需用户确认再删，不擅自动）
1. `C:\Users\Administrator\AppData\Local\Temp\Clash Verge-2.5.5-updater-iTnSzk\`（旧升级缓存，约 58MB）
2. `C:\Users\Administrator\Downloads\Clash.Verge_2.5.6_x64-setup.exe`（已装完的安装包，约 56MB）

## 后续（可选）
- 若不想再被更新提示打扰：Clash Verge 设置里关闭「自动检查更新」相关开关（具体文案以界面为准，未擅自改动 UI）。
