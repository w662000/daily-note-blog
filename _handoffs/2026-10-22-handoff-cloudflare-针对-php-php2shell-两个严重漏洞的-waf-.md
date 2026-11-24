---
layout: default
title: 交接文档 · Cloudflare 针对 PHP「php2shell」两个严重漏洞的 WAF 防护 · 调研稿（Q5）
date: 2026-10-22 12:00:00 +0800
---

# Cloudflare 针对 PHP「php2shell」两个严重漏洞的 WAF 防护 · 调研稿（Q5）

- **日期**：2026-10-22
- **状态**：✅ 已完结（scan 自动收集）
- **来源**：2026-10-22-22-03-16\Q5_调研稿_20261023.md

> 检索方式：通过 `mcp__agent-teams__agent_teams_web_search` 联网检索，检索日期 2026-10-23。
> 本题事件发生在 2026-10-21 前后，超出模型训练数据，**以下全部结论均来自联网检索结果，非凭记忆作答**。
> 来源标注：**官方一手** = Cloudflare 官方博客 / Cloudflare 官方 Changelog / 厂商安全公告；**第三方/媒体** = 安全厂商博客、新闻转述、社区帖子（已注明）。
> CVE 编号原则：**宁可写「未找到」也不猜**。本文两个编号均能在多条独立检索结果中逐字复现，且其中一条为 Cloudflare 官方博客原文。

---

## 一、这两个漏洞的 CVE 编号

| 项目 | 内容 |
|------|------|
| 漏洞代号 | **php2shell**（PHP2Shell） |
| CVE 编号 1 | **CVE-2026-109618** |
| CVE 编号 2 | **CVE-2026-109619** |
| 影响范围 | 所有运行 **PHP 5.4 及以上**版本的 Web 服务器（官方博客口径）；CERT-EU 表述为 PHP 5 及以后 |
| 严重级别 | **CVSS v4.0 = 9.2（Critical）**，两个漏洞均为 9.2 |
| 公开披露日 | **2026-10-21**（PHP 紧急安全版本同日发布） |

### 官方一手证据（Cloudflare 博客原文）

> "Today, **Calif.io, Wiz, OpenAI and Quarkslab** disclosed two vulnerabilities in PHP, tracked as **CVE-2026-109618** and **CVE-2026-109619** and known as **php2shell**. The vulnerabilities affect all web servers running PHP 5.4 or later and they may allow an attacker to cause denial of service, remote code execution, and …"

- https://blog.cloudflare.com/php-vulnerabilities-waf-protection

### 独立交叉印证（同一对编号，多个互不相关的来源）

- Wikipedia「PHP2Shell」条目：*"a pair of high-impact vulnerabilities (**CVE-2026-109618** and **CVE-2026-109619**) in PHP versions 5.4 – 8.5"* —— https://en.m.wikipedia.org/wiki/PHP2Shell
- 荷兰国家网络安全中心 NCSC-NL 运营信息仓库：*"php2shell vulnerabilities (**CVE-2026-109618**, **CVE-2026-109619**)"* —— https://github.com/NCSC-NL/php2shell
- Sansec 研究文章标题即含两个编号 —— https://sansec.io/research/php2shell
- CERT-EU 安全公告 2026-018 —— https://cert.europa.eu/publications/security-advisories/2026-018
- CrowdStrike：*"Tracked as **CVE-2026-109618** and **CVE-2026-109619**, both vulnerabilities carry a CVSS 4.0 score of 9.2 (Critical)"* —— https://www.crowdstrike.com/en-us/blog/crowdstrike-protects-customers-from-php-rce-zero-days
- Palo Alto Networks 产品安全公告（单条 CVE 页面）—— https://security.paloaltonetworks.com/CVE-2026-109618
- AWS 安全博客标题含两个编号 —— https://aws.amazon.com/blogs/security/using-aws-waf-to-apply-mitigations-for-php2shell-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619
- 中文转述（网易，2026-10-21）：*"这两项漏洞的编号分别为 **CVE-2026-109618** 和 **CVE-2026-109619**"* —— https://www.163.com/dy/article/L9Q4RQ080511BLFD.html

> **编号逐字核对**：`CVE-2026-109618` / `CVE-2026-109619` 两串在 8 条以上独立结果中完全一致，**未出现任何来源给出不同编号**，可判定逐字准确、无串号。

### 两个编号各自对应什么（技术细节，供参考）

- **CVE-2026-109618**：处理 out-of-memory 错误时通过 `longjmp()` 跳转，导致请求内存未初始化，攻击者可用 OOM 触发稳定实现 RCE —— https://security.paloaltonetworks.com/CVE-2026-109618
- **CVE-2026-109619**（php2shell 得名来源）：针对 PHP 的 `session.upload_progress` 回调，在应用代码执行前即触发；利用体仅约 450 字节，因此**基于请求大小的 WAF 规则无效** —— https://www.abstract.security/blog/php2shell-critical-php-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619
- 两者共性：CWE-824（Access of Uninitialized Pointer）、内存破坏类、可未授权触发 —— CrowdStrike（同上）、腾讯云安全通告 https://cloud.tencent.com/announce/detail/2525

---

## 二、官方说可能导致什么后果（至少两项）

Cloudflare 官方博客的表述是**三项**后果：

> "they may allow an attacker to cause **denial of service**, **remote code execution**, and **data exposure**."

1. **拒绝服务（Denial of Service）** —— 可使目标 Web 服务器不可用
2. **远程代码执行（Remote Code Execution）** —— 攻击者可在服务器上执行任意代码
3. **数据暴露 / 敏感数据泄露（Data exposure）** —— 可能造成数据外泄

证据：
- 官方原文前半段（"denial of service, remote code execution, and …"）：https://blog.cloudflare.com/php-vulnerabilities-waf-protection
- 第三项 "data exposure" 的完整转述：DataFLOQ —— *"Cloudflare says the flaws may allow an attacker to cause denial of service, remote code execution and data exposure."* —— https://datafloq.com/cloudflare-deployed-php2shell-protection-hours-before-disclosure-heres-what-the-head-start-doesnt-cover
- 中文转述同口径（网易）：*"可能导致拒绝服务、远程代码执行及敏感数据泄露"* —— https://www.163.com/dy/article/L9Q4RQ080511BLFD.html

补充后果（非 Cloudflare 官方原话，来自安全厂商，标注为第三方）：
- **未授权**即可触发：*"allow an unauthenticated network attacker to execute arbitrary code on the web-server process"* —— https://www.onesource.net/php2shell-critical-php-flaws-put-millions-of-websites-at-risk
- 可导致 **shell 访问 / 服务器完全失陷**：NCSC-NL *"may lead to unauthenticated remote code execution and shell access"* —— https://github.com/NCSC-NL/php2shell
- 腾讯云通告：*"未经身份验证的远程攻击者利用该漏洞可在服务器上以 Web 工作进程账户身份执行任意代码"* —— https://cloud.tencent.com/announce/detail/2525

---

## 三、Cloudflare 官方对「WAF 规则 vs 官方补丁」的表态

### 结论：**不能替代。WAF 只是纵深防御的一层，必须打 PHP 官方补丁。**

官方博客中有三句直接表态（原文引用）：

1. > "**Customers should patch their PHP repos even with WAF protections providing an additional layer of defense-in-depth mitigation.**"
2. > "**Keep Cloudflare WAF protections enabled while patching.**"
3. > "Restricting unnecessary uploads and limiting upload sizes can also reduce exposure, but **these measures do not replace the PHP fix**."

—— 全部出自 https://blog.cloudflare.com/php-vulnerabilities-waf-protection

即官方的逻辑是：**WAF 规则 = 争取时间的缓解措施（mitigation）；PHP 官方补丁 = 唯一彻底的修复（the PHP fix）**；两者是叠加关系，不是替代关系。

### 第三方对官方立场的复述（与官方原文一致）

- ITLDC：*"Cloudflare explicitly describes this as **defense in depth, not a replacement for patching**."* —— https://itldc.com/en/blog/php2shell-critical-php-rce-update
- 网易（中文）：*"Cloudflare反复强调，WAF防护只能作为纵深防御的一部分，**不能替代PHP官方补丁**"* —— https://www.163.com/dy/article/L9Q4RQ080511BLFD.html
- 横向对照（非 Cloudflare，但结论一致）：AWS 安全博客 *"AWS WAF is a defense-in-depth control in this situation, not a replacement for the PHP upgrade. … updating to a patched release is the only complete mitigation."* —— https://aws.amazon.com/blogs/security/using-aws-waf-to-apply-mitigations-for-php2shell-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619

### 一个重要的技术限制（解释了为什么 WAF 不能替代补丁）

- 其中一个漏洞（CVE-2026-109619）的利用请求体仅约 450 字节，**基于大小的 WAF 规则帮不上忙** —— https://www.abstract.security/blog/php2shell-critical-php-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619
- AWS 亦指出：*"One of the two vulnerabilities is largely outside the reach of any web application firewall"* —— 同上 AWS 链接

---

## 四、Cloudflare WAF 部署时间线（附带事实，便于理解「提前部署」）

| 时间 | 事件 | 来源性质 |
|------|------|----------|
| 2026-10-14 | Cloudflare 发布 **Emergency WAF Release**（早期缓解规则） | 官方 Changelog：https://developers.cloudflare.com/changelog/post/2026-10-14-emergency-waf-release |
| 2026-10-21 | 发布 **Emergency - Cloudflare Free Ruleset**（新增检测规则，动作为 Block） | 官方 Changelog：https://developers.cloudflare.com/changelog/post/2026-10-21-emergency-waf-release-free |
| 2026-10-21 | PHP 官方发布紧急安全版本 / 公开披露两个 CVE | 官方博客 + Recorded Future：https://www.recordedfuture.com/blog/php2shell-vulnerability-exploitation |
| 时间差 | 官方称 WAF 规则「比公开披露**提前约 9 小时**」部署 | 官方博客（同上） |
| 时间差（第三方口径） | 「2026-10-21 03:02 UTC 开始拦截，比 PHP GitHub 公告 13:34 UTC 提前 **10 小时 32 分**」 | 第三方 Nanosek：https://www.nanosek.com/blog/php2shell-cloudflare-waf-cve-2026-109618-109619 |

> 两个「提前量」数字不一致（9 小时 vs 10 小时 32 分），因为起算点不同（规则上线 vs 首次拦截、披露口径不同）。**以官方 9 小时为准，第三方的 10h32m 作为参考**。

### 规则投放方式（网易转述官方说明）

- **免费套餐**：无需手动开启，规则已自动部署在 Cloudflare 托管的 **Free Ruleset**
- **付费套餐**：通过 **Managed Ruleset** 提供，Pro / Business / Enterprise 用户应确认规则集已启用且处于 **Block（拦截）** 而非仅 Log（记录）模式
- 另在 **Managed Response Firewall** 默认规则中部署了高置信度攻击特征的默认拦截规则
—— https://www.163.com/dy/article/L9Q4RQ080511BLFD.html （第三方转述，官方 Changelog 可交叉验证规则动作）

---

## 五、来源清单（按性质分类）

**官方一手**
1. Cloudflare Blog《Cloudflare deploys protections against php2shell vulnerability》 — https://blog.cloudflare.com/php-vulnerabilities-waf-protection
2. Cloudflare Changelog《WAF Release - 2026-10-14 - Emergency》 — https://developers.cloudflare.com/changelog/post/2026-10-14-emergency-waf-release
3. Cloudflare Changelog《WAF Release - 2026-10-21 - Emergency - Cloudflare Free Ruleset》 — https://developers.cloudflare.com/changelog/post/2026-10-21-emergency-waf-release-free

**官方/权威机构（非 Cloudflare）**
4. CERT-EU 安全公告 2026-018 — https://cert.europa.eu/publications/security-advisories/2026-018
5. NCSC-NL 运营信息仓库 — https://github.com/NCSC-NL/php2shell
6. Palo Alto Networks 产品安全公告 — https://security.paloaltonetworks.com/CVE-2026-109618

**第三方安全厂商 / 媒体（转述，已标注）**
7. CrowdStrike — https://www.crowdstrike.com/en-us/blog/crowdstrike-protects-customers-from-php-rce-zero-days
8. Sansec — https://sansec.io/research/php2shell
9. AWS Security Blog — https://aws.amazon.com/blogs/security/using-aws-waf-to-apply-mitigations-for-php2shell-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619
10. Abstract Security — https://www.abstract.security/blog/php2shell-critical-php-rce-vulnerabilities-cve-2026-109618-and-cve-2026-109619
11. DataFLOQ — https://datafloq.com/cloudflare-deployed-php2shell-protection-hours-before-disclosure-heres-what-the-head-start-doesnt-cover
12. 网易（中文，2026-10-21） — https://www.163.com/dy/article/L9Q4RQ080511BLFD.html
13. 腾讯云安全通告 — https://cloud.tencent.com/announce/detail/2525
14. Wikipedia「PHP2Shell」 — https://en.m.wikipedia.org/wiki/PHP2Shell
15. Nanosek（Cloudflare WAF 实操指南） — https://www.nanosek.com/blog/php2shell-cloudflare-waf-cve-2026-109618-109619

---

## 六、未核实 / 存在冲突之处（如实标注）

| 项目 | 状态 | 说明 |
|------|------|------|
| 官方博客的完整后果句第三项 | **部分未逐字取到** | 检索片段在 "denial of service, remote code execution, and …" 处截断；第三项 "data exposure" 由 DataFLOQ 与网易转述补全，**属第三方转述，非我直接读到的官方原文** |
| WAF 提前量 | **官方与第三方不一致** | 官方「约 9 小时」；Nanosek「10 小时 32 分」。以官方为准 |
| PHP 公告发布日 | **存在冲突** | 多数来源（官方博客、Recorded Future、Sansec）为 **10-21**；ChainCatcher 转述称「10 月 20 日发布安全公告，尚未发布修复补丁」，与「10-21 已有修复版本」矛盾 —— 该条**不采信** |
| 具体修复版本号（如 8.4.x / 8.5.x） | **未核实** | 本次检索未取到 PHP 官方公告的逐字版本号，故不写具体版本，避免编造 |
| CVE 编号 | **已证实** | 8 条以上独立来源逐字一致，含 Cloudflare 官方博客原文 |

---

## 七、三问速答

1. **两个 CVE**：**CVE-2026-109618** 和 **CVE-2026-109619**（合称 php2shell，影响 PHP 5.4+，CVSS v4.0 = 9.2）。
2. **官方说的后果**（至少两项）：**拒绝服务（DoS）**、**远程代码执行（RCE）**、**数据暴露/敏感数据泄露（data exposure）**；第三方补充可导致未授权 shell 访问、服务器完全失陷。
3. **WAF 与补丁的关系**：官方明确 **WAF 只是 defense-in-depth 的附加一层缓解，不能替代 PHP 官方补丁**；原文 "Customers should patch their PHP repos even with WAF protections…"、"these measures do not replace the PHP fix"、"Keep Cloudflare WAF protections enabled while patching"。即：**先打补丁，WAF 在此期间保持开启**，不能只靠 WAF。
