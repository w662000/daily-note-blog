---
layout: default
title: 交接文档 · Web UI 升级注意事项
date: 2026-10-13 23:30:00 +0800
---

# Web UI 升级注意事项

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\user-operational-guidelines\references\web-ui-upgrade-notes.md

## 核心原则

### 1. 先确认对象
"升级" 可能指：
- 核心 Hermes Agent
- Web UI 外壳（`hermes-web-ui`）
- Desktop 壳层
- 其他插件/扩展

**禁止默认按升级 agent 处理。**

### 2. 先搜索再执行
执行任何升级前：
1. 确认目标项目名称和版本
2. 确认来源（GitHub release、npm package 等）
3. 确认本地当前版本
4. 确认升级路径和步骤

### 3. 拿不准就停
如果无法确认：
- 项目来源
- 版本号
- 升级命令
- 回滚方案

**必须停下来询问用户，不要猜测执行。**

## 已知事实

### Hermes Agent 版本
- 本机版本：**v0.20.0 (2026.8.3)**
- 安装位置：`D:\hermes-agent\venv\Lib\site-packages`
- 非 git 仓库，无法通过 git 确认版本

### Web UI 源码位置
- `D:\hermes-agent\web\`：前端源码
- `D:\hermes-agent\hermes_cli/web_dist/`：构建输出
- 测试文件：`D:\hermes-agent\venv\Lib\site-packages\tests\hermes_cli\test_web_ui_build.py`

### Web UI 版本特征
- `web/package.json` 中版本为 `0.0.0`，不代表实际发布版本
- 实际版本可能在 `hermes_cli/__init__.py` 中：`__release_date__ = "2026.7.7.2"`
- web UI 的构建输出服务于 dashboard，端口 9119

### 已知问题
- **`0.6.39` 来源未确认**：当前未找到 hermes-web-ui 0.6.39 的官方来源或对应关系
- 本机 `web/package.json` 使用 `@nous-research/ui: 0.18.2`
- 内置 web UI 与 hermes-web-ui 是否是同一个项目尚未确认

## 升级前检查清单

- [ ] 明确目标：升级的是 agent、web UI 还是 desktop？
- [ ] 确认版本：当前版本和期望版本
- [ ] 确认来源：GitHub release、npm、pip 还是其他？
- [ ] 确认路径：正确安装位置和构建目录
- [ ] 回滚方案：升级失败如何恢复
- [ ] 影响评估：是否需要停止服务、重建容器、重启进程

## 常见误解

### 误解 1：hermes desktop = web UI
- Desktop 是 Electron 壳层
- Web UI 是浏览器界面
- 两者共享同一后端，但前端独立

### 误解 2：web/package.json 版本 = 发布版本
- `0.0.0` 通常是开发占位符
- 实际版本在构建时确定
- 发布版本号在 Hermes Agent 主包中

### 误解 3：升级 web UI 等同于升级 agent
- Web UI 可能随 agent 一起升级
- 也可能独立升级
- 需要看具体发布说明

## 正确工作流程

```bash
# 1. 确认当前状态
hermes --version
cat D:/hermes-agent/web/package.json | grep version

# 2. 确认目标
# 询问用户：升级的是什么？版本号？来源？

# 3. 验证来源
# 检查 GitHub releases、npm registry、pip 等

# 4. 执行升级
# 按官方文档执行

# 5. 验证结果
# 启动服务，测试功能
```

## 相关文档
- `hermes-desktop-setup/SKILL.md`：Desktop 应用安装和故障排除
- `hermes-environment-setup/SKILL.md`：Hermes Agent 环境设置
