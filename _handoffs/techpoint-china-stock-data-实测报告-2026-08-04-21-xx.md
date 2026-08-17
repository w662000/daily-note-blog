---
layout: default
title: 技术点 · china-stock-data 实测报告（2026-08-04 21:xx）
date: 2026-08-04 23:30:00 +0800
---

# 技术点 · china-stock-data 实测报告（2026-08-04 21:xx）

> 来源：260804_china-stock-data 实测报告（2026-08-04 21_xx）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- > 环境：托管 venv `C:\Users\Administrator\.workbuddy\binaries\python\envs\default`
- ```
pip install --upgrade akshare tushare
akshare 1.18.81   (最新)
tushare 1.4.29
```
- 原始脚本 `akshare_report()` 调用 `ak.stock_jsyjs_anal_em(symbol=...)`，
- 但 **akshare 1.18 已移除该函数**（akshare 频繁重命名接口），且列名也不匹配新版本 → 直接报错：
- 列名同步更新为新版返回列：股票代码 / 股票简称 / 报告名称 / 东财评级 / 机构 / 行业 / 日期 / 报告PDF链接 / 2026-盈利预测-收益 / 2026-盈利预测-市盈率
- ```
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
- ✅ **`report` 已跑通**，无需 token、走 AKShare 公开接口。
- ```
client.DataApi._DataApi__http_url = "http://tushare.xyz"   # 把官方地址改指向非官方域名
TUSHARE_PRO = ts.pro_api('c8dbb3833192a3e47991b1975ad02d95a6567988826e519ba76b0ef5')  # 硬编码 token
```
- 对 6 个接口逐一试探：stock_basic / daily / trade_cal / anns_d / fina_indicator / income
- **结果：全部 `❌token/签名错误` —— "您的token不对，请确认。"**
- → 该 token 在官方 Tushare 上 **完全无效，0 个接口可用**。
- **结果：`[.xyz异常] Token已过期，请续费重新激活`**

## 三、关键产物与命令
- 删除第 512 行硬编码 token，改为读环境变量：`TUSHARE_PRO = ts.pro_api(os.environ.get('TUSHARE_TOKEN'))`
- 删除/改回第 511 行，指向官方 `http://api.tushare.pro`
- 去 https://tushare.pro 注册自己的 token（免费 120 积分可调用 `daily`/`stock_basic`/`trade_cal` 等基础接口；财务/公告等 pro 接口需攒积分）

---

## 四、如何复现 / 重打
仅调用技能里 `tushare_announce` 实际使用的 `anns_d` 一次
**结果：`[.xyz异常] Token已过期，请续费重新激活`**
→ 在 skill 自己的重定向代理上，该 token 也 **已过期失效**。

## 五、后续风险
（见源 handoff 后续风险字段）
