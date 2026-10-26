---
layout: default
title: 技术点 · SearXNG-Render 优化方案：多 agent 评审结论与执行报告
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · SearXNG-Render 优化方案：多 agent 评审结论与执行报告

> 来源：261022_SearXNG-Render 优化方案：多 agent 评审结论与执行报告_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：2026-10-22-22-03-16\SearXNG优化方案_多agent评审与执行_20261023.md
- > 输入：豆包《SearXNG-Render 部署完成：检查清单 + 优化&风险方案》
- 豆包方案的**方向对、字段错、优先级错**：8 条配置字段名全部写错（其中 2 条会直接搞挂服务）、
- 1 个环境变量不存在、1 条"最危险改动"是误判；而它自己标记为"紧急提醒"的
- **JSON 接口裸奔**，反而没有被列进它的"必须做"清单。
- | 1 | `server.limiter: true` + `limiter:` 块 **YAML 键重复自相矛盾**，且 limiter 需要 valkey（Render 免费档没有）→ 启动崩溃 | 官方 settings 模板 |
- | 2 | 方案 A（Cloudflare Worker 前置鉴权）**挡不住 origin 直连**——外界拿到 `*.onrender.com` 仍可绕过 Worker 直连后端 | 红队自标"推测"，维持推测 |
- **证伪**：线上实例当前正配着 `method: "POST"`，而我的 GET 探测（`/search?...&format=json`）
- `/search` 路由 GET/POST 都接收。→ 无需改回 GET。
- | `server.limiter: true` + `botdetection:` 段 | **证实**——无 valkey 开不了；`botdetection` 段上游已移除 |
- | JSON 接口裸奔 | **证实且至今未解**——替补为真实最高危项 |
- | `search_auth.py` | **新建**。容器内 WSGI 鉴权中间件：只对机器可读格式（json/csv/rss）要求 `X-Search-Key`，HTML 网页 UI 全放行；**同时解析 POST body**，堵住 `curl -X POST -d 'format=json'` 绕过 GET 查询串检查 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. **引擎换血未部署验证**——线上仍是旧配置，brave 限流 / duckduckgo 超时 / bing 是唯一稳定中文源
   这个矛盾要等部署后用真实流量判断。已用熔断器 + Tavily 兜底缓解。
2. **Tavily 回声效应**未根治——错误声明被检索结果复述时，数字核对会判"对上"。
   设计上不让任何模型出裁决，检索原文 + URL 全进评审 prompt，由审核员对照判断。
3. **数字核对只查一致性**——实测「月租金 10 万元，按 1.5% 缴纳增值税」，
   检索事实确认了 1.5% 却没提 10 万元，仍判 mismatch。方向安全（宁可多报），
   但审核员必须自己看懂证据块，不能只盯 mismatch 标记。
4. **CF 版未重新部署**——`wrangler deploy` 需要你执行；CF 版最后部署版本未端到端验证。
5. **本地版新事实核查层未用真评审器端到端验证**——目前是假 orchestrator 集成测试 + 线上直调
   `verifyClaims` 双轨，缺一环"真 codebuddy CLI 当评审员"的完整跑通。

## 6、部署状态
```bash
cd "D:/AI work/workbuddy/2026-10-22-22-03-16/searxng-render"
git add -A && git commit -m "引擎换血 + WSGI JSON 鉴权 + 8 处字段修正" && git push
```
Render 会自动重新部署。**同时必须设两个环境变量**（Render 面板 → Environment）：

| 变量 | 值 |
|---|---|
| `SEARXNG_SECRET` | 自己生成的随机密钥（不要用示例串） |
| `SEARCH_API_KEY` | JSON 接口鉴权 key，下面两个系统要用同一个值 |

**通过标准**：
```bash
curl -s "https://searxng-render-gn0d.onrender.com/healthz"                    # 200 OK
curl -s "https://.../search?q=测试&format=json"                              # 401/403（未认证被挡）
curl -s -H "X-Search-Key: <key>" "https://.../search?q=测试&format=json"     # 200 + JSON
```
