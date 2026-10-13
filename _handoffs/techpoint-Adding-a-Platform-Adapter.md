---
layout: default
title: 技术点 · Adding a Platform Adapter
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Adding a Platform Adapter

> 来源：261010_Adding a Platform Adapter_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
User ↔ Messaging Platform ↔ Platform Adapter ↔ Gateway Runner ↔ AIAgent
```
- ```
~/.hermes/plugins/my-platform/
  plugin.yaml      # Plugin metadata
  adapter.py       # Adapter class + register() entry point
```
- ```
name: my-platform
label: My Platform
kind: platform
version: 1.0.0
description: My custom messaging platform adapter
author: Your Name
requires_env:
  - MY_PLATFORM_TOKEN          # bare string works
  - name: MY_PLATFORM_CHANNEL  # or rich dict for better UX
    description: "Channel to join"
    prompt: "Channel"
    password: false
optional_env:
  - name: MY_PLATFORM_HOME_CHANNEL
    description: "Default channel for cron delivery"
    password: false
```
- ```
provides_tools:
  - my_platform_call
  - my_platform_list
```
- key under `platform_toolsets` in `config.yaml`. Plugin platform names are
- ```
from gateway.platforms._shared import extra_or_secret, get_scoped_secret, seed_extra_from_env
from gateway.platforms.base import BasePlatformAdapter, SendResult
from gateway.platforms.event import MessageEvent, MessageType
from gateway.config import Platform, PlatformConfig


class MyPlatformAdapter(BasePlatformAdapter):
    def __init__(self, config: PlatformConfig):
        super().__init__(config, Platform("my_platform"))
        # Explicit env (profile-scoped) → this profile's config.extra (YAML) → default. Under multiplexing a
        # scoped miss falls to the profile's own YAML, never to another profile's process env.
        self.token = extra_or_secret(config.extra, "token", "MY_PLATFORM_TOKEN")

    async def connect(self, *, is_reconnect: bool = False) -> bool:
        # Connect to the platform API, start listeners
        self._mark_connected()
        return True

    async def disconnect(self) -> None:
        self._mark_disconnected()

    async def send(self, chat_id, content, reply_to=None, metadata=None):
        # Send message via platform API
        return SendResult(success=True, message_id="...")

    async def get_chat_info(self, chat_id):
        return {"name": chat_id, "type": "dm"}


def check_requirements() -> bool:
    return bool(get_scoped_secret("MY_PLATFORM_TOKEN"))


def validate_config(config) -> bool:
    return bool(extra_or_secret(getattr(config, "extra", None), "token", "MY_PLATFORM_TOKEN"))


def _env_enablement() -> dict | None:
    if not get_scoped_secret("MY_PLATFORM_TOKEN", "").strip():
        return None
    return seed_extra_from_env(
        (("MY_PLATFORM_TOKEN", "token", None), ("MY_PLATFORM_CHANNEL", "channel", None)),
        home_env="MY_PLATFORM_HOME_CHANNEL",
    )


def register(ctx):
    """Plugin entry point — called by the Hermes plugin system."""
    ctx.register_platform(
        name="my_platform",
        label="My Platform",
        adapter_factory=MyPlatformAdapter,
        # PASSIVE probe — "are deps/config present right now?".  Called from
        # status displays and config loading, so it must NEVER pip-install.
        check_fn=check_requirements,
        # ACTIVE installer (optional) — only for platforms with a
        # lazy-installable SDK.  create_adapter() calls it when check_fn
        # returns False, right before the gateway connects the platform.
        # Typically wraps tools.lazy_deps.ensure_and_bind(...).  Omit it
        # and a False check_fn is a hard block.
        # ensure_deps_fn=ensure_requirements,
        validate_config=validate_config,
        required_env=["MY_PLATFORM_TOKEN"],
        install_hint="pip install my-platform-sdk",
        # Env-driven auto-configuration — seeds PlatformConfig.extra from
        # env vars before adapter construction. See "Env-Driven Auto-
        # Configuration" section below.
        env_enablement_fn=_env_enablement,
        # Cron home-channel delivery support. Lets deliver=my_platform cron
        # jobs route without editing cron/scheduler.py. See "Cron Delivery"
        # section below.
        cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",
        # Per-platform user authorization env vars
        allowed_users_env="MY_PLATFORM_ALLOWED_USERS",
        allow_all_env="MY_PLATFORM_ALLOW_ALL_USERS",
        # Message length limit for smart chunking (0 = no limit)
        max_message_length=4000,
        # LLM guidance injected into system prompt
        platform_hint=(
            "You are chatting via My Platform. "
            "It supports markdown formatting."
        ),
        # Display
        emoji="💬",
    )

    # Optional: register platform-specific tools
    ctx.register_tool(
        name="my_platform_search",
        toolset="my_platform",
        schema={...},
        handler=my_search_handler,
    )
```
- ```
gateway:
  platforms:
    my_platform:
      enabled: true
      extra:
        token: "..."
        channel: "#general"
```
- | YAML config bridge | `apply_yaml_config_fn` translates `config.yaml` keys into env vars / extras |
- | Token lock (multi-profile) | Use `acquire_scoped_lock()` in your `connect()` |
- ```
async def _send_request(args, chat_id, platform_name, pconfig):
    # `args` contains the host-driven send request fields.
    message_id = await client.send(
        address=chat_id,
        body=args["message"],
        subject=args.get("subject"),
    )
    return {"success": True, "platform": platform_name,
            "chat_id": chat_id, "message_id": message_id}


def _parse_address(raw):
    normalized = raw.strip().lower()
    if normalized.startswith("@") and "@" in normalized[1:]:
        return normalized, None  # (chat_id, optional thread_id)
    return None                 # continue to channel-directory resolution


def _validate_address(address):
    # True accepts; False rejects; a string rejects with that diagnostic.
    return True if address.endswith("@example.com") else "unsupported domain"


def register(ctx):
    ctx.register_platform(
        name="fmsg",
        label="Fixture Message",
        adapter_factory=lambda cfg: FmsgAdapter(cfg),
        check_fn=check_requirements,
        parse_target_ref_fn=_parse_address,
        validate_target_ref_fn=_validate_address,
        # May be a regular function or async def. Hermes awaits any awaitable
        # result, including callable objects and functools.partial wrappers.
        send_message_handler=_send_request,
        # Prefer this lower-level hook when cron must send from a process
        # without the live gateway.
        standalone_sender_fn=_standalone_send,
    )
```
- Read env through `gateway.platforms._shared.get_scoped_secret` — never `os.getenv`. Under `gateway.multiplex_profiles` the process env holds the DEFAULT profile's values; a secondary profile's `.env` exists only in its secret scope, and a raw read would enable your platform for the wrong profile with the wrong credentials. `seed_extra_from_env` builds the seed dict from a `(ENV_VAR, extra_key, conv)` table through that reader.
- ```
from gateway.platforms._shared import get_scoped_secret, seed_extra_from_env


def _env_enablement() -> dict | None:
    """Seed PlatformConfig.extra from env vars.

    Called by the platform registry during load_gateway_config().
    Return None when the platform isn't minimally configured — the
    caller then skips auto-enabling. Return a dict to seed extras.
    """
    token = get_scoped_secret("MY_PLATFORM_TOKEN", "").strip()
    channel = get_scoped_secret("MY_PLATFORM_CHANNEL", "").strip()
    if not (token and channel):
        return None
    # (ENV_VAR, extra_key, conv): blank values are skipped, a conv raising
    # ValueError drops the key. home_env seeds the special 'home_channel'
    # dict ({chat_id, name} from MY_PLATFORM_HOME_CHANNEL[_NAME], name
    # defaults to "Home"), which the core hook lifts into a HomeChannel.
    return {"token": token, "channel": channel, **seed_extra_from_env(
        (("MY_PLATFORM_PORT", "port", int), ("MY_PLATFORM_NICK", "nick", None)),
        home_env="MY_PLATFORM_HOME_CHANNEL",
    )}


def register(ctx):
    ctx.register_platform(
        name="my_platform",
        label="My Platform",
        adapter_factory=MyPlatformAdapter,
        check_fn=check_requirements,
        validate_config=validate_config,
        env_enablement_fn=_env_enablement,
        # ... other fields
    )
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
