---
layout: default
title: 交接文档 · Malicious Package Investigation Report
date: 2026-10-13 23:30:00 +0800
---

# Malicious Package Investigation Report

- **日期**：2026-10-10
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-10-hermes-upgrade\src-0215\optional-skills\security\oss-forensics\templates\malicious-package-report.md

---

## 📦 Package Metadata
- **Package Name**: 
- **Registry**: [NPM / PyPI / RubyGems / etc.]
- **Affected Versions**: 
- **Malicious Version(s)**: 
- **Downloads at Time of Detection**: 
- **Package URL**: 

---

## 🚩 Indicators of Compromise (IOCs)
- **Malicious URL(s)**: 
- **Exfiltrated Data Types**: [Environment variables, ~/.ssh/id_rsa, /etc/shadow, etc.]
- **Exfiltration Method**: [DNS tunneling, HTTP POST to C2, etc.]
- **C2 IP/Domain**: 

---

## 🛠️ Analysis Summary
- **Primary Mechanism**: [Typosquatting / Dependency Confusion / Maintainer Takeover]
- **Behavior Description**: 
  - [Example: Installs a postinstall script that exfiltrates environment variables.]
  - [Example: Patches `setup.py` to download a secondary payload.]

---

## 🔍 Evidence Registry
| Evidence ID | Type | Source | Description |
|-------------|------|--------|-------------|
| EV-XXXX     | ioc  | NPM    | Package install script snapshot |
| EV-YYYY     | web  | Wayback| Historical version comparison |

---

## 🛡️ Recommended Mitigations
1. [ ] Unpublish/Report the package to the registry.
2. [ ] Audit `package-lock.json` or `requirements.txt` across all projects.
3. [ ] Rotate secrets exfiltrated via environment variables.
4. [ ] Pin specific hashes (SHASUM) for mission-critical dependencies.
