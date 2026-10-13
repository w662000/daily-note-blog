---
layout: default
title: 技术点 · Axolotl - Dataset-Formats
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Axolotl - Dataset-Formats

> 来源：261010_Axolotl - Dataset-Formats_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **URL:** https://docs.axolotl.ai/docs/dataset-formats/tokenized.html
- Custom Pre-Tokenized Dataset
- ```
datasets:
  - path: /path/to/your/file.jsonl
    ds_type: json
    type:
```
- ```
{"input_ids":[271,299,99],"attention_mask":[1,1,1],"labels":[271,-100,99]}
{"input_ids":[87,227,8383,12],"attention_mask":[1,1,1,1],"labels":[87,227,8383,12]}
```
- In the case that the dataset is small and can be loaded entirely into memory, another approach to running pre-training is to use the completion format. This would mean that the entire dataset is pre-tokenized instead of on-demand in streaming.
- One benefit of this is that the tokenization can be performed separately on a CPU-only machine, and then transferred to a GPU machine for training to save costs.
- One step is equal to sequence_len * micro_batch_size * gradient_accumulation_steps * total_num_gpus tokens.
- Do you already have the dataset tokenized? If yes, check Pre-Tokenized Dataset.
- We suggest this approach when you want to bring your own tokenized dataset.
- Axolotl expects the dataset to have three keys:
- Make sure to add BOS/EOS tokens to your prompt and mask it appropriately.
- Reference: Pre-Tokenized Dataset Documentation.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
