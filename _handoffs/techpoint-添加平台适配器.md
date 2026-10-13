---
layout: default
title: 技术点 · 添加平台适配器
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · 添加平台适配器

> 来源：261010_添加平台适配器_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 本指南介绍如何向 Hermes gateway 添加新的消息平台。平台适配器将 Hermes 连接到外部消息服务（Telegram、Discord、WeCom 等），使用户可以通过该服务与 agent 交互。
- **Plugin**（推荐用于社区/第三方）：将 plugin 目录放入 `~/.hermes/plugins/` — 无需修改任何核心代码。参见下方 [Plugin 路径](#plugin-path-recommended)。
- **内置**：需修改代码、配置和文档共 20+ 个文件。参见下方 [内置清单](#step-by-step-checklist)。
- ```
用户 ↔ 消息平台 ↔ 平台适配器 ↔ Gateway Runner ↔ AIAgent
```
- **`connect()`** — 建立连接（WebSocket、长轮询、HTTP 服务器等）*(抽象方法)*
- 适配器接收入站消息后，通过 `self.handle_message(event)` 转发，基类将其路由到 gateway runner。
- ```
~/.hermes/plugins/my-platform/
  plugin.yaml      # Plugin 元数据
  adapter.py       # 适配器类 + register() 入口点
```
- Plugin 元数据。`requires_env` 和 `optional_env` 块会自动填充 `hermes config` UI 条目（参见下方[在 hermes config 中暴露环境变量](#surfacing-env-vars-in-hermes-config)）。
- ```
name: my-platform
label: My Platform
kind: platform
version: 1.0.0
description: My custom messaging platform adapter
author: Your Name
requires_env:
  - MY_PLATFORM_TOKEN          # 裸字符串有效
  - name: MY_PLATFORM_CHANNEL  # 或使用富字典以获得更好的 UX
    description: "Channel to join"
    prompt: "Channel"
    password: false
optional_env:
  - name: MY_PLATFORM_HOME_CHANNEL
    description: "Default channel for cron delivery"
    password: false
```
- ```
import os
from gateway.platforms.base import BasePlatformAdapter, SendResult
from gateway.platforms.event import MessageEvent, MessageType
from gateway.config import Platform, PlatformConfig


class MyPlatformAdapter(BasePlatformAdapter):
    def __init__(self, config: PlatformConfig):
        super().__init__(config, Platform("my_platform"))
        extra = config.extra or {}
        self.token = os.getenv("MY_PLATFORM_TOKEN") or extra.get("token", "")

    async def connect(self) -> bool:
        # 连接到平台 API，启动监听器
        self._mark_connected()
        return True

    async def disconnect(self) -> None:
        self._mark_disconnected()

    async def send(self, chat_id, content, reply_to=None, metadata=None):
        # 通过平台 API 发送消息
        return SendResult(success=True, message_id="...")

    async def get_chat_info(self, chat_id):
        return {"name": chat_id, "type": "dm"}


def check_requirements() -> bool:
    return bool(os.getenv("MY_PLATFORM_TOKEN"))


def validate_config(config) -> bool:
    extra = getattr(config, "extra", {}) or {}
    return bool(os.getenv("MY_PLATFORM_TOKEN") or extra.get("token"))


def _env_enablement() -> dict | None:
    token = os.getenv("MY_PLATFORM_TOKEN", "").strip()
    channel = os.getenv("MY_PLATFORM_CHANNEL", "").strip()
    if not (token and channel):
        return None
    seed = {"token": token, "channel": channel}
    home = os.getenv("MY_PLATFORM_HOME_CHANNEL")
    if home:
        seed["home_channel"] = {"chat_id": home, "name": "Home"}
    return seed


def register(ctx):
    """Plugin 入口点 — 由 Hermes plugin 系统调用。"""
    ctx.register_platform(
        name="my_platform",
        label="My Platform",
        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),
        check_fn=check_requirements,
        validate_config=validate_config,
        required_env=["MY_PLATFORM_TOKEN"],
        install_hint="pip install my-platform-sdk",
        # 环境变量驱动的自动配置 — 在适配器构建前从环境变量
        # 填充 PlatformConfig.extra。参见下方"环境变量驱动的自动配置"章节。
        env_enablement_fn=_env_enablement,
        # Cron 主频道投递支持。允许 deliver=my_platform 的 cron 任务
        # 无需编辑 cron/scheduler.py 即可路由。参见下方"Cron 投递"章节。
        cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",
        # 每平台用户授权环境变量
        allowed_users_env="MY_PLATFORM_ALLOWED_USERS",
        allow_all_env="MY_PLATFORM_ALLOW_ALL_USERS",
        # 智能分块的消息长度限制（0 = 无限制）
        max_message_length=4000,
        # 注入系统 prompt（提示词）的 LLM 指导
        platform_hint=(
            "You are chatting via My Platform. "
            "It supports markdown formatting."
        ),
        # 显示
        emoji="💬",
    )

    # 可选：注册平台专属工具
    ctx.register_tool(
        name="my_platform_search",
        toolset="my_platform",
        schema={...},
        handler=my_search_handler,
    )
```
- 用户在 `config.yaml` 中配置平台：
- ```
gateway:
  platforms:
    my_platform:
      enabled: true
      extra:
        token: "..."
        channel: "#general"
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
