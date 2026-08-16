---
layout: default
title: 交接文档 · 联想N50-80双系统部署Win10与Debian共享Hermes数据
date: 2026-08-16 23:30:00 +0800
---

# Handoff 文档 · 联想 N50-80 双系统部署（Win10 + Debian + Hermes 共享）

- **日期**：2026-08-05
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260805_联想N50-80双系统部署Win10与Debian共享Hermes数据_handoff.md（编码探测：utf-8）

> **文档类型**：Handoff（工作交接 / 续做上下文）
> **创建日期**：2026-08-05
> **创建人**：WorkBuddy
> **状态**：✅ 方案已定，待执行（用户选择「先给文件，今晚自动发布的事之后再定」，故**暂未**建自动化定时任务）
> **关联机器**：联想 N50-80（5 代 Intel 低压双核、4GB DDR3、128GB SSD、2015 年）

---

## 一、Handoff 摘要（给接手者 / 给未来的自己）

**要做什么**：把一台闲置联想 N50-80 笔记本，装成「Win10 应急 + Debian 常开跑 agent」双系统，并用一块 NTFS 共享盘让 Hermes Agent 在两个系统下数据互通（记忆/会话/技能共享）。

**当前进度**：方案与完整操作清单已定稿（见下文第四节正文）。尚未开始任何实际操作（没装系统、没分区）。

**关键决策（已和用户拍板）**：
1. 系统对比结论：Debian 比 Ubuntu 更轻（主因 Ubuntu 默认带 snapd），老机器选 Debian minimal 更优。
2. 机器定位：4GB 内存 + 5 代低压双核，**只能跑「调远程 API」的 agent，不能本地跑大模型**。
3. 双系统方案选 **路线 A**：Windows 装 **Win10**（不是 Win7——Win7 已停更且 Node18/Py3.10 装不上，会废掉 Hermes 双系统用途），Debian 常开为主。
4. 共享盘格式用 **NTFS**（Win/Debian 都原生读写），Hermes 数据真身放共享盘、两边软链，代码各留系统盘（避免跨平台代码互相覆盖）。
5. 发布方式：用户选「**本地 Markdown + 先给文件即可**」，**暂不建今晚自动发布的自动化**。

**待用户后续拍板/提供**：
- 其余几台闲置笔记本的型号/内存/硬盘/年份，以便排整体拓扑。
- 是否真的要「今晚自动发布」——若需要，再建定时任务（自动化）把本文档发布到指定目标（腾讯文档 / 站点等，待定）。
- 内存升级（加一根 DDR3L SO-DIMM 到 8GB，约 ¥20–40）是否执行。

---

## 二、背景与推导链（为什么是这套方案）

1. **起点问题**：OpenClaw / Hermes 等 agent 工具最初设计的系统环境是什么？
   - OpenClaw：Node/TS 跨平台，桌面端 macOS 15+ 优先，非 Linux-only。
   - Hermes Agent（NousResearch）：Linux/macOS/WSL2 优先，不原生支持 Windows。
2. **延伸：Ubuntu vs Debian 谁对硬件要求低？** → Debian 更低更轻（snapd 是关键差异），适合老机器。
3. **机器核实**：N50-80 规格确认（i3-4030U/i5-5200U、4GB、128GB SSD）→ 够跑 API 型 agent，不能本地推理。
4. **共享盘设想**：用户想「不管启哪个系统都能访问同一份 Hermes」→ 引出格式兼容（NTFS/exFAT）与「代码分平台、数据可共享」的关键认知。
5. **Win7 试探**：用户问能否装 Win7 → 否（Node18/Py3.10 装不上 + 已停更），路线 A（Win10）确立。
6. **落地**：生成完整部署清单，本次整理为 handoff 文档。

---

## 三、风险与约束（执行前必读）

- 🔴 **关 Windows 快速启动**：不关则 NTFS 被锁，Debian 下只能只读，Hermes 写不进数据，整套方案废掉。
- 🔴 **一次只启一个系统**：避免双系统同时挂同一 Hermes SQLite 库导致锁。
- ⚠️ **Hermes 代码与数据混在同一根目录**，官方不支持双系统共享；必须用「共享盘做数据真身 + 两边软链子目录 + 代码留系统盘」的稳健方案，不能整根软链。
- ⚠️ **NTFS fstab 挂载必须带 `uid=1000,gid=1000`**，否则 Hermes 因权限读不了配置。
- ⚠️ **装 Hermes 后先 `ls` 看真实子目录名**再搬数据，勿照抄假设名（sessions/skills/memory/config 仅为示例）。

---

## 四、部署清单正文（完整操作手册）

> 机器：联想 N50-80（5 代 Intel 低压双核 i3-4030U / i5-5200U，4GB DDR3，128GB SSD，2015 年）
> 目标：双系统（Win10 应急 + Debian 常开跑 agent），NTFS 共享盘互通数据，Hermes 两边都能用、记忆互通
> 适用：路线 A。所有命令基于官方文档，标注了来源可信度（T0=官方 / T1=高一致社区实测）

---

### ⚠️ 最重要的前提：Hermes 数据共享的正确姿势

直接说结论，免得你照做翻车：

1. **Hermes 的代码和数据混在同一个根目录**：
   - Linux 根目录：`~/.hermes/`（里面 `hermes-agent/` 是代码，其余是配置/会话/记忆/技能）
   - Windows 原生根目录：`%LOCALAPPDATA%\hermes`（同上结构）
2. **官方不支持双系统共享同一份数据**（官方文档原话：原生 Windows 数据和 WSL 数据分开、可共存不冲突——意思就是它俩各管各的）。
3. **不能直接把整个 `~/.hermes` 软链到共享盘**：两边安装时都会往共享盘的 `hermes-agent/` 写代码，Linux 版和 Windows 版 venv 互相覆盖，后装的一边会把先装的一边的代码冲掉，导致某一系统启动时 Hermes 直接崩。

**所以本清单采用的稳健方案（推荐）**：
- Debian 为 Hermes **主用系统**（数据在 Debian 的 `~/.hermes`）；
- Windows 装一份 **独立 Hermes 副本**（数据在 Win 的 `%LOCALAPPDATA%\hermes`）；
- 共享 NTFS 盘专门放 **"记忆 / 会话 / 技能 / 配置"这些纯数据子目录的同步副本**，用脚本在两边双向同步（**排除 `hermes-agent/` 代码目录**）。
- 效果：不管启哪个系统都能用 Hermes，且核心记忆/会话互通；代码各自独立不打架。

> 如果你非要"严格同一份、实时共享"，见文末【附录：激进软链方案（高风险）】，不推荐新手。

---

### 一、分区规划（方案 A 微调版，已扣 EFI）

总盘 128GB ≈ 119GiB 可用。建议这样切：

| 分区 | 大小 | 文件系统 | 用途 |
|---|---|---|---|
| EFI 系统分区 | 512 MB | FAT32 | 双系统引导（Win 安装会自动建，或手动建） |
| C:（Windows） | 60 GB | NTFS | Win10 系统 + 少量软件 |
| /（Debian） | 18 GB | ext4 | Debian 系统 + Hermes 代码 |
| D:（共享） | ~40 GB | NTFS | 两系统共享数据（Hermes 记忆同步、杂项） |

> 说明：上一轮说的"Win 64 / Deb 20 / 共享 43"没扣 EFI，实际扣掉 512MB 后 Debian 只剩 ~11.5G，偏紧。这里把 Win 收到 60、Deb 给 18、共享 40，更合理。4GB 内存建议不加 swap（或最多 1–2G，空间紧可省略，agent 不吃内存）。

---

### 二、准备工作（一台正常电脑 + 一个 ≥8GB U 盘）

1. **下载镜像（来源 T0 官方）**
   - Win10 官方 ISO：https://www.microsoft.com/zh-cn/software-download/windows10 （用"下载 Windows 10 磁盘映像"拿 ISO；注意 Win10 扩展支持已于 2025-10-14 结束，但安装包仍可下）
   - Debian 12/13 netinst：https://www.debian.org/distrib/netinst （选 "amd64 small CD"）
   - Ventoy（多 ISO 启动盘工具，省得反复格 U 盘）：https://www.ventoy.net

2. **做启动盘**
   - 用 Ventoy 把 U 盘格成 Ventoy 盘，把上面两个 ISO 直接拷进 U 盘根目录即可。
   - 进 N50-80 BIOS（开机狂按 F2 / Fn+F2）确认：
     - Boot Mode = UEFI（不要 Legacy/CSM，双系统 UEFI 最干净）
     - Secure Boot 可先关（装完 Debian 再开也行，关掉最省事）
     - SATA Mode = AHCI

3. **备份**：这台盘上若有任何旧数据，先拷出来。下面操作会清空整盘。

---

### 三、步骤 1：先装 Windows 10（关键顺序：Win 先、Debian 后）

> 顺序不能反。先装 Debian 再装 Win 会被 Win 的引导覆盖；先 Win 后 Debian，Debian 的 grub 会接管并自动识别 Win。

1. U 盘启动 → 选 Win10 ISO → 安装。
2. 到"你想将 Windows 安装在哪里"这一步：
   - 删掉原有所有分区，让磁盘变"未分配"。
   - 新建 → 输入 **61440 MB**（=60GB）→ 这是 C 盘，会自动建出 EFI(100%/512MB) + 主分区。
   - 再新建 → 输入 **40960 MB**（=40GB）→ 这是 D 盘（共享盘），**格式化为 NTFS**。
   - **剩下约 18GB 保持"未分配"**，留给 Debian，别动。
3. 选 C 盘装 Win10，走完安装、建账户、进桌面。
4. **首启优化**（让 Win 更干净，也避免后续抢共享盘）：
   - 设置 → 更新和安全 → Windows 更新：装完所有能装的更新（60G 够用）。
   - **关快速启动**（最重要，见步骤 5）。
   - 打开 D 盘，确认它是 NTFS、可在 Win 下正常读写（先放一个 `win-test.txt` 验证）。

---

### 四、步骤 2：装 Debian（双系统引导 + 分 18G）

1. U 盘重启 → 选 Debian ISO → Graphical install / Install。
2. 语言、地区、键盘按你习惯选（中文简体 / 中国 / 汉语）。
3. 网络：插网线最稳；Wi-Fi 在 Debian 安装界面可能要额外固件，老机器建议先用网线。
4. 分区这一步选 **"手动"**：
   - 选中那块 ~18GB 的"空闲空间" → 新建分区 → 用满全部 → 挂载点 `/` → 文件系统 ext4。
   - **不要**动已经建好的 EFI 分区（Debian 安装器会检测并复用它，挂载点选 `ESP`/已有的 EFI，不要格式化！）。
   - 不要建 swap（4G 内存跑 agent 够；要建也最多 1–2G，但空间紧建议省略）。
   - 共享盘（那 40G NTFS）**这一步先不挂**，留给装完系统后用 fstab 挂（更可控）。
5. 软件选择：取消勾选 "Debian 桌面环境"（你跑 agent 用不到 GUI，headless 最省），**只勾 "SSH server" + "标准系统实用工具"**。
6. 装引导程序 grub：选装到整块磁盘（如 `/dev/sda`），它会自动识别 Win10 并加入启动菜单。
7. 装完重启，应看到 grub 菜单：Debian 在上、Windows Boot Manager 在下。分别进一次确认都能启动。

> 来源 T1：Debian 官方安装指南 + 社区一致实践（双系统先 Win 后 Linux、grub 接管）。

---

### 五、步骤 3：Debian 挂载共享 NTFS 盘

1. 进 Debian，先看共享盘设备名：
   ```bash
   lsblk
   sudo blkid | grep -i ntfs
   ```
   记下共享盘的设备（如 `/dev/sda4`）和 LABEL（没有就给它起一个，Win 下右键重命名卷标为 `SHARED`）。

2. 装 NTFS 支持（Debian 12 内核自带 ntfs3，再装用户态工具兜底）：
   ```bash
   sudo apt update
   sudo apt install -y ntfs-3g
   ```

3. 建挂载点并手动挂一次验证：
   ```bash
   sudo mkdir -p /mnt/shared
   sudo mount -t ntfs-3g -o uid=1000,gid=1000,umask=022,windows_names /dev/sda4 /mnt/shared
   ls /mnt/shared   # 应看到你在 Win 下建的 win-test.txt
   ```
   `uid=1000,gid=1000` 让你的普通用户拥有共享盘文件，否则 Hermes 会因权限不足读不了配置。

4. 写入 `/etc/fstab` 实现开机自动挂（用 nano 或 vim 编辑）：
   ```
   # 共享数据盘（NTFS，双系统共用）
   /dev/disk/by-label/SHARED  /mnt/shared  ntfs-3g  defaults,uid=1000,gid=1000,umask=022,windows_names  0  0
   ```
   > 用 LABEL 比用 `/dev/sda4` 稳（设备名可能因插拔变）。如果没卷标，先去 Win 给 D 盘命名"SHARED"。
   > 测试 fstab 是否写对：`sudo umount /mnt/shared && sudo mount -a`，无报错即正确。

---

### 六、步骤 4：关掉 Windows"快速启动"（不做整个方案废掉）

这是双系统共享 NTFS 最容易翻车的点。不关的话，Win 关机其实是"休眠"，NTFS 卷被锁，Debian 挂载时**只能只读** → Hermes 在 Debian 下写不进数据。

1. 进 Windows。
2. 控制面板 → 电源选项 → 选择电源按钮的功能。
3. 点"更改当前不可用的设置"。
4. **取消勾选"启用快速启动（推荐）"**。
5. 保存修改。以后 Win 正常关机，Debian 才能读写共享盘。

---

### 七、步骤 5：两边各装 Hermes（代码各自独立）

> 来源 T0：Hermes Agent 官方安装文档（hermes-agent.nousresearch.com/docs/getting-started/installation）

**Debian 侧（主用）：**
```bash
sudo apt install -y git curl xz-utils

# 一键安装（跟踪 main，自动装 uv/Python3.11/Node22 等）
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 重载 shell
source ~/.bashrc
hermes   # 应能启动聊天；按提示配置 provider/model
```
- 数据根：`~/.hermes/`（代码在 `~/.hermes/hermes-agent/`，记忆/会话在 `~/.hermes/` 下其他子目录）

**Windows 侧（独立副本）：**
1. 以普通用户打开 PowerShell（不用管理员）。
2. 运行：
   ```powershell
   iex (irm https://hermes-agent.nousresearch.com/install.ps1)
   ```
   - 安装器自动处理：uv、Python 3.11、Node.js 22、ripgrep、ffmpeg、便携 Git Bash。
   - 数据根：`%LOCALAPPDATA%\hermes`（代码在 `%LOCALAPPDATA%\hermes\hermes-agent\`）。
3. 装完**重开一个 PowerShell 窗口**，`hermes` 命令应可用。

> 注意：Windows 原生安装仍是 early beta（官方原话），常见路径能用，但没 POSIX 安装器那么广测。真要最稳，Win 侧也可以走 WSL2 装 Linux 版（但那又多一层，本清单按"原生 Win + 原生 Debian"讲）。

---

### 八、步骤 6：共享 Hermes 数据（稳健同步方案）

核心思路：**代码各自留系统盘，只把"纯数据子目录"在共享盘做双向同步，且排除 `hermes-agent/` 代码目录。**

#### 8.1 先摸清两边的数据子目录结构

Debian 侧：
```bash
ls -la ~/.hermes
```
Windows 侧（PowerShell）：
```powershell
Get-ChildItem $env:LOCALAPPDATA\hermes
```
你会在两边根目录下看到类似 `hermes-agent/`（代码，排除）、以及 `sessions/`、`skills/`、`memory/`、`config/`、`auth/`、`cache/` 等（**具体名字以你 `ls` 看到的为准，不要照抄下面假设名**）。

#### 8.2 确定要同步的子目录

原则：
- ✅ 同步：对话记录、记忆、技能、配置、认证（这些是你要"两边互通"的）。
- ❌ **绝不**同步：`hermes-agent/`（代码，分平台）、`cache/`（可重建的缓存，没必要同步）。

假设 `ls` 后确认要同步的是 `sessions`、`skills`、`memory`、`config`（以你实际看到的替换）：

#### 8.3 用共享盘做"真身"，两边软链过去（推荐，比复制更省空间）

思路：把这些子目录的"真身"放在共享盘 `/mnt/shared/hermes-data/`，两边各建软链指过去。

**Debian 侧：**
```bash
# 在共享盘建数据真身目录
mkdir -p /mnt/shared/hermes-data

# 把现有数据搬过去（以实际子目录名为准）
for d in sessions skills memory config; do
  if [ -e ~/.hermes/$d ]; then
    mv ~/.hermes/$d /mnt/shared/hermes-data/$d
    ln -s /mnt/shared/hermes-data/$d ~/.hermes/$d
  fi
done
ls -la ~/.hermes   # 确认出现指向 /mnt/shared/hermes-data/... 的软链
```

**Windows 侧（PowerShell，管理员）：**
```powershell
# 共享盘在 Win 下是 D:，对应 Debian 的 /mnt/shared
New-Item -ItemType Directory -Force -Path D:\hermes-data

# 逐个搬并建目录 junction（Windows 用 junction 比 symlink 稳，不需特权）
$dirs = @("sessions","skills","memory","config")
foreach ($d in $dirs) {
  $src = "$env:LOCALAPPDATA\hermes\$d"
  $dst = "D:\hermes-data\$d"
  if (Test-Path $src) {
    Move-Item $src $dst
    cmd /c "mklink /J `"$src`" `"$dst`""
  }
}
```
> 注意：Win 侧子目录名要和 Debian 侧**完全一致**（sessions/skills/memory/config），否则软链对不上。先 `ls` 对齐再搬。

#### 8.4 同步脚本（改完一边，跑一下让另一边也有）

因为一次只跑一个系统，不需要实时。你在 Debian 改了记忆，下次进 Win 前跑一下同步即可。

**Debian → 共享盘（已经在软链，天然同步，无需额外操作）。**
**Win ↔ 共享盘（同样是软链，天然同步）。**

> 因为我们用的是"共享盘做真身 + 两边软链"的方式，**数据实时就是同一份**，不需要 rsync/robocopy 来回拷。这正是比"各留副本再同步"更优的地方——代码留在系统盘、数据真身在共享盘，两边软链指过去。

⚠️ **唯一硬性约束**：**一次只启一个系统**。如果两个系统同时挂同一个 NTFS 上的 Hermes SQLite 库，可能出现数据库锁。你本来就是双系统切换用，不会同时跑，所以无此问题。

---

### 九、收尾优化

1. **Debian 卸掉 snapd**（这台只有 4G 内存，能省则省；Debian minimal 默认没 snap，这步可跳过；若你装了 Ubuntu 才需要）：
   ```bash
   # 仅当你用的是 Ubuntu 才需要；Debian minimal 可忽略
   # sudo apt purge -y snapd
   ```
2. **开 SSH 常驻**（你已经装了 SSH server）：
   ```bash
   sudo systemctl enable --now ssh
   ```
   之后从你主力机 `ssh 用户名@N50的IP` 就能远程管这台 agent 节点。
3. **（可选，强烈建议）加一根内存条到 8GB**：N50-80 有 2 个 SO-DIMM 槽，现在多半单条 4G。买 **DDR3L（1.35V 低压）SO-DIMM** 二手约 ¥20–40，插上空槽变 8G，跑 agent 更从容，也能试小模型本地推理 Demo。
4. **确认双系统时间不打架**：Win 默认用本地时间、Linux 默认用 UTC，可能导致时间错乱。Debian 下执行：
   ```bash
   timedatectl set-local-rtc 1 --adjust-system-clock
   ```
   让 Linux 也用本地时间，和 Win 对齐。

---

### 附录：激进软链方案（高风险，不推荐新手）

如果你非要"整个 Hermes 数据根严格同一份、实时共享"，可以这么做，但**有踩坑风险**：

1. 把共享盘上建 `hermes-data/`，把两边 `~/.hermes`（Linux）和 `%LOCALAPPDATA%\hermes`（Win）**整体**软链过去。
2. **问题**：两边安装器都会往 `hermes-data/hermes-agent/` 写代码，后装的一边覆盖先装的一边 → 某一系统 Hermes 启动崩溃。
3. ** workaround**：装好一边后，把 `hermes-agent/` 从共享盘**移回各自系统盘真实目录**，只让其余数据子目录留在共享盘软链。但这要求你精确知道安装器把代码放在哪、且每次 Hermes 升级可能重写结构。
4. **结论**：除非你很熟 Linux/Win 目录结构、且愿意每次升级后排查，否则走正文"共享盘做数据真身 + 两边软链子目录 + 代码留系统盘"的稳健方案。

---

### 来源标注

- Win10 生命周期 / 停更日期：微软官方生命周期文档（T0）
- Node 18 放弃 Win7、Python 3.9 起拒绝 Win7：Node.js 官方公告 + python.org release notes（T0）
- Hermes Agent 安装命令、目录结构、Windows 原生 early beta 声明：hermes-agent.nousresearch.com 官方安装文档（T0）
- Debian 双系统安装、grub 接管、NTFS fstab 挂载：Debian 官方安装指南 + 社区一致实践（T1）
- 共享盘格式 NTFS/exFAT 兼容性、快速启动锁盘：Linux 内核 ntfs3/ntfs-3g 文档 + 社区实测（T1）

---

### 一句话总结

Win10 先装（60G+共享40G NTFS，留 18G 未分配）→ Debian 后装（18G ext4，grub 接管）→ 关 Win 快速启动 → Debian fstab 挂 NTFS → 两边各装 Hermes（代码各留系统盘）→ 把 Hermes 的"数据子目录"真身放共享盘、两边软链 → 一次只跑一个系统，记忆互通。

---

## 五、下一步 / Open Items（供续做）

- [ ] 用户确认其余闲置笔记本配置 → 排整体拓扑（哪台常开跑 agent、哪台当存储/下载机、哪台单 Debian 最省）。
- [ ] 若用户后续决定「今晚自动发布」：建一个 one-time 自动化任务，将本文档发布到指定目标（腾讯文档在线版 / 某静态站，待用户指定）。**当前未建。**
- [ ] 实际执行装机时，按第四节逐条走；遇 Win/Debian 识别不到 WiFi、USB 安装阶段键鼠失灵等老机器坑，单独排查。
- [ ] 内存升级（4G→8G DDR3L）视用户意愿执行。

## 六、相关文件

- 原部署清单：`N50-80_Win10+Debian双系统_Hermes共享部署清单.md`（同目录，本文档由其整理而来）
- 本 handoff 文档：`handoff_2026-08-05.md`
