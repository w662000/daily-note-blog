---
layout: default
title: 项目流 · 2026-11-27
date: 2026-11-27 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-27-10-33-05\.workbuddy\memory\2026-11-27.md

## 曦码（Xime / Rime）模糊音配置咨询
- 用户要在曦码里只加 en/eng、in/ing 两组前后鼻音模糊音，不要 an/ang。
- 给出 Rime `speller/algebra` 补丁：`derive/([ei])n$/$1ng/` + `derive/([ei])ng$/$1n/`（把参考里的 `[aei]` 改成 `[ei]`，两个方向各一行）。
- 关键提醒：只删参考里的 an/ang 两行无效，`[aei]` 里的 `a` 仍会让 an/ang 互通；若原方案自带旧规则，必须把旧行一起删/注释，再重新部署。
- 未确认：曦码具体方案的 custom.yaml 文件名、用户所用平台/方案；未在本机验证安装。已让用户补充平台+方案名。
- 交叉核对来源为公开博客（GitCode/CSDN 等），非 Rime 官方一手文档，已如实标注。
- 会话尾标 ID：35ec7807-75b1-47be-b507-81005a60d5ef

## 10:43 追加：Windows 版本机落地 + 纠错
- 本机已装 Windows 曦码：程序目录 `C:\Program Files\Xime`，Rime 用户目录 `C:\Users\Administrator\AppData\Roaming\Xime\rime`，当前方案 `pinyin_simp`（简体拼音）。
- **纠正上一轮错误**：Rime `patch: speller/algebra:` 是覆盖整个列表，不是追加；追加必须用 `speller/algebra/+:`。来源：Rime 官方 CustomizationGuide、rime-ice issue #121（T1）。上一轮基于用户贴的不可靠参考说成"追加"，已向用户明确纠正。
- 已直接在本机创建 `C:\Users\Administrator\AppData\Roaming\Xime\rime\pinyin_simp.custom.yaml`，用 `/+` 追加两条 derive，不动原 12 条 algebra。
- 待用户托盘「重新部署」并验证。
- 经验：Rime custom.yaml patch 对列表默认是覆盖；`/ +`（即 `/+`）才是合并。以后写模糊音补丁一律用 `/+`。

## 10:48 追加：曦码·曜 Windows 版部署入口
- 用户反馈托盘右键没有「重新部署」。**正确答案：在设置界面 →「输入方案」页 →「部署方案」按钮**，不在托盘菜单。
- 证据来源（本机一手）：从 `C:\Program Files\Xime\winxime-setup.exe` 二进制提取到字符串「首次启用快捷短语要重新部署方案（输入方案页 → 部署方案）」「方案…部署」；官方 GitHub README 未写该入口。
- 备用：`%APPDATA%\Xime\logs\server.log` 显示每次 `winxime-server.exe` 启动都会自动 `Running rime deployment...`，所以注销/重启或重启该进程也可生效。
- 判断补丁是否已部署：看 `%APPDATA%\Xime\rime\build\pinyin_simp.schema.yaml` 的 mtime 是否晚于 custom.yaml 写入时间。当前仍是 09:52（未部署）。
- 10:52 用户确认模糊音已生效（build mtime 更新到 10:50:58）。

## 10:52 追加：曦码候选数 5→9 的两处控制点
- 候选数由两处同时控制，缺一不可：
  1. 方案文件写死 `menu: page_size: 5`（server.exe 有提示：方案自定义 page_size 会限制候选数，需覆盖/删掉）→ 在 `pinyin_simp.custom.yaml` 的 patch 加 `menu/page_size: 9` 覆盖。
  2. 设置页「候选词数量」（范围 1–10，第 10 个用 0 选）→ 存为 `xime.custom.yaml` 的 `style.candidate_count`，控制候选栏渲染几个。已创建该文件设为 9。
- `xime.custom.yaml` 是曦码程序自己管理的文件，README 说只记录与默认值不同的部分、按 YAML 树深合并；手工创建只写差异项是安全的。
- 经验：曦码改候选数必须两处一起改，只改 Rime 的 page_size 不够（UI 仍按 candidate_count 渲染）。
- 10:56 用户改要 10 个（第 10 用 0 选）。**补上第三个卡点**：`default.custom.yaml` 里也写死 `menu: page_size: 5`，程序启动时按 candidate_count 自动同步它。所以完整三处是：xime.custom.yaml 的 style.candidate_count / pinyin_simp.custom.yaml 的 patch menu/page_size / default.custom.yaml 的 menu.page_size。三处已全改为 10。
- 注意：编辑 default.custom.yaml 时遇到"file modified since read"——曦码程序会自己重写这个文件，必须重新 Read 再 Edit，改完再次核对最终值。
- 经验总结：曦码·曜配置有一个"程序自管理"层（xime.custom.yaml + default.custom.yaml 会被程序重写），手工改后要立即 cat 复核，否则可能被覆盖。
- 11:03 用户确认全部生效，任务完成。已沉淀技能 `~/.workbuddy/skills/xime-yao-config/SKILL.md`（本机路径、部署入口在设置页输入方案页、patch /+ 追加坑、候选数三处控制、程序重写坑），下次改曦码直接调用。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-26-20-58-07\.workbuddy-ai\memory\2026-11-27.md, D:\workspace\workbuddyai\2026-11-27-15-01-30\.workbuddy-ai\memory\2026-11-27.md

## wxatp2022.link 域名托管（进行中）

- 用户在 linkme 免费领取域名 `wxatp2022.link`，目标托管到自己 CF 账号
- CF 已添加站点（Free），新 NS：jaziel/leia.ns.cloudflare.com；旧 NS：garret/paloma（也是 CF，说明 linkme 用自己 CF 账号托管）
- 卡点：linkme 后台无自助改 NS 入口；子域绑 CF 属 Enterprise 功能不可行（T0 已查证）
- 可行替代：linkme 面板支持 TXT/MX/CNAME/A/AAAA，可 A 记录指 VPS 或 CNAME 接 Vercel/Netlify，证书走 Let's Encrypt HTTP-01
- 交付：`D:\workspace\workbuddyai\2026-11-27-15-13-54\handoff-wxatp2022-link-托管.md`（含待办、客服英文模板）
- 下一步：用户找 linkme 客服改 NS，或走解析面板路径 B

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）