---
layout: default
title: 技术点 · 配置
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · 配置

> 来源：261010_配置_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- title: "配置"
- description: "配置 Hermes Agent — config.yaml、providers、模型、API 密钥等"
- ```
~/.hermes/
├── config.yaml     # 设置（模型、终端、TTS、压缩等）
├── .env            # API 密钥和机密
├── auth.json       # OAuth provider 凭据（Nous Portal 等）
├── SOUL.md         # 主要 agent 身份（系统提示词第 #1 槽位）
├── memories/       # 持久记忆（MEMORY.md、USER.md）
├── skills/         # Agent 创建的技能（通过 skill_manage 工具管理）
├── cron/           # 定时任务
├── sessions/       # Gateway 会话
└── logs/           # 日志（errors.log、gateway.log — 机密自动脱敏）
```
- ```
hermes config              # 查看当前配置
hermes config edit         # 在编辑器中打开 config.yaml
hermes config set KEY VAL  # 设置特定值
hermes config check        # 检查缺失选项（更新后使用）
hermes config migrate      # 交互式添加缺失选项

# 示例：
hermes config set model anthropic/claude-opus-4
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...  # 保存到 .env
```
- `hermes config set` 命令会自动将值路由到正确的文件 —— API 密钥保存到 `.env`，其他所有内容保存到 `config.yaml`。
- 2. **`~/.hermes/config.yaml`** —— 所有非机密设置的主配置文件
- 3. **`~/.hermes/.env`** —— 环境变量的回退；机密（API 密钥、token、密码）**必须**放这里
- 4. **内置默认值** —— 未设置任何内容时的硬编码安全默认值
- 机密（API 密钥、bot token、密码）放入 `.env`。其他所有内容（模型、终端后端、压缩设置、内存限制、工具集）放入 `config.yaml`。当两者都设置时，`config.yaml` 对非机密设置优先。
- 可以在 `config.yaml` 中使用 `${VAR_NAME}` 语法引用环境变量：
- ```
auxiliary:
  vision:
    api_key: ${GOOGLE_API_KEY}
    base_url: ${CUSTOM_VISION_URL}

delegation:
  api_key: ${DELEGATION_KEY}
```
- 关于 AI provider 设置（OpenRouter、Anthropic、Copilot、自定义端点、自托管 LLM、回退模型等），请参阅 [AI Providers](../integrations/providers.md)。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
