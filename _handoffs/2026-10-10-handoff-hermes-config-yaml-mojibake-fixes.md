---
layout: default
title: 交接文档 · Hermes config.yaml Mojibake Fixes
date: 2026-10-13 23:30:00 +0800
---

# Hermes config.yaml Mojibake Fixes

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\software-development\user-operational-guidelines\references\hermes-config-mojibake-fixes.md

> Windows 鐜涓� `config.yaml` 涓枃 label 甯歌涔辩爜鍙婁慨澶嶆槧灏勩��

## 涔辩爜鏄犲皠琛�

| 涔辩爜鍘熸枃 | 淇鍚� |
|---------|--------|
| `label: GLM-4.7-Flash (锟斤拷锟�)` | `label: GLM-4.7-Flash (free)` |
| `label: Gemini Flash (锟斤拷锟斤拷)` | `label: Gemini Flash (latest)` |
| `label: Step-3.7-Flash (step_plan 锟斤拷锟斤拷)` | `label: Step-3.7-Flash (step_plan subscription)` |
| `label: Gemma-4-31B ?(NVIDIA直锟斤拷)` | `label: Gemma-4-31B (NVIDIA direct)` |
| `label: Inkling ?(NVIDIA直锟斤拷)` | `label: Inkling (NVIDIA direct)` |
| `label: Nemotron-3-Super-120B ?(NVIDIA直锟斤拷)` | `label: Nemotron-3-Super-120B (NVIDIA direct)` |
| `label: Nemotron-3-Ultra-550B ?(NVIDIA直锟斤拷)` | `label: Nemotron-3-Ultra-550B (NVIDIA direct)` |
| `label: Step-3.7-Flash ?(NVIDIA直锟斤拷)` | `label: Step-3.7-Flash (NVIDIA direct)` |
| `label: GLM-5.2 ?(Z.ai锟届舰锟斤拷锟斤拷glm-5)` | `label: GLM-5.2 (Z.ai flagship / replaces glm-5)` |
| `label: GPT-OSS 120B ?(锟斤拷锟斤拷)` | `label: GPT-OSS 120B (reasoning)` |
| `label: DeepSeek-V4-Flash (锟斤拷锟斤拷锟斤拷锟皆硷拷锟侥端碉拷)` | `label: DeepSeek-V4-Flash (self-deployed endpoint)` |

## 淇鏂规硶

```python
from pathlib import Path
p = Path(r'C:/Users/Administrator/.hermes/config.yaml')
text = p.read_bytes().decode('utf-8', errors='replace')
replacements = {
    'label: GLM-4.7-Flash (锟斤拷锟�)': 'label: GLM-4.7-Flash (free)',
    # ... 鍏朵粬鏄犲皠
}
for old, new in replacements.items():
    text = text.replace(old, new)
p.write_bytes(text.encode('utf-8'))
```

## 娉ㄦ剰

- `patch` 宸ュ叿浼氭嫆缁濅慨鏀� `~/.hermes/config.yaml`锛岄渶鐢� Python 鐩存帴璇诲啓銆�
- 棰勯槻鑳滀簬淇锛氭柊澧� label 鏃朵紭鍏堜娇鐢ㄧ函鑻辨枃銆�
