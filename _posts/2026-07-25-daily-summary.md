---
layout: default
title: 每日工作总结 · 2026-07-25
date: 2026-07-25 23:30:00 +0800
---

# 每日工作总结 · 2026-07-25

> 数据来源：当日两段机器日志（①`2026-07-24-11-46-09/.workbuddy/memory/2026-07-25.md` 凌晨无锡爬虫续跑；②`2026-07-25-12-10-12/.workbuddy/memory/2026-07-25.md` 全天主任务）合并提炼。

## 一、今日完成事项

**1. 无锡 58 同城「买房 + 租房」全量数据爬取完成并落库（D1）【收尾交付】**
- 买房站 wx-houseing：7 区全部完成，累计 **3685 条**，凌晨已确认落 D1，看板可用。
- 租房站 wxzf：从凌晨梁溪起步，上午用户手动过掉 58 验证码后，一口气连跑锡山/新吴/江阴/宜兴 4 区，至 **10:55 确认 7/7 区全部完成**，累计 **7466 条**（梁溪673/滨湖1119/惠山1116/锡山1140/新吴1143/江阴1121/宜兴1154）。
- 买房+租房合计超 1.1 万条数据均已落 D1，看板可对外查看，**无锡项目整体交付完毕**。

**2. Hermes 模型清单导入 WorkBuddy**
- 读取 Hermes 配置（`C:\Users\Administrator\.hermes\config.yaml`）提取模型清单，备份原 `models.json` 后追加 15 条模型（Gemini×3 + OpenRouter 免费×12），与原有 9 条 GLM 合并為 **24 条**，原 GLM 一条未动。
- 验证 OpenRouter 模型连通正常；Gemini 本机直连受地区限制报 400（需代理才能用）。

**3. Wispbyte 面板「Adblocker detected」误报排障**
- 用 Playwright 干净 Chromium 实测，定位根因：本机网络在 SNI 层阻断了 3 个 Cloudflare 子域（static.cloudflareinsights.com / cdnjs.cloudflare.com / challenges.cloudflare.com），面板把"统计脚本加载失败"误判为广告拦截，关拦截器无效。
- 给出解法：让浏览器经代理访问这几个域名，或开全局代理。

**4. Wispbyte 免费 VPS 代理部署（罗马尼亚机房 w662000，端口 13986）**
- 服务器为非 root 的 Pterodactyl 容器（Debian 13）。一键脚本跑不了（需 root），先试 3proxy 编译（同样卡 root），**最终改用 gost 单二进制 SOCKS5 调通**，公网 IP 78.154.103.35:13986。
- 客户端选型：放弃 V2rayN（对 SOCKS5 认证支持差），推荐 **Clash Verge / FIclash（Clash.Meta 内核）**原生支持 SOCKS5 认证。
- 定位结论：YouTube 主动掐断该免费机房 IP（流媒体黑名单），属免费套餐无解；其余 GitHub/pypi 等走代理正常。

**5. 单端口代理方案探索（gost → sing-box → 回退 gost）**
- 因免费 VPS 只开放 13986 一个端口，探索用 sing-box 起 Shadowsocks 加密隧道弥补裸 SOCKS5 不加密的弱点（命令/配置已完整存档）。
- 因网页 Console 多行粘贴被吞、不支持 Ctrl+C，用户放弃 sing-box 部署，**回退到 gost SOCKS5 现状**，本地 Clash 配置改回 socks5 节点即可恢复罗马尼亚加速。

**6. 免费服务器资源全网搜索**
- 应公众号《512M+1G免费永久服务器》线索，产出《免费服务器资源汇总_2026-07.md》，分类整理：A 翼龙系同类（FalixNodes/Gaming4Free/翼龙中国）、B 永久免费云（Oracle 4C24G / Serv00 / Vultr）、C 国内限时试用（腾讯阿里华为京东百度雨云）、D 特殊（IBM LinuxONE / Cloudflare Workers 等）。

**7. Gaming4Free 平台情报 + 部署方案**
- 同类 Pterodactyl 托管（2.5GB RAM / 非 root / 支持 SFTP 端口2022 / 支持额外端口），比 Wispbyte 大方 5 倍、可多开端口铺多协议。
- 给出 sing-box 多协议部署指南（SS/VLESS/Hysteria2 各占端口）、SFTP 部署指南、自动续约指南 + `g4f_renew.py`（标准 API 做不到续约，需 cookie 重放 Extend 按钮，有 ToS 封号风险、Cookie 会过期）。
- 用户目前排队等开服，方案已备好待执行。

**8. Discord Bot 自建拆解**
- 产出《Discord_Bot_自建推荐_2026.md》：Discord bot 是纯出站连接、不需要入站端口，与 sing-box 完美共存；推荐 10 个全自部署开源 bot（discord.py / discord.js / Red-DiscordBot / Modmail / TomoriBot 等）+ 分阶段部署路线。

## 二、关键决策 / 注意事项

- **58 爬虫 IP 墙机制（重要认知修正）**：沙箱出口 IP 按信誉判 gate，Cookie / 代理都救不了 IP 级墙；但**用户在浏览器手动过掉 58 验证码，可给沙箱出口 IP 开宽松窗口**（推翻此前"必须重启光猫"结论）。手动验证窗口容量远大于之前估计——一次手动验证可连跑 4 个整区，不必每区停下等刷新。
- **租房分区增量补坑（必记）**：① 灌库必须用「只删本区叶子」DELETE，**不能全删**（会冲掉已补区）；② `import_data.sql` 是普通 INSERT 非 OR IGNORE，混合导入同一区会翻倍，须生成单区 SQL 或导入前删全涉及区叶子；③ 跑前**勿全清 listings**（会触发 `seed_from_backup` 播种旧数据污染）；④ 跑完**必 strip seed**（`DELETE FROM listings WHERE crawl_batch='seed'`）。
- **爬取完成判断**：看日志末尾有无"爬取完成"或监测日志文件大小≥20s 不变，不能只看实时行数（Python stdout 缓冲会吞日志）；`ps aux | grep crawler.py` 查进程最准。Git Bash 无 `pgrep`。
- **Gridea 发布铁律**：草稿 `published: false` 不会真正同步发布，给该用户写 Gridea 文章一律用 `published: true`（已第二次犯同款，记入记忆）。
- **Wispbyte / Gaming4Free 网页 Console 极不友好**：多行粘贴被吞成一行、不支持 Ctrl+C，部署改用 **SFTP（FileZilla，端口2022）上传文件**再执行。
- **Clash 客户端坑**：「系统代理」开关 ≠ 核心进程运行；魔改 Clash Verge 核心起不来，改用 **FIclash（mihomo 内核）**复用同一 yaml，可靠。
- **Gaming4Free 自动续约**：标准 Pterodactyl API 只有 start/stop/restart，**没有延长租约端点**；必须用浏览器 F12 复制 Extend 按钮的 cURL + Cookie 重放（katabump / 自写 `g4f_renew.py`），有封号风险、Cookie 非永久。
- **用户强制红线（已写入 ~/.workbuddy/MEMORY.md 顶部）**：绝不折叠长消息；涉及 how/步骤/原理/踩坑必须完整给出，禁止只给结论式短句。

## 三、生成的有用文件

| 文件 / 目录 | 路径 | 用途 |
|---|---|---|
| 每日工作总结 | `D:\AI work\workbuddy\2026-07-25-12-10-12\2026-07-25_每日工作总结.md` | 本文件 |
| Hermes 模型备份（原始） | `C:\Users\Administrator\.workbuddy\models.json.backup-20260725` | 导入前 models.json 备份 |
| Hermes 模型清单快照 | `D:\AI work\workbuddy\2026-07-25-12-10-12\hermes_models_backup.json` | Hermes config 解析出的模型清单 |
| WorkBuddy 导入前快照 | `D:\AI work\workbuddy\2026-07-25-12-10-12\workbuddy_models_before_import.json` | 合并前 WorkBuddy 原 9 条 GLM |
| 模型合并脚本 | `D:\AI work\workbuddy\2026-07-25-12-10-12\merge_models.py` | 合并 Hermes 与 WorkBuddy 模型清单 |
| Wispbyte 探测脚本 + 报告 | `D:\AI work\workbuddy\2026-07-25-12-10-12\probe_wispbyte.py` / `wispbyte_probe_report.json` | "Adblocker" 根因探测 |
| Wispbyte 代理探测 | `D:\AI work\workbuddy\2026-07-25-12-10-12\probe_wispbyte_proxy.py` / `wispbyte_proxy_report.json` / `wispbyte_proxy_test.png` | 经代理访问验证 |
| Wispbyte 3proxy 部署脚本 | `D:\AI work\workbuddy\2026-07-25-12-10-12\wispbyte_3proxy_deploy.sh` | 非 root 手动 3proxy 方案（后被 gost 替代） |
| Clash 客户端配置 | `C:\Users\Administrator\wispbyte-clash.yaml` | FIclash/Clash Verge 用的 SOCKS5 节点配置（当前为 socks5 节点） |
| 免费服务器资源汇总 | `D:\AI work\workbuddy\2026-07-25-12-10-12\免费服务器资源汇总_2026-07.md` | 全网免费 VPS/云资源分类报告 |
| Discord Bot 自建推荐 | `D:\AI work\workbuddy\2026-07-25-12-10-12\Discord_Bot_自建推荐_2026.md` | 10 个开源 bot + 部署路线 |
| Gaming4Free 系列指南 | `D:\AI work\workbuddy\2026-07-25-12-10-12\Gaming4Free_sing-box_部署指南_2026-07.md` / `Gaming4Free_SFTP部署指南_2026-07.md` / `Gaming4Free_自动续约指南_2026-07.md` | 部署/续约完整方案 |
| Gaming4Free 脚本 | `D:\AI work\workbuddy\2026-07-25-12-10-12\g4f_renew.py` / `deploy_sing-box.sh` / `gaming4free_startup.sh` | 自动续约 bot + sing-box 启动命令 |
| 无锡 58 项目交接文档 | `D:\AI work\workbuddy\2026-07-24-11-46-09\HANDOFF.md` / `HANDOFF_AGENT.md` | 人读/机读交接，含 11 条坑与命令速查 |
| Handoff 自动发布脚本 | `D:\AI work\workbuddy\handoff\handoff_flow.py` | 每日 23:30 自动推送博客+语雀+Gridea（automation-1784951947030） |
| Handoff 归档副本 | `D:\AI work\workbuddy\handoff\260725_58的无锡买房租房项目搭建_handoff.md` | handoff 人读副本 |
| 博客源（Jekyll） | `D:\AI work\daily-note-blog\_posts\2026-07-25-wuxi-58-scraper-delivery.md` 与 `2026-07-25-handoff.md` | 已本地写入/commit，push 因 sandbox 连不上 GitHub 挂起 |
| Gridea 浓缩版文章 | `C:\Users\Administrator\Documents\Gridea Pro\posts\260725-58的无锡买房租房项目搭建.md` | `published: true`，标题《58的无锡买房租房项目搭建》 |

## 四、待办 / 风险

- **无锡爬虫**：7/7 租房 + 7/7 买房均已落 D1，无遗留爬取；后续仅可能为增量更新（按需重跑单区）。
- **Gaming4Free 部署**：用户排队等待开服，拿到服务器后按方案部署 sing-box 多协议 + `g4f_renew.py` 自动续约；注意每 30 分钟点保位、改用 SFTP 上传避免网页 Console 卡死；自动续约违反 ToS 有封号风险、Cookie 会过期需重抓。
- **Discord Bot**：待用户选阶段一（discord.py 20 行 ping）练手。
- **GitHub 同步（博客/语雀）**：sandbox 环境无法连通 github.com:443，今日 `git push` 失败（exit 128）；需在可联网网络下执行 `cd "D:\AI work\daily-note-blog" && git push origin master` 触发 GitHub Actions 自动部署。语雀发布已由 23:30 自动化在本机联网时推送。
- **Wispbyte YouTube 流媒体**：被免费机房 IP 流媒体黑名单，免费套餐无解，仅能用于 GitHub/pypi 等非流媒体加速。
- **Gemini 直连**：受地区限制报 400，需代理才能用，本机暂不可用。
