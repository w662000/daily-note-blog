---
layout: default
title: 每日工作总结 · 2026-08-18
date: 2026-08-18 23:30:00 +0800
---

# 每日工作总结 · 2026-08-18

## 一、今日完成事项（分点，通俗语言）

1. **b.ai 模型接入 WorkBuddy（WB 端）**：把 b.ai（OpenAI 兼容，`https://api.b.ai/v1/`）的 `deepseek-v4-flash` 模型接进 WB。先用 curl 单发做了温和连通性验证（key 有效、模型存在、返回 `reasoning_content` 支持推理），再把条目写进 `~/.workbuddy/models.json`，并备份了原文件。

2. **b.ai 接入 DSH 与 Hermes 两套系统**：过程中纠正了一个关键认知错误——原来以为 `~/.dsh/settings.yaml` 是 Hermes 的配置，其实它是 DSH 应用（127.0.0.1:3080）的配置，Hermes 是另一个独立应用。理清了四套配置机制后，分别在 `.credentials.yaml`（存 key）、`~/.dsh/settings.yaml`、以及 Hermes 主配置 `~/.hermes/config.yaml` 三处加好 `b-ai` provider 并校验通过。

3. **二次纠错：补上 Hermes WebUI(8787) 与 Studio(8648) 漏掉的 b.ai**：发现 WebUI 和 Studio 真正读取的是 `~/.hermes/config.yaml`（代码铁证：`config.py:389` 指定 Hermes home 下的 config.yaml），而之前 13:05 改的 `AppData/Local/hermes/config.yaml` 是另一份互不干扰的独立副本，所以漏了。补上后并把旧缓存目录 rename 让其重启重建。至此理清 Hermes 拓扑：WebUI(8787) + Studio(8648) + gateway(5324) 三者共用 `~/.hermes/config.yaml`。

4. **新加模型流程固化为 skill**：把整套"WB / DSH / Hermes / Studio 四系统接入"流程沉淀为 user 级 skill `custom-model-onboarding`（含四系统拓扑表、前置温和验证、五步接入、PowerShell CIM 进程定位、验收清单、回滚、常见故障速查）。17:03 按用户要求把触发词改成中文「新加模型 / 新增模型」优先。

5. **系统维护：清理 Tabbit 浏览器升级残留双条目**：默认浏览器列表出现 `tabbit browser`(英文) 和 `Tabbit浏览器`(中文) 两条。根因是升级没卸干净——正版在 HKLM（显示中文），旧版残留是 HKCU 用户级带随机后缀的键（显示英文），指向同一 exe。备份注册表后删掉 HKCU 残留项，验证默认关联不变。

6. **11:00 发布链路 FAILOVER 巡检（目标日 08-17，第 13 次）**：4 活跃端（博客 / Gridea / 论坛 / 云笔记）日志 + handoff(7) + 技术点(7) 全部齐平零缺口，无需补发；语雀因禁用跳过。复核时特别做了大小写不敏感匹配，避免 slug 含旧日期的条目被 grep 漏检。

## 二、关键决策 / 注意事项

- **models.json 的 id 不能带供应商前缀**：第一次写成 `b.ai/deepseek-v4-flash`，结果 b.ai 侧返回 404 `model_not_found`（id 就是直接发给 API 的 `model` 参数）。已改为裸 `deepseek-v4-flash`，原 SenseNova 同名条目改名 `deepseek-v4-flash-sensenova` 避撞。
- **四套系统 = 四套配置格式，没理由再混**：WB 用 `~/.workbuddy/models.json`（扁平数组）；DSH 用 `~/.dsh/settings.yaml`（providers + key 在 `.credentials.yaml`）；Hermes 真配置是 `~/.hermes/config.yaml`（`custom_providers[]`）；Studio 可见性白名单在 `~/.hermes-web-ui/config.json`（`modelVisibility` / `customModels`）。
- **进程定位用 PowerShell CIM**：`wmic` 已被安全策略禁用，改用 `Get-CimInstance Win32_Process` 查进程命令行。
- **软件升级后出现默认程序重复项**：先扫 `HKCU\Software\RegisteredApplications` + `HKCU\Software\Clients\StartMenuInternet` 找带随机后缀的 per-user 残留，删 HKCU 那条即可，默认关联（HKLM/ProgId）不动。
- **所有 provider 改动都需重启对应服务才生效**：DSH(3080) / Hermes gateway(5324) / WebUI(8787) / Studio(8648) 当前在跑，但还没加载新 provider。

## 三、生成的有用文件（表格：文件/目录 | 路径 | 用途）

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| WB 模型清单（含 b.ai 条目） | `C:\Users\Administrator\.workbuddy\models.json` | WB 的模型注册表，新增 `deepseek-v4-flash` |
| models.json 接入前备份 | `C:\Users\Administrator\.workbuddy\models.json.bak-add-bai-20260818` | 改前备份，可回滚 |
| DSH 配置（b-ai provider） | `C:\Users\Administrator\.dsh\settings.yaml` | DSH 应用模型配置 |
| DSH 凭证（WB_KEY_11 = b.ai key） | `C:\Users\Administrator\.dsh\.credentials.yaml` | DSH 明文 key 存放 |
| Hermes 真配置（custom_providers.b-ai） | `C:\Users\Administrator\.hermes\config.yaml` | WebUI/Studio/gateway 共用的真配置 |
| Studio 可见性白名单 | `C:\Users\Administrator\.hermes-web-ui\config.json` | Studio UI 模型可见性 |
| user 级 skill | `C:\Users\Administrator\.workbuddy\skills\custom-model-onboarding\` | 新加模型四系统接入流程固化，可复用 |
| skill 打包 zip | `D:\AI work\workbuddy\2026-08-18-12-42-34\custom-model-onboarding.zip` | 分发用（编辑请改 skills 目录） |
| Tabbit 注册表备份 | `D:\tabbit_orphan_backup.reg` | 删残留前 `reg export` 备份 |
| 本总结 | `D:\AI work\workbuddy\2026-08-18-12-42-34\2026-08-18_每日工作总结.md` | 每日工作总结 |

## 四、待办 / 风险

- **P0/P1 待用户重启生效**：所有 provider 改动需重启 DSH(3080) / Hermes gateway(5324) / WebUI(8787) / Studio(8648) 才能加载新 provider；Hermes 默认模型仍是 `bazaarlink`，用户可自行 `/model` 切换或改 config.yaml。
- **P1 干扰副本未清理**：13:05 改的 `AppData/Local/hermes/config.yaml` 是独立副本、Hermes 不读它，无害但易混淆，待用户决定是否删除。
- **P1 巡检遗留（非目标日，未动）**：`260804` bbs1org `body>20000` 连续第 7 天失败；6 篇退化命名 handoff 卡收件箱；技术点 Hermes 8787 slug 双份重复。
- **P2 Studio 缓存待验证**：`.hermes-web-ui/cache/provider-model-catalog.json` 已 rename 为 `.old-20260818-1316`，需重启确认能正常重建（旧目录可恢复）。
