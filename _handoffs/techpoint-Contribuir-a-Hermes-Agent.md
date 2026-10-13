---
layout: default
title: 技术点 · Contribuir a Hermes Agent
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Contribuir a Hermes Agent

> 来源：261010_Contribuir a Hermes Agent_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Envuelve una CLI externa o API que el agente puede llamar a través de `terminal` o `web_extract`
- No necesita integración personalizada de Python ni gestión de claves API integrada en el agente
- Requiere integración de extremo a extremo con claves API, flujos de autenticación o configuración de múltiples componentes gestionada por el harness del agente
- ```
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# Crear venv con Python 3.11
uv venv venv --python 3.11
export VIRTUAL_ENV="$(pwd)/venv"

# Instalar con todos los extras (mensajería, cron, menús CLI, herramientas de desarrollo)
uv pip install -e ".[all,dev]"

# Opcional: herramientas de navegador
npm install
```
- ```
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}
cp cli-config.yaml.example ~/.hermes/config.yaml
touch ~/.hermes/.env

# Añadir al menos una clave de proveedor LLM:
echo "OPENROUTER_API_KEY=***" >> ~/.hermes/.env
```
- ```
# Enlace simbólico para acceso global
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes

# Verificar
hermes doctor
hermes chat -q "Hola"
```
- ```
# Preferido — coincide con CI (entorno hermético, 4 workers xdist); ver AGENTS.md
scripts/run_tests.sh

# Alternativa (activa el venv primero). El wrapper sigue recomendándose
# para paridad con GitHub Actions antes de abrir un PR:
pytest tests/ -v
```
- ```
hermes-agent/
├── run_agent.py              # Clase AIAgent — bucle de conversación central, despacho de herramientas, persistencia de sesión
├── cli.py                    # Clase HermesCLI — TUI interactiva, integración prompt_toolkit
├── model_tools.py            # Orquestación de herramientas (capa delgada sobre tools/registry.py)
├── toolsets.py               # Agrupaciones y presets de herramientas (hermes-cli, hermes-telegram, etc.)
├── hermes_state.py           # Base de datos de sesiones SQLite con búsqueda de texto completo FTS5, títulos de sesión
├── batch_runner.py           # Procesamiento en lote paralelo para generación de trayectorias
│
├── agent/                    # Internos del agente (módulos extraídos)
│   ├── prompt_builder.py         # Ensamblaje del prompt del sistema (identidad, habilidades, archivos de contexto, memoria)
│   ├── context_compressor.py     # Auto-resumición al acercarse a los límites de contexto
│   ├── auxiliary_client.py       # Resuelve clientes OpenAI auxiliares (resumición, visión)
│   ├── display.py                # KawaiiSpinner, formateo del progreso de herramientas
│   ├── model_metadata.py         # Longitudes de contexto del modelo, estimación de tokens
│   └── trajectory.py             # Ayudantes para guardar trayectorias
│
├── hermes_cli/               # Implementaciones de comandos CLI
│   ├── main.py                   # Punto de entrada, análisis de argumentos, despacho de comandos
│   ├── config.py                 # Gestión de configuración, migración, definiciones de variables de entorno
│   ├── setup.py                  # Asistente de configuración interactivo
│   ├── auth.py                   # Resolución de proveedor, OAuth, Nous Portal
│   ├── models.py                 # Listas de selección de modelos de OpenRouter
│   ├── banner.py                 # Banner de bienvenida, arte ASCII
│   ├── commands.py               # Registro central de comandos de barra (CommandDef), autocompletado, ayudantes del gateway
│   ├── callbacks.py              # Callbacks interactivos (aclarar, sudo, aprobación)
│   ├── doctor.py                 # Diagnósticos
│   ├── skills_hub.py             # CLI del Skills Hub + comando de barra /skills
│   └── skin_engine.py            # Motor de skins/temas — personalización visual de CLI basada en datos
│
├── tools/                    # Implementaciones de herramientas (auto-registradas)
│   ├── registry.py               # Registro central de herramientas (esquemas, manejadores, despacho)
│   ├── approval.py               # Detección de comandos peligrosos + aprobación por sesión
│   ├── terminal_tool.py          # Orquestación del terminal (sudo, ciclo de vida del entorno, backends)
│   ├── file_operations.py        # read_file, write_file, búsqueda, patch, etc.
│   ├── web_tools.py              # web_search, web_extract (Paralelo/Firecrawl + resumición Gemini)
│   ├── vision_tools.py           # Análisis de imágenes a través de modelos multimodales
│   ├── delegate_tool.py          # Lanzamiento de subagentes y ejecución paralela de tareas
│   ├── code_execution_tool.py    # Python sandboxado con acceso a herramientas vía RPC
│   ├── session_search_tool.py    # Búsqueda en conversaciones pasadas con FTS5 + ventanas ancladas
│   ├── cronjob_tools.py          # Gestión de tareas programadas
│   ├── skill_tools.py            # Búsqueda, carga y gestión de habilidades
│   └── environments/             # Backends de ejecución del terminal
│       ├── base.py                   # ABC BaseEnvironment
│       ├── local.py, docker.py, ssh.py, singularity.py, modal.py, daytona.py
│
├── gateway/                  # Gateway de mensajería
│   ├── run.py                    # GatewayRunner — ciclo de vida de plataformas, enrutamiento de mensajes, cron
│   ├── config.py                 # Resolución de configuración de plataformas
│   ├── session.py                # Almacén de sesiones, prompts de contexto, políticas de reset
│   └── platforms/                # Adaptadores de plataformas
│       ├── telegram.py, discord_adapter.py, slack.py, whatsapp.py
│
├── scripts/                  # Scripts del instalador y puente
│   ├── install.sh                # Instalador Linux/macOS
│   ├── install.ps1               # Instalador Windows PowerShell
│   └── whatsapp-bridge/          # Puente WhatsApp Node.js (Baileys)
│
├── skills/                   # Habilidades incluidas (copiadas a ~/.hermes/skills/ en la instalación)
├── optional-skills/          # Habilidades opcionales oficiales (descubribles vía hub, no activadas por defecto)
├── tests/                    # Suite de tests
├── website/                  # Sitio de documentación (hermes-agent.nousresearch.com)
│
├── cli-config.yaml.example   # Configuración de ejemplo (copiada a ~/.hermes/config.yaml)
└── AGENTS.md                 # Guía de desarrollo para asistentes de codificación IA
```
- | `~/.hermes/.env` | Claves API y secretos |
- ```
Mensaje del usuario → AIAgent._run_agent_loop()
  ├── Construir prompt del sistema (prompt_builder.py)
  ├── Construir kwargs de API (modelo, mensajes, herramientas, configuración de razonamiento)
  ├── Llamar al LLM (API compatible con OpenAI)
  ├── Si tool_calls en la respuesta:
  │     ├── Ejecutar cada herramienta a través del despacho del registro
  │     ├── Añadir resultados de herramientas a la conversación
  │     └── Volver a la llamada al LLM
  ├── Si respuesta de texto:
  │     ├── Persistir sesión en DB
  │     └── Devolver final_response
  └── Compresión de contexto si se acerca al límite de tokens
```
- **Inyección efímera**: Los prompts del sistema y los mensajes de relleno se inyectan en el momento de la llamada API, nunca se persisten en la base de datos ni en los logs.
- **Abstracción de proveedor**: El agente funciona con cualquier API compatible con OpenAI. La resolución del proveedor ocurre en el momento de la inicialización.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
