---
layout: default
title: 技术点 · Subagent Delegation
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Subagent Delegation

> 来源：261010_Subagent Delegation_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- An unavailable API-server route stays pending without repeated missing-route warnings.
- Malformed messaging routes still produce diagnostics. On the API server, an async delegation
- ```
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42"
)
```
- ```
delegate_task(tasks=[
    {"goal": "Research topic A", "context": "Focus on recent primary sources"},
    {"goal": "Research topic B", "context": "Compare the leading explanations"},
    {"goal": "Fix the build", "context": "Project root: /home/user/project"}
])
```
- ```
delegate_task(
    tasks=[{
        "goal": "Check which of these three endpoints return 200",
        "context": "https://a.example, https://b.example, https://c.example",
        "output_schema": {
            "type": "object",
            "properties": {
                "healthy": {"type": "array", "items": {"type": "string"}},
                "failing": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["healthy", "failing"]
        }
    }]
)
```
- ```
# BAD - subagent has no idea what "the error" is
delegate_task(goal="Fix the error")

# GOOD - subagent has all context it needs
delegate_task(
    goal="Fix the TypeError in api/handlers.py",
    context="""The file api/handlers.py has a TypeError on line 47:
    'NoneType' object has no attribute 'get'.
    The function process_request() receives a dict from parse_body(),
    but parse_body() returns None when Content-Type is missing.
    The project is at /home/user/myproject and uses Python 3.11."""
)
```
- ```
delegate_task(tasks=[{
    "goal": "Compare the rendered dashboard against the design mock and list layout deviations",
    "context": "The app runs at http://localhost:3000; the repo is at /home/user/dash.",
    "images": ["/home/user/mocks/dashboard-v2.png",
               "https://cdn.example.com/current-render.png"],
}])
```
- ```
delegate_task(tasks=[
    {
        "goal": "Research the current state of WebAssembly in 2025",
        "context": "Focus on: browser support, non-browser runtimes, language support"
    },
    {
        "goal": "Research the current state of RISC-V adoption in 2025",
        "context": "Focus on: server chips, embedded systems, software ecosystem"
    },
    {
        "goal": "Research quantum computing progress in 2025",
        "context": "Focus on: error correction breakthroughs, practical applications, key players"
    }
])
```
- ```
delegate_task(
    goal="Review the authentication module for security issues and fix any found",
    context="""Project at /home/user/webapp.
    Auth module files: src/auth/login.py, src/auth/jwt.py, src/auth/middleware.py.
    The project uses Flask, PyJWT, and bcrypt.
    Focus on: SQL injection, JWT validation, password handling, session management.
    Fix any issues found and run the test suite (pytest tests/auth/)."""
)
```
- ```
delegate_task(
    goal="Refactor all Python files in src/ to replace print() with proper logging",
    context="""Project at /home/user/myproject.
    Use the 'logging' module with logger = logging.getLogger(__name__).
    Replace print() calls with appropriate log levels:
    - print(f"Error: ...") -> logger.error(...)
    - print(f"Warning: ...") -> logger.warning(...)
    - print(f"Debug: ...") -> logger.debug(...)
    - Other prints -> logger.info(...)
    Don't change print() in test files or CLI output.
    Run pytest after to verify nothing broke."""
)
```
- ```
{"tasks": [
  {"goal": "Review PR #101 ..."},
  {"goal": "Review PR #102 ..."},
  {"goal": "Benchmark approach A ...", "group": "bench"},
  {"goal": "Benchmark approach B ...", "group": "bench"}
]}
```
- ```
delegation:
  surface_child_process_notifications: true   # default: false
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
