---
layout: default
title: 技术点 · 联想 N50-80 双系统部署清单：Win10 + Debian + Hermes 数据共享
date: 2026-08-05 23:30:00 +0800
---

# 技术点 · 联想 N50-80 双系统部署清单：Win10 + Debian + Hermes 数据共享

> 来源：260805_联想 N50-80 双系统部署清单：Win10 + Debian + Hermes 数据共享_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260805_联想 N50-80 双系统部署清单：Win10 + Debian + Hermes 数据共享_handoff.md（编码探测：utf-8）
- > 来源：2026-08-05-20-56-42\N50-80_Win10+Debian双系统_Hermes共享部署清单.md
- > 适用：路线 A。所有命令基于官方文档，标注了来源可信度（T0=官方 / T1=高一致社区实测）
- Linux 根目录：`~/.hermes/`（里面 `hermes-agent/` 是代码，其余是配置/会话/记忆/技能）
- **所以本清单采用的稳健方案（推荐）**：
- 共享 NTFS 盘专门放 **"记忆 / 会话 / 技能 / 配置"这些纯数据子目录的同步副本**，用脚本在两边双向同步（**排除 `hermes-agent/` 代码目录**）。
- > 如果你非要"严格同一份、实时共享"，见文末【附录：激进软链方案（高风险）】，不推荐新手。
- | D:（共享） | ~40 GB | NTFS | 两系统共享数据（Hermes 记忆同步、杂项） |
- 5. 软件选择：取消勾选 "Debian 桌面环境"（你跑 agent 用不到 GUI，headless 最省），**只勾 "SSH server" + "标准系统实用工具"**。
- ```
   lsblk
   sudo blkid | grep -i ntfs
```
- ```
   sudo apt update
   sudo apt install -y ntfs-3g
```
- ```
   sudo mkdir -p /mnt/shared
   sudo mount -t ntfs-3g -o uid=1000,gid=1000,umask=022,windows_names /dev/sda4 /mnt/shared
   ls /mnt/shared   # 应看到你在 Win 下建的 win-test.txt
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
