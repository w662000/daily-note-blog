---
layout: default
title: 技术点 · Axolotl - Api
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Axolotl - Api

> 来源：261010_Axolotl - Api_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\mlops\training\axolotl\references\api.md
- **URL:** https://docs.axolotl.ai/docs/api/cli.cloud.modal_.html
- ```
cli.cloud.modal_.ModalCloud(config, app=None)
```
- ```
cli.cloud.modal_.run_cmd(cmd, run_folder, volumes=None)
```
- **URL:** https://docs.axolotl.ai/docs/api/core.trainers.base.html
- ```
core.trainers.base.AxolotlTrainer(
    *_args,
    bench_data_collator=None,
    eval_data_collator=None,
    dataset_tags=None,
    **kwargs,
)
```
- ```
core.trainers.base.AxolotlTrainer.log(logs, start_time=None)
```
- ```
core.trainers.base.AxolotlTrainer.push_to_hub(*args, **kwargs)
```
- ```
core.trainers.base.AxolotlTrainer.store_metrics(
    metrics,
    train_eval='train',
    reduction='mean',
)
```
- **URL:** https://docs.axolotl.ai/docs/api/prompt_strategies.input_output.html
- ```
prompt_strategies.input_output.RawInputOutputPrompter()
```
- ```
prompt_strategies.input_output.RawInputOutputStrategy(
    *args,
    eos_token=None,
    **kwargs,
)
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
