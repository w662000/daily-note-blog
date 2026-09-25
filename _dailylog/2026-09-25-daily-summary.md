---
layout: default
title: 每日工作总结 · 2026-09-25
date: 2026-09-25 23:30:00 +0800
---

# 每日工作总结 · 2026-09-25

## 一、今日完成事项

1. **排查 lobsterai 连续弹出 git 控制台窗口问题**
   - 现象：用户反馈多个 git 窗口连续弹出
   - 根因：`cloud_daily.py` 流水线中的 `publish_site.py` 用 `subprocess.run(["git"]+args)` 调 git，父进程是 pythonw（无控制台），subprocess 没加 `CREATE_NO_WINDOW` 标志，每次 git 调用都弹黑框
   - 结论：非 Git Credential Manager 问题，纯窗口显示问题

2. **落地修复 git 弹窗问题**
   - 修改 `C:\Users\Administrator\lobsterai\project\publish_site.py`：在 `git()` 函数内加 `creationflags=CREATE_NO_WINDOW`
   - 修改 `C:\Users\Administrator\lobsterai\project\cloud_daily.py`：在 `run()` 函数的 subprocess.run 加 `creationflags=CREATE_NO_WINDOW`
   - 验证：两文件 py_compile 通过，grep 确认代码落地
   - 效果：下次计划任务拉起时自动生效，弹窗消除

3. **梳理 lobsterai cloud_daily 流水线用途**（应用户追问）
   - 调度机制：Windows 计划任务，周一至五 14:40-16:30 每5分钟
   - 三波任务：14:45 尾盘潜伏 / 15:30 涨停天梯 / 15:55 主线收盘
   - 子脚本链：update_daily → tianti → mainline_scan → cloud_notify → publish_site
   - 性质：个人 A 股复盘研究自动化，代码已注明"不构成投资建议"

## 二、关键决策 / 注意事项

- **修复策略**：用 `creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)` 安全写法，避免非 Windows 平台报错
- **验证方式**：py_compile + grep 双重确认，确保代码改动落地且语法正确
- **生效时机**：编辑时无残留进程，下次计划任务（交易日 14:40-16:30）自动用新代码，无需手动重启

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|-----------|------|------|
| 本总结 | `D:\AI work\workbuddy\2026-09-25_每日工作总结.md` | 当日工作总结 |
| publish_site.py | `C:\Users\Administrator\lobsterai\project\publish_site.py` | 修改后修复 git 弹窗 |
| cloud_daily.py | `C:\Users\Administrator\lobsterai\project\cloud_daily.py` | 修改后修复 git 弹窗 |

## 四、待办 / 风险

- ⏳ **无阻塞风险**：修复已落地，下次计划任务自动生效
- ℹ️ **待观察**：交易日 14:40-16:30 窗口期，验证 git push 无弹窗且正常推送
- 📝 **建议跟进**：可考虑给 lobsterai 项目加个 issue 记录此次修复，方便日后追溯
