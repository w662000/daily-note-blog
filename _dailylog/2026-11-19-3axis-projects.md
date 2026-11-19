---
layout: default
title: 项目流 · 2026-11-19
date: 2026-11-19 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\2026-11-17-22-32-26\.workbuddy\memory\2026-11-19.md, D:\AI work\workbuddy\2026-11-18-14-41-01\.workbuddy\memory\2026-11-19.md

## 活清单全模型评分（51个，锚点GLM-5.3=80，黄蓝双色条）

- 需求：活清单所有模型（含WB内置）全部评分，基准 GLM-5.3=80，要黄蓝双色条详情表。
- 活清单：~/.workbuddy/models.json 51 条唯一id，10平台（NIM13/intern-ai10/GLM6/CF5/Bazaar5/Gemini4/SenseNova3/Groq2/DeepSeek2/讯飞1）。
- **三层映射口径**（保持昨天认可的 intern-ai 分完全一致）：
  - T1 SuperCLUE 2026-11 榜(21模型,更新至11-18,superclueai.com)：差值映射 `80+(SL−50.66)`，9个，高可信。
  - T2 干活选型榜「得分」列(model-speed-radar/模型干活选型排行榜.md)：线性缩放 `得分×80/87`，19个，中可信。
  - C 官方定位/参数/同系推断：23个，低可信。
- 结果：Kimi91/DeepSeek88/Sage-S2.1-Flash85/SenseNova GLM-5.2 84/Gemini3FlashPreview84/GLM-5.3(锚)80；尾部 GLM-4-Flash37/Riva-Translate35。
- 产物：`活清单全模型评分看板_20261119.html`（零依赖,黄蓝条,可筛选排序搜索,浏览器实测OK）、`活清单全模型评分报告_20261119.md`、脚本 `分析脚本/score_all_models.py`+`render_score_board.py`。
- 口径提醒：分数=能力上限≠可用性（Kimi/DeepSeek 实测不可用，见双雷达报告）。这套评分与"可用性"是两回事，别混。

## 14:05 用户发客户端截图(工作日志40项/技术点8312项/项目表394项)
- 排查客户端计数 vs CLI 不符:
  - 文件夹树:根→我的资源(SVRA0A...)->workbuddy(5BB7...)→{工作日志7587B5CC.../项目表C533B557.../技术点9C31CBCE...}。**folder ID 正确,补发没传错地方**。
  - CLI list -f 工作日志:第一页就50条,含10月/11月全部每日工作总结;分页拉尽145篇。
  - 截图里的 autoclaw-2026-08-16 精确搜到(ID 845F37...),与截图同一篇 → 数据是同一批,只是App显示口径/懒加载问题。
-  App 顶部显示的是旧内容(08-16等),疑似按创建时间升序或默认排序+只加载首屏;客户端"40项/8312项/394项"计数与CLI实际(145/221/222)不符,是App统计口径问题(可能含历史幽灵/回收站),非数据丢失。
- 建议用户在App内按标题搜"每日工作总结 · 2026-10-15"验证(CLI已确认在)。

## 14:15 导出云端清单 + 查明 11-02~11-12 缺口根因（只读）
- 导出云端三目录全量清单：工作日志145/项目表264/技术点242（项目表与技术点比昨日+2/+5，为今晨列车新发）。产物：`云端三轴完整清单_20261119.md` + `cloud_3axis_full_list.json`（当前工作目录）。
- **11-02~11-12 缺口定性**：publish_train 日志最早只到 2026-11-13 → **发布列车 11-13 才上线**，之前日报生成链路不存在；但 11-04/11-08/11-09/11-11/11-12 有旧会话 memory 日志留存（9~78行不等）→ 当天有工作内容，只是没生成日报。
- 补传可行性：那 11 天可从旧会话 memory 日志人工/半自动补写日报，但属"重新生成内容"而非"补传"，需用户拍板。

## 14:57 补传 11 月上旬 5 天日报到有道云（用户拍板"补那11天"）
- 来源核对：WB 会话 memory 有 11-04/11-09(×2)/11-11/11-12；AutoClaw memory 有 11-10。**11-02/03/05/06/07/08 六天无任何日志来源→不造假、保持缺口**（吸取 11-16"空日志定稿"教训）。
- 格式完全对齐现有日报（四 agent 节 + 无日志写"今日无机器日志记录" + 总计/待办），内容忠实提炼自日志原文。
- 生成+查重+上传+回查一次完成：5/5 成功（11-04/09/10/11/12），均获唯一笔记 ID；G5 回查 5/5 命中。G3 expected=5 未熔断；G4 台账 `补传日报_11月上旬/upload_ledger.json`。
- 笔记ID：11-04=4D50ADC7... / 11-09=923F7F31... / 11-10=5836B7E8... / 11-11=EDCD36BF... / 11-12=629C7103...
- 本地副本：`补传日报_11月上旬/`（工作目录）。注：run_list 单页50条的坑仍在（G1查重只覆盖第一页），但标题带唯一日期+全量list已确认不存在，无重复风险。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-11-19-11-44-58\.workbuddy-ai\memory\2026-11-19.md, D:\workspace\workbuddyai\2026-11-19-13-30-30\.workbuddy-ai\memory\2026-11-19.md

## D 盘清理方案（只读分析，未动文件）
- 用户给了 `C:\Users\Administrator\Documents\WizTree_20261119123505.csv`（WizTree 4.27 导出，302MB，144 万行），要 D 盘清理/归类/整理/去重方案。
- **硬约束：涉及 agent 的目录一律不动**（怕脚本跑不起来）；用户自己保存的文件可参与整理。
- 分析产物：
  - 只读统计脚本：`.workbuddy-ai/tmp/scan_disk.py`、`scan_disk2.py`
  - 汇总 JSON：`.workbuddy-ai/tmp/disk_report.json`、`disk_report2.json`
  - 交付方案：`D:\workspace\workbuddyai\2026-11-19-13-30-30\D盘清理整理方案.md`
- 关键结论：D 盘 831GB / 已用 561GB / 剩 270GB；大头 video 162GB、ghost 118GB、phonephoto 65GB、HDDownload 46GB、Program Files 44GB、111 43GB。
- agent 红线目录：`D:\AI work\workbuddy\`（16.4GB）、`D:\hermes-agent\`、`D:\LobsterAI_backup\`、`D:\autoclaw-asar-work\`、`Program Files` 下 QClaw/AutoClaw/WorkBuddy/Loomy/ZCode/OmniRoute/CodeBuddy/DeepSeekHarness 等；系统级 `pagefile.sys`/`wsl`/`$MFT` 也不动。
- 待用户确认 3 件事：ghost 系统镜像只留最新(251212.GHO)、HDDownload 非 agent 安装包清理、执行方式（出哈希清单 or 分批移到待确认目录）。
- 状态：方案已交付；后续用户确认后已执行（见下）。

## 2026-11-19 下午 执行结果
- 用户决策：①归类按方案执行、**保留原文件夹名**（111 整个文件夹搬，不摊平）；②系统镜像档不动；③去重移到待删除区观察；④VOB 判断错误已撤销（DVD 每张盘都叫 VTS_01_1.VOB，是标准命名，已联网核实）。
- **归类已完成**：15 个目录移动（video\网络课程→01_视频课程；video 其余→02_视频其他；phonephoto 4 子目录→03_照片；ghost\拆迁录像→04_录像；111→05_资料；HDDownload+迅雷下载→06_下载）。ghost\sysbackup 及零碎文件未动。
- **去重已完成**：29 组 43 个文件（1.27GB）经 SHA256 校验一致后移到 `D:\_待确认删除\dedup_*\`，保留原目录结构，未永久删除。
- 回滚脚本：`tmp/organize_move.py rollback`（15 步）、`tmp/dedup_apply.py rollback`（43 步）；日志 `organize_log.json` / `dedup_apply_log.json`；去重计划 `dedup_plan.json`。
- **注意**：去重脚本内有路径映射 PREFIX_MAP（归类后 phonephoto→03_照片、video\网络课程→01_视频课程），回滚时脚本会按日志里的新路径放回。
- 交付：`去重执行清单.md`、`整理执行完成报告.md`。
- 未做：系统镜像 73GB、非 agent 安装包 25-30GB、缓存约 4GB（等用户后续点头）。
- 关键教训：WizTree CSV 行数 158 万、302MB，Read 工具读不了，须用 Python 流式处理；Windows 上 PowerShell COM(WScript.Shell) 解 .lnk 被安全策略拦截，改用 ls 找同名文件。


# 2026-11-19 工作日志

## YouTube 日本生活中文博主清单（自建搜索调研）

- 用户需求：用自建 SearXNG 在 YouTube 查 50 位介绍日本生活的中文博主（本人长期在日、旅游博主不算），生成含主页 + 3-5 篇视频的 HTML。
- 交付：`D:\workspace\workbuddyai\2026-11-19-14-46-27\日本生活中文博主清单.html`（33 位、160 条视频链接、带关键词过滤）。
- 中间数据与脚本：`jp_bloggers/`（collect_candidates*.py、verify_batch1-10.json、manual_verified.json、build_html.py、validate_final.py）。
- 方法：自建 SearXNG（4 轮 ~100 个查询 + 反查博主名）收集约 250 个频道候选 → 逐条用 `r.jina.ai/http(s)://www.youtube.com/<handle|channel>/videos` 抓频道简介与视频列表（部分用 `youtube.com/feeds/videos.xml?channel_id=` RSS 兜底）→ 按「说中文 + 本人长期在日 + 在日生活内容」三条件核验约 100 个频道 → 生成 HTML。
- 结论：公开可核实范围内只找到 33 位，未凑满 50，未编造补足；剔除大量英语/日语频道、旅游攻略号、新闻搬运号、人在港台或加拿大的频道。唯一视频不足的是「燕子日本农村生活」（频道页 404、搜索无视频直链），HTML 里标注待补。
- 限制：YouTube 不公开博主 IP 属地，无法技术验证 IP；以频道自述「定居日本X年/在日港人/在日中国人」+ 视频内容互证为准，已在 HTML 页脚注明可信度。
- 经验：WebFetch 直连 YouTube 吃 cookie 墙；r.jina.ai 通道对部分 handle 间歇 401/fetch failed，RSS feed 是稳定兜底；WebFetch 返回整段 markdown 很长，交给子 agent 批量提取可避免污染主上下文。


# 2026-11-19

## autoclaw-115（AutoClaw 1.15）

> 数据源：无

（该 Agent 当天日志中未检出此类段落）

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）