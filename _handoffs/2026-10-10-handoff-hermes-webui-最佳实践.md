---
layout: default
title: 交接文档 · Hermes WebUI 最佳实践
date: 2026-10-13 23:30:00 +0800
---

# Hermes WebUI 最佳实践

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\user-operational-guidelines\references\hermes-webui-best-practices.md

## 🎯 技能概述

本文档记录了 Hermes WebUI 使用的最佳实践，基于实际会话中的经验总结。

## 📋 WebUI 优先原则

### 为什么优先使用 WebUI

1. **零配置启动**: WebUI 无需构建，立即可用
2. **功能完整**: 提供所有 Hermes 核心功能
3. **稳定可靠**: 避免了 Desktop 构建的复杂性
4. **跨平台**: 在浏览器中运行，不受 OS 限制

### WebUI 访问方式

```bash
# 启动 Web Dashboard
hermes dashboard

# 浏览器访问
# http://localhost:8787/
```

## 🛠️ WebUI 工具使用

### 核心工具集

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `terminal` | 执行 shell 命令 | 系统操作、文件管理 |
| `file` | 文件读写搜索 | 代码编辑、配置修改 |
| `code_execution` | Python 代码执行 | 数据分析、脚本运行 |
| `browser` | 浏览器自动化 | 网页操作、爬虫 |
| `vision` | 图像分析 | 图片理解、OCR |
| `computer_use` | 桌面操作 | Windows GUI 控制 |

### 常用命令示例

```bash
# 查看 Hermes 版本
hermes --version

# 列出工具
hermes tools list

# 查看技能
hermes skills list

# 查看配置
hermes config
```

## 📝 命令行操作模式

### 在 WebUI 中使用 terminal

```bash
# 基本命令
terminal(command="ls -la")
terminal(command="pwd")
terminal(command="git status")

# 后台运行
terminal(command="long-running-task", background=true, notify_on_complete=true)

# 带工作目录
terminal(command="npm install", workdir="/path/to/project")
```

### 使用 code_execution

```bash
# 执行 Python 代码
execute_code(code="import os; print(os.getcwd())")

# 复杂脚本
execute_code(code="""
import requests
response = requests.get('https://api.github.com')
print(f'Status: {response.status_code}')
""")
```

## ⚠️ 常见问题与解决方案

### 问题 1：命令不识别

**症状**: `command not found`

**解决**:
```bash
# 检查 PATH
echo $PATH

# 重新加载配置
hermes config reload
```

### 问题 2：权限问题

**症状**: `Permission denied`

**解决**:
```bash
# 检查文件权限
ls -la /path/to/file

# 修改权限（如需要）
chmod +x /path/to/script
```

### 问题 3：Node.js 路径问题

**症状**: `npm not found`

**解决**:
```bash
# 添加 Node.js 到 PATH
export PATH="/c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0:$PATH"
```

## 📊 工作流程建议

### 日常使用流程

1. **启动 WebUI**
   ```bash
   hermes dashboard
   ```

2. **检查状态**
   ```bash
   hermes status
   hermes tools list
   hermes skills list
   ```

3. **执行任务**
   - 使用 terminal 进行系统操作
   - 使用 code_execution 运行 Python
   - 使用 file 工具编辑文件

### 技能加载流程

```bash
# 查看可用技能
hermes skills list

# 加载特定技能
hermes -s test-driven-development

# 加载多个技能
hermes -s skill1,skill2,skill3
```

## 🎓 学习建议

### 新手路径

1. **熟悉 WebUI 界面**
   - 了解工具面板
   - 学习斜杠命令
   - 掌握基本操作

2. **学习核心技能**
   - terminal 工具使用
   - file 工具操作
   - code_execution 脚本编写

3. **进阶技能**
   - browser 自动化
   - computer_use 桌面控制
   - 多代理协作

## 📚 相关资源

- [Hermes 官方文档](https://hermes-agent.nousresearch.com/docs/)
- [CLI 命令参考](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
- [斜杠命令参考](https://hermes-agent.nousresearch.com/docs/reference/slash-commands)
- [工具参考](https://hermes-agent.nousresearch.com/docs/reference/tools-reference)

---
*最后更新：2026-08-05*
*基于实际 WebUI 使用经验*
