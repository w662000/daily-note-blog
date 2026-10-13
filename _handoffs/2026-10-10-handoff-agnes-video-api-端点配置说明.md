---
layout: default
title: 交接文档 · Agnes Video API 端点配置说明
date: 2026-10-13 23:30:00 +0800
---

# Agnes Video API 端点配置说明

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\backup\20261010_173538\.hermes\skills\creative\agnes-video-generator\references\api-endpoint-configuration.md

## 问题背景

2026-08-04 会话中发现的API端点配置问题。

## 现象

- 第一个视频生成成功（测试视频5秒）
- 后续所有视频生成失败，返回HTTP 404
- 错误信息：`litellm.NotFoundError: NotFoundError: OpenAIException - {"detail":"Not Found"}`

## 根本原因

Agnes Video Generator项目的默认配置使用了错误的API端点：

```python
# 错误的配置（项目默认）
AGNES_DOMAIN_MAP = {
    "com": "https://apihub.agnes-ai.com",  # ❌ 错误
    "cn": "https://apihub.agnes-ai.cn",    # ❌ 错误
}
```

正确的API端点应该是（与Hermes的Agnes provider配置一致）：

```python
# 正确的配置
AGNES_DOMAIN_MAP = {
    "com": "https://api.agnes-ai.com",   # ✅ 正确
    "cn": "https://api.agnes-ai.cn",     # ✅ 正确
}
```

## 解决方案

### 方案1：修改源代码（推荐）

编辑 `core/config.py` 文件第482-484行：

```bash
# Windows (PowerShell)
(Get-Content D:\workspace\agnes-video-generator\core\config.py).replace('apihub.agnes-ai', 'api.agnes-ai') | Set-Content D:\workspace\agnes-video-generator\core\config.py

# 或使用sed (Git Bash)
sed -i 's/apihub\.agnes-ai/agnes-ai/g' core/config.py
```

### 方案2：通过环境变量覆盖（临时）

```bash
# 设置环境变量（在server.py启动前）
export AGNES_BASE_URL="https://api.agnes-ai.cn/v1"
```

注意：需要修改 `core/config.py` 的 `get_agnes_base_url()` 函数以支持环境变量覆盖。

### 方案3：使用网页版

如果无法修改代码，可以直接使用网页版：
- https://video.lichuanyang.top
- 或 https://video.lichuanyang.top/studio

## 验证方法

修改配置后，验证API端点是否正确：

```bash
# 测试Chat API（应该成功）
curl -s https://api.agnes-ai.cn/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"agnes-2.5-flash","messages":[{"role":"user","content":"hi"}]}'

# 测试Video API（应该成功）
curl -s -X POST https://api.agnes-ai.cn/v1/videos \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"agnes-video-v2.0","prompt":"test"}'
```

## 相关资源

- Hermes配置：`~/.hermes/config.yaml` 中 `providers.agnes` 部分
- Agnes平台：https://platform.agnes-ai.com
- GitHub Issue：如有问题可在此仓库提交issue
