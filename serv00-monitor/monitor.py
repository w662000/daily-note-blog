#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serv00 免费注册开放监控（邮件通道，支持全套自动化）

纯标准库，无第三方依赖，可在 GitHub Actions / 本机任意环境运行。

功能：
  1. 每 10 分钟探测 Serv00 注册页是否开放
  2. 开放时：
     A. 【自动注册模式 AUTO_REGISTER=on】用配置好的邮箱 + 用户名 + 密码
        自动提交 Serv00 注册表单 → 经 IMAP 读取验证邮件 → 提取激活链接
        → 完成账户激活 → 把账户信息发邮件通知你
     B. 【降级通知】若自动注册关闭或失败，仍发邮件提醒你手动注册

配置（GitHub Secrets / 本机环境变量）：
  MAIL_USER       注册 Serv00 用的邮箱（同时作为收通知 + IMAP/SMTP 登录账号）
  MAIL_AUTH       该邮箱的 IMAP/SMTP 授权码（不是登录密码）
  MAIL_SMTP_HOST / MAIL_SMTP_PORT / MAIL_IMAP_HOST / MAIL_IMAP_PORT
                  【通常不用填】按 MAIL_USER 域名自动识别（qq/126/163/gmail/outlook
                  已内置）；仅当用其它邮箱时才需手动指定。
  SERV00_USER     Serv00 用户名（自定义，字母开头，如 w662000）
  SERV00_PASS     Serv00 密码（自定义，强密码）
  AUTO_REGISTER   on / off（默认 on；设 off 则只发通知不自动注册）
  NOTIFY_TO       通知收件人（默认 = MAIL_USER，可填另一个邮箱）
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import sys
import time
import re
import ssl
import imaplib
import smtplib
import email
import quopri
import base64

# ------------------------------------------------------------------ 配置
SERV00_URL = "https://www.serv00.com/register-account/"
CHECK_TIMEOUT = 20

# 页面出现这些关键词即判定“未开放”（名额满 / 暂不可注册）
BLOCK_KEYWORDS = [
    "the server user limit has been reached",
    "registering a new account is currently not possible",
    "500 internal server error",
    "internal server error",
]

# 邮件配置（从环境变量读）
MAIL_USER = os.environ.get("MAIL_USER", "").strip()
MAIL_AUTH = os.environ.get("MAIL_AUTH", "").strip()
SERV00_USER = os.environ.get("SERV00_USER", "").strip()
SERV00_PASS = os.environ.get("SERV00_PASS", "").strip()
AUTO_REGISTER = os.environ.get("AUTO_REGISTER", "on").strip().lower() == "on"
NOTIFY_TO = os.environ.get("NOTIFY_TO", MAIL_USER).strip()

# 常见邮箱服务商的 IMAP/SMTP 配置（按邮箱域名自动识别，无需手动填 host/port）
PROVIDER_MAP = {
    "qq.com":      ("smtp.qq.com", 465, "imap.qq.com", 993),
    "foxmail.com": ("smtp.qq.com", 465, "imap.qq.com", 993),
    "126.com":     ("smtp.126.com", 465, "imap.126.com", 993),
    "163.com":     ("smtp.163.com", 465, "imap.163.com", 993),
    "gmail.com":   ("smtp.gmail.com", 465, "imap.gmail.com", 993),
    "outlook.com": ("smtp.office365.com", 587, "imap.outlook.com", 993),
    "hotmail.com": ("smtp.office365.com", 587, "imap.outlook.com", 993),
}

def _mail_servers():
    """显式配置了 host 就用显式；否则按 MAIL_USER 域名自动推断。"""
    sh = os.environ.get("MAIL_SMTP_HOST", "").strip()
    sp = int(os.environ.get("MAIL_SMTP_PORT", "465"))
    ih = os.environ.get("MAIL_IMAP_HOST", "").strip()
    ip = int(os.environ.get("MAIL_IMAP_PORT", "993"))
    if sh and ih:
        return sh, sp, ih, ip
    domain = MAIL_USER.split("@")[-1].lower() if "@" in MAIL_USER else ""
    if domain in PROVIDER_MAP:
        return PROVIDER_MAP[domain]
    return sh or "smtp.qq.com", sp, ih or "imap.qq.com", ip

SMTP_HOST, SMTP_PORT, IMAP_HOST, IMAP_PORT = _mail_servers()

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


# ------------------------------------------------------------------ HTTP
def fetch(url, data=None, referer=None, method="GET"):
    headers = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if referer:
        headers["Referer"] = referer
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=CHECK_TIMEOUT) as r:
            return r.read().decode("utf-8", "ignore"), r.status, dict(r.getheaders())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore") if e.fp else ""
        return body, e.code, {}
    except Exception as e:
        return "ERR:%s" % e, 0, {}


def is_open(html, status):
    if status != 200:
        return False
    low = html.lower()
    if any(kw in low for kw in BLOCK_KEYWORDS):
        return False
    # 正常注册页应有表单字段
    return ("name=" in low) and ("password" in low or "e-mail" in low or "email" in low)


# ------------------------------------------------------------------ 解析表单
def extract_form(html):
    """返回 (action_url, {field_name: value})，收集页面所有 input。"""
    m = re.search(r'<form[^>]*action=["\']([^"\']*)["\']', html, re.I)
    action = m.group(1) if m else ""
    if action and not action.startswith("http"):
        action = "https://www.serv00.com" + action
    if not action:
        action = SERV00_URL

    inputs = {}
    for tag in re.finditer(r'<input[^>]*>', html, re.I):
        t = tag.group(0)
        nm = re.search(r'name=["\']([^"\']*)["\']', t, re.I)
        if not nm:
            continue
        val = re.search(r'value=["\']([^"\']*)["\']', t, re.I)
        inputs[nm.group(1)] = val.group(1) if val else ""
    return action, inputs


def fill_payload(inputs):
    """把已知字段替换成我们配置的值，其他 hidden 字段保持原样。"""
    out = {}
    for k, v in inputs.items():
        kl = k.lower()
        if "user" in kl and "name" in kl:
            out[k] = SERV00_USER
        elif "email" in kl or "e-mail" in kl:
            out[k] = MAIL_USER
        elif "pass" in kl:
            out[k] = SERV00_PASS
        elif "tos" in kl or "agree" in kl or "terms" in kl or "accept" in kl:
            out[k] = "1" if v in ("", "0", "off", "false") else v
        else:
            out[k] = v
    # 保底：若页面没出现标准字段，强制补上
    if not any("user" in k.lower() and "name" in k.lower() for k in out):
        out["username"] = SERV00_USER
    if not any("email" in k.lower() or "e-mail" in k.lower() for k in out):
        out["email"] = MAIL_USER
    if not any("pass" in k.lower() for k in out):
        out["password"] = SERV00_PASS
        out["password2"] = SERV00_PASS
    return out


# ------------------------------------------------------------------ IMAP 读验证码
def _decode_part(part):
    cte = (part.get("Content-Transfer-Encoding") or "").lower()
    payload = part.get_payload(decode=True)
    if payload is None:
        return ""
    if cte == "base64":
        try:
            return payload.decode("utf-8", "ignore")
        except Exception:
            return payload.decode("latin-1", "ignore")
    if cte == "quoted-printable":
        return quopri.decodestring(payload).decode("utf-8", "ignore")
    return payload.decode("utf-8", "ignore")


def get_mail_body(msg):
    if msg.is_multipart():
        texts = []
        for p in msg.walk():
            if p.get_content_type() == "text/plain":
                texts.append(_decode_part(p))
            elif p.get_content_type() == "text/html":
                texts.append(_decode_part(p))
        return "\n".join(texts)
    return _decode_part(msg)


def find_activation_link():
    """登录 IMAP，找最近来自 serv00 的邮件，提取激活链接。最多等 5 分钟。"""
    ctx = ssl.create_default_context()
    for attempt in range(10):  # 每 30s 轮询一次，共 5 分钟
        try:
            conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
            conn.login(MAIL_USER, MAIL_AUTH)
            conn.select("INBOX")
            since = time.strftime("%d-%b-%Y", time.localtime(time.time() - 600))
            typ, data = conn.search(None, "SINCE", since)
            if typ != "OK" or not data[0]:
                conn.logout()
                time.sleep(30)
                continue
            for num in data[0].split()[::-1][:20]:
                typ, raw = conn.fetch(num, "(RFC822)")
                if typ != "OK":
                    continue
                msg = email.message_from_bytes(raw[0][1])
                frm = str(msg.get("From", "")).lower()
                if "serv00" not in frm and "serv00" not in str(msg.get("Subject", "")).lower():
                    continue
                body = get_mail_body(msg)
                links = re.findall(r'https?://[^\s"\'<>\)]+', body)
                for link in links:
                    if "serv00" in link and ("activate" in link or "verify" in link
                                             or "confirm" in link or "token" in link):
                        conn.logout()
                        return link, body[:500]
                # 放宽：只要是 serv00 域名下的链接都试一遍
                for link in links:
                    if "serv00.com" in link:
                        conn.logout()
                        return link, body[:500]
            conn.logout()
        except Exception as e:
            print("[IMAP] 读取失败(第%d次): %s" % (attempt + 1, e))
        time.sleep(30)
    return None, ""


# ------------------------------------------------------------------ 自动注册
def auto_register():
    """返回 (success: bool, info: str)"""
    if not (MAIL_USER and MAIL_AUTH and SERV00_USER and SERV00_PASS):
        return False, "自动注册缺少配置（需 MAIL_USER/MAIL_AUTH/SERV00_USER/SERV00_PASS）"

    # 1) GET 注册页，提取表单
    html, status, _ = fetch(SERV00_URL)
    if not is_open(html, status):
        return False, "注册页当前未开放（status=%s）" % status
    action, inputs = extract_form(html)
    payload = fill_payload(inputs)
    print("[注册] 表单字段:", list(payload.keys()))

    # 2) POST 提交
    data = urllib.parse.urlencode(payload).encode("utf-8")
    resp, code, _ = fetch(action, data=data, referer=SERV00_URL, method="POST")
    print("[注册] POST 响应 status=%s, len=%d" % (code, len(resp)))
    if code not in (200, 302) and "error" in resp.lower():
        return False, "POST 注册表单失败(status=%s): %s" % (code, resp[:300])

    # 3) 读验证邮件，提取激活链接
    print("[注册] 等待 Serv00 验证邮件（IMAP 轮询，最多 5 分钟）...")
    link, snippet = find_activation_link()
    if not link:
        return False, ("已提交注册但 5 分钟内未收到验证邮件。"
                        "可能需手动查收 %s 并点击激活链接。") % MAIL_USER

    # 4) 访问激活链接
    print("[注册] 访问激活链接:", link[:80])
    act, acode, _ = fetch(link)
    ok = acode in (200, 302) and ("activated" in act.lower() or "success" in act.lower()
                                  or "welcome" in act.lower() or acode == 302)
    info = (
        "Serv00 自动注册%s！\n\n"
        "用户名: %s\n"
        "密码: %s\n"
        "SSH 主机: %s.serv00.net\n"
        "SSH 端口: 22\n"
        "注册邮箱: %s\n\n"
        "提醒：免费版严禁跑代理/VPN/隧道（会封号），建站/SSH 练手可用；"
        "免费号 90 天不登录会被删，需定期登录保号。\n"
        "激活链接已访问(status=%s)。" % (
            "成功" if ok else "已提交",
            SERV00_USER, SERV00_PASS, SERV00_USER, MAIL_USER, acode)
    )
    return ok or True, info


# ------------------------------------------------------------------ 邮件通知
def send_mail(subject, body):
    if not (MAIL_USER and MAIL_AUTH):
        print("[邮件] 未配置 MAIL_USER/MAIL_AUTH，仅打印不发送：")
        print("==== %s ====\n%s\n====" % (subject, body))
        return False
    ctx = ssl.create_default_context()
    try:
        if SMTP_PORT == 465:
            s = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=20)
        else:
            s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
            s.starttls(context=ctx)
        s.login(MAIL_USER, MAIL_AUTH)
        msg = email.message.EmailMessage()
        msg["From"] = MAIL_USER
        msg["To"] = NOTIFY_TO or MAIL_USER
        msg["Subject"] = subject
        msg.set_content(body)
        s.send_message(msg)
        s.quit()
        print("[邮件] 已发送至 %s" % (NOTIFY_TO or MAIL_USER))
        return True
    except Exception as e:
        print("[邮件] 发送失败:", e)
        return False


# ------------------------------------------------------------------ 主流程
def main():
    html, status = fetch(SERV00_URL)
    if not is_open(html, status):
        print("[未开放] HTTP %s，10 分钟后重试" % status)
        return

    print("[开放] 检测到 Serv00 免费注册开放！")
    if AUTO_REGISTER:
        ok, info = auto_register()
        if ok:
            send_mail("✅ Serv00 自动注册完成", info)
        else:
            send_mail("⚠️ Serv00 自动注册未完成（需手动）", info +
                      "\n\n手动注册地址：https://www.serv00.com/register-account/")
    else:
        send_mail(
            "🔔 Serv00 免费注册已开放",
            "立刻前往 https://www.serv00.com/register-account/ 注册。\n\n"
            "提醒：免费版严禁跑代理/VPN/隧道（会封号），建站/SSH 练手可用；"
            "注册后 SSH 为 用户名@用户名.serv00.net:22；"
            "免费号 90 天不登录会被删，需定期登录保号。",
        )


if __name__ == "__main__":
    main()
