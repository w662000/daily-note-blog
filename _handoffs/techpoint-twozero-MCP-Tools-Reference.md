---
layout: default
title: 技术点 · twozero MCP Tools Reference
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · twozero MCP Tools Reference

> 来源：261010_twozero MCP Tools Reference_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- Execute Python code inside TouchDesigner and return the result. Has full access to TD Python API (op, project, app, etc). Print statements and the last expression value are captured. Best for: wiring connections (inputConnectors), setting expressions (par.X.expr/mode), querying parameter names, and batch creation scripts (5+ operators). For creating 1-4 operators, prefer td_create_operator instead.
- | `parameters` | object | no | Key-value pairs of parameters to set on the created operator |
- | `parameters` | object | no | Key-value pairs of parameters to set |
- Capture a screenshot of the actual screen via TD's screenGrabTOP. Saves the image to a file and returns the file path. Use your file-reading tool to view the image. Unlike td_get_screenshot (operator viewer), this shows what the user literally sees on their monitor — TD windows, UI panels, everything. Use when simulating mouse/keyboard input to verify what happened on screen. Workflow: td_get_screen_screenshot → read file → td_input_execute → wait idle → td_get_screen_screenshot again. TWO-STEP ASYNC: Step 1 — call without request_id: returns {'status':'pending','requestId':'...'}. Step 2 — call with request_id: returns {'file': '/tmp/.../screen_id.jpg', 'info': '...metadata...'}. Then read the file to see the image. The requestId also stays usable with td_screen_point_to_global for later coordinate lookup. crop_x/y/w/h are in ACTUAL SCREEN PIXELS (not image pixels). Crops exceeding screen bounds are auto-clamped. SMART DEFAULTS: max_size is auto when omitted — 1920 for full screen (good overview), max(crop_w,crop_h) for cropped (guarantees 1:1 scale). At 1:1 scale: screen_coord = crop_origin + image_pixel. Otherwise use the formula from metadata.
- Send a sequence of mouse/keyboard commands to TouchDesigner. Commands execute sequentially with smooth bezier movement. Returns immediately — poll td_input_status() until status='idle' before proceeding. Command types: 'focus' — bring TD to foreground. 'move' — smooth mouse move: {type,x,y,duration,easing}. 'click' — click: {type,x,y,button,hold,duration,easing}. hold=seconds to hold down. duration=smooth move before click. 'dblclick' — double click: {type,x,y,duration}. 'mousedown'/'mouseup' — {type,x,y,button}. 'key' — keystroke: {type,keys} e.g. 'ctrl+z','tab','escape','shift+f5'. Requires Accessibility permission on Mac. 'type' — human-like typing: {type,text,wpm,variance} — layout-independent Unicode, variable timing. 'wait' — pause: {type,duration}. 'scroll' — {type,x,y,dx,dy,steps} — human-like scroll: moves mouse to (x,y) first, then sends dy (vertical, +up) and dx (horizontal, +right) as multiple ticks with natural timing. steps=4 by default. Mouse commands may include coord_space='logical' (default) or coord_space='physical'. On macOS, 'physical' means actual screen pixels from td_get_screen_screenshot and is converted to CGEvent logical coords automatically. Top-level coord_space applies to commands that do not override it. on_error: 'stop' (default) clears queue on error; 'continue' skips failed command. IMPORTANT: call td_get_hints('input_simulation') before first use to learn focus recovery, coordinate systems, and testing workflow.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
