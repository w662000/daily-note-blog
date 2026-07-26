---
layout: default
title: 每日工作总结 · 2026-07-20
date: 2026-07-20 23:30:00 +0800
---

# 每日工作总结 · 2026-07-20

## 一、今日完成事项
**hermes-webui 免费部署平台全网调研 + 实战落地**：
1. **Back4App + Cloudflare 流程**：澄清"back4app 当 VPS"误区，产出部署指南 + deploy-kit（极简 Dockerfile 读 $PORT）。
2. **平台横向调研**：Render(512MB 易 OOM) / Koyeb(已被 Mistral 收购，免费档对新用户关闭) / Oracle Always Free(4C24G 真免费但需绑卡) / Cloud Run / Fly.io / Railway 均不推荐。
3. **Koyeb 套件**：实测安装 Koyeb CLI 并校验精确参数，产出 `hermes-webui-koyeb/` 套件（README + deploy 脚本 + .env.example）。
4. **Render 实测 OOM → 切 HF Spaces**：用户已在 Render 部署但切换模型转圈（512MB+0.1vCPU 跑双进程 OOM Kill）。最终选 Hugging Face Spaces Docker（2vCPU/16GB），产出 `hermes-webui-hf-spaces/`。用户获取 OpenRouter Key。
5. **2026 免费平台收紧盘点**：HF Spaces Docker 对新账号变 Paid、ClawCloud 已停运、Koyeb 免费关闭。
6. **SnapDeploy 实战（最终选择）**：用户无外币卡，被迫选 SnapDeploy（无卡、512MB、auto-sleep）。踩坑："Always-On $12/mo"是营销提示，走完 Port+Env 向导后免费部署变蓝。UptimeRobot 每 5min ping /health 保活。

## 二、关键决策 / 注意事项
- **Render 512MB OOM 判因**：webui(~200-300MB)+agent(~150-200MB)+开销，临界状态，切模型 API 触发额外分配→Kill→重启→超时。
- **SnapDeploy 必须 GitHub 仓库 + Dockerfile 流程**，无"直接填镜像"入口。
- 教训：先让用户走完向导再判断是否真要付费，别被营销提示吓退。

## 三、生成的有用文件
| 文件/目录 | 路径 | 用途 |
|---|---|---|
| Back4App 指南 | `2026-07-20-11-59-37\hermes-webui-back4app-cloudflare-deploy.md` | Back4App+Cf 部署详指 |
| Render/Koyeb 指南 | `hermes-webui-render-koyeb-deploy.md` | 含 Oracle 备选 |
| HF Spaces 套件 | `hermes-webui-hf-spaces\` | Dockerfile + README + .env.example |
| SnapDeploy 套件 | `hermes-webui-snapdeploy\` | Dockerfile + start.sh + README |
| Koyeb 套件 | `hermes-webui-koyeb\` | CLI 一键部署脚本 |
| 极简部署包 | `deploy-kit\` | 读 $PORT 的通用 Dockerfile |
| 其他 | `it-tools-snapdeploy\`、`baihu-deploy\`、`baihu-data\` | it-tools 部署 / 白虎面板（前序项目） |

## 四、待办 / 风险
- SnapDeploy 需 UptimeRobot 保活（15min auto-sleep）。
- 用户 OpenRouter Key 已获取，待配置进 Hermes WebUI Provider。
- HF Spaces 已变 Paid，若 SnapDeploy 不满足再评估 Oracle（需绑卡）。
