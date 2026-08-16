---
layout: default
title: 技术点 · China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全
date: 2026-08-04 23:30:00 +0800
---

# 技术点 · China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全

> 来源：260804_China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260804_China Stock Data（@kekewater_china-stock-data v2.0.0）用法大全_handoff.md（编码探测：utf-8）
- > 本机安装路径：`C:\Users\Administrator\.workbuddy\skills\@kekewater\china-stock-data`
- > 主脚本：`scripts/china_stock.py`；监控：`scripts/stock_monitor.py`；新闻：`scripts/news_aggregator.py`
- > ⚠️ **路径修正（重要）**：SKILL.md 里把 monitor / news 脚本写成 `~/.hermes/skills/financial/china-stock-data/scripts/...`，那是给 Hermes 的路径，**在本机 WorkBuddy 下是错的**。本大全全部改用上面正确的 WorkBuddy 路径。
- > ⚠️ **依赖**：首次使用需先 `pip install -r requirements.txt`（核心：requests / pytdx / beautifulsoup4 / lxml / pandas / openpyxl；akshare 较重按需装）。问财/JQData/Tushare/米筐需各自 token 或账号。
- ```
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
- > 调用时建议在脚本目录内运行（`cd "$SKILL_DIR/scripts"`），避免脚本内部相对导入问题。
- > 下文实例统一用 `$PY $SCRIPT <子命令> ...` 表示，跑的时候替换成真实路径即可。
- ```
# 实例：查贵州茅台（600519）实时行情（自动含PE/市值/换手率）
$PY $SCRIPT quote 600519

# 实例：查平安银行（000001）
$PY $SCRIPT quote 000001
```
- **前置**：pytdx（无需 Key）。iFinD 未配置时自动跳过。
- ```
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
- **前置**：pytdx，无需 Key。内置 4 台服务器轮询、每次调用间隔 ≥0.5s 防封。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. **TDX 服务器轮询 + 限速**：内置 4 台服务器，调用间隔 ≥0.5s，勿高频轰炸。
2. **EastMoney 限流**：板块排行已自动切同花顺，但 AKShare 研报/资金流仍可能受限，降频调用。
3. **iFinD token 7 天过期**：脚本自动 refresh，但若 refresh 也失效需重配 `ifind_config.json`。
4. **问财需 API Key**：IP 级易 403，未配 `WENCAI_TOKEN` 直接报错属正常。
5. **pandas 降级风险**：装 `jqdatasdk`/`rqdatac` 可能把 pandas 降到 2.3.x，影响 akshare；装完记得 `pip install --upgrade pandas`。
6. **公告优先 CNINFO**：三级降级 CNINFO → Tushare → AKShare，CNINFO 免 Key 且支持全文搜索。
7. **CNINFO PDF**：公告详情页 PDF 地址动态生成，需用浏览器打开详情页取真实链接。

---
