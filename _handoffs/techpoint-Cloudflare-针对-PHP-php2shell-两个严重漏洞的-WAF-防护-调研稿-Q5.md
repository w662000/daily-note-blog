---
layout: default
title: 技术点 · Cloudflare 针对 PHP「php2shell」两个严重漏洞的 WAF 防护 · 调研稿（Q5）
date: 2026-10-22 23:30:00 +0800
---

# 技术点 · Cloudflare 针对 PHP「php2shell」两个严重漏洞的 WAF 防护 · 调研稿（Q5）

> 来源：261022_Cloudflare 针对 PHP「php2shell」两个严重漏洞的 WAF 防护 · 调研稿（Q5）_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- | 影响范围 | 所有运行 **PHP 5.4 及以上**版本的 Web 服务器（官方博客口径）；CERT-EU 表述为 PHP 5 及以后 |
- 1. **拒绝服务（Denial of Service）** —— 可使目标 Web 服务器不可用
- 2. **远程代码执行（Remote Code Execution）** —— 攻击者可在服务器上执行任意代码
- 中文转述同口径（网易）：*"可能导致拒绝服务、远程代码执行及敏感数据泄露"* —— https://www.163.com/dy/article/L9Q4RQ080511BLFD.html
- 可导致 **shell 访问 / 服务器完全失陷**：NCSC-NL *"may lead to unauthenticated remote code execution and shell access"* —— https://github.com/NCSC-NL/php2shell
- 腾讯云通告：*"未经身份验证的远程攻击者利用该漏洞可在服务器上以 Web 工作进程账户身份执行任意代码"* —— https://cloud.tencent.com/announce/detail/2525
- 即官方的逻辑是：**WAF 规则 = 争取时间的缓解措施（mitigation）；PHP 官方补丁 = 唯一彻底的修复（the PHP fix）**；两者是叠加关系，不是替代关系。
- | 时间差 | 官方称 WAF 规则「比公开披露**提前约 9 小时**」部署 | 官方博客（同上） |
- **免费套餐**：无需手动开启，规则已自动部署在 Cloudflare 托管的 **Free Ruleset**
- 另在 **Managed Response Firewall** 默认规则中部署了高置信度攻击特征的默认拦截规则
- | PHP 公告发布日 | **存在冲突** | 多数来源（官方博客、Recorded Future、Sansec）为 **10-21**；ChainCatcher 转述称「10 月 20 日发布安全公告，尚未发布修复补丁」，与「10-21 已有修复版本」矛盾 —— 该条**不采信** |
- | 具体修复版本号（如 8.4.x / 8.5.x） | **未核实** | 本次检索未取到 PHP 官方公告的逐字版本号，故不写具体版本，避免编造 |

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）

## 6、部署状态
| 时间 | 事件 | 来源性质 |
|------|------|----------|
| 2026-10-14 | Cloudflare 发布 **Emergency WAF Release**（早期缓解规则） | 官方 Changelog：https://developers.cloudflare.com/changelog/post/2026-10-14-emergency-waf-release |
| 2026-10-21 | 发布 **Emergency - Cloudflare Free Ruleset**（新增检测规则，动作为 Block） | 官方 Changelog：https://developers.cloudflare.com/changelog/post/2026-10-21-emergency-waf-release-free |
| 2026-10-21 | PHP 官方发布紧急安全版本 / 公开披露两个 CVE | 官方博客 + Recorded Future：https://www.recordedfuture.com/blog/php2shell-vulnerability-exploitation |
| 时间差 | 官方称 WAF 规则「比公开披露**提前约 9 小时**」部署 | 官方博客（同上） |
| 时间差（第三方口径） | 「2026-10-21 03:02 UTC 开始拦截，比 PHP GitHub 公告 13:34 UTC 提前 **10 小时 32 分**」 | 第三方 Nanosek：https://www.nanosek.com/blog/php2shell-cloudflare-waf-cve-2026-109618-109619 |

> 两个「提前量」数字不一致（9 小时 vs 10 小时 32 分），因为起算点不同（规则上线 vs 首次拦截、披露口径不同）。**以官方 9 小时为准，第三方的 10h32m 作为参考**。
