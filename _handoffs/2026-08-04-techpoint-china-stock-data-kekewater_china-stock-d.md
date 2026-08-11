---
layout: default
title: 技术点 · china-stock-data（@kekewater/china-stock-data）用法大全
date: 2026-08-11 13:30:00 +0800
---

# 技术点 · 多源 A 股数据访问层（自动降级 CLI）

> 对应项目轴 Handoff：`2026-08-04-handoff-china-stock-data-kekewater_china-stock-d.md`
> 目的：从该项目提炼**可复用技术资产**——「多个不稳定外部数据源 → 一个稳定统一接口」这类问题的技术选型、降级策略、限流规避与环境约束，下次接任何行情/资讯类多源数据都能直接套用，不必重踩坑。

## 一、技术选型

| 选型项 | 选定 | 落选 | 依据 |
|---|---|---|---|
| 接口形态 | **CLI 子命令**（`china_stock.py <cmd> <args>`，16 个子命令） | Python 库 import / 常驻服务 | Agent 侧调用只需拼一行命令，不必管进程生命周期与依赖隔离；输出统一 JSON 易解析（T1 实测） |
| 免 Key 主行情源 | **通达信 TDX（pytdx）** | 直接用付费终端 API | 免 Key、带 5 档盘口与多周期 K 线，其它免费源给不了盘口（T1） |
| 免 Key 兜底行情源 | **腾讯财经 `qt.gtimg.cn`** | 东方财富 `push2.eastmoney.com` | 东财系在本机网络环境被封（T1 日志实证）；腾讯 HTTP 接口稳定且自带 PE/PB/市值/换手率 |
| 公告源 | **巨潮 CNINFO** 首选 | Tushare Pro / AKShare | CNINFO 免 Key、支持全文搜索、返回真实 PDF 直链，另两者都要 token 或重依赖（T1） |
| 研报/资金流 | **AKShare** | 自己爬东财页面 | AKShare 已封装东财接口并持续跟进字段变更；自爬维护成本高（T1） |
| 语义选股 | **iWencai 问财** | 自建规则筛选 | 自然语言直出候选集；代价是需 token 且 IP 级易 403（T1） |
| Python 运行时 | **WorkBuddy 托管 venv** `binaries/python/envs/default` | 系统 Python / 新建 venv | 依赖已装齐、与其它 skill 共享，避免多份重复环境（T1） |

**选型的核心结论**：免费数据源单个都不可靠，但**故障模式互不相关**（TDX 挂的是 TCP 出网、东财挂的是限流、iFinD 挂的是 token 过期）。所以正确做法不是挑一个"最好的"，而是**按可靠性排序做降级链**。

## 二、实施要点与关键技术

1. **两条降级链，是整套方案的骨架**（T1 实测跑通）：
   - 行情：`TDX → 腾讯 → iFinD`
   - 公告：`CNINFO → Tushare Pro → AKShare`
   降级必须**静默自动**且在返回体里回写 `source` 字段，调用方才知道数据实际来自哪。实测样本里 `quote 600519` 在 TDX 不通时自动落到腾讯并返回 `"source": "腾讯财经"`，链路有效。

2. **路径来源必须核对，不能照抄 SKILL.md**（T1，本项目真实坑）：SKILL.md 把 monitor / news 脚本写成 `~/.hermes/skills/financial/china-stock-data/scripts/...`，那是 Hermes 的路径；在 WorkBuddy 下真实路径是：
   ```bash
   SKILL_DIR="C:/Users/Administrator/.workbuddy/skills/@kekewater/china-stock-data"
   PY="C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
   ```
   **通用教训**：跨宿主分发的 skill，文档里的绝对路径大概率是作者宿主的，安装后必须实测一次。

3. **Windows 路径用带盘符原生形式，不要用 `/c/...` POSIX 形式**（T1）——Git Bash 下 `/c/...` 会被下游工具当成相对路径拼成 `D:\c\...`。

4. **在脚本目录内调用**：`cd "$SKILL_DIR/scripts"` 后再执行，规避脚本内部相对导入失败（T1）。

5. **主动限速，不等对方封你**（T1）：TDX 侧内置 4 台服务器轮询 + 每次调用间隔 ≥0.5s。这是"客户端自律"模式——比被封后再加退避重试成本低得多。

6. **凭据分级管理**：
   - 免 Key：TDX、腾讯、CNINFO、同花顺板块/快讯
   - 环境变量：`WENCAI_TOKEN`、`JQ_USER`/`JQ_PASS`、`RQ_USER`/`RQ_PASS`
   - 配置文件：`ifind_config.json`（`access_token` 7 天有效，脚本用 `refresh_token` 自动续；refresh 也失效才需人工重配）

7. **`status` 子命令是排障入口**（可复用设计）：一条命令列出全部数据源的 ✅可用 / ⚠️待配置 / ❌未安装。多源系统必须有这么一个自检出口，否则出问题时无法快速定位是哪条链断了。

8. **依赖分层装**（T1）：核心 `requests / pytdx / beautifulsoup4 / lxml / pandas / openpyxl` 必装；`akshare` 较重按需装。
   **⚠️ 依赖冲突坑**：装 `jqdatasdk` / `rqdatac` 会把 pandas 降到 2.3.x 影响 akshare，装完补 `pip install --upgrade pandas`。

9. **网络环境约束（本机实证，T1）**：
   - 东方财富系（`push2his` / `push2.eastmoney.com`）被封
   - TDX 行情服务器 TCP 出网被沙箱拦截 → `tdx-*` 子命令在沙箱内必失败，本机正常网络可用
   - akshare 走系统代理报 ProxyError，**新浪源 + `requests` 设 `trust_env=False` 可直连**（这条是同期全市场日线下载能跑通的关键）
   - 托管 pip 默认 safe-delete 进回收站，沙箱无回收站会 `SAFE_DELETE_FAIL_CLOSED` 中止 → 需给 pip 单开沙箱豁免

10. **CNINFO PDF 详情页地址动态生成**（T1）：列表接口返回的 `pdf_url` 可直接用，但详情页里的其它附件需浏览器打开取真实链接。

## 三、模块职责划分

- **`china_stock.py` = 统一查询入口**：16 个子命令，承载全部行情/财务/公告/板块/选股，内部实现降级与源标注。
- **`stock_monitor.py` = 状态触发器**：`check <code> [阈值] [above|below]` 与 `watchlist`，只做"当前值 vs 阈值"判定，不存历史；配 cron 就是盯盘。
- **`news_aggregator.py` = 资讯聚合**：`daily` / `indices` / `headlines`，与行情通道解耦（挂了不影响报价）。
- **`sec_edgar.py` = 境外数据旁路**：美股 SEC，与 A 股主链无耦合。
- **`references/` = 外部接口知识库**：CNINFO API、TDX 协议与限速、东财限流备忘、同花顺快讯 API 等 6 篇笔记。**这一层最容易被忽略但价值最高**——外部接口的字段与限流规则会漂移，把已验证的细节沉淀成文档，比散落在代码注释里可复用得多。
- **职责边界原则**：数据获取（多源+降级）、状态判定（阈值）、内容聚合（资讯）三者分离，任一条挂掉不拖垮其它两条。

## 四、如何选型（可复用的决策方法论）

1. **先按"是否需要凭据"分层**：免 Key 源做主链和兜底，需 Key 源做增强。这样系统在零配置状态下就能跑出可用结果，配置只提升上限、不决定可用性。
2. **降级链的排序依据是"数据质量 × 可用概率"，不是"名气"**：TDX 排第一是因为它给盘口（质量最高），腾讯排第二是因为它几乎不挂（概率最高），iFinD 排第三是因为 token 会过期。
3. **故障模式要互不相关**：如果降级链上两个源都走东方财富，东财一限流两个一起死，降级等于没做。选备胎时优先选**不同厂商、不同协议、不同鉴权方式**的源。
4. **判断一个第三方数据源能不能长期用**，看三点：是否免 Key、字段是否稳定（有无历史改名记录）、限流是否可预测。三项全不满足的只能当"锦上添花"，不能进主链。
5. **同类能力优先复用已有封装**（AKShare 之于东财接口），自己爬只在封装缺失或已失效时做。

## 五、深化学习指引

| 主题 | 看哪 | 类型 | 可信度 |
|---|---|---|---|
| AKShare 全部接口与参数 | akshare.akfamily.xyz 官方文档 | 官方文档 | T0 |
| pytdx / 通达信协议 | pytdx 项目文档 + skill 内 `references/tdx-protocol-notes.md` | 官方+自记 | T1 |
| TDX 限速与反封策略 | skill 内 `references/tdx-rate-limiting.md`（4 服务器轮询 / ≥0.5s） | 自己实测 | T1 |
| 巨潮 CNINFO 接口 | skill 内 `references/cninfo-api.md` + `cninfo-pdf-extraction.md` | 自记 | T1 |
| 东方财富限流边界 | skill 内 `references/eastmoney-limitations.md` | 自记 | T1 |
| 同花顺快讯结构（`data.list` / `shareUrl`） | skill 内 `references/tonghuashun-headlines-api.md` | 自记 | T1 |
| Tushare Pro 积分与接口权限 | tushare.pro 官网 | 官方 | T0 |
| JQData / RiceQuant 量化接口 | joinquant.com / ricequant.com 文档 | 官方 | T0 |
| 问财语义选股的查询表达法 | 暂无权威文档，靠试 | 待补 | T2（待核实） |
| `trust_env=False` 绕系统代理的适用边界 | requests 官方文档 + 本机实测 | 官方+实测 | T1 |

## 六、技术结合点

- **降级链 + 源标注**：单有降级不够，必须回写 `source`。否则调用方拿到数据不知道是盘口级还是快照级，会做出错误判断。两者合起来才是"可信的高可用"。
- **主动限速 + 服务器轮询**：单独轮询会把每台服务器都打到限流，单独限速则吞吐太低；4 台轮询 × ≥0.5s 间隔，等效单机间隔 2s、整体吞吐不降，这是 1+1>2 的组合。
- **`status` 自检 + 凭据分级**：分级让系统零配置可跑，自检让用户知道"再配哪个能解锁什么"。缺任一个，多源系统就变成黑盒。
- **免 Key 主链 + 环境变量增强源**：免 Key 保证下限，token 源提升上限，且 token 失效时自动退回下限而不是整体报错——这是"优雅降级"落到凭据层面的具体形态。
- **`references/` 知识库 + 代码**：外部接口漂移是必然事件（同期就撞上 AKShare 函数改名）。把限流数值、字段名、协议细节沉淀成独立文档，修复时改一处、查一处，比在代码里考古快一个量级。

---
> 本文为技术点轴产出（对应 Handoff 2026-08-04）。固定六章：技术选型 / 实施要点与关键技术 / 模块职责划分 / 如何选型 / 深化学习指引 / 技术结合点。
