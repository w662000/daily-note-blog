---
layout: default
title: 交接文档 · Clash_v2rayN 最新免费节点查询与验证
date: 2026-11-14 23:30:00 +0800
---

# Clash/v2rayN 最新免费节点查询与验证

- **日期**：2026-11-11
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-11-11-16-10-05\backup\clash-node-check_20261111_1625\SKILL.md

---
name: "clash-node-check"
version: "1.2.0"
description: "查最新可用免费节点(Clash/v2rayN):搜索→GitHub拉源→镜像验证→TCP抽检→时效核查→互转服务实测→双格式订阅链接→双格式HTML报告(报告开头自动冠以生成方agent名)。触发:查clash最新/查最新可用"
---

# Clash/v2rayN 最新免费节点查询与验证

用户说「查clash最新」「查最新可用」「查v2rayN节点」「查免费节点」「查节点」等时执行本流程。

产出 = 聊天正文结论（**首行标题与报告一致：`xxx免费节点订阅报告`**；**每组订阅同时给 v2rayN 与 Clash Verge 两条可粘贴链接**）+ `reports/免费节点订阅报告_YYYYMMDD.html`（双格式版）。

**报告开头必须署生成方 agent 名**：`<title>` 与 `<h1>` 均为 `<agent名>免费节点订阅报告`。例：WorkBuddy 国际版生成 → `workbuddy国际版免费节点订阅报告`；Loomy 生成 → `loomy免费节点订阅报告`；小浣熊生成 → `小浣熊免费节点订阅报告`。名字由脚本自动识别，不用手工改 HTML。

> **v1.2.0（2026-11-10）新增：报告署生成方 agent 名**。同一个 skill 分发到 6 个 agent，以前生成的报告标题完全一样、同日还会互相覆盖文件名，分不清是谁跑的。现 `dual_report_template.py` 自动解析宿主 agent 名并注入 `<title>` / `<h1>` / `<meta name=generator>` / 页脚，同时加入「标题与 H1 必须含 agent 名」的自校验、HTML 转义与 `--print-agent` 自检。每个安装位根目录新增纯文本 `AGENT_NAME`（各写各的名字，**同步时不能整体覆盖**）；脚本被复制到别处时按安装路径规则兜底。可选 `--agent-in-filename` 让文件名也带前缀（默认不带，保持旧路径兼容）。已用 6 种身份 + 转义 + CLI 回归测试全 PASS。
>
> **v1.1.1（2026-11-10）修复**：`dual_report_template.py` 的一键复制 JS 原先直接调 `navigator.clipboard.writeText(...)`，在 `file://` / 旧内核下该对象整个不存在时会抛 TypeError 且 `.then` 的 rejection 兜底不执行；兜底分支还漏了按钮文字 1.4s 恢复。现改为 `try/catch` + 统一 `fallback()` + `execCommand` + 统一的「已复制」反馈与恢复。已用 Node 模拟 DOM 验证 4 种场景（clipboard 正常 / Promise reject / 同步 throw / 对象不存在）全部通过。
>
> **v1.1.0（2026-11-09）变更**：报告从「一条订阅一个链接」升级为「双格式版」——新增互转服务实测、双链接生成/验证、两列一键复制、纯文本双链接清单、互转限制说明；同时**合并了 WorkBuddy 国内版副本的二次实战补充**（gh 限流改走 Atom feed、Clash 列表项计数、一键复制兜底、README 过滤规则等）。同步到各安装位前先完整备份（P0 红线）。

## 核心原则

1. 所有订阅链接必须**实测下载成功**后才推荐，不许把未验证的搜索结果直接给用户。
2. 交付链接一律用**镜像通道**（gh-proxy.com / ghproxy.net），用户客户端无需已有代理即可拉取。
3. 必须用 GitHub 数据查仓库最后推送/提交时间，戳破「每日/每小时更新」的假宣传——以 commits 时间为准。**`gh` token 失效 / 撞未认证 60 次每小时限流（403 `API rate limit exceeded`）时不要重试死磕**：先 `gh auth status` + `gh api rate_limit` 各查一次确认根因，再按序回退 ① 公开 REST API `GET /repos/{owner}/{repo}` 的 `pushed_at` ② `https://gh-proxy.com/https://github.com/<repo>/commits/main.atom`，解析**第二处** `<updated>`（feed 级之后即最新 commit）。Atom feed 同为 GitHub 官方数据，可信度不降级，且能完全绕开 API 限流。
4. TCP 抽检可连 ≠ 协议可用，报告和正文都必须注明，并建议导入后测真连接延迟。
5. **每条有效订阅默认产出两条链接**（v2rayN / Clash Verge）。两条是同一批节点的两种格式，按客户端挑一列，**不要两列都导入**。
6. **能用实测直链就别经过转换服务**：优先级 `原生直链 → 同源另一格式 → 转换生成`。转换生成的链接必须逐条请求验证；未通过的如实标「未通过」，不许拿未验证链接凑数。
7. 改本 skill、覆盖既有报告或数据文件前，先完整备份并 `diff -rq` 校验一致（用户 P0 红线）；启动任何子进程必须静默无窗口、禁 `detached`。
8. **报告开头必须冠以生成方 agent 名**（v1.2.0）：`<title>` 与 `<h1>` 都写成 `<agent名>免费节点订阅报告`，聊天正文首行用同款标题。名字由脚本自动识别；识别不到会打 WARN，此时必须用 `--agent-name` 或 `report_meta.json:agent_name` 显式指定，不许交付没署名的报告。改标题要改生成脚本，别手改 HTML（下次重跑会退回去）。

## 流程（7 步，脚本模板见 scripts/）

### 1. SearXNG 搜索候选
- 按 `searxng-web-search` skill 调自建搜索（key 从 `D:\workspace\workbuddyai\agent-teams\.env` 读，勿写死勿入日志）。
- 3-4 组查询：`v2rayN 免费节点 订阅链接 最新 <年份>`、`Clash Verge 免费节点 订阅 <年份>`、`免费 v2ray clash 节点聚合 github 每天`、`free proxy nodes subscription v2ray clash daily update`。
- ⚠️ Python urllib 必须 **ProxyHandler({}) 禁系统代理**（Clash 7897 上游常断，走它对 Render/谷歌都 SSL EOF）；中文查询禁止 curl（GBK 转码）；超时放长 + 重试 1-2 次（Render 冷启动 30-80s）。
- 脚本开头 `sys.stdout.reconfigure(line_buffering=True)`；结果落盘当前工作目录（可移植，跨 agent 可用）。

### 2. GitHub 拉 README 提取订阅候选
- raw.githubusercontent.com 直连被墙（WinError 10054）、Clash 代理不可靠 → 优先 `gh api repos/<repo>/contents/README.md?ref=main`（`-H Accept: application/vnd.github.raw+json`，main/master 都试）；gh 不可用时走公开 REST API `/readme`。
- subprocess 必须带 `creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)`（2026-08-15 弹窗风暴红线）。
- **README 提取的过滤规则（国内版实战）**：必须同时满足「扩展名 ∈ {.yaml,.yml,.txt,.json,.base64}」+ 排除 `docs?/|tutorial|guide|troubleshoot|/blob/|.md` + raw 路径归属本仓库（owner/repo 匹配）。zhuhaiuk 的 README 里 10 个 URL 有 8 个是 `proxy-client-tutorials/docs/*.md` 教程页，不过滤会浪费大量下载超时。也过滤 license/issue/workflows/.svg/.png/shields.io/t.me/register 页。
- **已是 CDN 直链别再套 gh-proxy 前缀**：`cdn.jsdelivr.net/gh/...` 先直接访问，失败才试镜像；套成 `https://gh-proxy.com/https://cdn.jsdelivr.net/...` 必 404。jsDelivr 直连常 URLError 时，把它还原成 `raw.githubusercontent.com/<owner>/<repo>/<branch>/<file>` 再套 `gh-proxy.com/` 前缀（实测 70KB / 43KB 大文件 1-2s 就下来了）。
- **别把「README 指向的第三方源」当成该仓库自己的订阅**：`Flik6/Free-Node` 自称每小时更新、atom 显示停在 2026-09-05，README 指向 `a2470982985/getNode` 的死链 → 以「停更 + 转发死链」排除。`jichangx/free-nodes` 只是转发 `free18/v2ray`，报告里要写成「free18/v2ray（经 jichangx README 指向）」并单独查真实源的时效。

### 3. 镜像多通道下载验证 + 统一口径节点计数
- 通道优先序：`https://gh-proxy.com/{原始URL}`（通常最快）→ `https://ghproxy.net/{原始URL}` → `https://ghfast.top/{原始URL}`（慢且偶发挂）→ `https://cdn.jsdelivr.net/gh/<owner>@<branch>/<path>` → raw 直连（基本必败，留底）。
- 单通道超时 ≥18s：实测大文件（500KB-1MB）有 33-40s 才回来的；失败按序换通道，别急着判死。**一个死链跑满 5 通道可能耗 30-60s**，建议先做「discover 只提链接不下载」的快速轮，人工筛掉停更仓库后再下载验证。
- **节点计数（国内版二次实战修正，优先级最高）**：先切出 `proxies:` 到下一个顶层键之间的段落，**数段内 `^\s*-\s` 列表项**。别用 `^\s*-\s*\{?\s*name\s*:`——很多 YAML 节点以 `- type: vless` 开头、name 在后一行，实测 free18 c.yaml 107 节点旧正则只数出 10。
  - 端点提取仍需兼容三种写法：一行式 `- {"name":"x","server":"ip","port":123}`、多行式 `- name: ... / server: ... / port: ...`、`name` 不在首行 `- client-fingerprint: ... / name: ... / port: "443"`；`server`/`port` 正则允许带引号，端口限 1-65535。
  - **同仓库的 Clash 与 v2ray 两份文件应互相校验节点数**（同一批节点两种编码，数量应接近），差异过大说明解析有问题。
- v2ray txt：先判明文协议 URI（vmess/vless/ss/ssr/trojan/hysteria2/hy2/tuic），否则 base64 解码再数；URI 去重。

### 4. TCP 抽检 + 时效核查 → `final_results.json`
- 每个活订阅抽 ≤10 个端点，3s 超时测 TCP 连通，记 ok/total。
- 提交时间：`gh api repos/<repo>/commits?per_page=1 -q '.[0].commit.committer.date'`；gh 挂了按核心原则 3 的回退链（REST `pushed_at` → `commits/main.atom`）。宣称高频更新但 >2 天没提交的降权或排除（案例：Au1rxx 自称每小时刷新实际 9 天没提交且 TCP 0/10；a2470982985/getNode 9 月停更订阅已死）。
- **数据契约（第 5/6/7 步的输入）**：`final_results.json` = JSON 数组，每条目至少含：

  | 字段 | 含义 |
  |---|---|
  | `name` / `repo` / `kind` | 显示名 / `owner/repo` / `clash`\|`v2ray` |
  | `raw` | 原始 `raw.githubusercontent.com` 绝对地址，**给转换服务用** |
  | `url` | 本次实测下载成功的**镜像地址**，交付给用户 |
  | `alive` / `nodes_final` | 是否下载成功 / 统一口径节点数 |
  | `tcp_ok_final` / `tcp_total_final` | TCP 抽检结果 |
  | `pushed_at` / `age_days` / `secs` | 最后推送 / 距今天数 / 下载耗时 |
  | `score`（可选） | 质量分，报告排序用 |

### 5. 互转服务实测（新增）
- 先搜候选站（3-4 组查询：subconverter 公共实例 / `sub?target=clash` / clash 转 v2ray API），然后**严格探测**，不能只看 HTTP 200：
  - 依次试 `/sub`、`/api/sub`、`/convert`、`/api/convert`；
  - 用一小份 v2ray 订阅 + 一小份 Clash YAML 做双向探针；
  - 判「通过」= HTTP 200 **且**响应体确实是目标格式（clash 要含 `proxies:` + ≥1 个 `name:`；v2ray 方向要能数出通用 URI）；
  - **必须排除 SPA 假 200**：响应前 2000 字符含 `<!doctype|<html|<head|<script` 一律判 `html(SPA)`，那是前端页面不是转换结果。
- `target` 参数实测结论（14 个值扫过）：

  | target | 结果 |
  |---|---|
  | `clash` | v2ray 通用订阅 → Clash YAML，主用 |
  | `mixed` | Clash YAML → 通用 URI / base64，**clash→v2ray 方向只能用这个** |
  | `v2ray` | **恒返回空**，别用 |
  | `base64` / `auto` / `v2rayn` / `uri` | HTTP 400 |
  | `surge` / `quanx` / `loon` / `singbox` 等 | 其他客户端格式，非本流程需要 |

- `list=true` 是关键：只输出 `proxies` 节点列表（约 1.6 KB），不带 1.5 MB 分流规则，也不覆盖本地端口/模式设置。

### 6. 双格式链接生成 + 逐条验证 → `dual_links.json`（新增）
- 对每个 `alive` 且 `nodes_final >= 5` 的订阅，生成 `v2ray` / `clash` 两条链接，按优先级取第一个命中的：

  | 来源标记 | 规则 | 是否需验证 |
  |---|---|---|
  | `原生直链`（绿） | 该订阅本身就是目标格式，用 `url` | 已在第 3 步实测，免验 |
  | `同源另一格式`（蓝） | 同一 `repo` 下存在另一 `kind` 的实测成功订阅，取质量分最高的 | 已实测，免验 |
  | `转换生成`（黄） | 前两者都没有，才走公共转换服务 | **必须逐条请求验证** |

- 转换链接格式（嵌 `raw` 原始地址，**不是镜像地址**——去取文件的是境外转换服务器，它自己能直连 GitHub）：
  ```
  https://sub.ops.ci/sub?target=clash&list=true&insert=false&emoji=false&url=<原始订阅URL>
  ```
- 验证：HTTP 200 + 响应体是目标格式 + 数出节点数，写回 `out_nodes` / `verified` / `bytes` / `secs`。
- 失败的转换链接按序重试（最多约 18 个变体）：换 3 个备用域名 → 换输入源（`/refs/heads/` 改 `/`、`v2ray.txt` 改 `base64.txt`、raw 前加 `gh-proxy.com` 前缀）→ 加/去 `list=true`。仍失败就标「未通过」，别无限重试（会吃 429）。
- **数据契约**：`dual_links.json` = 数组，每条 `{name, repo, kind, score, v2ray:{url,src,verified,nodes,note,...}, clash:{...}}`；`src` 三选一，`verified` 为布尔。

### 7. 双格式报告与回复
- **报告开头署名（v1.2.0，脚本自动做，别手改 HTML）**：`<title>` = `<agent名>免费节点订阅报告 <时间戳>`，`<h1>` = `<agent名>免费节点订阅报告`，lead 行与页脚写「生成方 xxx」，`<meta name="generator">` 记 `clash-node-check v1.2.0 / xxx`。生成前先跑 `python <skill>/scripts/dual_report_template.py --print-agent` 确认身份解析正确（打印名字 + 来源）。
  - 解析优先级：`--agent-name` > 环境变量 `CLASH_NODE_AGENT_NAME` / `CLASH_NODE_CHECK_AGENT` > `report_meta.json:agent_name` > skill 根目录 `AGENT_NAME` 文件 > CWD 的 `AGENT_NAME` > 脚本/CWD 安装路径关键字 > 兜底 `本agent`（会打 WARN）。
  - 6 个安装位各自的 `AGENT_NAME`：`workbuddy国际版` / `workbuddy国内版` / `autoclaw` / `小浣熊` / `lobsterai` / `loomy`。**把脚本复制到工作目录跑时路径规则会失效**，此时用环境变量或 `--agent-name` 指定，别让报告变成「本agent免费节点订阅报告」。
  - 可选 `--agent-in-filename`：输出成 `reports/<agent名>免费节点订阅报告_YYYYMMDD.html`，多个 agent 同一天各跑一份时避免互相覆盖；默认文件名不变，旧引用不受影响。
- `reports/免费节点订阅报告_YYYYMMDD.html`（双格式版）必须包含：
  1. 指标块：候选仓库数 / 下载成功数 / **双格式订阅组数（共 2N 条链接）** / 原生+同源直链数 / **转换链接通过数 / 生成总数**；
  2. 推荐清单 + 全部明细两张表，**各有「v2rayN 订阅」「Clash Verge 订阅」两列**，按钮按来源三色区分（绿/蓝/黄），转换按钮显示 `(N 节点)` 或「未通过」，悬停显示完整 URL；
  3. 一键复制 JS（含 `document.execCommand('copy')` 降级）；
  4. 纯文本双链接清单（`<details>` 折叠，方便手动复制）；
  5. **互转服务实测表 + 已测不可用站表**；
  6. 互转限制说明：`target=v2ray` 恒空、clash→v2ray 转出数量依源而定（实测 0～1502 个 URI，Clash 私有协议 reality/hysteria2/xhttp 无法逆推）、只有带 `/sub` API 的站能拼订阅链接、公共转换服务无 SLA 且能看到订阅内容（**别贴付费机场订阅**）；
  7. 已排除源及原因、两个客户端各自的导入步骤、验证方法与可信度分级、免费节点风险提示；
  8. 明确写「同一条订阅的两列是同一批节点的两种格式，按客户端挑一列，不要两列都导」；
  9. **订阅链接必须「点一下就复制」**：`cp()` 要同时有 `navigator.clipboard.writeText` 主通道 + `textarea`/`document.execCommand('copy')` 兜底（file:// 或旧内核下 `navigator.clipboard` 可能整个对象不存在，只写主通道会抛 TypeError 且 fallback 不执行）+ 按钮变「已复制」1.4s 反馈；只给 `<input readonly onclick="this.select()">` **不算复制**。**改报告要改生成脚本，别只改 HTML**（只改产物下次重跑就退回去了）；改完用 Playwright 实测一次点击（禁 `file:` 协议，需临时 `python -m http.server`，验证完关掉），检查按钮文字变化 + `navigator.clipboard.readText()` 与 `code.title` 一致。
- 交付前确认 stdout 有 `AGENT -> <名字> (from ...)` 且 `HTML check: PASS`；跑 **HTML 标签配对 + 未闭合标签 + 占位符残留 + 标题/H1 含 agent 名**校验（零红色波浪线红线），PASS 才 `present_files`。缺署名会直接 FAIL（exit 1）。agent 名一律 `html.escape` 后再注入，别把外部字符串拼进模板。
- 正文：**首行标题用同款 `<agent名>免费节点订阅报告`** + 质量排序表 + 最优源**两列**可粘贴链接 + 已排除源及原因 + 使用要点（导入后测真连接、1-6h 自动更新、TCP 可连≠协议可用）+ `## 交付物` 列报告链接。

## 已知可用互转服务（2026-11-09 本机实测，非官方 SLA）

| 站点 | 类型 | 结论 |
|---|---|---|
| `sub.ops.ci` | `/sub` API + 网页 | 主用。`target=clash` / `mixed` 双向通过，`list=true` 有效 |
| `convsub.com` | `/sub` API + 网页 | 备用域名，响应特征与 sub.ops.ci 几乎一致，疑似同一实现，别当独立第二份保障 |
| `subconverters.com` | `/sub` API | 备用，连续请求触发 **HTTP 429**，轻度使用 |
| `acl4ssr-sub.github.io` | 纯网页前端 | 只能手动粘贴转换，`/sub` 等 4 路径全 404，不能拼订阅链接 |
| `subconverter.org` / `sub.jungley.net` | 文档 + 前端 | 首页能开，未找到可用 `/sub`，转换功能未做端到端验证 |

**已测不可用（11 组，别再浪费时间）**：`sub.xeton.dev`(522) / `sub.id9.cc`(SSL) / `sub.maoxiongnet.com`(403) / `api.dler.io`·`sub.dler.io`·`sub.kuailian.xyz`·`sub.stic.host`·`sub.watson.sh`(DNS) / `sub.9bit.cc`(TLS) / `subconverter.hyperts.net`(SSL) / `sub.scorpion.workers.dev`(超时) / `sub.d1.mk`·`sub-web.netlify.app`(**假 200：返回 SPA HTML**) / `suburl.v1.mk`·`api-sub.0z.gs`·`clashconverter.com`(4 路径全 404)。

## 脚本模板清单

| 文件 | 作用 | 用法 |
|---|---|---|
| `scripts/node_check_template.py` | 第 1-4 步：搜索 / README / 镜像下载 / TCP / 时效 | 改 `QUERIES` `TARGETS` 后 `python node_check_template.py` |
| `scripts/dual_links_template.py` | 第 5-6 步：探测转换站 + 生成/验证/重试双链接 | `python dual_links_template.py --all`（输入 `final_results.json`） |
| `scripts/dual_report_template.py` | 第 7 步：双格式 HTML 报告 + 开头署 agent 名 + 自校验 | `python dual_report_template.py`（输入 `final_results.json` + `dual_links.json`）；`--print-agent` 只查身份；`--agent-name` 覆盖；`--agent-in-filename` 文件名带前缀 |
| `AGENT_NAME`（skill 根目录，纯文本一行） | 声明本安装位属于哪个 agent，决定报告开头显示的名字 | 6 个安装位内容**各不相同**，同步时按位置单独写，不能整体覆盖 |

三个脚本都输出到 CWD、默认禁系统代理、不写死 key、不需要第三方包。报告需要的本次专属文案（排除源清单、转换站实测结论、特别提示）通过可选的 `report_meta.json` 注入，模板内置通用默认值；`report_meta.json:agent_name` 也能覆盖报告署名（优先级低于 `--agent-name` 与环境变量）。

## 跨 agent 移植说明

本技能已分发到：AutoClaw（`C:\Users\Administrator\.openclaw-autoclaw\workspace\skills\`，workshop 安装位）、WorkBuddy 国内版（`~\.workbuddy\skills\`）、WorkBuddy 国际版（`~\.workbuddy-ai\skills\`）、小浣熊（`~\.office-raccoon\agent\skills\`）、LobsterAI（`%APPDATA%\LobsterAI\SKILLs\`，大写 K）、Loomy 0.9.38（`C:\Users\Public\Loomy\e7d3e769f3f5\opencode\skills\`，实测生效路径；opencode 内核同时扫 `.claude`/`.agents` 下 `{skill,skills}/**/SKILL.md`）。模板脚本输出到 CWD，任何 agent 沙箱内都能跑。**同步新版时把 `scripts/` 整个目录一起带上，并逐处先备份再覆盖**；曾出现国内版副本自带二次实战补充而主版本没有的情况，同步前务必先 diff，别用主版本直接盖掉本地经验。

**v1.2.0 报告署名的安装位名单**（`AGENT_NAME` 文件内容，UTF-8 纯文本一行）：

| 安装位 | `AGENT_NAME` | 报告 H1 |
|---|---|---|
| WorkBuddy 国际版 `~\.workbuddy-ai\skills\` | `workbuddy国际版` | `workbuddy国际版免费节点订阅报告` |
| WorkBuddy 国内版 `~\.workbuddy\skills\` | `workbuddy国内版` | `workbuddy国内版免费节点订阅报告` |
| AutoClaw `~\.openclaw-autoclaw\workspace\skills\` | `autoclaw` | `autoclaw免费节点订阅报告` |
| 小浣熊 `~\.office-raccoon\agent\skills\` | `小浣熊` | `小浣熊免费节点订阅报告` |
| LobsterAI `%APPDATA%\LobsterAI\SKILLs\` | `lobsterai` | `lobsterai免费节点订阅报告` |
| Loomy `C:\Users\Public\Loomy\e7d3e769f3f5\opencode\skills\` | `loomy` | `loomy免费节点订阅报告` |

同步时注意：`SKILL.md` 与 `scripts/` 六处逐字节一致，**只有 `AGENT_NAME` 必须按上表分别写**，把主版本的 `AGENT_NAME` 一起复制过去会让所有 agent 都自称 `workbuddy国际版`。分发完在每处跑一次 `--print-agent` 核对，再 `diff -rq` 验证除 `AGENT_NAME` 外无差异。

## 已知坑位（2026-11-08 / 11-09 实战沉淀）

- ghfast.top 多次 URLError；gh-proxy.com 偶发单链接超时 → 多通道轮换是必须，不是可选。
- Clash 7897 端口 LISTEN ≠ 可用：netstat 看进程在听，但上游断了照样 SSL EOF；一律禁代理直连镜像。
- 上千节点的聚合 YAML（Barabama clashmeta.yaml 1385 节点、nodev2ray.txt 3960 节点）下载 0.5-1MB，超时别设太小。
- **gh CLI token 会悄悄失效**：`gh auth status` 报 `The token in default is invalid` 时调用仍会发出去，但退化成未认证（60 次/小时，出口 IP 常被多人共享 → 额度可能已被别人用完）。表现是「第 1 个仓库成功、从第 2 个起全部返回空」，容易误判成「仓库不存在」。先 `gh api rate_limit` 看 `remaining`，别急着怪仓库，也别重试死磕。
- **GitHub API 限流后不必等重置**：`commits/main.atom`（Atom feed）和 `raw/.../README.md` 都能被 `gh-proxy.com` 代理，单次实测 14755B / 11211B 正常返回，完全绕开 API 限流。`gh api` 不是唯一通道。
- Clash YAML 只按 `^\s*-\s*name:` 数会严重低估（`- type:` 开头、name 在后一行）；按 `proxies:` 段内 `^\s*-\s` 列表项数，并与同仓 v2ray 文件的 URI 数交叉验证。
- 转换站「HTTP 200」不等于能用：`sub.d1.mk` / `sub-web.netlify.app` 返回的是前端 SPA HTML，必须按响应体分类。
- `target=v2ray` 恒空、`base64/auto/v2rayn/uri` 返回 400；clash→v2ray 只能用 `target=mixed`，转出 0～1502 个 URI 依源里协议而定，别写死「只能转出 1 个」。
- 转换服务不认 GitHub 的 `/refs/heads/` 路径时，换成 `/` 或改用 `base64.txt` 变体；`subconverters.com` 会 429，别并发轰炸。
- 转换链接里嵌 **raw 原始地址**，别嵌 `gh-proxy.com` 镜像地址（转换服务器在境外，自己能直连 GitHub；嵌镜像反而多一跳）。
- 免费节点存活以小时计，报告注明「当天导入当天用」；仓库页宣传的「M/S 速度」是营销话术，不作依据。
- 镜像前缀可互换：ghproxy.net ↔ gh-proxy.com ↔ ghfast.top，某个失效换下一个；原始 raw 链接在能直连 GitHub 的网络下同样有效。
- **升级本 skill 或覆盖报告前先 `cp -a` 完整备份 + `diff -rq` 校验**（备份别放在 `skills/` 目录内，否则会被加载器当成第二个同名 skill）。
- **Windows 下别用 `python -c "...含 \n 的多行样例..."` 传复杂字符串**：shell 转义会悄悄破坏内容，导致误判脚本 bug；调试一律落盘成 .py 再跑。
- **报告署名（v1.2.0）**：把 `dual_report_template.py` 复制到工作目录跑且没带 `AGENT_NAME` 时，路径规则识别不到 agent，标题会退回 `本agent免费节点订阅报告` 并打 WARN；同步 6 个安装位时 `AGENT_NAME` 必须按位置分别写，整体覆盖会全员自称 `workbuddy国际版`。别为了改标题直接编辑 HTML 产物。
