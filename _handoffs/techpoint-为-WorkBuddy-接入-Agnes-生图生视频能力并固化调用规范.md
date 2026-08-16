---
layout: default
title: 技术点 · 为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范
date: 2026-08-01 23:30:00 +0800
---

# 技术点 · 为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范

> 来源：260801_为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：handoff\bak\260801_为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范_handoff.md（编码探测：utf-8）
- 活清单（~/.workbuddy/models.json）里 Agnes-AI 原有 6 个文本模型，多模态的 agnes-image-2.1-flash、agnes-video-v2.0 此前被误删（chat 返 404 是路由级而非模型下线，被错判"死了"）。
- 生图 POST https://api.agnes-ai.cn/v1/images/generations，response_format 必须放进 extra_body（放顶层会被忽略）。
- 生视频 POST https://api.agnes-ai.cn/v1/videos（注意不是 /videos/generations）；num_frames 须 8n+1 ≤ 441；异步任务，取返回 task_id 轮询 GET https://api.agnes-ai.cn/v1/videos/{task_id}（单 /v1）直到 completed。
- 取片（重大纠偏）：官方文档证明推荐方式只需 API Key —— GET https://api.agnes-ai.cn/agnesapi?video_id=<VIDEO_ID>&model_name=agnes-video-v2.0，响应顶层 url 字段即 mp4 直链，curl 下载即可。根本不需要登录控制台 cookie（此前误判"需控制台会话取片"，根因是只轮询了状态接口 /v1/videos/{task_id}、没调结果接口 /agnesapi）。
- 下载时 Windows schannel 证书吊销离线错误（CRYPT_E_REVOCATION_OFFLINE，走本地代理所致）→ curl 加 --ssl-no-revoke 解决。
- SKILL.md：完整流程 + 所有易踩坑（response_format 进 extra_body、num_frames 8n+1、轮询 vs 结果接口区分、下载 SSL 坑、两模型非对话模型 /chat 404 正常）。
- scripts/agnes_gen.py：基于 stdlib urllib 的一键脚本（无需装包），内置 429/5xx 温和退避重试。
- 取片用 API Key 走 /agnesapi，不要再去控制台拿 cookie（以官方文档为准）。
- 生视频是异步，必须轮询 /v1/videos/{task_id} 到 completed 再调 /agnesapi 取片。
- | 文件 | 路径 | 用途 |
- 论坛发布（bbs1org/phpBB）在本机沙箱缺代理时曾 SSL 握手失败，自动化环境（venv python）通常正常；08-01 handoff 发布时若失败可次日补。

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
- 论坛发布（bbs1org/phpBB）在本机沙箱缺代理时曾 SSL 握手失败，自动化环境（venv python）通常正常；08-01 handoff 发布时若失败可次日补。
- 视频模型对血腥画面（如"斩断双腿"）可能弱化，需改 prompt 淡化。
