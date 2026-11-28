---
layout: default
title: 每日工作总结 · 2026-11-27
date: 2026-11-27 23:30:00 +0800
---

# 多 Agent 每日工作日志 · 2026-11-27

> 数据源：wb-cn / wb-intl / autoclaw-115 / zcode 四个 Agent 的当天日志，按 agent 分节；某 agent 当天无机器日志记录，不许编造。

## 一、WB 国内版（wb-cn）
- **曦码（Xime/Rime）配置优化**：
    - 提供了针对 en/eng、in/ing 模糊音的 `speller/algebra` 补丁方案，并纠正了使用 `/+` 进行追加而非覆盖的配置误区。
    - 解决了候选词数量控制问题，确定需通过 `xime.custom.yaml` (style.candidate_count)、`pinyin_simp.custom.yaml` (menu/page_size) 及 `default.custom.yaml` (menu/page_size) 三处同时控制。
    - 沉淀技能文档：`~/.workbuddy/skills/xime-yao-config/SKILL.md`。
- **文案撰写**：为 AutoClaw 推广活动编写了 3 版不同风格（英文/中文/技术向）的发帖文案。
- **信息查证**：确认 hy4 flash 免费额度官方未公布具体数值，明确了限免时间及额度耗尽后的转换机制。

## 二、WB 国际版（wb-intl）
- **Skill 版本迭代与分发**：
    - 完成 `custom-model-onboarding-v2` skill 向全部 8 个 Agent 的全量分发。
    - 停用了全量 Agent 上的 18 个旧版加模型 skill，并按 manifest 记录完成备份归档（`skill_archive_model_20261127_100849/`）。
- **环境清理与三层分离检查**：
    - 通过 `check_three_layer.py` 验证，除 AutoClaw 2.0 国内版（遗留数据）外，其余 7 个 Agent 均符合三层分离标准。
    - 清理了网关孤儿进程（PID 11444）及 AutoClaw 2.0 国内版残留数据（包括自启动项、目录及配置文件），已通过 `robocopy /MIR` 完成数据同步并清理回收站释放空间。
- **新模型接入（dots.ai）**：
    - 成功通过 v2 skill 将 `dots3-note-prev` 模型接入全部常用 Agent。
    - 覆盖范围包括：WB 双版本（`add_dots_wb.py`）、AutoClaw 国际版（`add_dots_au_intl.cjs`）、AutoClaw 1.x（`add_dots_autoclaw1x.cjs`）、ZCode（`import_models_to_zcode.py`）、LobsterAI（`lobster_inject.py`）、Loomy（`add_dots_loomy.py`）、小浣熊（`add_dots_raccoon.py`）、DSH（`add_dots_dsh.py`）及 Hermes（`add_dots_hermes.py`）。
- **关键决策/教训**：明确后续接入新模型时应优先阅读归档中的 4 份旧 skill 文档与脚本，避免重复研究。

## 三、AutoClaw 1.15（autoclaw-115）
今日无机器日志记录

## 四、ZCode（zcode）
- **用户会话记录**：当日记录 2 个会话，包含 20 条关于模型身份及模型名称的查询消息。

## 五、总计 / 待办
- **有日志 Agent 数**：3
- **日志总字符数**：约 4070
- **跨 agent 待办**：
    - 待用户验证曦码（Xime）模糊音补丁及候选词数量修改是否在端侧生效。