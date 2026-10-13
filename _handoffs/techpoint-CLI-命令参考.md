---
layout: default
title: 技术点 · CLI 命令参考
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · CLI 命令参考

> 来源：261010_CLI 命令参考_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- title: "CLI 命令参考"
- description: "Hermes 终端命令及命令族的权威参考"
- 本页介绍从 shell 运行的**终端命令**。
- 关于聊天内斜杠命令，请参阅 [斜杠命令参考](./slash-commands.md)。
- ```
hermes [global-options] <command> [subcommand/options]
```
- | `--profile <name>`, `-p <name>` | 选择本次调用使用的 Hermes profile（配置文件）。覆盖 `hermes profile use` 设置的粘性默认值。 |
- | `--yolo` | 跳过危险命令的审批提示。 |
- | `--ignore-user-config` | 忽略 `~/.hermes/config.yaml`，回退到内置默认值。`.env` 中的凭据仍会加载。 |
- | 命令 | 用途 |
- | `hermes gateway` | 运行或管理消息 gateway 服务。 |
- | `hermes proxy` | 本地 OpenAI 兼容代理，附加 OAuth provider 凭据。参见 [订阅代理](../user-guide/features/subscription-proxy.md)。 |
- | `hermes setup` | 全部或部分配置的交互式设置向导。 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
