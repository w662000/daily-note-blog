---
layout: default
title: 交接文档 · china-stock-data 实测报告（2026-08-04 21_xx）
date: 2026-08-10 23:30:00 +0800
---

> 来源：2026-08-04-20-35-31\china-stock-data-akshare与tushare测试_20260804.md
> 由 handoff_flow.py（scan 阶段）自动收集/提炼，标题取自文档 H1 或日志小节标题，待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。

# china-stock-data 实测报告（2026-08-04 21:xx）

> 环境：托管 venv `C:\Users\Administrator\.workbuddy\binaries\python\envs\default`
> 技能：`@kekewater/china-stock-data` → `~/.workbuddy/skills/@kekewater/china-stock-data`

---

## 一、akshare 安装（最新版）

```
pip install --upgrade akshare tushare
akshare 1.18.81   (最新)
tushare 1.4.29
```
已装进托管默认 venv，可正常 `import akshare, tushare`。

---

## 二、跑通 `report`（券商研报）

### 问题
原始脚本 `akshare_report()` 调用 `ak.stock_jsyjs_anal_em(symbol=...)`，
但 **akshare 1.18 已移除该函数**（akshare 频繁重命名接口），且列名也不匹配新版本 → 直接报错：
`module 'akshare' has no attribute 'stock_jsyjs_anal_em'`

### 修复（最小改动，已写入脚本）
- 函数名：`stock_jsyjs_anal_em` → `stock_research_report_em`（东方财富研报，参数签名 `symbol=` 不变）
- 列名同步更新为新版返回列：股票代码 / 股票简称 / 报告名称 / 东财评级 / 机构 / 行业 / 日期 / 报告PDF链接 / 2026-盈利预测-收益 / 2026-盈利预测-市盈率

> 改动文件：`~/.workbuddy/skills/@kekewater/china-stock-data/scripts/china_stock.py` 的 `akshare_report()`

### 实测输出（真实数据）

**`report 600519 5`（贵州茅台）**
```json
{"source":"AKShare(研报)","code":"600519","reports":[
  {"股票代码":"600519","股票简称":"贵州茅台","报告名称":"需求根基稳固，市场化定价持续兑现",
   "东财评级":"买入","机构":"中邮证券","行业":"白酒Ⅱ","日期":"2026-07-23",
   "报告PDF链接":"https://pdf.dfcfw.com/pdf/H3_AP202607231827290069_1.pdf",
   "2026-盈利预测-收益":67.19,"2026-盈利预测-市盈率":19.42},
  {"股票代码":"600519","股票简称":"贵州茅台","报告名称":"飞天茅台年内二次提价，进一步落实市场化机制",
   "东财评级":"持有","机构":"群益证券","行业":"白酒Ⅱ","日期":"2026-07-20",
   "报告PDF链接":"https://pdf.dfcfw.com/pdf/H3_AP202607201827134022_1.pdf",
   "2026-盈利预测-收益":68.91,"2026-盈利预测-市盈率":18.0}
  // … 共 5 条
]}
```

**`report 000001 3`（平安银行）** 同样返回 3 条真实研报（国信/东兴证券，含 PDF 直链、盈利预测）。

✅ **`report` 已跑通**，无需 token、走 AKShare 公开接口。

---

## 三、Tushare token 能力探测（温和、单次、间隔 3s，未触发限流）

技能 `china_stock.py` 第 511–512 行：
```python
client.DataApi._DataApi__http_url = "http://tushare.xyz"   # 把官方地址改指向非官方域名
TUSHARE_PRO = ts.pro_api('c8dbb3833192a3e47991b1975ad02d95a6567988826e519ba76b0ef5')  # 硬编码 token
```

### 探测 1：走官方 `api.tushare.pro`（安全、不碰 .xyz）
对 6 个接口逐一试探：stock_basic / daily / trade_cal / anns_d / fina_indicator / income
**结果：全部 `❌token/签名错误` —— "您的token不对，请确认。"**
→ 该 token 在官方 Tushare 上 **完全无效，0 个接口可用**。

### 探测 2：复现 skill 实际路径（重定向到 `tushare.xyz`）
仅调用技能里 `tushare_announce` 实际使用的 `anns_d` 一次
**结果：`[.xyz异常] Token已过期，请续费重新激活`**
→ 在 skill 自己的重定向代理上，该 token 也 **已过期失效**。

### 结论
| 目标 endpoint | 返回 | token 状态 | 可调数据 |
|---|---|---|---|
| `api.tushare.pro`（官方） | 您的token不对，请确认 | 无效 | 0 个接口 |
| `tushare.xyz`（skill 重定向） | Token已过期，请续费重新激活 | 过期 | 0 个接口 |

**这个硬编码 token 已经死了，在官方和代理两端都调不到任何数据。`tushare-ann` 及任何 Tushare 依赖路径当前实际不可用。**

### 安全/数据完整性发现 🔴
1. **硬编码 token**：明文写死随包分发，任何装此 skill 的人都能拿到（且已失效）。其它源（问财/聚宽/米筐/同花顺）都走环境变量或配置文件，唯独 Tushare 硬编码，设计不一致。
2. **非官方重定向**：第 511 行把 Tushare 请求静默改发到 `tushare.xyz`（非官方域名）。即使 token 有效，数据也经过不可信第三方代理，**数据来源/完整性无法验证**，属于供应链风险。

### 建议（需你确认后再改，属"重写"安装产物）
- 删除第 512 行硬编码 token，改为读环境变量：`TUSHARE_PRO = ts.pro_api(os.environ.get('TUSHARE_TOKEN'))`
- 删除/改回第 511 行，指向官方 `http://api.tushare.pro`
- 去 https://tushare.pro 注册自己的 token（免费 120 积分可调用 `daily`/`stock_basic`/`trade_cal` 等基础接口；财务/公告等 pro 接口需攒积分）

---

## 四、下一步可选
- A：应用上述修复（去硬编码 token + 去 .xyz 重定向，改读 `TUSHARE_TOKEN`），需你点头
- B：只在官方 endpoint 用你自己的 token 跑一次 `tushare-ann` 验证
- C：本报告仅作结论，先不动脚本