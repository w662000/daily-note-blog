---
layout: default
title: 交接文档 · Hermes Desktop 排障指南
date: 2026-10-13 23:30:00 +0800
---

# Hermes Desktop 排障指南

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\hermes-desktop-troubleshooting\SKILL.md

---
name: hermes-desktop-troubleshooting
category: software-development
description: "Hermes Desktop Windows setup fixes and WebUI alternatives."
version: "1.0.0"
author: "Hermes Agent"
tags: ["hermes", "desktop", "windows", "nodejs", "troubleshooting"]
---

# Hermes Desktop 排障指南

## 🎯 技能概述

本技能提供 Hermes Desktop 应用在 Windows 系统上的常见问题排查和解决方案。基于实际会话中的真实问题记录。

## 📋 常见问题与解决方案

### 问题 1：Node.js 未安装或不在 PATH 中

**症状**：
```
Desktop GUI requires Node.js/npm, but npm was not found on PATH.
```

**解决方案**：
```bash
# 查找已安装的 Node.js
find /c -name "node.exe" 2>/dev/null | head -5

# 常见安装位置
# - /c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/X.X.X/
# - /c/Users/Administrator/.workbuddy/binaries/node/versions/X.X.X/

# 添加到 PATH
export PATH="/c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0:$PATH"

# 验证
node --version
npm --version
```

### 问题 2：npm 版本不兼容

**症状**：
```
npm error code EBADENGINE
npm error engine Not compatible with your version of node/npm
```

**要求**：
- Node.js >= 22.22.0
- npm < 11.10.0 或 >= 11.17.0

**解决方案**：
```bash
# 升级到兼容版本
npm install npm@11.17.0 --global

# 验证
npm --version
```

### 问题 3：缺少 TypeScript 编译器

**症状**：
```
'tsc' is not recognized as an internal or external command
```

**解决方案**：
```bash
# 全局安装 TypeScript
npm install -g typescript

# 或在项目目录安装
cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop
npm install typescript --save-dev
```

### 问题 4：缺少 mermaid 依赖

**症状**：
```
Error: [vite]: Rolldown failed to resolve import "mermaid"
```

**解决方案**：
```bash
cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop
npm install mermaid --legacy-peer-deps
```

### 问题 5：package-lock.json 不同步

**症状**：
```
npm error code EUSAGE
npm error `npm ci` can only install packages when your package.json 
npm error and package-lock.json are in sync.
```

**解决方案**：
```bash
cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop
rm -f package-lock.json
npm install --legacy-peer-deps
```

### 问题 6：Electron 资源忙

**症状**：
```
npm error code EBUSY
npm error syscall rmdir
npm error path node_modules/electron
```

**解决方案**：
```bash
# 关闭所有 Hermes 进程
# 然后重试
hermes desktop --force-build
```

## 🔄 推荐替代方案

如果 Desktop 应用无法成功启动，使用以下替代方案：

### 方案 1：WebUI（推荐）
```bash
# 启动 Web Dashboard
hermes dashboard

# 浏览器访问
# http://localhost:8787/
```

优点：
- 无需构建
- 功能完整
- 稳定可靠

### 方案 2：CLI 模式
```bash
# 经典 CLI
hermes --cli

# 现代 TUI
hermes --tui
```

### 方案 3：使用现有工具
WebUI 已提供完整的工具支持：
- terminal - 终端操作
- file - 文件操作
- code_execution - 代码执行
- browser - 浏览器自动化
- computer_use - 桌面操作

## 📊 快速诊断脚本

```bash
#!/bin/bash
echo "=== Hermes Desktop 诊断 ==="

# Node.js 检查
echo ""
echo "1. Node.js 检查："
if command -v node &> /dev/null; then
    echo "   ✓ Node.js: $(node --version)"
    npm_version=$(npm --version)
    echo "   ✓ npm: $npm_version"
else
    echo "   ✗ Node.js 未安装"
fi

# TypeScript 检查
echo ""
echo "2. TypeScript 检查："
if command -v tsc &> /dev/null; then
    echo "   ✓ tsc: $(tsc --version)"
else
    echo "   ⚠ TypeScript 未安装"
fi

# Desktop 应用检查
echo ""
echo "3. Desktop 应用检查："
desktop_path="/d/hermes-agent/venv/Lib/site-packages/apps/desktop"
if [ -d "$desktop_path" ]; then
    echo "   ✓ Desktop 应用已安装"
else
    echo "   ✗ Desktop 应用未找到"
fi

echo ""
echo "=== 诊断完成 ==="
```

## 📚 相关参考

- `hermes-agent` - Hermes 核心配置和命令
- `hermes-environment-setup` - 环境设置指南
- WebUI 已提供完整功能，无需 Desktop

---
*最后更新：2026-08-05*
*基于真实会话问题解决*
