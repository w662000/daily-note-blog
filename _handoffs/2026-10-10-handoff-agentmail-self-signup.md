---
layout: default
title: 交接文档 · AgentMail Self-Signup
date: 2026-10-13 23:30:00 +0800
---

# AgentMail Self-Signup

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\email\agentmail\references\signup.md

Use this when the agent does not have an AgentMail API key. A human must receive
and provide the OTP.

## Sign Up

```bash
npm install -g agentmail-cli@latest
agentmail agent sign-up \
  --human-email you@example.com \
  --username my-agent \
  --source agentmail-cli \
  --referrer hermes-agent \
  --format json
```

Export the returned `api_key`:

```bash
export AGENTMAIL_API_KEY="am_..."
```

Verify with the OTP:

```bash
agentmail agent verify --otp-code 123456
```

## Notes

- Use a real human email address for `--human-email`.
- `human_email` is the signup idempotency key, but signing up again with the
  same email rotates the API key.
- Before verification, the account has one inbox, 10 sends/day, and can only
  send to the signup human email.

## First Check

```bash
agentmail inboxes list --format json
agentmail inboxes:messages send \
  --inbox-id my-agent@agentmail.to \
  --to you@example.com \
  --subject "AgentMail verified" \
  --text "My AgentMail inbox is verified." \
  --format json
```

Continue with [core.md](core.md).
