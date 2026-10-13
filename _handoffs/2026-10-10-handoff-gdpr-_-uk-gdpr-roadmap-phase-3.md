---
layout: default
title: 交接文档 · GDPR _ UK-GDPR (roadmap - Phase 3)
date: 2026-10-13 23:30:00 +0800
---

# GDPR / UK-GDPR (roadmap - Phase 3)

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\security\unbroker\references\legal\gdpr.md

For EU/UK subjects. Not part of the P0 US-first scope; templates and routing land in Phase 3.

## Rights invoked

- **Erasure** ("right to be forgotten") - Article 17.
- **Object** to processing - Article 21.

## Request content

Render with `legal.render_request("gdpr", broker, fields)` ->
`templates/emails/gdpr-erasure.txt`. Address the controller's privacy/DPO contact. Include the data
subject's name, the contact email, and the listing URL(s); cite Article 17.

## Notes

- Controllers must respond within one month (Article 12(3)).
- EU-specific brokers and portals (e.g. Acxiom's EU consumer portals) are added in Phase 3 with
  `jurisdictions: ["EU"]` records and residency-aware routing.
