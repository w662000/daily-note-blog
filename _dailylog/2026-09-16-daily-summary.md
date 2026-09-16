---
layout: default
title: 每日工作总结 · 2026-09-16
date: 2026-09-16 23:30:00 +0800
---

# 每日工作总结 · 2026-09-16

## 一、今日完成事项

1. **AutoClaw「云端方案优化」频繁 403 根因排查**（上午，另一会话）
   - 定位到 GLM-5.3 免费额度耗尽（与账号积分是两套池子），官方给三条路：切 Auto / 开会员 / 买 Coding Plan。
   - 用户切 Auto 后仍 403，进一步定位到 AutoClaw 内置 zai 共享通道服务端间歇性拒绝；叠加「无模型回退 + 错误映射为空」→ 体感频繁且裸 403。建议默认模型改走自有 provider（agnes-ai 今日 0 失败 / glm-api）。

2. **活清单模型可用性温和测试**（14:00）
   - 读雷达快照发现 md 列 79 个但 models.json 真实只有 47 个——md 已脱钩。
   - 47 个中可用 12（25%），失败 5 类：真·下线 9、地区封锁 12、额度耗尽 6、端点误报 5、临时抖动 6。

3. **12 平台全量拉目录 + 并行温和重测**（14:32–16:40）
   - 8 平台成功拉全量目录，新增 283 个（去重后）合并进 models.json → 47→330。
   - 并行拨测 7 桶：原 sub-agent 方案被框架运行时长上限杀掉 → 改后台 Bash 进程 + 增量写盘脚本，成功出齐。
   - **最终 328 模型探测 / 24 可用**（合并前基线 12，净增 +12）。

4. **雷达 vs 探针交叉验证**（16:55）
   - 判定口径=两源都 ok 为「真正可用」→ 真正可用 12（NIM 10 + CF 2 + Groq 0）。
   - NIM 真失效 60 个应清理；抖动 16 个建议单枪复测。

5. **重制活清单 md**（下午）
   - 按国内/国外分组生成 `model-speed-radar/模型能力清单_2026-09-16.md`（原 24 个版本漏了 GLM/DeepSeek/SenseNova/Agnes/BazaarLink/b.ai）。

6. **裁剪 WB 自定义模型 330→41**（17:49）
   - 保留集=全量探针+雷达任一源 ok 的国内可用 + Gemini/Groq（国内部署地区封锁·国外可用）。
   - 实际保留 41（非之前表的 24）。分布：NIM15/CF3/Gemini3/Groq3/Agnes3/BazaarLink5/GLM3/DeepSeek2/SenseNova2/b.ai2。删除 289。

7. **活清单前缀整理 + 去重 41→39**（21:06）
   - 删 BazaarLink 2 个裸 id 冷却重复；给 18 个不带 [厂商] 前缀的条目统一加前缀。
   - 备份 models.json.bak-prefix-20260916_2106。

8. **雷达刷新到 39**（21:18–21:25）
   - 测速雷达（8848）：POST /api/run-now 唤醒，跑完第 328 轮 done 39/39。
   - 限速雷达（8849）：卡在旧 330 轮 → 杀旧进程 + 清 partial.json + 重新拉起，重启即跑一轮「第 80 轮限流扫描开始 (39 模型/10 平台)」。
   - 活清单 md 同步重写为完整 39 个。

9. **Gemini/Groq 代理复测三轮**（22:05–22:44）
   - 原节点：Gemini 400（key 地区限制）、Groq 403（出口 IP 地理封锁）。
   - 日本节点：两家均 Remote end closed（连接层被掐），比原节点更不可用。
   - 美国节点：Groq **HTTP 200 ttft≈1237ms 通了**；Gemini TLS 握手超时（链路抖动，非 key 地区）。
   - 结论：**Groq 3 确认可用（需美国节点代理）**；Gemini 3 仍失败根因疑链路非 key。活清单 md 第二节已同步。

## 二、关键决策 / 注意事项

- **长耗时拨测别用 sub-agent 后台跑**（有运行时长上限会被杀丢数据）→ 改用后台 Bash 进程 + 增量写盘脚本。此经验可存为 skill「parallel-model-probe」。
- **两雷达都每轮 load_models() 重读 models.json** → 裁剪后下轮自动只测 39；想立刻刷新用 `/api/run-now` 唤醒（比另起 --once 安全）。限速雷达若卡在旧轮必须重启（杀进程 + 清 partial）。
- **自动刷新雷达 vs 另起 --once**：有守护进程跑时优先 `/api/run-now`，避免并行双拨测触发 429/503 红线。
- **Gemini/Groq 活清单"需国外环境"归类偏乐观** → 实际走代理也救不活（日本节点更差）；仅 Groq 美国节点能通，Gemini 仍 TLS 超时。
- **ALL_PROXY 无效残留值**建议清理（当前不影响，urllib 优先 HTTPS_PROXY）。

## 三、生成的有用文件

| 文件/目录 | 路径 | 用途 |
|---|---|---|
| 活清单可用性快照 md | `model-speed-radar/进度/进度_20260916_1400_活清单健康测试.md` | 14:00 温和测试记录 |
| 并行拨测进度 | `model-speed-radar/进度/进度_20260916_1432_并行拨测12平台.md` | 14:32–16:40 12 平台合并结果 |
| 雷达 vs 探针交叉验证 | `model-speed-radar/进度/进度_20260916_1655_雷达vs探针_NIM_Groq_CF.md` | 16:55 两源对比结论 |
| 活清单 md（39 个完整版） | `model-speed-radar/模型能力清单_2026-09-16.md` | 当日可用模型清单（国内/国外分组） |
| models.json 备份 1（合并前） | `C:\Users\Administrator\.workbuddy\models.json.bak-merge-20260916_143001` | 合并 283 个前的基线 |
| models.json 备份 2（裁剪前） | `C:\Users\Administrator\.workbuddy\models.json.bak-trim-20260916_1749` | 裁剪到 41 前的 330 全量 |
| models.json 备份 3（前缀整理前） | `C:\Users\Administrator\.workbuddy\models.json.bak-prefix-20260916_2106` | 整理前缀前的 41 |
| 探针脚本 | `C:/Users/Administrator/AppData/Local/Temp/gentle_probe_vendors.py` | 7 sub-agent 并行拨测（后改 Bash） |
| 探针脚本（改进版） | `C:/Users/Administrator/AppData/Local/Temp/stream_probe_vendors.py` | 增量写盘版 |
| 探针脚本（Gemini/Groq） | `C:/Users/Administrator/AppData/Local/Temp/gentle_gemini_groq_probe.py` | 三轮代理复测 |
| 活清单生成脚本 | `C:/Users/Administrator/AppData/Local/Temp/gen_live_list.py` | 原 24 版生成 |
| 活清单生成脚本（39 版） | `C:/Users/Administrator/AppData/Local/Temp/gen_live_list_39.py` | 当日 39 版生成 |
| 本机日志（AutoClaw 403） | `C:\Users\Administrator\.workbuddy\.workbuddy\memory\2026-09-16.md` | 另一会话的 AutoClaw 排查记录 |
| 本机日志（模型活清单） | `D:\AI work\workbuddy\2026-09-16-13-57-32\.workbuddy\memory\2026-09-16.md` | 当前会话主日志 |

## 四、待办 / 风险

- [ ] NIM 真失效 60 个待清理（雷达 latest.json 仍旧 328，下轮会刷新到 39；但历史轮次仍残留旧数据）。
- [ ] 抖动 16 个模型建议单枪复测确认（最可能真能用的：NIM 的 Gemma-4-31B / llama-3.2-11b-vision / Poolside Laguna-XS-2.1 / Nemotron-3-Ultra-550B / glm-5.3-flash + CF 的 qwq-32b）。
- [ ] ALL_PROXY 无效残留值建议清理（当前不影响）。
- [ ] Gemini 3 美国节点仍 TLS 超时，需后续再试或换节点验证。
- [ ] AutoClaw 内置 zai 共享通道 403 问题：建议默认模型改走自有 provider（agnes-ai / glm-api）；若 UI 支持配模型回退更佳。
- [ ] 活清单 md 与 models.json 保持同步——下次裁剪/增补后记得重跑 gen_live_list 脚本。
