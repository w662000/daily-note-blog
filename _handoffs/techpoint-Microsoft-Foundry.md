---
layout: default
title: 技术点 · Microsoft Foundry
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Microsoft Foundry

> 来源：261010_Microsoft Foundry_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- **Anthropic-style** — `POST /v1/messages` on endpoints like `https://<resource>.services.ai.azure.com/anthropic`. Used when Microsoft Foundry serves Claude models via the Anthropic Messages API format.
- **Either** an API key (from the Azure Portal under "Keys and Endpoint") **or** the **Azure AI User** RBAC role on the Foundry resource if you plan to use Microsoft Entra ID (the keyless path Microsoft recommends). Some tenants may show the role as **Foundry User** during Microsoft's rename rollout.
- ```
hermes model
# → Select "Azure Foundry"
# → Enter your endpoint URL
# → Choose Authentication:
#     1. API key
#     2. Microsoft Entra ID  (managed identity / workload identity / az login)
# → (Entra) Hermes probes DefaultAzureCredential; on success it never asks for a key
# → (API key) Enter your API key
# Hermes probes the endpoint and auto-detects transport + models
# → Pick a model from the list (or type a deployment name manually)
```
- 4. **Fall back to manual entry** — private/gated endpoints that reject every probe still work; you pick the API mode and type a deployment name by hand.
- Microsoft recommends [keyless authentication with Microsoft Entra ID](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/configure-entra-id) for production Foundry workloads. Hermes supports Entra ID for **both** API surfaces:
- **OpenAI-style** (`api_mode: chat_completions` / `codex_responses`) — GPT-4/5, Llama, Mistral, DeepSeek, etc.
- **Anthropic-style** (`api_mode: anthropic_messages`) — Claude models on Microsoft Foundry.
- OpenAI-style uses the OpenAI Python SDK's native callable `api_key=` contract — the SDK mints a fresh JWT per request automatically.
- Anthropic-style uses an `httpx.Client` with a request event hook installed by `agent.azure_identity_adapter.build_bearer_http_client`, because the Anthropic SDK does not accept callable `auth_token` natively. The hook rewrites `Authorization: Bearer <fresh-jwt>` per outbound request. Same Microsoft RBAC, same Foundry scope — the SDK contract is the only difference.
- No long-lived API keys to rotate or revoke.
- Access and audit logs are segmented by assignee instead of all callers sharing one static key.
- ```
az role assignment create \
  --assignee <principal-or-agent-identity-client-id> \
  --role "Azure AI User" \
  --scope <foundry-resource-id>
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
