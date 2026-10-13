---
layout: default
title: 技术点 · Contributing to Hermes Agent
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Contributing to Hermes Agent

> 来源：261010_Contributing to Hermes Agent_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
  gh search issues --repo NousResearch/hermes-agent "<your terms>"
  gh search prs --repo NousResearch/hermes-agent --state all "<your terms>"
```
- It wraps an external CLI or API that the agent can call via `terminal` or `web_extract`
- It doesn't need custom Python integration or API key management baked into the agent
- It requires end-to-end integration with API keys, auth flows, or multi-component configuration managed by the agent harness
- ```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
cd "${HERMES_HOME:-$HOME/.hermes}/hermes-agent"

# Add dev/test extras on top of the standard install.
uv pip install -e ".[all,dev]"

# Optional: docs site + workspace dependencies.
npm install
```
- ```
git checkout -b fix/description
scripts/run_tests.sh
```
- ```
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# Create venv with Python 3.11, OUTSIDE the source tree
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
export VIRTUAL_ENV="$HOME/.hermes/venvs/hermes-dev"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Install with all extras (messaging, cron, CLI menus, dev tools)
uv pip install -e ".[all,dev]"

# Optional: workspace / docs dependencies
npm install
```
- ```
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}
cp cli-config.yaml.example ~/.hermes/config.yaml
touch ~/.hermes/.env

# Add at minimum an LLM provider key:
echo "OPENROUTER_API_KEY=***" >> ~/.hermes/.env
```
- ```
# The standard installer already put `hermes` on PATH.
hermes doctor
hermes chat -q "Hello"
```
- ```
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes
```
- ```
# Preferred — matches CI (hermetic `env -i`, per-file subprocess isolation
# via run_tests_parallel.py, worker count auto-scaled); see AGENTS.md
scripts/run_tests.sh

# Alternative (activate the venv first). The wrapper is still recommended
# for parity with GitHub Actions before you open a PR:
pytest tests/ -v
```
- ```
hermes-agent/
├── run_agent.py              # AIAgent facade (~1.5k LOC) — the turn loop lives in agent/conversation_loop.py + agent/turn_*.py
├── cli.py                    # HermesCLI class — interactive CLI orchestrator (~4.6k LOC + hermes_cli/cli_*_mixin.py)
├── model_tools.py            # Tool orchestration (thin layer over tools/registry.py)
├── toolsets.py               # Tool groupings and presets (hermes-cli, hermes-telegram, etc.)
├── hermes_state.py           # SessionDB facade (~1.4k LOC); implementation in hermes_state_*.py (21 siblings) — FTS5 search, session titles
├── batch_runner.py           # Parallel batch processing for trajectory generation
│
├── agent/                    # Agent internals (extracted modules)
│   ├── conversation_loop.py      # run_conversation() — the agent turn loop (phases in turn_*.py)
│   ├── tool_executor.py          # Tool dispatch (inline agent-level tools, delegate, registry)
│   ├── session_persistence.py    # Session/trajectory saving
│   ├── prompt_builder.py         # System prompt assembly (identity, skills, context files, memory)
│   ├── context_compressor.py     # Auto-summarization when approaching context limits
│   ├── auxiliary_client.py       # Resolves auxiliary OpenAI clients (summarization, vision)
│   ├── display.py                # KawaiiSpinner, tool progress formatting
│   ├── model_metadata.py         # Model context lengths, token estimation
│   └── trajectory.py             # Trajectory saving helpers
│
├── hermes_cli/               # CLI command implementations
│   ├── main.py                   # Entry point, argument parsing, command dispatch
│   ├── cli_*_mixin.py            # HermesCLI mixins (slash commands, display, session, ...)
│   ├── config.py                 # Config management, migration, env var definitions
│   ├── setup.py                  # Interactive setup wizard
│   ├── auth.py                   # Provider resolution, OAuth, Nous Portal (facade + auth_*.py siblings)
│   ├── models.py                 # OpenRouter model selection lists
│   ├── banner.py                 # Welcome banner, ASCII art
│   ├── commands.py               # Central slash command registry (CommandDef), autocomplete, gateway helpers
│   ├── callbacks.py              # Interactive callbacks (clarify, sudo, approval)
│   ├── doctor.py                 # Diagnostics
│   ├── skills_hub.py             # Skills Hub CLI + /skills slash command
│   ├── skin_engine.py            # Skin/theme engine — data-driven CLI visual customization
│   ├── web_server.py             # Dashboard server (facade + web_server_*.py siblings)
│   └── web_routers/              # Dashboard FastAPI routers (one file per surface)
│
├── tools/                    # Tool implementations (self-registering)
│   ├── registry.py               # Central tool registry (schemas, handlers, dispatch)
│   ├── approval.py               # Dangerous command detection + per-session approval
│   ├── terminal_tool.py          # Terminal orchestration (sudo, env lifecycle, backends)
│   ├── file_operations.py        # read_file, write_file, search, patch, etc.
│   ├── web_tools.py              # web_search, web_extract (Parallel/Firecrawl + Gemini summarization)
│   ├── vision_tools.py           # Image analysis via multimodal models
│   ├── delegate_tool.py          # Subagent spawning and parallel task execution
│   ├── code_execution_tool.py    # Sandboxed Python with RPC tool access (env allowlists in code_execution_env.py)
│   ├── mcp_tool.py               # MCP client (facade + mcp_tool_*.py siblings: config, discovery, transport, ...)
│   ├── browser_tool.py           # Browser automation (facade + browser_tool_*.py siblings)
│   ├── session_search_tool.py    # Search past conversations with FTS5 + anchored windows
│   ├── cronjob_tools.py          # Scheduled task management
│   ├── skill_tools.py            # Skill search, load, manage
│   └── environments/             # Terminal execution backends
│       ├── base.py                   # BaseEnvironment ABC
│       ├── local.py, docker.py, ssh.py, singularity.py, modal.py, daytona.py
│
├── gateway/                  # Messaging gateway
│   ├── run.py                    # GatewayRunner facade (~5.5k LOC); phases in run_*.py (startup, inbound, turn, busy, ...)
│   ├── slash_commands_*.py       # Gateway slash command handler mixins
│   ├── config.py                 # Platform configuration resolution
│   ├── session.py                # Session store, context prompts, explicit resets (+ session_*.py siblings)
│   └── platforms/                # Platform adapters
│       ├── telegram.py, discord_adapter.py, slack.py, whatsapp.py
│
├── scripts/                  # Installer and bridge scripts
│   ├── install.sh                # Linux/macOS installer
│   ├── install.ps1               # Windows PowerShell installer
│   └── whatsapp-bridge/          # Node.js WhatsApp bridge (Baileys)
│
├── skills/                   # Bundled skills (copied to ~/.hermes/skills/ on install)
├── optional-skills/          # Official optional skills (discoverable via hub, not activated by default)
├── tests/                    # Test suite
├── website/                  # Documentation site (hermes-agent.nousresearch.com)
│
├── cli-config.yaml.example   # Example configuration (copied to ~/.hermes/config.yaml)
└── AGENTS.md                 # Development guide for AI coding assistants
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
