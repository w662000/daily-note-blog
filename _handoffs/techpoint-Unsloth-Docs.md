---
layout: default
title: 技术点 · Unsloth Docs
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Unsloth Docs

> 来源：261010_Unsloth Docs_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- <table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>DeepSeek-OCR</strong></td><td>Fine-tune DeepSeek's latest OCR model.</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FP6V5vkGfGPBdRlkpB35Q%2Fdeepseek%20ocr%20logo.png?alt=media&#x26;token=43a73901-37a9-4cb9-a25c-fa01cf03baea">deepseek ocr logo.png</a></td><td><a href="../new/deepseek-ocr-how-to-run-and-fine-tune">deepseek-ocr-how-to-run-and-fine-tune</a></td></tr><tr><td><strong>Qwen3-VL</strong></td><td>Run &#x26; fine-tune Qwen's new vision models!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXrFygtnLnqHhVmEIidg3%2Fqwen3-vl%20promo.png?alt=media&#x26;token=82f58481-4e0c-4977-af26-2ea08a227ad2">qwen3-vl promo.png</a></td><td><a href="../models/qwen3-vl-how-to-run-and-fine-tune">qwen3-vl-how-to-run-and-fine-tune</a></td></tr><tr><td><strong>gpt-oss</strong></td><td>Run &#x26; Train OpenAI's new open LLMs.</td><td data-object-fit="fill"><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FX0pJKFv8zDMf4TJomAts%2Fgpt-oss%20image.png?alt=media&#x26;token=60c73c0d-cf83-4269-9619-f4b71e25767a">gpt-oss image.png</a></td><td><a href="../new/gpt-oss-reinforcement-learning">gpt-oss-reinforcement-learning</a></td></tr></tbody></table>
- <table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Unsloth Docker image</strong></td><td>Train LLMs with no setup with our new Docker!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FomKrFeo6Y2Z6ffPjygKP%2Ftrain%20without%20setup.png?alt=media&#x26;token=e5c60f27-689f-4929-9453-49dc0e45a122">train without setup.png</a></td><td><a href="../new/how-to-fine-tune-llms-with-unsloth-and-docker">how-to-fine-tune-llms-with-unsloth-and-docker</a></td></tr><tr><td><strong>Vision Reinforcement Learning</strong></td><td>VLM RL is now in Unsloth! RL with Qwen, Gemma.</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FPOHnYqLRCh4d9TvBRNlY%2Fvision%20rl%20site.png?alt=media&#x26;token=26f859e5-53e5-444b-bf90-7f1901a9058a">vision rl site.png</a></td><td><a href="../new/vision-reinforcement-learning-vlm-rl">vision-reinforcement-learning-vlm-rl</a></td></tr><tr><td><strong>How do Unsloth 1-bit Dynamic GGUFs perform?</strong></td><td>See GGUF benchmarks on Aider Polyglot!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdiwpvMM4VA4oZqaANJOE%2Fdynamic%20v2%20with%20unsloth.png?alt=media&#x26;token=adc64cb6-2b52-4565-a44e-ac4acbd4247d">dynamic v2 with unsloth.png</a></td><td><a href="../new/unsloth-dynamic-ggufs-on-aider-polyglot">unsloth-dynamic-ggufs-on-aider-polyglot</a></td></tr></tbody></table>
- ```
pip install unsloth
```
- <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FLrqITvuoKyiMl8mqfu5B%2Flarge%20sloth%20wave.png?alt=media&#x26;token=3077792b-90ff-459d-aa52-57abcf219adf" alt="" width="188"><figcaption></figcaption></figure>
- <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FjT759hR4zq8ygzg1oEwI%2FLarge%20sloth%20Question%20mark.png?alt=media&#x26;token=ca8d2f56-889a-4da8-8106-da88d22e69d2" alt="" width="188"><figcaption></figcaption></figure>
- ```
pip install --upgrade unsloth unsloth_zoo
```
- ```
pip install --force-reinstall --no-cache-dir --no-deps unsloth==2025.1.5
```
- ```
pip uninstall unsloth unsloth_zoo -y && pip install --no-deps git+https://github.com/unslothai/unsloth_zoo.git && pip install --no-deps git+https://github.com/unslothai/unsloth.git
```
- ```
pip install --upgrade --force-reinstall --no-cache-dir --no-deps git+https://github.com/unslothai/unsloth.git
pip install --upgrade --force-reinstall --no-cache-dir --no-deps git+https://github.com/unslothai/unsloth-zoo.git
```
- ```
pip install --upgrade pip
pip install "unsloth[cu121-torch240] @ git+https://github.com/unslothai/unsloth.git"
```
- ```
pip install --upgrade pip
pip install "unsloth[cu124-torch250] @ git+https://github.com/unslothai/unsloth.git"
```
- ```
pip install "unsloth[cu121-ampere-torch240] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu118-ampere-torch240] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu121-torch240] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu118-torch240] @ git+https://github.com/unslothai/unsloth.git"

pip install "unsloth[cu121-torch230] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu121-ampere-torch230] @ git+https://github.com/unslothai/unsloth.git"

pip install "unsloth[cu121-torch250] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu124-ampere-torch250] @ git+https://github.com/unslothai/unsloth.git"
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
