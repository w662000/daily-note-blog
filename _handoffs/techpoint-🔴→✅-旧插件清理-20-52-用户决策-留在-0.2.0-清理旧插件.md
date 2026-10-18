---
layout: default
title: 技术点 · 🔴→✅ 旧插件清理（20:52 用户决策：留在 0.2.0，清理旧插件）
date: 2026-10-18 23:30:00 +0800
---

# 技术点 · 🔴→✅ 旧插件清理（20:52 用户决策：留在 0.2.0，清理旧插件）

> 来源：261018_🔴→✅ 旧插件清理（20_52 用户决策：留在 0.2.0，清理旧插件）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
**最终状态（21:50 验证）：dsh web 零警告零失败启动，Web UI 完全可用。**

| 插件 | 处理 | 结果 |
|---|---|---|
| dsh-better-sidebar | 0.13.1 → **0.28.0**（0.2.x 线构建，peer 要 ^0.2.1-rc.1） | ✅ 官方 `allow-version --accept-risk` 豁免后装上，启动无警告 |
| @linxin666/dsh-web-ui-all（含 aionui-panel/settings/task-board/pet/skin-center/ssh 等 10+ 客户端组件） | 移除 | ✅ registry 最新 0.3.6 仍是 8 月底 0.1.x 构建，无 0.2.x 适配版 |
| @omdsh-dev/dsh-genui | 移除 | ✅ 本地 vendor，registry 404 |
| dsh-discovery | 移除 | ✅ 本地定制 0.1.0，无新版 |
| @ccchase/dsh-plugin-wechat | 移除 | ✅ 0.3.0 已是最新仍坏 |
| dsh-at-file | 移除 | ✅ vendor 版已是最新 0.6.3 仍坏 |

**关键机制发现（踩坑）**：插件行存放在**三处**——① `profiles/web/package.json` 的 dependencies + bundles；② `cordis.yml`；③ **`cordis.patch.yml`（用户个人补丁层，548 行）**。`dsh plugin remove` 只清 ①，残留在 ③ 里的行会继续强制加载（wechat-bridge 和 describe-image 就是从这来的，导致卸了还在 boot 图里、import failed）。必须手工编辑 cordis.patch.yml 切除（备份：`cordis.patch.yml.bak-pre-cleanup-20261018-214536`）。注意区分：patch 里的 `wechat:` provider 配置（LLM 提供商）要保留，只删插件行。

**最终 profile**：bundles = dsh-base + dsh-web-app + better-sidebar + agent-teams；启动输出干净（无 skipping/failed to import/did not activate）。

**当前服务**：PID 60，监听 3080。token URL（每次重启会变）：
`http://127.0.0.1:3080/?token=8hvvOAQd4b2KG8QGKT71ZA4-v4cI3W5u5N2BVTj9ric`

**副作用提醒**：dsh 0.2.x 首次启动把 `~/.dsh/settings.yaml` 迁移成了 `settings.yaml.imported`（旧设置已导入）；微信桥接移除后微信消息不再进 DSH 会话；Web UI 少了 genui/任务板/宠物/皮肤中心/ssh 等扩展面板。

---

### 关键技术要点（自动抽取）
- **关键机制发现（踩坑）**：插件行存放在**三处**——① `profiles/web/package.json` 的 dependencies + bundles；② `cordis.yml`；③ **`cordis.patch.yml`（用户个人补丁层，548 行）**。`dsh plugin remove` 只清 ①，残留在 ③ 里的行会继续强制加载（wechat-bridge 和 describe-image 就是从这来的，导致卸了还在 boot 图里、import failed）。必须手工编辑 cordis.patch.yml 切除（备份：`cordis.patch.yml.bak-pre-cleanup-20261018-214536`）。注意区分：patch 里的 `wechat:` provider 配置（LLM 提供商）要保留，只删插件行。
- **当前服务**：PID 60，监听 3080。token URL（每次重启会变）：
- `http://127.0.0.1:3080/?token=8hvvOAQd4b2KG8QGKT71ZA4-v4cI3W5u5N2BVTj9ric`
- 关键机制发现（踩坑）**：插件行存放在**三处**——① `profiles/web/package.json` 的 dependencies + bundles；② `cordis.yml`；③ **`cordis.patch.yml`（用户个人补丁层，548 行）**。`dsh plugin remove` 只清 ①，残留在 ③ 里的行会继续强制加载（wechat-bridge 和 describe-image 就是从这来的，导致卸了还在 boot 图里、import failed）。必须手工编辑 cordis.patch.yml 切除（备份：`cordis.patch.yml.bak-pre-cleanup-20261018-214536`）。注意区分：patch 里的 `wechat:` provider 配置（LLM 提供商）要保留，只删插件行。

## 三、关键产物与命令
- 关键机制发现（踩坑）**：插件行存放在**三处**——① `profiles/web/package.json` 的 dependencies + bundles；② `cordis.yml`；③ **`cordis.patch.yml`（用户个人补丁层，548 行）**。`dsh plugin remove` 只清 ①，残留在 ③ 里的行会继续强制加载（wechat-bridge 和 describe-image 就是从这来的，导致卸了还在 boot 图里、import failed）。必须手工编辑 cordis.patch.yml 切除（备份：`cordis.patch.yml.bak-pre-cleanup-20261018-214536`）。注意区分：patch 里的 `wechat:` provider 配置（LLM 提供商）要保留，只删插件行。
- 副作用提醒**：dsh 0.2.x 首次启动把 `~/.dsh/settings.yaml` 迁移成了 `settings.yaml.imported`（旧设置已导入）；微信桥接移除后微信消息不再进 DSH 会话；Web UI 少了 genui/任务板/宠物/皮肤中心/ssh 等扩展面板。

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
