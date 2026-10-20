---
layout: default
title: 每日工作总结 · 2026-10-20
date: 2026-10-20 23:30:00 +0800
---

# 每日工作总结 · 2026-10-20

## 一、今日完成事项

1. **slg-qa（cf-multi-agent-qa）Cloudflare Workers 全链路部署**（14:43–22:50，10 轮迭代）
   - 初始部署：npm install、wrangler login、建 D1 数据库 `slg-kb`、建表 schema、灌种子数据
   - 修复 `NonRetryableError` 来源错误（`cloudflare:workflows` 而非 `cloudflare:workers`）
   - 端到端验证：health 接口正常、ADMIN_TOKEN secret 配置、自定义域 `qa.780.de5.net` 绑定成功（国内直连）

2. **M2 门禁系统修复与验证**（18:27–19:50）
   - 定位两个代码 bug：① `robustJson` 未校验 expect 类型导致单对象返回被拒；② plan maxTokens 400 过小截断
   - 新增 D1 读数版门禁脚本 `scripts/gate-from-db.mjs`，避开本地 dev 的 miniflare 缺陷
   - 最终 6 项门禁全绿：审核有效性 5/5、矛盾识别 2/2、预算偏差 ✅、重试率 ✅、回答多样性 5/5、负向用例 2/2

3. **系统架构升级 v2**（21:08–22:50）
   - 三步骨架：repair 循环（2 轮带审核反馈 + 预算闸）、门禁拦截（矛盾未消强制 compose 逐条回应）、任务板化（board_tasks 表 + 前端实时进度 chips）
   - 多轮上下文：注入 prevTaskId，critique 新增「与提问一致性」维度（防数字幻觉）
   - compose-v3 输出结构合同：正文≥70% 自足可读 + 矛盾处理放末节
   - 彻底清除 KB 模块（searchKb/retrieve/grounded 分支/kb_articles 表），系统转为独立多 agent 问答
   - 最终版本 `5365f118`，日额度 1341/8500 neurons

## 二、关键决策 / 注意事项

1. **D1 读数版门禁 vs 本地 dev**：本地 miniflare 跑 Workflow step 调远程 AI binding 必挂（GitHub cloudflare/computer#63 已知缺陷），改用直连 D1 读数方案
2. **maxTokens 阶梯设计**：plan 400→600（只抬天花板不白扣）、extract/critique/compose 1400/900/2800、reasoning_effort:'low' 等效关 gpt-oss 思考
3. **自定义域绑双入口**：workers.dev（国内需代理）+ `qa.780.de5.net`（国内直连推荐），home 首页改版适配查询功能
4. **GBK 污染坑**：Git Bash curl 发中文 JSON 被 GBK 污染（hex 实锤 U+FFFD），改用 node fetch 重测

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 进度日志 | `D:\AI work\workbuddy\2026-10-20-14-43-25\进度\进度_20261020_1737_slg-qa部署.md` | 完整迭代记录（116 行） |
| 门禁脚本 | `C:\Users\Administrator\WorkBuddy AI\2026-10-20-11-50-43\cf-multi-agent-qa\scripts\gate-from-db.mjs` | D1 读数版门禁（6 项全绿） |
| 线上入口 | https://qa.780.de5.net | 国内直连（推荐） |
| 线上入口 | https://qa.wxatp.workers.dev | 国际入口（需代理） |

## 四、待办 / 风险

1. **额度监控**：日用量 1341/8500 neurons（15.8%），后续若继续迭代注意配额
2. **旧 token 权限**：7 月旧 OAuth token 缺 d1:write，本次已重登修复，需定期检查 token 有效期
3. **本机代理依赖**：访问 workers.dev 需走 `http://127.0.0.1:7897`，Node 脚本需 `NODE_USE_ENV_PROXY=1`

---
*生成时间：2026-10-20 22:55 GMT+8*
*基于真实机器日志（进度_20261020_1737_slg-qa部署.md）*
