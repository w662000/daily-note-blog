---
layout: default
title: 交接文档 · autoclaw-slg-resume-plan
date: 2026-08-12 23:30:00 +0800
---

# slg-resume-plan（AutoClaw 项目表）— 交接文档

# SLG 采集恢复计划（路线 A / 路线 B）

> 背景：2026-08-09 实测确认微信对"新浏览器环境"做了环境级风控（任何新 profile 窗口 2 秒内"请重新登录"，即使正常扫码）。同日已停止全部自动化并清理。
> 目的：冷却期过后按本计划恢复 SLG 公众号采集。**冷却建议 24-48 小时**（8/10 晚 ~ 8/11 再动手）。

---

## 路线 A：复制真实 profile + Playwright 复用（首选）

原理：把用户真实 Edge profile（含登录态、指纹、历史）完整复制到非默认目录，Playwright 用它启动——微信看到的是"熟悉的浏览器环境 + 已有登录态"，理论上不触发环境风控，且**无需扫码**。

### 前置条件
- [ ] 冷却期 ≥24h（从 8/9 13:15 起算）
- [ ] 用户正常 Edge 保持登录态（**不要退出登录、不要清理数据**）
- [ ] D 盘有 ≥2GB 空闲

### 步骤（冷却后执行）
1. **完全退出 Edge**（所有窗口 + 任务管理器确认无 msedge.exe）
2. 运行克隆脚本（约 1-3 分钟）：
   ```powershell
   powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\edge-profile-clone.ps1
   ```
   - 源：`C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default`（~1.1GB）
   - 目标：`D:\edge-pw-profile\Default`（排除 Cache/GPUCache 等纯缓存）
   - 验证输出：Cookies / Local Storage / Network / Preferences 全部 OK
3. 修改抓取脚本 profile 路径（把 `D:\edge-pw-profile` 写入）：
   ```powershell
   # 复制 tmp 下的脚本到 workspace 正式位置，改 PROFILE 变量
   Copy-Item C:\Users\Administrator\.openclaw-autoclaw\workspace\.openclaw\tmp\pw_repost2.py C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\slg_repost_grab.py
   ```
   - 编辑 `slg_repost_grab.py`：`PROFILE = r'D:\edge-pw-profile'`
   - **预期无需扫码**（profile 自带登录态）；若仍提示登录 → 说明风控未解除，立即停止并等更久
4. 单号验证（温和，1 个请求）：
   ```powershell
   python slg_repost_grab.py 九牧手游助手
   ```
   - 成功标志：打印 ROW（文章行）+ A（mp.weixin 链接带 __biz/mid/idx/sn）
5. 全量温和抓取（6 个号，每次间隔 ≥30 秒）：
   ```powershell
   python slg_repost_grab.py 九牧配将君; sleep 30; python slg_repost_grab.py 九牧手游攻略站; ...
   ```
   - 每个号 1 次搜索、count 默认 10 条左右
6. 入库：把抓到的链接增量写入 D1（复用 `json_to_sql.py` + `wrangler d1 execute`，INSERT OR IGNORE 去重）
7. 挂回每日自动化：`automation-1785299048973` PAUSE → ACTIVE（先手动跑通 1 天再恢复）

### 失败判定与回退
- 复制 profile 后启动仍"请重新登录" → **风控未解除**，停手，再冷却 48h 或转路线 B
- Playwright 报 profile 锁 → Edge 没退干净，重来
- 抓取正常但链接缺 SN → 检查结果页 DOM（链接在结果项点击后的新窗口 URL，可能需要点开第一项验证）

### 长期维护
- 抓取脚本固定用 `D:\edge-pw-profile`；微信 cookie 2-3 天过期 → 每 2 天重新克隆一次 profile（覆盖复制）刷新登录态；或接受每周重克隆
- 克隆频率与自动化频率解耦：克隆 = 续命登录态，抓取 = 每日增量

---

## 路线 B：wewe-rss（微信读书通道，备用/长期）

与公众号后台无关（走 weread），不受本次风控影响。WorkBuddy 8/2 已设计完整，挂起在：
- 方案设计：`D:\AI work\workbuddy\2026-08-02-18-41-45\wewe-rss-test\SLG_A方案_wewe-rss_实测与多方案设计_2026-08-02.md`
- 主机部署：`SLG_A方案_主机决策_Wispbyte_2026-08-02.md`（7 步命令齐全）
- 集成草图：`integration_sketch.md`（consume_rss → D1）
- 唤醒词：跟 WorkBuddy 说「wispbyte项目」

### 执行要点（冷却期可并行准备）
1. Wispbyte Console（78.154.103.35）执行 7 步：停 gost → Node/pm2 → clone wewe-rss → start.sh（PORT 13986）→ pm2 save → Startup 改 `pm2 resurrect`
2. 浏览器开 `http://78.154.103.35:13986` → 微信读书扫码 → 订阅 6 个 SLG 公众号（分享链接添加）
3. 拿 feed URL（`/feeds/MP_WXS_<id>.json`）→ 写 `consume_rss()` 消费 → 复用现有 json_to_sql/D1 入库
4. 风险点：微信读书账号 2-3 天重扫一次；weread 中转若被封则方案失效（当前 8/2 实测 HTTP 200 存活）

---

## 决策树（冷却期后）

```
冷却 ≥24h
 ├─ 路线 A 单号验证成功 → 全量 → 挂自动化（首选）
 ├─ 路线 A 失败（仍被风控）→ 等 48h 再试一次
 │    └─ 仍失败 → 路线 B（wewe-rss 部署）
 └─ 用户手动模式兜底：每周手动转载搜索 5 分钟，链接存文件，我做增量入库
```

## 红线（踩过的坑，勿重犯）
- ❌ 反复新建浏览器实例弹登录页（触发环境风控的直接原因）
- ❌ 向新实例注入 cookie（被识别为自动化）
- ❌ 风控期连续重试（加深标记；每次失败后至少停 24h）
- ✅ 只在"用户真实环境"（真实 profile 或复制品）里操作
- ✅ 每号每天 1 次搜索、间隔 ≥30 秒、count ≤10
