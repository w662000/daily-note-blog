---
layout: default
title: 交接文档 · China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全
date: 2026-08-17 23:30:00 +0800
---

# China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全

- **日期**：2026-08-04
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260804_China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全_handoff.md（编码探测：utf-8）

> 来源：2026-08-04-20-35-31\china-stock-data-用法大全.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。


> 本机安装路径：`C:\Users\Administrator\.workbuddy\skills\@kekewater\china-stock-data`
> 主脚本：`scripts/china_stock.py`；监控：`scripts/stock_monitor.py`；新闻：`scripts/news_aggregator.py`
>
> ⚠️ **路径修正（重要）**：SKILL.md 里把 monitor / news 脚本写成 `~/.hermes/skills/financial/china-stock-data/scripts/...`，那是给 Hermes 的路径，**在本机 WorkBuddy 下是错的**。本大全全部改用上面正确的 WorkBuddy 路径。
>
> ⚠️ **依赖**：首次使用需先 `pip install -r requirements.txt`（核心：requests / pytdx / beautifulsoup4 / lxml / pandas / openpyxl；akshare 较重按需装）。问财/JQData/Tushare/米筐需各自 token 或账号。

## 0. 统一约定（变量 + 代码格式）

```bash
# 本机真实路径（Windows 原生，带盘符，别用 /c/... POSIX 形式）
SKILL_DIR="C:/Users/Administrator/.workbuddy/skills/@kekewater/china-stock-data"
SCRIPT="$SKILL_DIR/scripts/china_stock.py"
MON="$SKILL_DIR/scripts/stock_monitor.py"
NEWS="$SKILL_DIR/scripts/news_aggregator.py"
# 用托管 venv 的 python（已装核心依赖）
PY="C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"

# 股票代码格式（脚本自动识别沪/深，无需 sh/sz 前缀）
#   上海A股  6xxxxx   例 600519（贵州茅台）
#   深圳主板 00xxxx   例 000001（平安银行）
#   创业板   30xxxx   例 300750（宁德时代）
#   科创板   688xxx   例 688981
```

> 调用时建议在脚本目录内运行（`cd "$SKILL_DIR/scripts"`），避免脚本内部相对导入问题。
> 下文实例统一用 `$PY $SCRIPT <子命令> ...` 表示，跑的时候替换成真实路径即可。

---

## A. 智能行情（自动降级：TDX → 腾讯 → iFinD）

自动选最优源，并补 PE / 市值 / 换手率。

```bash
# 实例：查贵州茅台（600519）实时行情（自动含PE/市值/换手率）
$PY $SCRIPT quote 600519

# 实例：查平安银行（000001）
$PY $SCRIPT quote 000001
```

**返回**：名称、代码、现价、涨跌幅、昨收、今开、最高/最低、成交量、PE、总市值、流通市值、换手率等。
**前置**：pytdx（无需 Key）。iFinD 未配置时自动跳过。

---

## B. 通达信 TDX（实时 + 5档盘口 + K线）

```bash
# 实例1：贵州茅台 实时行情 + 5档买卖盘口
$PY $SCRIPT tdx-quote 600519

# 实例2：宁德时代（300750）日K线（默认约30条）
$PY $SCRIPT tdx-kline 300750 daily

# 实例3：贵州茅台 周K线
$PY $SCRIPT tdx-kline 600519 weekly

# 实例4：贵州茅台 60分钟K线
$PY $SCRIPT tdx-kline 600519 60min

# 周期可选：daily / weekly / monthly / 60min / 30min / 15min / 5min
```

**返回（tdx-quote）**：现价、买一~买五（价/量）、卖一~卖五（价/量）、涨停/跌停价等。
**返回（tdx-kline）**：OHLCV 序列（日期、开、高、低、收、量、额）。
**前置**：pytdx，无需 Key。内置 4 台服务器轮询、每次调用间隔 ≥0.5s 防封。

---

## C. 腾讯财经（财务指标 + 批量）

```bash
# 实例1：平安银行（000001）PE/PB/市值/换手率
$PY $SCRIPT tencent-quote 000001

# 实例2：批量查 茅台/宁德/平安
$PY $SCRIPT tencent-batch 600519,300750,000001
```

**返回**：PE(TTM)、PB、总市值、流通市值、换手率、现价、涨跌幅。
**前置**：requests（公开 HTTP API `qt.gtimg.cn`，无需 Key）。

---

## D. 同花顺 iFinD（专业行情，需 token）

```bash
# 实例：贵州茅台 专业行情（含PE/换手率/股息率/振幅）
$PY $SCRIPT ifind-quote 600519
```

**返回**：实时价、PE、换手率、股息率、振幅等 iFinD 专业字段。
**前置**：
1. 在脚本同目录放 `ifind_config.json`：`{"access_token":"...","refresh_token":"..."}`
2. access_token 7 天有效，脚本会自动用 refresh_token 刷新。

---

## E. AKShare（研报 / 资金流向）

```bash
# 实例1：贵州茅台 最近10份券商研报
$PY $SCRIPT report 600519 10

# 实例2：贵州茅台 最近5天资金流向
$PY $SCRIPT moneyflow 600519 5
```

**返回（report）**：研报标题、机构、评级、日期、原文链接。
**返回（moneyflow）**：主力净流入、超大单/大单/中单/小单净额、日期。
**前置**：akshare（较重，按需 `pip install akshare`）。EastMoney 源可能限流，建议降频。

---

## F. 公告查询（三级降级：巨潮 CNINFO → Tushare Pro → AKShare）

```bash
# 实例1：贵州茅台 最近20条公告（自动选最佳源，首选 CNINFO）
$PY $SCRIPT announce 600519 20

# 实例2：强制走 Tushare Pro 公告
$PY $SCRIPT tushare-ann 600519

# 实例3：Tushare Pro 最新20条公告
$PY $SCRIPT tushare-ann 600519 20
```

**返回**：公告标题、日期、交易所、公告链接（CNINFO 支持全文搜索且无需 Key）。
**前置**：CNINFO 免 Key；Tushare 分支需 `pip install tushare` 并配置 token（脚本内 `http://tushare.xyz`）。

---

## G. 板块排行 & 热点题材

```bash
# 实例1：行业板块排行 TOP20
$PY $SCRIPT sector

# 实例2：热点题材（行业 + 概念）
$PY $SCRIPT themes
```

**返回（sector）**：板块名、涨跌幅、领涨股、成交额排行。
**返回（themes）**：行业/概念板块涨幅榜。EastMoney 限流时自动切同花顺页面。
**前置**：requests / AKShare（无需 Key）。

---

## H. 问财语义搜索（自然语言选股，需 WENCAI_TOKEN）

```bash
# 实例：搜索「人形机器人 + 丝杠」相关标的
$PY $SCRIPT search 人形机器人 丝杠

# 实例：华为概念 + 业绩预增
$PY $SCRIPT search 华为概念 业绩预增
```

**返回**：符合条件股票列表（代码、名称、相关指标）。
**前置**：`export WENCAI_TOKEN=your_token`（问财接口目前 IP 级易 403，需经 SkillHub 拿 API Key）。
**注意**：未配置会直接报错，这是预期行为。

---

## I. Tushare Pro（财报/公告类，需 token）

```bash
# 实例：贵州茅台 最新20条公告
$PY $SCRIPT tushare-ann 600519 20
```

**返回**：公告列表（同 F 节）。
**前置**：`pip install tushare` + 脚本内配置 token；国内需 `http://tushare.xyz`。

---

## J. JQData 聚宽（量化因子 + 宏观，需账号）

```bash
# 实例1：贵州茅台 财报指标
$PY $SCRIPT jq-financial 600519

# 实例2：宏观数据（GDP/CPI）
$PY $SCRIPT jq-macro
```

**返回（jq-financial）**：ROE、毛利率、营收/净利等基本面因子。
**返回（jq-macro）**：GDP、CPI 等宏观序列。
**前置**：`export JQ_USER=手机号 JQ_PASS=密码`；`pip install jqdatasdk`；JoinQuant 免费注册。

---

## K. RiceQuant 米筐（量化回测，需账号）

- 接口 `rqdatac`，配置 `export RQ_USER=用户名 RQ_PASS=密码`，`pip install rqdatac`。
- SKILL.md 当前未单列米筐子命令示例，能力并入量化数据通道；如需具体命令以 `china_stock.py` 实际子命令为准（可用 `python china_stock.py --help` 查看）。

---

## L. Stock Monitor 股票监控（内置，无需 Key）

```bash
# 实例1：检查贵州茅台当前价格
$PY $MON check 600519

# 实例2：检查是否跌破 1300
$PY $MON check 600519 1300 below

# 实例3：自选股异动扫描（读默认 watchlist）
$PY $MON watchlist

# 实例4：指定列表异动扫描
$PY $MON watchlist 600519,300750,000001
```

**返回（check）**：当前价 + 是否触发阈值（可配合 cron 定时盯盘）。
**返回（watchlist）**：列表内个股涨跌幅异动、触发预警项。
**前置**：pytdx（核心）。可配 cronjob 定时跑 `check`/`watchlist` 做自动盯盘。

---

## M. News Aggregator 新闻简报（内置，无需 Key）

```bash
# 实例1：当日金融简报（指数 + 头条）
$PY $NEWS daily

# 实例2：主要指数行情
$PY $NEWS indices

# 实例3：同花顺快讯
$PY $NEWS headlines
```

**返回（daily）**：主要指数涨跌幅 + 当日头条新闻汇总。
**返回（indices）**：上证/深证/创业板/沪深300 等实时点位与涨跌。
**返回（headlines）**：同花顺快讯流（最新 `data.list` 结构，字段 `shareUrl`）。
**前置**：requests / beautifulsoup4。

---

## N. 系统状态 status

```bash
# 实例：查看全部数据源可用状态
$PY $SCRIPT status
```

**返回**：每个数据源（TDX / 腾讯 / iFinD / AKShare / 问财 / JQData / Tushare / 米筐 / CNINFO）的 ✅ 可用 / ⚠️ 待配置 状态，便于排查哪个源没配好。

---

## 常见坑（实战提醒）

1. **TDX 服务器轮询 + 限速**：内置 4 台服务器，调用间隔 ≥0.5s，勿高频轰炸。
2. **EastMoney 限流**：板块排行已自动切同花顺，但 AKShare 研报/资金流仍可能受限，降频调用。
3. **iFinD token 7 天过期**：脚本自动 refresh，但若 refresh 也失效需重配 `ifind_config.json`。
4. **问财需 API Key**：IP 级易 403，未配 `WENCAI_TOKEN` 直接报错属正常。
5. **pandas 降级风险**：装 `jqdatasdk`/`rqdatac` 可能把 pandas 降到 2.3.x，影响 akshare；装完记得 `pip install --upgrade pandas`。
6. **公告优先 CNINFO**：三级降级 CNINFO → Tushare → AKShare，CNINFO 免 Key 且支持全文搜索。
7. **CNINFO PDF**：公告详情页 PDF 地址动态生成，需用浏览器打开详情页取真实链接。

---

## 实测样本（本机真实跑出来的输出）

> 环境：本机托管 venv（已装核心依赖 requests/pytdx/bs4/lxml/pandas/openpyxl）。
> 网络说明：**通达信(TDX) 的 TCP 出网在本沙箱被拦截**，所以 `tdx-*` 命令报错；但 `quote` 的**自动降级（TDX→腾讯）正常工作**，下方可见。在用户本机（正常网络）TDX 应可用。
> 需 token / 需 akshare（report、moneyflow、ifind、问财、JQData、Tushare、米筐）未配置，对应命令见上面各章节说明。

### ① status —— 全源状态
```json
{
  "通达信(TDX)": "✅可用",
  "腾讯财经": "✅可用",
  "同花顺(iFinD)": "⚠️未配置token",
  "AKShare": "✅可用",
  "iWencai(问财)": "⚠️未配置WENCAI_TOKEN",
  "JQData(聚宽)": "❌未安装",
  "JQData认证": "⚠️需JQ_USER/JQ_PASS",
  "Tushare Pro": "❌未安装",
  "RiceQuant(米筐)": "❌未安装",
  "RiceQuant认证": "⚠️需RQ_USER/RQ_PASS"
}
```

### ② tencent-quote 000001 —— 平安银行实时财务
```json
{"source": "腾讯财经", "code": "000001", "name": "平安银行", "price": 11.44,
 "open": 11.58, "high": 11.62, "low": 11.42, "last_close": 11.62,
 "change": -0.18, "change_pct": -1.55, "volume": 1221130, "amount": 512459.0,
 "turnover_rate": 0.63, "pe": 5.16, "market_cap": 2220.04,
 "circulating_cap": 2220.0, "time": "20260804161451"}
```

### ③ quote 600519 —— 智能行情（演示自动降级）
> TDX 在本沙箱连不通，脚本自动降级到腾讯财经，成功返回：
```json
{"source": "腾讯财经", "code": "600519", "name": "贵州茅台", "price": 1328.36,
 "open": 1350.06, "high": 1350.94, "low": 1328.36, "last_close": 1358.98,
 "change": -30.62, "change_pct": -2.25, "volume": 37450, "amount": 15440.0,
 "turnover_rate": 0.3, "pe": 20.08, "market_cap": 16605.58,
 "circulating_cap": 16605.58, "time": "20260804161455"}
```

### ④ tdx-quote 600519 —— TDX 实时+盘口（沙箱出网被拦，仅环境限制）
```json
{"error": "TDX查询失败:600519"}
```
> 本沙箱拦截了到 TDX 行情服务器的 TCP 连接，故报错；**本机正常网络下应返回实时价 + 五档盘口**。不影响其它源。

### ⑤ sector —— 同花顺行业板块 TOP20（取前 3，共 20 条）
```json
{"source": "同花顺(行业板块)", "sectors": [
 {"序号":"1","板块":"元件","涨跌幅(%)":"146.28","总成交额（亿元）":"1123.39","净流入（亿元）":"65.07","上涨家数":"63","下跌家数":"0","领涨股":"嘉立创","最新价":"208.01"},
 {"序号":"2","板块":"电子化学品","涨跌幅(%)":"13.43","总成交额（亿元）":"436.50","净流入（亿元）":"31.64","上涨家数":"43","下跌家数":"0","领涨股":"唯特偶","最新价":"92.8"},
 {"序号":"3","板块":"半导体","涨跌幅(%)":"20.00","总成交额（亿元）":"3363.67","净流入（亿元）":"233.68","上涨家数":"178","下跌家数":"5","领涨股":"和林微纳","最新价":"93.79"}
]}
```

### ⑥ themes —— 同花顺热点（行业 + 概念）
```json
{"source": "同花顺热点", "industry": [
 {"序号":"1","板块":"元件","涨跌幅(%)":"146.28","净流入（亿元）":"65.07","领涨股":"嘉立创","最新价":"208.01"},
 {"序号":"2","板块":"电子化学品","涨跌幅(%)":"13.43","净流入（亿元）":"31.64","领涨股":"唯特偶","最新价":"92.8"}
], "concept": []}
```

### ⑦ announce 600519 5 —— 巨潮 CNINFO 公告（免 Key，真实链接）
```json
{"source": "巨潮资讯网(CNINFO)", "code": "600519", "announcements": [
 {"title":"贵州茅台重大事项公告","date":"2026-07-18","pdf_url":"http://www.cninfo.com.cn/finalpage/2026-07-18/1225431263.PDF"},
 {"title":"贵州茅台2025年年度权益分派实施公告","date":"2026-06-22","pdf_url":"http://www.cninfo.com.cn/finalpage/2026-06-22/1225379934.PDF"},
 {"title":"贵州茅台董事、高级管理人员考核和薪酬管理办法","date":"2026-06-12","pdf_url":"http://www.cninfo.com.cn/finalpage/2026-06-12/1225366261.PDF"},
 {"title":"北京市金杜律师事务所关于贵州茅台酒股份有限公司2025年度股东会之法律意见书","date":"2026-06-12","pdf_url":"http://www.cninfo.com.cn/finalpage/2026-06-12/1225366263.PDF"},
 {"title":"贵州茅台第五届董事会2026年度第一次会议决议公告","date":"2026-06-12","pdf_url":"http://www.cninfo.com.cn/finalpage/2026-06-12/1225366262.PDF"}
]}
```
