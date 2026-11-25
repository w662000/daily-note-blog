---
layout: default
title: 技术点 · 2026-11-25
date: 2026-11-25 23:30:00 +0800
---

## wb-cn（WB 国内版）

> 数据源：D:\AI work\workbuddy\.workbuddy\memory\2026-11-25.md, D:\AI work\workbuddy\2026-11-25-10-55-54\.workbuddy\memory\2026-11-25.md

## SenseNova 免费模型清单更新 + 写入 WB 活清单

- 官方 `GET https://token.sensenova.cn/v1/models` 单次拉取 HTTP 200，当前 7 个模型（T0）。接口字段精简，不再返回 pricing/features。
- 对比 9/10 旧清单（8 个）：新增 deepseek-flash / sensenova-6.8-flash / glm-5.3；下架 deepseek-v4-pro / glm-5.2 / sensenova-6.7-flash-lite / sensenova-u1-fast。
- 实测 glm-5.3 chat 单枪撞 429（EndpointTPMExceeded，0.16s），按温和测试红线未重试。
- WB 真正活清单是 `C:\Users\Administrator\.workbuddy\models.json`（不是项目目录 8 月旧文件）。从 51 → 55 条，新增 4 条 SenseNova：glm-5.3-sensenova、deepseek-flash-sensenova、sensenova-6.8-flash、kimi-k3。前两个因与 intern-ai / DeepSeek 官方撞名加后缀。
- 备份：`models.json.bak-sensenova-20261125-110013`。JSON 校验通过，无重复 id。
- 报告：`SenseNova免费模型清单更新_20261125.md`（会话目录）。

## 续：用户三项要求（删/改回官方id/同步其他agent）
- ①删 glm-5.2：WB 活清单 55→54。②撞名条目改回官方 id（glm-5.3 / deepseek-flash），靠 [SenseNova] 显示名区分；修正上一轮 -sensenova 后缀的 404 隐患。依据：11-16 备份里 deepseek-v4-flash/openai/gpt-oss-20b 就是重复 id 不同 vendor，长期在用→WB 允许重复 id。
- ③选 skill：`custom-model-onboarding`（主，含 SenseNova 五端落点表）+ `autoclaw-add-model`（辅，版本判定/2.0 机制）。
- 已同步 6 个可用模型(deepseek-v4-flash/deepseek-flash/glm-5.3/kimi-k3/6.8-flash-lite/6.8-flash)，删下架 glm-5.2+6.7-flash-lite：DSH(cordis.patch.yml)/Hermes(config.yaml)/Hermes Studio(config.json 两处白名单)/龙虾(sqlite custom_2)/AutoClaw2.0(runtime.sqlite 追加4删2+重建凭证103匹配)。
- AutoClaw2.0 凭证是孤儿文件(oskey 11-17 解不开旧 enc，报 Unsupported state)→按 skill 用当前 key 全量重建凭证为 wb-bridge 占位(bridge 忽略鉴权)，数据库仍追加式其他 101 条未动。
- AutoClaw 1.x 还在跑(settings.json 被内存态频繁写回)→备好脚本 `AutoClaw1x_更新SenseNova_关进程后运行.py`，待用户关进程后自行运行。
- 报告：`SenseNova更新_五端同步报告_20261125.md`。未重启任何 agent。


# 2026-11-25 工作日志

## SenseNova 免费模型清单更新 + 写入 WB 活清单
- 官方 GET token.sensenova.cn/v1/models 单次 HTTP 200，当前 7 个模型（T0）。接口不再返回 pricing/features。
- 对比 9/10（8 个）：新增 deepseek-flash / sensenova-6.8-flash / glm-5.3；下架 deepseek-v4-pro / glm-5.2 / sensenova-6.7-flash-lite / sensenova-u1-fast。
- 实测 glm-5.3 单枪 429（TPM 限制），按红线未重试。
- WB 活清单 ~/.workbuddy/models.json：51 → 55 条，新增 glm-5.3-sensenova / deepseek-flash-sensenova / sensenova-6.8-flash / kimi-k3（前两个因撞名加后缀）。备份 models.json.bak-sensenova-20261125-110013。
- 报告在会话目录 2026-11-25-10-55-54/SenseNova免费模型清单更新_20261125.md。

## 续（12:15）：用户三项要求
- ①删 glm-5.2 ②撞名改回官方 id(glm-5.3/deepseek-flash,靠显示名区分,修正上轮 -sensenova 后缀 404 隐患) ③同步其他 agent。
- 选 skill: custom-model-onboarding(主) + autoclaw-add-model(辅)。
- 同步 6 模型到 DSH/Hermes/Hermes Studio/龙虾/AutoClaw2.0；2.0 凭证孤儿文件用当前 key 全量重建(wb-bridge 占位)，库仍追加式。
- AutoClaw1.x 在跑(内存态写回)，备好脚本 AutoClaw1x_更新SenseNova_关进程后运行.py 待用户关进程后运行。
- 报告: SenseNova更新_五端同步报告_20261125.md。

## wb-intl（WB 国际版）

> 数据源：D:\workspace\workbuddyai\2026-10-29-16-13-56\.workbuddy-ai\memory\2026-11-25.md, D:\workspace\workbuddyai\2026-11-25-13-25-06\.workbuddy-ai\memory\2026-11-25.md

（该 Agent 当天日志中未检出此类段落）

## autoclaw-115（AutoClaw 1.15）

> 数据源：C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\2026-11-25.md

## 短板#2 落地执行（用户 11:07 拍板"全部同意 执行吧"）

### ① 回灌分发 skill-creator（完成）
- au 端 11-24 官方新版（+175/-90 行）回灌 wb-cn 源头，再 `sync_skill.py skill-creator --to primary` 推平 7 端
- **合并 3 个本地补丁进官方新版**（不补丁直接分发会让 8 端脚本报错）：
  - `init_skill.py`：safe_print 防 emoji 崩溃 + stdout UTF-8 重配置（wb-cn 旧版补丁重放）
  - `quick_validate.py`：PyYAML 缺失降级（yaml=None 时走正则解析扁平 frontmatter；第一版 except NameError 设计错误 AttributeError 漏过，改 if/else 结构修复）
  - `quick_validate.py`：`read_text()` 补 `encoding='utf-8'`（官方脚本 GBK 崩溃，就是 api-test-pitfalls 那条红线）
  - `quick_validate.py`：未知 frontmatter key（agent_created/version 等本机惯例）从 return False 降为 warning 打印，不阻断绿灯闸
- 修正后 skill-creator 全 8 端 GREEN；备份 `workspace\backups\skill-creator_wbcn_20261125`

### ② 冒烟挂进星图每日编排（完成）
- 编排器 `D:\workspace\workbuddyai\2026-10-29-16-13-56\run_daily_star_scan.py` 升 v1.2：三步流水后追加第 4 步冒烟
  - 所有 subprocess 加 CREATE_NO_WINDOW（弹窗红线）；冒烟失败不阻断星图流水（rc4 计入总退出码但超时放行）
  - 冒烟结果自动追加进 `扫描日志\2026-11-25.md` 的「**冒烟测试**」小节
  - 新增 `--smoke-only` 参数单独跑
- dry-run 全流程实测通过（scan=0 memory=0 merge=0 smoke=0）；备份 `workspace\backups\run_daily_star_scan.py.bak-20261125`
- 注意：星图扫描器 11:00 已自动把 smoke_tests 目录收编为节点 p179

### ③ 分发绿灯闸（完成）
- `sync_skill.py` 升 v1.1：真实推送完成后自动跑 `smoke_common_skills.py --skill <名>`，红灯=分发失败 exit 1；黄灯默认放行 `--strict` 也拦；`--dry-run` 不触发闸（v1.1 初版漏了这个，已补）
- **红灯拦截实测通过**：注入语法坏脚本 → 冒烟 RED → `[ABORT] 绿灯闸拦截`
- **自修复案例**：测试时 rename 掉 au 端 skill-vetter 的 SKILL.md，推送自己把它重建了——sync 先修复、闸门验推送后状态，放行正确
- 闸门输出不能带 emoji（✅ 在 GBK 控制台崩溃，又被自己的坑教育了一次）
- SKILL.md 流程文档已补绿灯闸说明；v1.1 推平 8 端 hash 全一致；备份 `workspace\backups\cross-agent-skill-install_wbcn_20261125`

### 终态
- 全量冒烟：17 绿 / 0 黄 / 0 红；smoke_log.txt 持续追加；文件：`workspace\smoke_tests\`（smoke_common_skills.py v1.1 + 报告 HTML）
- 短板#2 从"建议"变成"已运行的机制"：每日 11:00/23:00 自动冒烟 + 每次分发强制绿灯

## zcode（ZCode）

> 数据源：C:\Users\Administrator\.zcode\cli\db\db.sqlite

（该 Agent 当天日志中未检出此类段落）