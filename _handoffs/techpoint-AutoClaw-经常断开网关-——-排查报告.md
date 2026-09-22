---
layout: default
title: 技术点 · AutoClaw 经常断开网关 —— 排查报告
date: 2026-09-21 23:30:00 +0800
---

# 技术点 · AutoClaw 经常断开网关 —— 排查报告

> 来源：260921_AutoClaw 经常断开网关 —— 排查报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- 排查时间：2026-09-21 16:07
- 结论：**与 hosts 文件屏蔽域名无关**，是本地网关进程 native 崩溃。
- 路径 `C:\Windows\System32\drivers\etc\hosts`，只有 3 条，均为遥测类：
- ```
127.0.0.1 ieonline.Microsoft.com   # 微软 IE/Edge 遥测
127.0.0.1 xti.qq.com               # QQ 体验数据上报
::1       xti.qq.com
```
- 无任何 AutoClaw / 智谱 / openclaw 相关域名。且 AutoClaw 的云端接口
- （`autoglm-acceleration-api.zhipuai.cn`、`/userapi/v1/...`）在日志里能正常拿到 HTTP 响应
- （403、200 都是服务器返回的，说明网络通），DNS 层面无屏蔽。
- 形态：AutoClaw 主进程 fork 出的本地 Node 子进程
- ```
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
- 2. V8 native 崩溃 → 进程退出码 2147483651
- 3. 主进程检测 `gateway-exit-attempt-1` → `gateway.force_restart` → 自动重启
- `POST https://autoglm-acceleration-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw/chat/completions`

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
