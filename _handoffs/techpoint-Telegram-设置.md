---
layout: default
title: 技术点 · Telegram 设置
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Telegram 设置

> 来源：261010_Telegram 设置_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 每个 Telegram 机器人都需要由 [@BotFather](https://t.me/BotFather)（Telegram 官方机器人管理工具）颁发的 API token（令牌）。
- 5. BotFather 会回复你的 **API token**，格式如下：
- ```
123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```
- 请妥善保管你的机器人 token。任何持有该 token 的人都可以控制你的机器人。如果泄露，请立即通过 BotFather 的 `/revoke` 命令撤销。
- 以下 BotFather 命令可改善用户体验。向 @BotFather 发送：
- | 命令 | 用途 |
- | `/setcommands` | 定义命令菜单（聊天中的 `/` 按钮） |
- 对于 `/setcommands`，一个实用的初始命令集：
- ```
help - Show help information
new - Start a new conversation
sethome - Set this chat as the home channel
```
- 以 `/` 命令开头的消息
- 服务消息（成员加入/离开、置顶消息等）
- 禁用隐私模式的替代方案：将机器人提升为**群组管理员**。管理员机器人无论隐私设置如何都能接收所有消息，这样就无需切换全局隐私模式。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
1. 将环境变量添加到 Fly.io 应用密钥：

```bash
fly secrets set TELEGRAM_WEBHOOK_URL=https://my-app.fly.dev/telegram
fly secrets set TELEGRAM_WEBHOOK_SECRET=$(openssl rand -hex 32)
```

2. 在 `fly.toml` 中暴露 webhook 端口：

```toml
[[services]]
  internal_port = 8443
  protocol = "tcp"

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

3. 部署：

```bash
fly deploy
```

gateway 日志应显示：`[telegram] Connected to Telegram (webhook mode)`。
