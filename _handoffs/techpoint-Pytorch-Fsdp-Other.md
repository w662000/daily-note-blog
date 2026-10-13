---
layout: default
title: 技术点 · Pytorch-Fsdp - Other
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Pytorch-Fsdp - Other

> 来源：261010_Pytorch-Fsdp - Other_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ProcessGroup.hpp: contains the abstract API of all process group implementations. The c10d library provides 3 implementations out of the box, namely, ProcessGroupGloo, ProcessGroupNCCL, and ProcessGroupMPI. DistributedDataParallel uses ProcessGroup::broadcast() to send model states from the process with rank 0 to others during initialization and ProcessGroup::allreduce() to sum gradients.
- Stable (API-Stable): These features will be maintained long-term and there should generally be no major performance limitations or gaps in documentation. We also expect to maintain backwards compatibility (although breaking changes can happen and notice will be given one release ahead of time).
- Unstable (API-Unstable): Encompasses all features that are under active development where APIs may change based on user feedback, requisite performance improvements or because coverage across operators is not yet complete. The APIs and performance characteristics of these features may change.
- The generic join context manager facilitates distributed training on uneven inputs. This page outlines the API of the relevant classes: Join, Joinable, and JoinHook. For a tutorial, see Distributed Training with Uneven Inputs Using the Join Context Manager.
- kwargs (dict) – a dict containing any keyword arguments to modify the behavior of the join hook at run time; all Joinable instances sharing the same join context manager are forwarded the same value for kwargs.
- Experimental Object Oriented Distributed API#
- This is an experimental new API for PyTorch Distributed. This is actively in development and subject to change or deletion entirely.
- This is intended as a proving ground for more flexible and object oriented distributed APIs.
- Create a new process group with the given backend and options. This group is independent and will not be globally registered and thus not usable via the standard torch.distributed.* APIs.
- type(model) is “unioned” with FSDPModule in-place. For example, if model is originally of type nn.Linear, then fully_shard changes type(model) from nn.Linear to FSDPLinear in-place. FSDPLinear is an instance of both nn.Linear and FSDPModule. It retains all methods of nn.Linear while also exposing FSDP2-specific APIs under FSDPModule, such as reshard() and unshard().
- FSDP2 exposes APIs for manual control over prefetching and collective scheduling, allowing power users more customization. See the methods on FSDPModule below for details.
- FSDP2 simplifies some of the API surface: e.g. FSDP2 does not directly support full state dicts. Instead, users can reshard the sharded state dicts containing DTensor s to full state dicts themselves using DTensor APIs like DTensor.full_tensor() or by using higher-level APIs like PyTorch Distributed Checkpoint ‘s distributed state dict APIs. Also, some other args have been removed; see here for details.

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
