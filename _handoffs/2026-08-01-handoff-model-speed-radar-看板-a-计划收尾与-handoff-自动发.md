---
layout: default
title: 交接文档 · model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复
date: 2026-08-17 23:30:00 +0800
---

# model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复

- **日期**：2026-08-01
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260801_model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复_handoff.md（编码探测：utf-8）

> 来源：项目文档 `2026-08-01-14-48-09\HANDOFF_radar-handoff-fix.md`
> 由 handoff_flow.py（scan 阶段）自动收集，标题取自文档 H1（即主要干的活），待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。


> 项目时间：2026-08-01
> 来源 session：2026-08-01-14-48-09
> 文档用途：记录 model-speed-radar 守护进程看板的 A 计划 bug 收尾工作，以及 handoff 自动发布链路（Gridea/博客/语雀/论坛）的两处 bug 修复与自动化时序调整。

## 一、model-speed-radar 看板 A 计划收尾
- 能力明细标题左对齐 UI 修复：.cap-toggle 绝对定位到最左边，与完整排行对齐（版本号 20260801c）。
- 活清单加回误删模型：共加回 4 个（Agnes 2 多模态 + 2 文本），并清理 15 条无效条目（分类：NVIDIA 7 真下线 410、OpenRouter 2 无端点、SenseNova 1 查无、OmniRoute 3 重复、Agnes 2 误删）。
- 新增 endpoint_mismatch 错误分类（C 项"给雷达加归类"）：
  - 生成类探针命中路由级 404（FastAPI {"detail":"Not Found"}）→ 归 endpoint_mismatch；
  - chat 类命中 404 → 归 model_gone（模型真下线）；
  - 生成类无端点 → 归 model_gone。
  - 辅助函数 _is_route_404() 区分"not found/404 page"与"model is not found/does not exist/no endpoints"。
  - 已端到端验证：生成类探针真实归 endpoint_mismatch。
  - 前端：ERR_TAG 加 endpoint_mismatch（"接口不符"，琥珀色 .dead-item.mismatch），index.html 版本号升 20260801d。
- B1/C1 暂不改，只观察记录（写入 A3 报告第八节）。

## 二、handoff 自动发布链路修复
- 根因：此前 scan 阶段把 handoff 退化成"每日完成项目"每日打包，且 extract_completed() 只取同级标题导致 Gridea 浓缩版正文空白；自动化时序 scan(23:01) 跑在日报(约23:25)生成之前，导致当天 handoff 漏发。
- 修复 1（内容空白）：extract_completed() 改为匹配到「今日完成事项」后，继续吞入所有更深层子节，直到同级/更高级标题。并用修复后逻辑重生成 07-31 handoff 源与 Gridea 稿件。
- 修复 2（标题不知所云）：Gridea handoff 标题从「每日完成项目（YY-MM-DD Handoff）」改为「每日完成项目 · YYYY-MM-DD」，去掉 "Handoff" 字样。
- 修复 3（时序）：自动化调为 scan 23:30、publish 23:35、Gridea 自动同步 23:45，确保日报先写完再扫描。
- 验证：手动跑 gridea_auto_sync.py 渲染整站（39 篇文章、21 文件变更）并 push 到 GitHub Pages；博客源 daily-note-blog/_handoffs/ 生成并 git push；语雀 handoff 补推成功。

## 三、关键决策 / 注意事项
- handoff 本意是**项目交接文档**（一个已结束项目一份），标题应是"主要干的活"，不是每天打包的"每日完成项目"。本次修复把 scan 拉回正确语义（见关联项目：Agnes 接入项目中已启动 scan 改造）。
- 自动化改时序后，需确认 23:30 时当天日报已存在，否则仍会漏扫。

## 四、生成的有用文件
| 文件 | 路径 | 用途 |
|---|---|---|
| 看板脚本 | D:/AI work/workbuddy/model-speed-radar/speed_daemon.py | 模型测速守护进程 |
| handoff 流程 | D:/AI work/workbuddy/handoff/handoff_flow.py | scan/publish 自动发布 |
| A3 报告 | D:/AI work/workbuddy/model-speed-radar/BUG_A3_20260801.md | 看板 bug 记录 |

## 五、待办 / 风险
- 论坛发布（bbs1org/phpBB）在沙箱缺代理时 SSL 握手失败，自动化(venv python)正常；失败不阻断 Gridea/博客/语雀。
- handoff_flow.py 的 scan 逻辑已进一步改造为"按项目文档收集"（优先 HANDOFF*.md，缺则回退收集 session 根下主题 markdown），详见改造后的脚本。
