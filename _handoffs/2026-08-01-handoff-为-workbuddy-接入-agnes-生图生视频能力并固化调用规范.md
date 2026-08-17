---
layout: default
title: 交接文档 · 为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范
date: 2026-08-17 23:30:00 +0800
---

# 为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范

- **日期**：2026-08-01
- **状态**：✅ 已完结（新方法重生成）
- **来源**：handoff\bak\260801_为 WorkBuddy 接入 Agnes 生图生视频能力并固化调用规范_handoff.md（编码探测：utf-8）

> 来源：项目文档 `2026-08-01-14-48-09\HANDOFF_agnes-multimodal.md`
> 由 handoff_flow.py（scan 阶段）自动收集，标题取自文档 H1（即主要干的活），待 publish 阶段分发到 Gridea / 博客 / 语雀 / 论坛。


> 项目时间：2026-08-01
> 来源 session：2026-08-01-14-48-09
> 文档用途：把 Agnes 两个多模态生成模型（agnes-image-2.1-flash 生图、agnes-video-v2.0 生视频）接入 WorkBuddy 活清单，并固化"怎么调、怎么取片"的调用规范与一键 skill，供后续任何模型/对话指挥生成图文视频。

## 一、背景与动机
- 活清单（~/.workbuddy/models.json）里 Agnes-AI 原有 6 个文本模型，多模态的 agnes-image-2.1-flash、agnes-video-v2.0 此前被误删（chat 返 404 是路由级而非模型下线，被错判"死了"）。
- 目标：恢复并正式接入这两个生成模型，让 WorkBuddy 能生图、生视频。

## 二、做了什么
1. 活清单加回模型：
   - 补回 agnes-image-2.1-flash、agnes-video-v2.0（以及 agnes-2.0-flash、agnes-2.5-pro 等共 4 个此前误删/遗漏的多模态与文本模型），同时清理 15 条无效条目（NVIDIA 7 真下线、OpenRouter 2 无端点、SenseNova 1 查无、OmniRoute 3 重复）。
   - 备份：models.json.bak-agnes-add-20260801-200129。

2. 摸清两个模型的真实调用方式（关键坑位）：
   - 生图 POST https://api.agnes-ai.cn/v1/images/generations，response_format 必须放进 extra_body（放顶层会被忽略）。
   - 生视频 POST https://api.agnes-ai.cn/v1/videos（注意不是 /videos/generations）；num_frames 须 8n+1 ≤ 441；异步任务，取返回 task_id 轮询 GET https://api.agnes-ai.cn/v1/videos/{task_id}（单 /v1）直到 completed。
   - 取片（重大纠偏）：官方文档证明推荐方式只需 API Key —— GET https://api.agnes-ai.cn/agnesapi?video_id=<VIDEO_ID>&model_name=agnes-video-v2.0，响应顶层 url 字段即 mp4 直链，curl 下载即可。根本不需要登录控制台 cookie（此前误判"需控制台会话取片"，根因是只轮询了状态接口 /v1/videos/{task_id}、没调结果接口 /agnesapi）。
   - 下载时 Windows schannel 证书吊销离线错误（CRYPT_E_REVOCATION_OFFLINE，走本地代理所致）→ curl 加 --ssl-no-revoke 解决。

3. 写调用规范文档：agnes-models-usage-spec.md（会话副本），并另存为 handoff/bak/「Agnes 生图 ／ 生视频 模型调用规范.md」（唯一真源，用全角／避开 Windows 禁斜杠）。文档含：连接信息、生图/生视频完整流程、给模型的系统提示（指针版+内联版，让任意模型看到后能指挥生成）、排错表（含 endpoint_mismatch / 503 / SSL 吊销）。

4. 创建 agnes-media-gen skill（用户级，~/.workbuddy/skills/agnes-media-gen/）：
   - SKILL.md：完整流程 + 所有易踩坑（response_format 进 extra_body、num_frames 8n+1、轮询 vs 结果接口区分、下载 SSL 坑、两模型非对话模型 /chat 404 正常）。
   - scripts/agnes_gen.py：基于 stdlib urllib 的一键脚本（无需装包），内置 429/5xx 温和退避重试。
   - 触发：用户说"用agnes生视频/生图""准备生视频/生图"即加载该 skill。
   - 已实跑验证：单发生图（遇 503 重试成功）、生成 3 个视频全链路通。

5. 实测生成 3 个凡人修仙传视频（验证链路）：
   - 韩立庚剑阵 10s（1088×832，约 3.7MB）
   - 韩立大庚剑阵 10s（1088×832，约 1.7MB）
   - 韩立 vs 王婵 15s（185帧@12fps，约 3.3MB，含简单怒吼配音——推翻"文生视频无配音"的想当然假设）
   - 均落盘到 2026-08-01-14-48-09/。

## 三、关键决策 / 注意事项
- 取片用 API Key 走 /agnesapi，不要再去控制台拿 cookie（以官方文档为准）。
- 生视频是异步，必须轮询 /v1/videos/{task_id} 到 completed 再调 /agnesapi 取片。
- 出发前先读官方文档再下结论（本次若早读 docs 就不会误判 cookie、白折腾用户一轮）。
- 文生视频模型会带简单音效（怒吼），不要预设静音。

## 四、生成的有用文件
| 文件 | 路径 | 用途 |
|---|---|---|
| 调用规范（真源） | D:/AI work/workbuddy/handoff/bak/Agnes 生图 ／ 生视频 模型调用规范.md | 任何模型调 Agnes 生成能力的权威文档 |
| 规范（会话副本） | D:/AI work/workbuddy/2026-08-01-14-48-09/agnes-models-usage-spec.md | 同上副本 |
| skill | ~/.workbuddy/skills/agnes-media-gen/ | 一键生图/生视频 skill |
| 视频成品 | 2026-08-01-14-48-09/agnes_video_*.mp4 | 三个实测视频 |

## 五、待办 / 风险
- 论坛发布（bbs1org/phpBB）在本机沙箱缺代理时曾 SSL 握手失败，自动化环境（venv python）通常正常；08-01 handoff 发布时若失败可次日补。
- 视频模型对血腥画面（如"斩断双腿"）可能弱化，需改 prompt 淡化。
