---
layout: default
title: 交接文档 · _Source Name_
date: 2026-10-13 23:30:00 +0800
---

# <Source Name>

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\research\osint-investigation\templates\source-template.md

## 1. Summary

What this data source is, who publishes it, why it matters for investigations.

## 2. Access Methods

- API endpoint(s)
- Bulk download URLs
- Auth requirements (none / API key / OAuth)
- Rate limits

## 3. Data Schema

Key fields, record types, table relationships. List the columns the fetch
script emits.

## 4. Coverage

- Jurisdiction
- Time range
- Update frequency
- Data volume (rows / GB)

## 5. Cross-Reference Potential

Which other sources can be joined and on what keys. Be explicit:

- `<source>` ↔ `<column>` (join key: <normalized entity name / EIN / CIK / etc.>)

## 6. Data Quality

Known issues — formatting inconsistencies, missing fields, duplicates,
historical gaps, redaction.

## 7. Acquisition Script

Path: `scripts/fetch_<source>.py`

Example:

```bash
python3 SKILL_DIR/scripts/fetch_<source>.py --<filter> <value> --out data/<source>.csv
```

Output CSV columns: `<col1>, <col2>, ...`

## 8. Legal & Licensing

- Public records law / FOIA basis
- Terms of use / acceptable use
- Attribution requirements (if any)

## 9. References

- Official docs: <url>
- Data dictionary: <url>
- Related coverage / journalism: <url>
