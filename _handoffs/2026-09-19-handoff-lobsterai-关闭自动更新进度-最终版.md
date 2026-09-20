---
layout: default
title: 交接文档 · LobsterAI 关闭自动更新进度（最终版）
date: 2026-09-20 23:30:00 +0800
---

# LobsterAI 关闭自动更新进度（最终版）

- **日期**：2026-09-19
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-09-19-12-31-24\lobsterai_disable_autoupdate_progress.md

## 背景
用户回滚到 2026.8.14 后，LobsterAI 仍自动检查、下载新版并弹出"更新已就绪 / 重启完成更新"。目标：彻底关闭自动检查、自动下载、以及已就绪状态的恢复与展示。

## 三轮排查与最终根因

### 第一轮（错误方向）
- 定位到 `dist-electron/main/libs/appUpdateCoordinator.js`，patch 了 `isUpdateDisabled()` 和 `restoreStoredReadyState()`。
- **失败原因：改的不是运行时加载的文件。**

### 第二轮（仍无效）
- 清理了已下载的安装包与 sqlite 里的 `app_update_ready_file:auto` 记录，并在 libs 文件上追加了 `getState()`、`shouldAutoOpenReadyModal()` 两道保险。
- **仍然失败。** 日志出现 `restoring persisted ready file` / `begin flow`，且从未出现补丁该打印的 `updates are disabled by enterprise config`。

### 第三轮（找到真凶）✅
- 进程路径确认：`D:\Program Files\LobsterAI\LobsterAI.exe`（唯一安装，另一个是备份）。
- `package.json` 的 `main` 字段 = **`dist-electron/main.js`**，这是一个 **10MB / 25万行的 bundle**，内部**内联了完整的 AppUpdateCoordinator 类**。
- `dist-electron/main/libs/appUpdateCoordinator.js` 只是未被加载的源码副本（死代码），`main.js.map` 是它的 sourcemap。
- `app.asar.unpacked` 里没有 appUpdate 相关 JS（只有 better-sqlite3、npm），排除"副本覆盖加载"可能。
- 结论：**运行时执行的是 bundle 里的副本**，必须 patch `dist-electron/main.js`。

## 最终补丁（打在 dist-electron/main.js bundle 内）
| 补丁 | 方法 | 作用 |
|---|---|---|
| 1 | `isUpdateDisabled()` | 永远 `return true`，阻止检查/下载/安装，并触发 resetToIdle |
| 2 | `restoreStoredReadyState()` | 开头 `return;`，启动时不再恢复 sqlite 持久化的 ready 状态 |
| 3 | `shouldAutoOpenReadyModal()` | 永远 `return false`，禁止自动弹出更新弹窗 |
| 4 | `getState()` | 若状态为 Ready 或存在 readyFilePath，强制重置为 initialState() |

bundle 内可用标识符已确认：`initialState`（65969 行定义）、`AppUpdateStatus`（560 行，`Idle: "idle"`）。

## 执行记录
1. 关闭 LobsterAI 进程。
2. 备份原 asar：`app.asar.bak_20260919_132749`、`app.asar.before_patch_20260919_133249`。
3. 解包 → patch bundle（4 处，均通过唯一性校验 occurrences=1）→ 重新打包 → 替换。
4. 清理重新下载的安装包 `lobsterai-update-auto-1789802168630.exe`（~255MB）。
5. 清理 sqlite 的 `app_update_ready_file:auto` / `:manual` 记录（本次均为 0 行，已被上轮清掉）。

## 当前状态
- ✅ 补丁已写入 `D:\Program Files\LobsterAI\resources\app.asar`
- ✅ installed asar SHA256：`987d8a136577c14eec9b4e872e6e4564c91650cb121ad2a50444a3bf5ad6b348`
- ✅ 从 installed asar 提取 `dist-electron/main.js` 复核，四个补丁标记全部为 `true`
- ✅ updates 目录已清空，sqlite 无 ready 记录
- ⚠️ 沙箱无法启动 GUI 做可视验证，需用户手动启动确认

## 回滚方法
```bash
cp "D:\AI work\workbuddy\2026-09-19-12-31-24\lobsterai_asar_patches\app.asar.bak_20260919_132749" "D:\Program Files\LobsterAI\resources\app.asar"
```

## 关键教训（可复用）
- **patch Electron asar 前，先看 `package.json` 的 `main` 字段确认真正入口。**
- 构建产物常是 bundle：源码目录（如 `main/libs/*.js`）可能与 bundle 内同名代码并存，**改错文件会静默失效**。
- 验证补丁是否真的执行，靠**运行时日志里的特征字符串**（如本例 `updates are disabled by enterprise config`），而不是只检查文件里的补丁标记是否存在。
- 相关域名：更新接口 `api-overmind.youdao.com`，下载 `ydschool-video.nosdn.127.net`。
