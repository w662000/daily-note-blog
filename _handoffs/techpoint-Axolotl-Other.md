---
layout: default
title: 技术点 · Axolotl - Other
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Axolotl - Other

> 来源：261010_Axolotl - Other_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
# Automatic BF16 detection (recommended)
bf16: auto

# Or explicitly enable
bf16: true

# For evaluation with BF16
bf16: full  # Equivalent to bf16_full_eval in the HF trainer
```
- ```
# Enable FP8 mixed precision
fp8: true

# Optional: Enable FP8 for FSDP all-gather operations
fp8_enable_fsdp_float8_all_gather: true

# Enable torch.compile (almost always necessary for FP8 speedups)
torch_compile: true
```
- ```
fp8: true
fp8_enable_fsdp_float8_all_gather: true

torch_compile: true

# FSDP configuration
fsdp_version: 2
fsdp_config:
  offload_params: false
  cpu_ram_efficient_loading: true
  auto_wrap_policy: TRANSFORMER_BASED_WRAP
  transformer_layer_cls_to_wrap: LlamaDecoderLayer
  state_dict_type: FULL_STATE_DICT
  reshard_after_forward: true
```
- A: This is likely due to vocab size mismatch. By default, Axolotl expands the model’s embeddings if the tokenizer has more tokens than the model. Please use the axolotl merge-lora command to merge the adapters instead of using your own scripts.
- On the other hand, if the model has more tokens than the tokenizer, Axolotl does not shrink the model’s embeddings unless shrink_embeddings: true is set in the config.
- Q: ValueError: Asking to pad but the tokenizer does not have a padding token. Please select a token to use as pad_token
- A: This is because the tokenizer does not have a padding token. Please add a padding token to the tokenizer via:
- Q: IterableDataset error or KeyError: 'input_ids' when using preprocess CLI
- A: We use torch APIs to retrieve this information. You can see https://docs.pytorch.org/docs/stable/notes/cuda.html#cuda-memory-management for more information.
- A: The specific turn’s start/end could not be detected. Please ensure you have set the eos_token following your chat_template. Otherwise, this could be a chat_template which doesn’t use proper boundaries for each turn (like system). On the rare occurrence, make sure your content is not [[dummy_message]]. Please let us know about this.
- Q: The EOS token is incorrectly being masked or not being masked / EOS token __ not found in chat template.
- Q: “chat_template choice is tokenizer_default but tokenizer’s chat_template is null. Please add a chat_template in tokenizer config”

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
