---
layout: default
title: 交接文档 · AgentMail WebSockets
date: 2026-10-13 23:30:00 +0800
---

# AgentMail WebSockets

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\email\agentmail\references\websockets.md

Use WebSockets when a local agent process needs realtime inbound mail. After an
event arrives, use the CLI for inbox, send, reply, label, and attachment work.

## Python

The Python example needs the separate AgentMail Python SDK, not the CLI:

```bash
pip install agentmail
```

`AgentMail()` reads `AGENTMAIL_API_KEY` from the environment. If the SDK is
unavailable, use the `Raw` WebSocket below instead.

```python
from agentmail import AgentMail, MessageReceivedEvent, Subscribe

client = AgentMail()

with client.websockets.connect() as socket:
    socket.send_subscribe(Subscribe(
        inbox_ids=["agent@agentmail.to"],
        event_types=["message.received"],
    ))
    for event in socket:
        if isinstance(event, MessageReceivedEvent):
            print(event.message.subject, event.message.from_)
```

## Raw

```text
wss://ws.agentmail.to/v0?api_key=$AGENTMAIL_API_KEY
```

EU region:

```text
wss://ws.agentmail.eu/v0?api_key=$AGENTMAIL_API_KEY
```

Subscribe frame:

```json
{ "type": "subscribe", "event_types": ["message.received"], "inbox_ids": ["agent@agentmail.to"] }
```

Omit `inbox_ids` and `pod_ids` for the API key scope.

## Loop Rules

- Dedupe every event by `event_id`.
- Reconnect with backoff and resubscribe after reconnecting.
