---
layout: default
title: 交接文档 · AutoClaw 经常断开网关 —— 排查报告
date: 2026-09-22 23:30:00 +0800
---

# AutoClaw 经常断开网关 —— 排查报告

- **日期**：2026-09-21
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-09-21-16-06-46\autoclaw网关断开诊断_20260921.md

排查时间：2026-09-21 16:07
结论：**与 hosts 文件屏蔽域名无关**，是本地网关进程 native 崩溃。

## 一、hosts 文件实际内容

路径 `C:\Windows\System32\drivers\etc\hosts`，只有 3 条，均为遥测类：

```
127.0.0.1 ieonline.Microsoft.com   # 微软 IE/Edge 遥测
127.0.0.1 xti.qq.com               # QQ 体验数据上报
::1       xti.qq.com
```

无任何 AutoClaw / 智谱 / openclaw 相关域名。且 AutoClaw 的云端接口
（`autoglm-acceleration-api.zhipuai.cn`、`/userapi/v1/...`）在日志里能正常拿到 HTTP 响应
（403、200 都是服务器返回的，说明网络通），DNS 层面无屏蔽。

## 二、网关的真实形态

- 地址：`ws://127.0.0.1:18889`（本机回环），日志中 `runtimeTarget: local`、
  `usingExternalGateway: false`、`remote=127.0.0.1`
- 形态：AutoClaw 主进程 fork 出的本地 Node 子进程
  （`D:\Program Files\AutoClaw\resources\node\node.exe gateway-launcher.cjs gateway run --port 18789`）
- **本机回环不经过 DNS，hosts 屏蔽任何域名都影响不到它**

## 三、真正的原因：V8 native 崩溃

`C:\Users\Administrator\.openclaw-autoclaw\logs\gateway.log` 中出现：

```
# Fatal error in , line 0
# Check failed: (location_) != nullptr.
#FailureMessage Object: 00000073415FEA30
------ Native stack trace -----
 3: V8_Fatal+197
 5: v8::SharedValueConveyor::SharedValueConveyor+386753
15: node::CallbackScope::~CallbackScope+534
20: uv_run+1007
21: node::SpinEventLoop+405
```

- 退出码 `2147483651` = `0x80000003` = STATUS_BREAKPOINT（V8_Fatal 触发）
- 今天已崩溃 **2 次**：16:03:41（childPid 8932）、16:06:02（childPid 2356）
- 不是 JS heap OOM（rss 725MB / heapUsed 439MB，未触及上限），是 V8 内部 CHECK 失败
- 崩溃点两次都紧跟在 `[bundle-mcp]` 批量启动 connector 之后
  （lexiang / ima / tianyancha / feishu 启动失败或需 OAuth）

崩溃前征兆：

- `config.get` 耗时 11045ms / 9919ms / 10036ms（正常 50–500ms）
- health 快照：`eventLoop.degraded=true, reasons=["event_loop_utilization","cpu"], utilization=1`
- `startup model warmup timed out after 5000ms`
- `[ws] handshake timeout ... 127.0.0.1:14181->127.0.0.1:18889`

## 四、断开的完整链路

1. 网关 event loop 打满（config.get 10 秒级、MCP 批量连接）
2. V8 native 崩溃 → 进程退出码 2147483651
3. 主进程检测 `gateway-exit-attempt-1` → `gateway.force_restart` → 自动重启
4. 重启耗时 20–60 秒（startup trace total 最大 59245ms）
5. 期间 ws `code=1006` 异常关闭、`Connection stalled (status=handshaking) for 120s, forcing reset`
6. 界面显示"网关断开"，正在跑的任务被中断（`gateway.client.disconnect.runs_interrupted`）

今天统计（autoclaw-dev.log）：disconnect 10 次、reconnect 8 次、
GatewayServiceRestart 6 次、force_restart 4 次。

## 五、附带发现（另一回事）

日志里有 `403 status code (no body)`：
`POST https://autoglm-acceleration-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions`
这是模型鉴权/配额问题，服务器返回了 403 = 网络是通的，与 hosts、与网关断开都无关。
可用已有的 `autoclaw-403-diagnose` skill 单独处理。

## 六、可选的缓解方向（未执行，等你确认）

1. 在配置里关闭未授权/用不到的 bundle MCP connector（lexiang、ima、tianyancha、feishu
   每次启动都尝试连接且失败，是最直接的触发面）
2. 清理旧会话（当前 39 个 session）、减少常驻插件
3. 升级 AutoClaw / 其内置 Node（V8 CHECK 失败多为引擎侧 bug）
4. 观察 cron 任务频率（当前每 60 秒 cron.list 轮询）

## 七、关键路径备查

| 用途 | 路径 |
| --- | --- |
| 网关日志 | `C:\Users\Administrator\.openclaw-autoclaw\logs\gateway.log` |
| 主进程日志 | `C:\Users\Administrator\.openclaw-autoclaw\logs\autoclaw-dev.log` |
| 崩溃退出记录 | 搜 `2147483651` / `Fatal error in` |
| 配置 | `C:\Users\Administrator\.openclaw-autoclaw\openclaw.json` |
| 网关 token | `C:\Users\Administrator\.openclaw-autoclaw\.gateway-token` |
