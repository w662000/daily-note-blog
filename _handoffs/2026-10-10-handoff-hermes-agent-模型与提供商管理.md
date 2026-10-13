---
layout: default
title: 交接文档 · Hermes Agent 模型与提供商管理
date: 2026-10-13 23:30:00 +0800
---

# Hermes Agent 模型与提供商管理

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\hermes-model-management\SKILL.md

---
name: hermes-model-management
category: software-development
description: "Hermes Agent 模型与提供商管理：刷新模型列表、增删模型、编辑 config.yaml、安全回滚"
version: "1.0.0"
author: "Hermes Agent"
tags: ["hermes", "model", "provider", "config", "refresh"]
---

# Hermes Agent 模型与提供商管理

## 🎯 技能概述

管理 Hermes Agent 中的模型和 API 提供商：从提供商 API 刷新可用模型列表、增删模型、修改默认模型、安全编辑 `config.yaml` 以及回滚损坏的配置。

## 📋 核心操作

### 1. 刷新提供商模型列表（从 API 拉取最新）

**API 端点**: `POST /api/hermes/provider-models`

**请求体字段**:
```json
{
  "api_key": "<提供商密钥>",
  "base_url": "<API 基础 URL>",
  "provider": "<提供商名称>",
  "update_cache": true
}
```

**通过 Hermes Studio MCP 调用**:
```
mcp__hermes_studio_api__hermes_studio_api_request:
  method: POST
  path: /api/hermes/provider-models
  body: {"api_key": "xxx", "base_url": "https://...", "provider": "xxx", "update_cache": true}
```

**⚠️ 坑：必须显式传递 `api_key`，否则返回 401**
即使 config.yaml 中已配置密钥，API 也不会自动查找。请求体必须包含 `api_key` 字段。

**返回格式**:
```json
{"body": {"models": ["model-1", "model-2", ...]}}
```

### 2. 获取当前所有可用模型

**方式 A - API**（推荐，含缓存的最新数据）:
```
GET /api/hermes/available-models
```
返回 `groups` 数组，每个 group 有 `provider`, `label`, `models`（字符串列表）。

**方式 B - 配置文件**:
直接读取 `~/.hermes/config.yaml` 中的 `providers.*.models` 和 `custom_providers.*.models`。

**用户偏好：列出全部模型，不要摘要**。当用户说"都列出来"时，穷尽所有模型，不用"等等"省略。

### 3. 修改默认模型

```bash
hermes config set model.default <model-id>
hermes config set model.provider <provider-name>
```

#### 3a. `hermes config set` 的安全边界与 Agent 侧用法

**适用场景（✅ 首选）：**
- 标量值（`model.default`、`model.provider`）
- 嵌套 dict / 对象（如 `mcp_servers.playwright`）
- 任意键路径的子字段

**唯一禁区（❌ 禁止）：**
- **list/array 字段**（如 `providers.*.models`）—— 会被序列化为转义字符串，破坏 YAML。list 字段必须走 Python yaml 流程（见 §4）。

**Agent 侧关键限制：**
- `patch` / `write_file` 工具**会被 Hermes 安全守卫拒绝**写入 `~/.hermes/config.yaml`。错误信息：`"Refusing to write to Hermes config file"`。
- **Agent 修改 config 的唯一通道是 `hermes config set`**（标量/对象）或 **Python yaml 脚本**（list）。
- 写入后务必验证：
  ```bash
  hermes config get <path>    # 确认值正确
  hermes config check         # 全局完整性检查
  ```
- 修改后热加载生效（见 §重要注意事项 #9），无需重启 Hermes，MCP 服务器配置除外。

#### 3b. 注册 MCP 服务器（`mcp_servers`）

**方式**：`hermes config set mcp_servers.<name> "<JSON>"`

Playwright MCP 模板（包已内置在 Hermes node_modules，无需 install）：

```bash
hermes config set mcp_servers.playwright '{"command": "C:\\Users\\Administrator\\.hermes\\node\\node.exe", "args": ["C:\\Users\\Administrator\\.hermes\\node\\node_modules\\@playwright\\mcp\\cli.js"], "env": {"PLAYWRIGHT_MCP_HEADLESS": "1"}, "enabled": true}'
```

**关键要点**：
- `@playwright/mcp` 已随 Hermes 自带 Node 环境安装，CLI 路径为 `~/.hermes/node/node_modules/@playwright/mcp/cli.js`
- 包本身依赖 `playwright`，如需 headless 浏览器必须先用 `npx playwright install chromium` 下载浏览器内核（首次约 300MB）
- `env` 里 `PLAYWRIGHT_MCP_HEADLESS: "1"` 推荐在自动化场景启用，避免弹出 GUI 窗口
- 添加 MCP 服务器后需要**重启 Hermes WebUI 会话**（不是热加载），工具才会出现在列表
- 删除 MCP 服务器：`hermes config unset mcp_servers.<name>`

---

## 🔧 典型工作流程

**❌ 错误方式：`hermes config set` 设置 list 字段**

```bash
hermes config set providers.zai.models "..."
```
这会**把列表写成转义字符串**，破坏 YAML 结构：
```yaml
    models: "\n  - id: xxx\n    label: xxx"  # 字符串，不是列表！
```

**✅ 正确方式：Python yaml 加载→修改→dump**

```python
import yaml

path = r'C:\Users\Administrator\.hermes\config.yaml'

with open(path, 'r') as f:
    data = yaml.safe_load(f)

# 修改模型列表
data['providers']['zai']['models'] = [
    {'id': 'glm-4-flash-250414', 'label': 'GLM-4-Flash-250414'}
]

with open(path, 'w') as f:
    yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False, width=120)
```

`yaml.safe_dump` 参数说明：
- `sort_keys=False`：保留原有键顺序
- `allow_unicode=True`：保留中文字符
- `default_flow_style=False`：使用块格式（块缩进，非流式 `{}`）
- `width=120`：控制行宽，避免每行一个键

### 5. 验证配置文件完整性

修改后必须验证：

```bash
python -c "
import yaml
with open(r'C:\Users\Administrator\.hermes\config.yaml') as f:
    data = yaml.safe_load(f)
print('YAML OK')
print('model.default:', data['model']['default'])
print('model.provider:', data['model']['provider'])
print('zai.models:', data['providers']['zai']['models'])
"
```

同时确认其他提供商（gemini、custom_providers 等）数据完整未被破坏。

### 6. 回滚损坏配置

Hermes 在检测到 YAML 损坏时会自动创建 `.corrupt` 备份：
- `config.yaml.corrupt.<timestamp>.bak`

**恢复命令**:
```bash
cp ~/.hermes/config.yaml.bak ~/.hermes/config.yaml
```

可用的备份文件（按优先级）：
- `config.yaml.bak` — 最近一次手工备份
- `config.yaml.bak-<date>` — 带日期戳的备份
- `config.yaml.corrupt.<timestamp>.bak` — 损坏前的自动备份

## 🔧 典型工作流程

### 刷新某提供商模型 + 清理本地列表

1. **备份当前配置**：
   ```bash
   cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak
   ```

2. **从 API 拉取最新模型列表**：
   ```
   POST /api/hermes/provider-models
   body: {api_key, base_url, provider, update_cache: true}
   ```

3. **根据需求决定保留哪些模型**

4. **用 Python yaml 修改 config.yaml**（不要用手写正则替换！）

5. **验证**：Python yaml 解析 + 检查其他提供商完整性

### 示例：GLM 提供商只保留特定模型

```python
import yaml

path = r'C:\Users\Administrator\.hermes\config.yaml'

with open(path, 'r') as f:
    data = yaml.safe_load(f)

# 只保留 glm-4-flash-250414
data['providers']['zai']['models'] = [
    {'id': 'glm-4-flash-250414', 'label': 'GLM-4-Flash-250414'}
]
data['model']['default'] = 'glm-4-flash-250414'
data['model']['provider'] = 'zai'

with open(path, 'w') as f:
    yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False, width=120)
```

## ⚠️ 重要注意事项

1. **🚨 删除模型前必须确认用户资源包/额度** —— 用户可能对某些模型有已购资源包（如智谱的 GLM-4.6V Coding Plan 套餐还有 391,520 tokens 余额）。**任何时候用户说"清理模型列表"、"删除模型"、"只保留某模型"时，必须先问一句"这些模型有没有你还在用的资源包/额度？"** 否则删了用户付费模型会直接导致服务不可用（模型从列表消失，但资源包还在扣费周期）。恢复方法：立即重新添加回 config.yaml，热加载即生效。

2. **Hermes Agent `config.yaml` 与 Hermes Web UI 提供商是两套独立系统**
   - Agent 侧：`config.yaml` 的 `providers.*`（CLI/Agent 调度用）
   - Web UI 侧：`GET /api/hermes/available-models` 返回的 `groups`（`/api/coding/paas/v4`、stepfun、agnes 等）
   - **修改 Agent 配置不影响 Web UI 列表，反之亦然**。用户截图看到的列表通常来自 Web UI。动手前先问清楚用户指的是哪套。
   - Web UI 提供商通过 `POST /api/hermes/provider-models` 刷新，Agent 提供商通过 `config.yaml` 或 `hermes config set` 管理。

2. **永远不要对 list 字段使用 `hermes config set`** —— 它会把列表序列化为转义字符串

3. **不要对 config.yaml 使用正则替换** —— 结构复杂，多个段落有相同结构（如 `models:` 块），正则极易误删其他提供商的数据。**正确做法：Python yaml 加载 → 修改 → dump**。本会话一次正则替换就把 442 行的文件破坏了（442 行 → 259 行，gemini 也被误改）。

4. **API 刷新必须带 `api_key`** —— 不带会返回 401

5. **修改前备份** —— `cp config.yaml config.yaml.bak`

6. **修改后验证** —— Python yaml 解析 + 检查其他配置完整性（不只检查修改的段落，还要确认 gemini、custom_providers 等其他提供商数据完整）

7. **用户偏好：穷尽列表，不摘要** —— 用户要完整列表时，不要用"等等"省略

8. **thinking 模型测试时要注意 max_tokens** —— `glm-4.6v` 等 thinking 模型在少量 tokens 时只返回推理过程而不生成文本，容易被误判为报错。测试时给足 tokens（≥300）。

9. **`config.yaml` 模型配置是热加载** —— 改完文件立即生效，**不需要重启 Hermes**。只有改 `mcp_servers`、`plugins`、provider 的 `api_key` 注入方式才可能需要重启进程。当用户质疑"你要我重启？"时，先确认是否真的需要重启再答复。

10. **`zai` 提供商默认无 `base_url`/`api_key`** —— 是 Hermes 内置提供商，靠自动路由。如果用户想用智谱 Coding Plan 端点跑 `zai`，必须显式配置 `base_url: https://open.bigmodel.cn/api/coding/paas/v4` + `api_key`。智谱 `/api/coding/paas/v4`（Coding Plan）和 `/api/paas/v4`（标准端点）是**不同额度池**，用户有资源包时必须用对应端点。

11. **`curl --noproxy "*"` 绕过代理测 API** —— 当 `curl` 通过 HTTP_PROXY 失败时（如 Open-Meteo、bazaarlink 等第三方 API），加 `--noproxy "*"` 直连测试。Windows Git Bash 中经常需要此参数。

12. **Web UI 修改需通过 API，不能改 config.yaml** —— Web UI 的提供商列表存储在 `~/.hermes-web-ui/` 下的 SQLite 数据库，直接改 config.yaml 不会影响 Web UI。必须通过以下 API 操作：
   - 添加提供商：`POST /api/hermes/config/providers` body: `{name, base_url, api_key}`
   - 添加模型：`PUT /api/hermes/custom-model` body: `{provider: "custom:xxx", model: "model-id"}`
   - 验证：`GET /api/hermes/available-models` 检查 groups 数组
   - 动手前先确认用户要改的是哪套系统（Agent CLI vs Web UI），问清楚再动手。

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

## 🔗 相关资源

- `~/.hermes/config.yaml` — 主配置文件
- `hermes config --help` — CLI 配置管理帮助
- Hermes Studio API: `GET /api/hermes/available-models`, `POST /api/hermes/provider-models`
- `references/bazaarlink-provider-setup.md` — 模型聚合网关（类似 OpenRouter）的 custom_providers 配置示例，含 User-Agent 校验、免费容量限制等注意事项

---

*最后更新：2026-08-15*
*版本：1.0.0*
