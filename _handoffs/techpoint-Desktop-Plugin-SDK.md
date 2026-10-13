---
layout: default
title: 技术点 · Desktop Plugin SDK
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Desktop Plugin SDK

> 来源：261010_Desktop Plugin SDK_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- description: "Extend the native Hermes Desktop app — panes, pages, sidebar nav, status bar, palette commands, keybinds, themes, and a scoped backend namespace, with one import and no build step."
- entries, keybinds, themes — registers into one central registry. Core registers
- The three do not share code, APIs, or delivery. Only the backend `plugin_api.py`
- namespace (`/api/plugins/<id>`) is shared between the desktop and dashboard SDKs.
- (`/api/plugins/<id>`) if you ship a `plugin_api.py`.
- ```
// ~/.hermes/desktop-plugins/hello/plugin.js
import { host, haptic, useValue } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

function HelloPane() {
  const gateway = useValue(host.state.gateway)

  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm',
    children: [
      jsx('div', { className: 'font-medium', children: 'Hello, Hermes' }),
      jsx('div', {
        className: 'text-(--ui-text-tertiary)',
        children: `gateway: ${gateway}`
      })
    ]
  })
}

export default {
  id: 'hello', // must match the folder name
  name: 'Hello',
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'hello',
      data: { placement: 'right', width: '260px' },
      render: () => jsx(HelloPane, {})
    })
    ctx.register({
      id: 'chip',
      area: 'statusBar.right',
      order: 130,
      render: () =>
        jsx('button', {
          type: 'button',
          className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
          onClick: () => {
            haptic('tap')
            host.notify({ kind: 'info', message: 'Hello from my plugin!' })
          },
          children: 'hello'
        })
    })
  }
}
```
- ```
interface HermesPlugin {
  /** Stable slug — becomes the `plugin:<id>` source and the id namespace. */
  id: string
  /** Human name for Settings / about UI. Defaults to `id`. */
  name?: string
  /** Registers on load when the user hasn't chosen (default true). Set false
   *  for opt-in plugins: they inventory in Capabilities ▸ Plugins, off until the
   *  user flips the switch. */
  defaultEnabled?: boolean
  /** Called once at load; wire contributions through `ctx`. */
  register: (ctx: PluginContext) => void
}
```
- ```
interface PluginContext {
  /** Resolved source tag, e.g. `'plugin:hello'`. */
  readonly source: string
  /** Register one contribution (id namespaced, source stamped). Returns a disposer. */
  register: (c: PluginContribution) => () => void
  /** Register several at once; the returned disposer removes all of them. */
  registerMany: (cs: PluginContribution[]) => () => void
  /** REST to this plugin's own backend namespace (`/api/plugins/<id>`). */
  rest: <T>(path: string, opts?: PluginRestOptions) => Promise<T>
  /** Live WebSocket to this plugin's own namespace. Returns a disposer. */
  socket: (path: string, onMessage: (data: unknown) => void) => () => void
  /** Gateway event stream by type (`'*'` = all). Tracked: removed on unload/reload/disable. */
  onEvent: (type: string, listener: (event: GatewayEvent) => void) => () => void
  /** Any other cleanup to run on unload/reload/disable (store subscriptions, injected DOM). */
  onDispose: (fn: () => void) => void
  /** Scoped timers and DOM listeners — cleared with the plugin. Each returns a disposer. */
  setTimeout: (fn: () => void, ms: number) => () => void
  setInterval: (fn: () => void, ms: number) => () => void
  addEventListener: (target: EventTarget, type: string, listener: EventListener, options?: AddEventListenerOptions | boolean) => () => void
  /** The curated OS door: native notification, open-external, reveal-in-file-manager, clipboard. */
  os: PluginOs
  /** Plugin-scoped JSON persistence (keys live under `hermes.plugin.<id>.`). */
  storage: PluginStorage
}
```
- ```
interface Contribution {
  id: string          // you write the local id; the host namespaces it
  area: string        // WHERE it goes (a contribution-area constant)
  title?: string
  order?: number      // sort within the area (lower = earlier)
  when?: () => boolean // dynamic visibility; re-evaluated by the area
  enabled?: boolean
  render?: () => ReactNode  // the component to mount
  data?: unknown      // area-specific payload (see the cookbook)
}
```
- | Keybind | `KEYBINDS_AREA` | `data: KeybindContribution` |
- ```
ctx.register({
  id: 'pane',
  area: 'panes',
  title: 'my pane',
  data: { placement: 'right', width: '260px' },
  render: () => jsx(MyPane, {})
})
```
- ```
// Below the conversation, 200px tall.
data: {
  placement: 'bottom',
  dock: { pane: 'workspace', pos: 'bottom' },
  height: '200px'
}
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
