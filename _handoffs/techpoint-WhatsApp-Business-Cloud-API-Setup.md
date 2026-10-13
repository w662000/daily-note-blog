---
layout: default
title: 技术点 · WhatsApp Business Cloud API Setup
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · WhatsApp Business Cloud API Setup

> 来源：261010_WhatsApp Business Cloud API Setup_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- title: "WhatsApp Business (Cloud API)"
- description: "Set up Hermes Agent as a WhatsApp bot via Meta's official Business Cloud API"
- Hermes can connect to WhatsApp through Meta's **official** WhatsApp Business Cloud API. This is the production-grade path: no Node.js bridge subprocess, no QR codes, no account-ban risk.
- **Cloud API (this guide)** — running a real business bot, want stability, fine with the Meta verification + template paperwork
- ```
hermes whatsapp-cloud
```
- 4. After creation you'll land on **Customize use case → Connect on WhatsApp → Quickstart**.  Click **Start using the API** → you're now on the **API Setup** page.
- 5. Make sure a WhatsApp Business Account (WABA) is linked.  If you created a new portfolio in step 3, one was auto-created.  Verify in the API Setup page.
- | **Phone Number ID** | App Dashboard → WhatsApp → API Setup → below the "From" dropdown | Numeric, 15-17 digits | **NOT** the phone number itself. The #1 setup mistake is pasting the actual phone number here. |
- | **Access Token** | App Dashboard → WhatsApp → API Setup → "Generate access token" | Starts with `EAA`, 100+ chars | Temp tokens last 24h — see "Permanent token" below for production. |
- | **WABA ID** (optional) | App Dashboard → WhatsApp → API Setup → near the top | Numeric, 15+ digits | Not required for messaging, useful for analytics. |
- Temporary access tokens expire after **24 hours**, which means a token generated today stops working tomorrow.  For production deployments use a **System User permanent token**:
- 4. **Generate token** with these permissions:

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
