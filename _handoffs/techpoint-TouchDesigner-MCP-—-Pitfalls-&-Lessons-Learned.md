---
layout: default
title: 技术点 · TouchDesigner MCP — Pitfalls & Lessons Learned
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · TouchDesigner MCP — Pitfalls & Lessons Learned

> 来源：261010_TouchDesigner MCP — Pitfalls & Lessons Learned_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
def safe_par(node, name, value):
    p = getattr(node.par, name, None)
    if p is not None:
        p.val = value
        return True
    return False
```
- ```
# WRONG — crashes if param doesn't exist:
node.par.nonexistent = value

# CORRECT — defensive access:
if hasattr(node.par, 'nonexistent'):
    node.par.nonexistent = value
```
- ```
menuNames: ['useinput','eighth','quarter','half','2x','4x','8x','fit','limit','custom','parpanel']
```
- ```
node.par.outputresolution = 'custom'  # correct
node.par.resolutionw = 1280; node.par.resolutionh = 720
```
- ```
gl.par.value0name = 'uTime'
gl.par.value0.expr = "absTime.seconds"
# In GLSL: uniform float uTime;
```
- ```
t = root.create(constantTOP, 'time_driver')
t.par.format = 'rgba32float'
t.par.outputresolution = 'custom'
t.par.resolutionw = 1; t.par.resolutionh = 1
t.par.colorr.expr = "absTime.seconds % 1000.0"
t.outputConnectors[0].connect(glsl.inputConnectors[0])
```
- ```
fragColor = TDOutputSwizzle(color);
```
- ```
# Agent side: write shader to /tmp/shader.glsl via write_file
# TD side:
sd = root.create(textDAT, 'shader_code')
with open('/tmp/shader.glsl', 'r') as f:
    sd.text = f.read()
```
- ```
kids = list(root.children)  # snapshot
for child in kids:
    if child.valid:  # check — earlier destroys may cascade
        child.destroy()
```
- ```
# td_execute_python:
for c in list(root.children):
    if c.valid and c.name.startswith('my_'):
        c.destroy()
# ... then create my_audio, my_shader etc. in same script → CRASHES
```
- ```
# Call 1: td_execute_python — clean only
for c in list(root.children):
    if c.valid and c.name.startswith('my_'):
        c.destroy()

# Call 2: td_execute_python — build (separate MCP call)
audio = root.create(audiofileinCHOP, 'my_audio')
# ... rest of build
```
- ```
fb = root.create(feedbackTOP, 'fb_delay')
fb.par.top = comp.path          # reference only — no wire to fb input
fb.outputConnectors[0].connect(xf)  # fb output -> transform -> fade -> comp
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
