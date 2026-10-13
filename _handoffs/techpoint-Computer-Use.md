---
layout: default
title: 技术点 · Computer Use
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Computer Use

> 来源：261010_Computer Use_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- cursor doesn't move, keyboard focus doesn't change, and your virtual
- | Linux | AT-SPI (X11 + Wayland) | XTest (X11) / virtual-keyboard (Wayland) |
- ```
hermes computer-use install
```
- ```
hermes -t computer_use chat
```
- browser route; a leftover key in config.yaml is ignored.
- ```
# config.yaml
computer_use:
  permission_mode: bounded
  capability_manifest: ~/.hermes/cua-manifest.yaml
```
- ```
# config.yaml
computer_use:
  allow_unsigned_driver: true   # local driver development only
```
- ```
$ hermes computer-use doctor
⚠️  cua-driver VERSION on darwin: degraded
  ✅ binary_version: cua-driver VERSION
  ✅ platform_supported: macOS 26.4.1 (arm64)
  ✅ session_active: MCP session is active.
  ❌ bundle_identity: Process has no CFBundleIdentifier.
      → Run the binary inside CuaDriver.app so TCC grants attribute correctly.
  ✅ tcc_accessibility: Accessibility is granted.
  ✅ tcc_screen_recording: Screen Recording is granted.
  ✅ ax_capability: AX is trusted and reachable.
  ✅ screen_capture_capability: ScreenCaptureKit reachable; 1 display(s) shareable.
```
- ```
cua-driver skills install
```
- (`get_window_state`, `element_token`, `snapshot_id`), which the `computer_use`
- 4. `computer_use(action="key", keys="return", capture_after=True)` —
- Destructive actions (click, type, drag, scroll, key, focus_app)

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
