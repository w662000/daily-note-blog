---
layout: default
title: 技术点 · 扩展 Dashboard
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · 扩展 Dashboard

> 来源：261010_扩展 Dashboard_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "为 Hermes Web Dashboard 构建主题和插件——调色板、字体排版、布局、自定义标签页、shell 插槽、页面级插槽以及后端 API 路由"
- 3. **后端插件（Backend plugins）** — 插件目录内的 Python 文件，暴露一个 FastAPI `router`；路由挂载在 `/api/plugins/<name>/` 下，由插件的 UI 调用。
- 主题和插件相互独立，但可协同工作。主题可以单独使用（仅一个 YAML 文件）。插件也可以单独使用（仅一个标签页）。两者结合可构建带有自定义 HUD 的完整视觉换肤方案——内置的 `strike-freedom-cockpit` 演示正是如此。参见[主题 + 插件组合演示](#combined-theme--plugin-demo)。
- [后端 API 路由](#backend-api-routes)
- [API 参考](#api-reference)
- [故障排查](#troubleshooting)
- 主题是存储在 `~/.hermes/dashboard-themes/` 中的 YAML 文件。文件名无关紧要（系统使用主题的 `name:` 字段），但惯例是 `<name>.yaml`。所有字段均为可选——缺失的键会回退到内置的 `default` 主题，因此一个主题可以只包含一个颜色。
- ```
mkdir -p ~/.hermes/dashboard-themes
```
- ```
# ~/.hermes/dashboard-themes/neon.yaml
name: neon
label: Neon
description: Pure magenta on black

palette:
  background: "#000000"
  midground: "#ff00ff"
```
- 这就是全部入门流程：一个文件，两个颜色。以下内容均为可选的进阶配置。
- 调色板由三层颜色加一个暖光晕（warm-glow）颜色和一个噪点颗粒倍增器组成。Dashboard 的设计系统级联通过 CSS `color-mix()` 从这三层颜色派生出所有兼容 shadcn 的 token（card、popover、muted、border、primary、destructive、ring 等）。覆盖三个颜色即可级联影响整个 UI。
- ```
palette:
  background:
    hex: "#05091a"
    alpha: 1.0
  midground: "#d8f0ff"          # bare hex, alpha = 1.0
  foreground:
    hex: "#ffffff"
    alpha: 0                    # invisible top layer
  warmGlow: "rgba(255, 199, 55, 0.24)"
  noiseOpacity: 0.7
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
