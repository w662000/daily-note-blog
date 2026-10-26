---
layout: default
title: 技术点 · SearXNG-Render 优化方案 · 多 agent 评审输入（2026-10-23）
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · SearXNG-Render 优化方案 · 多 agent 评审输入（2026-10-23）

> 来源：261022_SearXNG-Render 优化方案 · 多 agent 评审输入（2026-10-23）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- > 不允许凭记忆断言 SearXNG 配置项——本文件第 3 节已用官方源码/文档逐条核实过。
- 一个 SearXNG 实例部署在 Render 免费档，要改造成**两个多 agent 问答系统的主搜索源**：
- | 本地仓库 | `D:\AI work\workbuddy\2026-10-22-22-03-16\searxng-render`（4 文件：Dockerfile / entrypoint.sh / settings.yml / README.md，已推送 GitHub，Render 自动部署） |
- | 接入方 2 | 本地版：`D:\workspace\workbuddyai\agent-teams\mcp\lib\grounding.mjs` 的 `searchOne(apiKey, claim, fetchImpl)` / `verifyClaims({...})` |
- 供审核员与草稿原文比对。任何搜索失败都静默降级，绝不阻塞主链路。
- > 环境背景：Render Free，512M内存，闲置15min自动Sleep；账号共享750小时运行额度；出口IP搜索引擎风控；公网JSON接口；无鉴权。
- 2. JSON 接口测试 `curl ".../search?q=大模型发展&format=json"`；403 = settings.yml 漏写 `search.formats: [html,json]`；大量空 results = 出口 IP 风控
- 4. 核对环境变量：`SEARXNG_SECRET` 不是默认示例字符串；`SEARXNG_BASE_URL` 末尾带 `/`、域名一致
- 1. 闲置 15 分钟 Sleep，AI 调用第一次要等 30–80 秒冷启动，脚本易超时；UptimeRobot 保活只能缓解
- 2. 512MB 内存，多引擎并发查询易 OOM
- 3. **JSON 接口完全公开无鉴权**：被爬虫扫到会疯狂刷，耗尽带宽 + 750 小时，Render 可能冻结服务
- ```
search:
  safe_search: 0
  lang: zh-CN
  max_search_time: 6   # 原来8，缩短超时
  formats: [html, json]
  max_results: 10      # 新增，限制返回结果数量
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
1. Sleep ≠ Suspend，不用时手动 Suspend 释放时长
2. 512M 不要开一堆引擎
3. JSON 无鉴权是高危点，不要泄露 URL
4. AI 调用代码必须写重试、长超时

---
