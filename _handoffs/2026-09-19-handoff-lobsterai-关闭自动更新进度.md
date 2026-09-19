---
layout: default
title: 交接文档 · LobsterAI 关闭自动更新进度
date: 2026-09-19 23:30:00 +0800
---

# LobsterAI 关闭自动更新进度

- **日期**：2026-09-19
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-09-19-12-31-24\lobsterai_disable_autoupdate_progress.md

## 背景
用户回滚到 2026.8.14 后，LobsterAI 仍自动检查并提示"发现新版本 v2026.9.4 / 立即更新"，且出现"更新已就绪 / 重启完成更新"卡片。需要在 asar 级别关闭自动检查、自动下载、以及已就绪状态的恢复与展示。

## 已执行操作
1. 关闭 LobsterAI 进程。
2. 备份原 `app.asar` 到：
   - `D:\AI work\workbuddy\2026-09-19-12-31-24\lobsterai_asar_patches\app.asar.bak_20260919_132749`
   - `D:\AI work\workbuddy\2026-09-19-12-31-24\lobsterai_asar_patches\app.asar.before_patch_20260919_133249`
3. 安装 asar 工具：`@electron/asar` 于 managed Node workspace。
4. 解包 `D:\Program Files\LobsterAI\resources\app.asar` 到工作目录。
5. 定位自动更新核心逻辑：`dist-electron\main\libs\appUpdateCoordinator.js`。
6. 实施四处 asar 级补丁：
   - **Patch 1**：`isUpdateDisabled()` 永远 `return true`，阻止新的检查、下载、安装。
   - **Patch 2**：`restoreStoredReadyState()` 开头直接 `return;`，启动时不再恢复 sqlite 里持久化的 ready 更新状态。
   - **Patch 3**：`getState()` 返回状态前强制检查，若状态为 `Ready` 或存在 `readyFilePath`，立即重置为 `Idle`，永远不把 Ready 状态暴露给渲染进程。
   - **Patch 4**：`shouldAutoOpenReadyModal()` 永远 `return false`，禁止自动弹出"更新已就绪"弹窗。
7. 删除已下载到本地的 2026.9.4 安装包：
   - 路径：`C:\Users\Administrator\AppData\Roaming\LobsterAI\updates\lobsterai-update-auto-1789800971150.exe`（约 255MB）
8. 删除 sqlite 中残留的 ready 记录：
   - `DELETE FROM kv WHERE key='app_update_ready_file:auto';`（删除 1 行）
9. 重新打包并替换原 `app.asar`。
10. 校验：新 asar 与打包文件 SHA256 一致；内部 `appUpdateCoordinator.js` 四个补丁标记均为 `true`。

## 当前状态
- ✅ 补丁已写入 `D:\Program Files\LobsterAI\resources\app.asar`
- ✅ 已删除已下载的新版安装包
- ✅ 已删除 sqlite 中的 `app_update_ready_file:auto` 记录
- ✅ 已确认 `%LOCALAPPDATA%\LobsterAI` 无额外缓存
- ⚠️ 因沙箱限制，无法在本会话了直接启动 GUI 程序做可视验证，需用户手动启动 LobsterAI 确认。

## 回滚方法
若补丁导致异常，可还原备份：
```bash
cp "D:\AI work\workbuddy\2026-09-19-12-31-24\lobsterai_asar_patches\app.asar.bak_20260919_132749" "D:\Program Files\LobsterAI\resources\app.asar"
```

## 备注
- 自动更新服务器域名：`api-overmind.youdao.com`
- 下载域名：`ydschool-video.nosdn.127.net`
- 2026.9.4 的安装包文件名：`lobsterai-update-auto-1789800971150.exe`
