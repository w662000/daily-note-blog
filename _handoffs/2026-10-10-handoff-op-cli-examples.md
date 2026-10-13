---
layout: default
title: 交接文档 · op CLI examples
date: 2026-10-13 23:30:00 +0800
---

# op CLI examples

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\security\1password\references\cli-examples.md

## Sign-in and identity

```bash
op signin
op signin --account my.1password.com
op whoami
op account list
```

## Read secrets

```bash
op read "op://app-prod/db/password"
op read "op://app-prod/npm/one-time password?attribute=otp"
```

## Inject secrets

```bash
echo "api_key: {{ op://app-prod/openai/api key }}" | op inject
op inject -i config.tpl.yml -o config.yml
```

## Run command with secrets

```bash
export DB_PASSWORD="op://app-prod/db/password"  # example op:// reference, resolved by `op run`
op run -- sh -c '[ -n "$DB_PASSWORD" ] && echo "DB_PASSWORD is set"'
```
