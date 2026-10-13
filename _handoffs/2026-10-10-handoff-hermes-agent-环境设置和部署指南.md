---
layout: default
title: 交接文档 · Hermes Agent 环境设置和部署指南
date: 2026-10-13 23:30:00 +0800
---

# Hermes Agent 环境设置和部署指南

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\hermes-environment-setup\SKILL.md

---
name: hermes-environment-setup
category: software-development
description: "Hermes Agent环境设置和部署指南，包括终端环境配置、技能安装、故障排除和最佳实践"
version: "1.1.0"
author: "Hermes Agent"
tags: ["hermes", "setup", "environment", "terminal", "deployment"]
---

# Hermes Agent 环境设置和部署指南

## 🎯 技能概述

本技能提供Hermes Agent的完整环境设置指南，包括终端环境配置、技能安装、故障排除和最佳实践。基于实际用户需求和学习路径，提供详细的操作指南。

## 📋 核心功能

### 环境验证
- 终端环境检测（Git Bash, WSL, PowerShell）
- Python环境验证
- 网络连接测试
- 依赖项检查

### 技能安装
- 内置技能管理
- 第三方技能安装
- 技能配置和验证
- 批量技能部署

### 故障排除
- 终端环境问题解决
- 技能安装失败处理
- 网络连接问题
- 权限和配置问题

### 最佳实践
- 环境优化建议
- 技能组合推荐
- 工作流程优化
- 性能调优

## 🚀 快速开始

### 步骤1：验证环境
```bash
# 检查Git Bash环境
git --version
which bash
uname -a

# 检查Python环境
python --version
pip --version

# 检查Hermes安装
hermes --version
```

### 步骤2：安装Hermes Agent
```bash
# 方法1：使用shell安装程序
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 方法2：通过PyPI安装
pip install hermes-agent

# 方法3：使用uv安装
uv pip install hermes-agent
```

### 步骤3：验证安装
```bash
# 检查Hermes状态
hermes status

# 列出已安装技能
hermes skills list

# 检查工具集
hermes tools list
```

## 🔧 终端环境配置

### Git Bash 环境
```bash
# 验证Git Bash环境
echo "Git Bash环境检查："
git --version
echo "Bash路径：$(which bash)"
echo "系统信息：$(uname -a)"

# 检查Python环境
echo "Python环境检查："
python --version
python -c "import sys; print(f'Python路径: {sys.executable}')"

# 检查Hermes环境
echo "Hermes环境检查："
hermes --version 2>/dev/null || echo "Hermes未安装"
```

### WSL 环境
```bash
# 检查WSL状态
echo "WSL环境检查："
wsl --list --verbose

# 测试WSL功能
wsl -d Ubuntu -- echo "WSL测试成功"

# 检查WSL中的Python
wsl -d Ubuntu -- python3 --version
```

### PowerShell 环境
```powershell
# 检查PowerShell版本
$PSVersionTable.PSVersion

# 检查Git安装
Get-Command git -ErrorAction SilentlyContinue

# 检查Chocolatey（如果安装）
Get-Command choco -ErrorAction SilentlyContinue
```

## 🖥️ Hermes Desktop 应用配置

### Desktop 应用概述

**Hermes Desktop 是官方原生 Electron 应用**，提供：
- 流式响应聊天界面
- 并排文件预览
- 内置文件浏览器
- 语音支持
- 自动更新功能

**版本**: v0.17.0
**要求**: Node.js >= 22.22.0, npm < 11.10.0 或 >= 11.17.0

### Windows Node.js 配置

```bash
# 查找已安装的 Node.js
find /c -name "node.exe" 2>/dev/null | head -5

# 常见路径
# - /c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0/
# - /c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2/

# 添加到 PATH
export PATH="/c/Users/Administrator/.meituan-catpaw/runtimes/node/versions/24.18.0:$PATH"

# 验证版本
node --version  # 应该 >= 22.22.0
npm --version   # 应该 < 11.10.0 或 >= 11.17.0
```

### Desktop 启动命令

```bash
# 启动 Desktop（需要 Node.js 和 npm 正确配置）
hermes desktop

# 如果构建失败，使用替代方案
hermes dashboard    # Web UI（推荐）
hermes --cli        # 经典命令行界面
hermes --tui        # 现代 TUI 界面
```

### Desktop 依赖问题排查

如果 `hermes desktop` 启动失败：

```bash
# 1. 检查依赖
cd /d/hermes-agent/venv/Lib/site-packages/apps/desktop

# 2. 重新安装依赖
npm install --legacy-peer-deps

# 3. 如果缺少 mermaid
npm install mermaid --legacy-peer-deps

# 4. 如果 lock 文件不同步
rm -f package-lock.json
npm install --legacy-peer-deps

# 5. 强制重新构建
hermes desktop --force-build
```

### WebUI 作为替代方案

**WebUI 提供与 Desktop 相同的核心功能**，是 Windows 上的推荐方案：

```bash
# 启动 Web Dashboard
hermes dashboard

# 浏览器访问
# http://localhost:8787/
```

WebUI 功能：
- ✅ 所有 Hermes 核心功能
- ✅ 完整技能系统
- ✅ 命令行工具（terminal, file, code_execution）
- ✅ 浏览器自动化
- ✅ 计算机控制（computer_use）

## ⚠️ Windows终端兼容性注意事项

### Git Bash 环境问题

在 Git Bash (MINGW64) 环境中运行 Hermes 时，可能会遇到终端兼容性问题：

**错误示例**：
```
prompt_toolkit.output.win32.NoConsoleScreenBufferError: Found xterm-256color, while expecting a Windows console.
```

**原因**：
- Git Bash 检测到 xterm-256color 终端环境
- Hermes 期望 Windows 控制台环境
- Python 的 prompt_toolkit 库不兼容 Git Bash

**解决方案**：

1. **方案A：使用 Windows Terminal 或 PowerShell（推荐）**
   ```bash
   # 使用 PowerShell
   powershell -Command "hermes -s test-driven-development"
   
   # 或使用 Windows Terminal
   # 直接在 Windows Terminal 中运行 hermes
   ```

2. **方案B：使用 Web UI（推荐，无终端问题）**
   ```bash
   # 启动 Web UI
   hermes dashboard
   
   # 然后在浏览器中访问
   # http://localhost:8787/
   ```

3. **方案C：直接在项目目录使用（如果项目有特殊配置）**
   ```bash
   cd "D:\AI work\workbuddy"
   hermes -s test-driven-development
   ```

4. **方案D：使用 winpty 包装（不推荐，有兼容性问题）**
   ```bash
   winpty hermes -s test-driven-development
   ```

### 持久化解决方案

如果 Git Bash 是必需的，可以在 `~/.bashrc` 中添加别名：

```bash
# 在 ~/.bashrc 中添加
alias hermes='powershell -Command "hermes"'
```

这样可以保持 Git Bash 的使用习惯，同时解决兼容性问题。

## 📚 技能安装指南

### 必装技能列表
```bash
# 安装核心开发技能
hermes skills install test-driven-development
hermes skills install architecture-diagram
hermes skills install github-pr-workflow
hermes skills install systematic-debugging

# 安装数据科学技能
hermes skills install jupyter-live-kernel
hermes skills install huggingface-hub

# 安装生产力技能
hermes skills install obsidian
hermes skills install notion
```

### 第三方技能安装
```bash
# 安装superpowers技能
hermes skills install superpowers-lab
hermes skills install superpowers-brainstorming

# 安装Grill Me技能
hermes skills install skills-sh/mattpocock/skills/grill-me
hermes skills install skills-sh/vinvcn/mattpocock-skills-zh-cn/grill-me
```

### 技能配置
```bash
# 创建技能配置目录
mkdir -p ~/.hermes/skills/{test-driven-development,architecture-diagram}/config

# 创建TDD配置
cat > ~/.hermes/skills/test-driven-development/config/settings.yaml << EOF
features:
  strict_tdd: true
  test_first: true
  refactoring_support: true
  coverage_tracking: true
EOF

# 创建架构图配置
cat > ~/.hermes/skills/architecture-diagram/config/settings.yaml << EOF
diagram_style:
  theme: "dark"
  components: "modern"
  layout: "auto"
export_format: "html"
EOF
```

## 🔍 故障排除

### 常见问题1：终端环境问题
```bash
# 问题：命令不存在
# 解决方案：
echo "检查PATH环境变量："
echo $PATH | grep -E "(git|python|hermes)"

# 修复PATH
export PATH="$PATH:/usr/bin:/usr/local/bin"

# 检查命令可用性
which hermes || echo "Hermes未找到"
which python || echo "Python未找到"
```

### 常见问题2：技能安装失败
```bash
# 问题：安装被取消
# 解决方案：
echo "y" | hermes skills install <skill-name>

# 或者手动安装
git clone <skill-repo>
cp -r <skill-dir> ~/.hermes/skills/

# 验证安装
hermes skills list | grep <skill-name>
```

### 常见问题3：网络连接问题
```bash
# 测试网络连接
curl -I https://github.com
curl -I https://api.github.com

# 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 设置代理（如果需要）
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### 常见问题4：权限问题
```bash
# 检查权限
ls -la ~/.hermes/

chmod -R 755 ~/.hermes/

# 检查技能目录权限
ls -la ~/.hermes/skills/

chmod -R 755 ~/.hermes/skills/
```

## 📊 环境检查脚本

### 完整环境检查
```bash
#!/bin/bash
# 环境检查脚本

echo "=== Hermes Agent 环境检查 ==="
echo

# 检查基础环境
echo "1. 基础环境检查："
echo "   Git版本：$(git --version 2>/dev/null || echo '未安装')"
echo "   Bash路径：$(which bash 2>/dev/null || echo '未找到')"
echo "   系统信息：$(uname -a 2>/dev/null || echo '未知')"
echo

# 检查Python环境
echo "2. Python环境检查："
python --version 2>/dev/null || echo "   Python未安装"
pip --version 2>/dev/null || echo "   pip未安装"
echo

# 检查Hermes环境
echo "3. Hermes环境检查："
if command -v hermes &> /dev/null; then
    echo "   Hermes已安装：$(hermes --version 2>/dev/null || echo '版本未知')"
    echo "   Hermes配置：$(hermes config path 2>/dev/null || echo '路径未知')"
    echo "   已安装技能数量：$(hermes skills list 2>/dev/null | grep -c '│' || echo '未知')"
else
    echo "   Hermes未安装"
fi
echo

# 检查网络连接
echo "4. 网络连接检查："
if curl -I https://github.com &> /dev/null; then
    echo "   GitHub连接正常"
else
    echo "   GitHub连接失败"
fi
echo

# 检查WSL环境
echo "5. WSL环境检查："
if wsl --list &> /dev/null; then
    echo "   WSL已安装"
    wsl -d Ubuntu -- echo "   Ubuntu WSL正常" 2>/dev/null || echo "   Ubuntu WSL不可用"
else
    echo "   WSL未安装"
fi
echo

echo "=== 环境检查完成 ==="
```

## 🎯 最佳实践

### 环境优化建议
```bash
# 创建环境配置文件
cat > ~/.bashrc << 'EOF'
# Hermes Agent 环境配置
export PATH="$PATH:$HOME/.local/bin"
export PYTHONPATH="$PYTHONPATH:$HOME/.hermes"
export HERMES_CONFIG="$HOME/.hermes/config.yaml"

# 别名设置
alias hs='hermes skills'
alias ht='hermes tools'
alias hc='hermes config'
alias hsetup='hermes setup'
EOF
```

### 技能组合推荐
```bash
# 开发环境组合
echo "开发环境组合："
echo "1. test-driven-development + systematic-debugging"
echo "2. architecture-diagram + github-pr-workflow"
echo "3. jupyter-live-kernel + huggingface-hub"

# 数据科学环境组合
echo "数据科学环境组合："
echo "1. jupyter-live-kernel + huggingface-hub"
echo "2. arxiv + llm-wiki"
echo "3. obsidian + notion"

# 生产力环境组合
echo "生产力环境组合："
echo "1. obsidian + notion"
echo "2. airtable + google-workspace"
echo "3. teams-meeting-pipeline + powerpoint"
```

### 工作流程优化
```bash
# 创建工作流脚本
cat > ~/hermes-workflow.sh << 'EOF'
#!/bin/bash
# Hermes Agent 工作流

echo "启动Hermes Agent..."
hermes -s test-driven-development

echo "技能已加载，可以开始TDD开发"
EOF

chmod +x ~/hermes-workflow.sh
```

## 📈 学习路径

### 初学者路径（1-2周）
1. **环境设置**（1-2天）
   - 安装Hermes Agent
   - 配置终端环境
   - 验证安装

2. **基础技能**（3-5天）
   - test-driven-development
   - architecture-diagram
   - github-pr-workflow

3. **进阶技能**（1-2周）
   - systematic-debugging
   - jupyter-live-kernel
   - obsidian

### 中级用户路径（1-2个月）
1. **技能组合**（1-2周）
   - 学习技能组合使用
   - 创建自定义工作流
   - 优化配置

2. **第三方技能**（2-3周）
   - 安装superpowers
   - 安装Grill Me
   - 集成到工作流

3. **高级配置**（1-2周）
   - 自定义配置
   - 性能优化
   - 团队协作

## 🔥 常见问题解决

### 问题1：Hermes命令不存在
```bash
# 重新安装Hermes
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 或通过PyPI安装
pip install hermes-agent

# 验证安装
hermes --version
```

### 问题2：技能安装失败
```bash
# 方法1：使用echo确认安装
echo "y" | hermes skills install <skill-name>

# 方法2：手动安装
git clone <skill-repo>
cp -r <skill-dir> ~/.hermes/skills/

# 方法3：检查网络和权限
curl -I https://github.com
chmod -R 755 ~/.hermes/
```

### 问题3：终端环境问题
```bash
# 检查终端类型
echo $SHELL
echo $TERM

# 确保在Git Bash中运行
if [[ "$OSTYPE" == "msys" ]]; then
    echo "当前在Git Bash环境中"
else
    echo "请在Git Bash终端中运行"
fi
```

## 🎯 总结

本技能提供了Hermes Agent的完整环境设置指南，包括：

- **环境验证**: 检查Git Bash、Python、Hermes环境
- **技能安装**: 内置和第三方技能安装方法
- **故障排除**: 常见问题的解决方案
- **最佳实践**: 环境优化和工作流程建议
- **学习路径**: 从初学者到高级用户的进阶路径

**重要提示**：在 Git Bash 环境中使用 Hermes 时，请使用 PowerShell 或 Windows Terminal 来避免终端兼容性问题。

---

## 🔒 Gateway Token 修复

**症状**：AutoClaw UI 报错 `Connection closed: 1008 unauthorized: gateway token mismatch`

**原因**：`.hermes-web-ui/.token` 与 `.hermes/.env` 中的 `HERMES_DASHBOARD_SESSION_TOKEN` 不一致

**排查步骤**：
```bash
# 1. 查看 Gateway token（.env 文件中）
grep HERMES_DASHBOARD_SESSION_TOKEN ~/.hermes/.env

# 2. 查看 AutoClaw UI token
cat ~/.hermes-web-ui/.token

# 3. 对比是否一致
```

**修复**：
```bash
# 同步 token（用 .env 中的值覆盖 .token）
TOKEN=$(grep HERMES_DASHBOARD_SESSION_TOKEN ~/.hermes/.env | cut -d= -f2)
echo "$TOKEN" > ~/.hermes-web-ui/.token
```

**注意**：Gateway token 可能因重启/更新而变化，如果修复后再次出现 token mismatch，需要重新同步。

---

*最后更新：2026年7月*
*版本：1.1.0*
