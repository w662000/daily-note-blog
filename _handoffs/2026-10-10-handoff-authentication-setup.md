---
layout: default
title: 交接文档 · Authentication & Setup
date: 2026-10-13 23:30:00 +0800
---

# Authentication & Setup

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\devops\inference-sh-cli\references\authentication.md

## Install the CLI

```bash
curl -fsSL https://cli.inference.sh | sh
```

## Login

```bash
infsh login
```

This opens a browser for authentication. After login, credentials are stored locally.

## Check Authentication

```bash
infsh me
```

Shows your user info if authenticated.

## Environment Variable

For CI/CD or scripts, set your API key:

```bash
export INFSH_API_KEY=your-api-key
```

The environment variable overrides the config file.

## Update CLI

```bash
infsh update
```

Or reinstall:

```bash
curl -fsSL https://cli.inference.sh | sh
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| "not authenticated" | Run `infsh login` |
| "command not found" | Reinstall CLI or add to PATH |
| "API key invalid" | Check `INFSH_API_KEY` or re-login |

## Documentation

- [CLI Setup](https://inference.sh/docs/extend/cli-setup) - Complete CLI installation guide
- [API Authentication](https://inference.sh/docs/api/authentication) - API key management
- [Secrets](https://inference.sh/docs/secrets/overview) - Managing credentials
