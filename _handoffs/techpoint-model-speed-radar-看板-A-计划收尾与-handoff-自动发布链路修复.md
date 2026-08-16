---
layout: default
title: 技术点 · model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复
date: 2026-08-01 23:30:00 +0800
---

# 技术点 · model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复

> 来源：260801_model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260801_model-speed-radar 看板 A 计划收尾与 handoff 自动发布链路修复_handoff.md（编码探测：utf-8）
- > 文档用途：记录 model-speed-radar 守护进程看板的 A 计划 bug 收尾工作，以及 handoff 自动发布链路（Gridea/博客/语雀/论坛）的两处 bug 修复与自动化时序调整。
- 能力明细标题左对齐 UI 修复：.cap-toggle 绝对定位到最左边，与完整排行对齐（版本号 20260801c）。
- 生成类探针命中路由级 404（FastAPI {"detail":"Not Found"}）→ 归 endpoint_mismatch；
- 前端：ERR_TAG 加 endpoint_mismatch（"接口不符"，琥珀色 .dead-item.mismatch），index.html 版本号升 20260801d。
- 根因：此前 scan 阶段把 handoff 退化成"每日完成项目"每日打包，且 extract_completed() 只取同级标题导致 Gridea 浓缩版正文空白；自动化时序 scan(23:01) 跑在日报(约23:25)生成之前，导致当天 handoff 漏发。
- 修复 1（内容空白）：extract_completed() 改为匹配到「今日完成事项」后，继续吞入所有更深层子节，直到同级/更高级标题。并用修复后逻辑重生成 07-31 handoff 源与 Gridea 稿件。
- 修复 2（标题不知所云）：Gridea handoff 标题从「每日完成项目（YY-MM-DD Handoff）」改为「每日完成项目 · YYYY-MM-DD」，去掉 "Handoff" 字样。
- 修复 3（时序）：自动化调为 scan 23:30、publish 23:35、Gridea 自动同步 23:45，确保日报先写完再扫描。
- handoff 本意是**项目交接文档**（一个已结束项目一份），标题应是"主要干的活"，不是每天打包的"每日完成项目"。本次修复把 scan 拉回正确语义（见关联项目：Agnes 接入项目中已启动 scan 改造）。
- | 文件 | 路径 | 用途 |
- | 看板脚本 | D:/AI work/workbuddy/model-speed-radar/speed_daemon.py | 模型测速守护进程 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
- 论坛发布（bbs1org/phpBB）在沙箱缺代理时 SSL 握手失败，自动化(venv python)正常；失败不阻断 Gridea/博客/语雀。
- handoff_flow.py 的 scan 逻辑已进一步改造为"按项目文档收集"（优先 HANDOFF*.md，缺则回退收集 session 根下主题 markdown），详见改造后的脚本。
