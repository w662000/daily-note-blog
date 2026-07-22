---
layout: default
title: 每日工作总结 · 2026-07-22
date: 2026-07-22 23:30:00 +0800
---

# 每日工作总结 · 2026-07-22

## 一、今日完成事项
1. **诊断并清理 D 盘根异常文件夹**：查清 `D:\c`(510M)、`D:\d`(226M) 成因——昨晚 Hermes 容器重建时 compose 宿主机挂载路径漏 `C:` 盘符，Docker 当相对路径在 D 盘根自动建了这两个副本。确认不被任何容器挂载后删除，腾出 ~736MB。
2. **全量复盘 ds v4 昨晚操作**：整理出 6 类错误操作链（force-recreate 红线事件 / 路径坑 / 无效操作 / 散落垃圾 / 备份翻车 / 认知错误），写成防再犯档案。
3. **全量清理遗留临时产物**：删除 C 盘根误建 docker-compose.yml、4 个临时脚本、C:\tmp、D:\tmp、6 个 hermes 构建日志（保留 bootstrap.py 与 config.yaml.bak 安全网）。
4. **跨工具护栏部署**：把"最小动作 + 后果预判 + 不确定先问"护栏铺到 WorkBuddy / Hermes / Trae / Qoder 全部工具（master 文件 `AGENT_GUARDRAILS.md` + 各工具注入点），防事故复发。
5. **SOUL.md 强制句生效验证**：确认 Hermes 的 SOUL.md 在 agent 构造时缓存（非实时读盘），用 `docker compose restart`（非 recreate）重启后实测 `/api/memory` 含强制句、mtime 吻合，确认生效。
6. **WorkBuddy 对齐 Hermes 的 GLM 模型**：WorkBuddy 只能接 3 个 GLM（漏了赠送的 6 个）。实测同 key 三端点 9 模型均可聊，根因是 models.json 名单漏列；补齐为 9 个（沿用原 url+key）。
7. **GLM 9 模型速度测试**：流式测速（双字段解析推理模型），结论——`glm-4.5-air` 最快最稳(首字430ms/总7s/42.8字每秒)为干活首选；`glm-4.6v` 首字最快且支持看图；其余 turbo/flash 重思考+限流体验差。报告+脚本已归档。
8. **建立每日工作总结机制**（本报告）：把机器日志转成人读总结，归档到当天文件夹。

## 二、关键决策 / 注意事项
- **命名卷已生效但非必须**：hermes-agent-src/webui-venv/webui-uvcache 三卷已挂载且有真实数据（是那次 recreate 的副产品），保持现状即可，**勿为"让卷生效"再去 recreate**（重蹈覆辙）。
- **每日工作总结**替代原先"每日人读总结"称呼（更自然）；机制：每天结束生成人读版总结 + 有用文件清单，归档当天文件夹。
- WorkBuddy models.json 改动需**重启桌面端**才生效（启动加载）。

## 三、生成的有用文件
| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 护栏 master | `D:\AI work\AGENT_GUARDRAILS.md` | 跨工具通用护栏（已部署到 4 工具） |
| 测速报告 | `D:\AI work\workbuddy\2026-07-22\GLM_speed_test_report.md` | 9 模型速度对比与切换建议 |
| 测速脚本 | `D:\AI work\workbuddy\2026-07-22\test_glm_speed.py` | 可复用，含 7 条测速逻辑要点注释 |
| 各工具护栏 | `.trae\rules\guardrails.md`、`.qoder\rules\guardrails.md`、`AGENTS.md`、`C:\Users\Administrator\.hermes\memories\USER.md`、`SOUL.md` | 各工具实际生效位置 |
| 安全网(保留) | `C:\Users\Administrator\.hermes\config.yaml.bak-20260721T013122Z` | 配置改前留底 |

## 四、待办 / 风险
- 重启 WorkBuddy 桌面端让 9 GLM 模型生效。
- 可设"每日工作总结"为定时自动化，省去手动触发（已提议）。
- Hermes 还有一未声明匿名卷(`/opt/data`)，recreate 时不复用，但为缓存数据，丢了通常无害。
