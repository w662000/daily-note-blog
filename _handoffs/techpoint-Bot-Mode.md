---
layout: default
title: 技术点 · Bot Mode
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Bot Mode

> 来源：261010_Bot Mode_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **Copy API keys from the main profile** — on by default. Each Bot gets its own credential store: static API keys are copied in, while single-use OAuth logins (Anthropic, OpenAI Codex, xAI) are not copied — sign the Bot in itself with `hermes -p <name> auth add <provider>`. See [Every profile owns its credentials](./profiles.md#every-profile-owns-its-credentials).
- the error>` (secret-shaped tokens redacted, long lines truncated), or `builder couldn't start — too many bots running` when the local
- **Direct messages** — every Bot Chat carries the `message_agent` tool: a Bot messages a teammate by calling `message_agent(target="researcher", message="…")`. The target is the teammate's profile name, its friendly name (`hermes profile rename` or the Bot Mode title — `Scribe`, `Dr. Foo`) or the `@`-tag the Desktop inserts for it (`@scribe`, `@dr-foo`, `@drfoo`); `@hermes` always means the primary Bot. A profile name is matched first, so it can never be hijacked by another Bot's friendly name, and a friendly name shared by two Bots is refused with the roster instead of guessing. The tool validates the target against the live roster, prefixes the sender's `Message from 🤖 <friendly name> (@<handle>):` attribution automatically, and delivers into the teammate's canonical Bot Chat. Delivery is **fire-and-forget**: the sender gets a *dispatch* acknowledgement (`status: queued` plus a `delivery_id` — and a `process_id` for the background delivery process — means the message was handed to that process, not that it was delivered), finishes its turn, and that process's completion notification carries the outcome — the reply, or the delivery failure. On surfaces that cannot receive completion notifications (an `api_server` session, one-shot runners) the acknowledgement instead carries `reply_delivery: poll`: the sender retrieves the outcome with `process(action="wait", session_id=…)` before ending its turn, and the outcome is also saved into the sender's session transcript as a delivery row when the process exits, so the reply is never silently lost. The notification carries the reply whole up to the message size limit (16,000 characters); a longer one arrives as its tail and says how much was cut (`process(action="log", session_id=…)` has the rest). The message travels as a real parameter (nothing shell-interpreted — quotes, `$(...)`, and backticks arrive verbatim), and the Bot composes its own message rather than forwarding your words. The teammate roster — names **and roles** from each profile's title/description — is part of every Bot Chat's system prompt, so Bots know who does what before choosing a recipient. The tool exists **only** in canonical Bot Chat sessions on Bot-Mode-managed installs; regular chats, group-room member sessions, and CLI sessions never see it.
- **Staying silent** — a Bot that has nothing to add may end a turn with one of the [intentional silence tokens](./messaging/index.md#intentional-silence-tokens) (`[SILENT]`, `NO_REPLY`, …). The Bot Chat keeps that turn in its transcript but renders nothing, and a teammate that messaged it gets an empty reply instead of the token. Failed turns and prose that merely mentions a token are shown as-is.
- ```
agent:
  bot_mode_protocol: true   # inject the bot-to-bot messaging protocol into canonical Bot Chats
```
- ```
# the canonical forever-chat, created once per Bot (later runs resume it)
hermes -p <bot> chat -c "Bot Chat" --create-if-missing
```
- ```
# ~/.hermes/profiles/<any-bot>/profile.yaml — an empty block is enough to mark the install
ui_meta:
  hermes-bots: {}
```
- Bots on one machine can message Bots on **another machine's gateway** without any desktop in the loop. Register the other gateway as a *peer* (its API server URL + `API_SERVER_KEY`):
- ```
hermes peer add spark --url http://spark.lan:8377 --key <API_SERVER_KEY>
hermes peer list
hermes peer dm spark < ~/.hermes/cache/scratch/dm.txt        # message body from a file (nothing shell-interpreted)
hermes peer dm spark/researcher < ~/.hermes/cache/scratch/dm.txt   # named profile on a multiplexed peer
hermes peer run spark --idempotency-key ticket-123 < ~/.hermes/cache/scratch/long-task.txt
hermes peer status spark run_abc123
hermes peer stop spark run_abc123
```
- `hermes peer dm` delivers into the remote agent's canonical Bot Chat over the peer's existing API server, runs one agent turn there, and prints the reply on stdout — the exact cross-machine twin of the local `hermes -p <bot> chat` command.
- canonical Bot Chat transcript, and a stable `--idempotency-key` makes a retry
- Requirements: the peer machine runs the `api_server` gateway platform with a strong `API_SERVER_KEY`; reachability is your network's business (LAN, Tailscale, VPN). The key is a credential and lives in `~/.hermes/.env` as `HERMES_PEER_<NAME>_KEY`; peer names/URLs live in `config.yaml` under `bot_peers`.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
