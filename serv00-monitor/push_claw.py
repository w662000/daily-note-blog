#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serv00 免费注册开放探测 + 微信(claw)推送
纯标准库，无第三方依赖，可在 GitHub Actions / 本机 / CF Worker(Python) 任意环境运行。

推送通道（已确认）：ClawBot 已绑定微信，成功时【直接经 ClawBot 推送到微信】。
只需一个 Secret：CLAW_BOT_TOKEN（ClawBot 的 bot token）。
可选 Secret：
  - CLAW_TO_USER       你的微信 user_id（形如 xxx@im.wechat）；不填则自动从最近一条消息取
  - CLAW_CONTEXT_TOKEN 上下文 token；不填则自动从最近一条消息取

兼容兜底：若同时配置了 CLAW_WEBHOOK（通用 webhook 地址），则优先走 webhook。
"""

import urllib.request
import json
import os
import sys
import time
import base64
import random
import struct

URL = "https://www.serv00.com/register-account/"
CHECK_TIMEOUT = 20

# 判定为“未开放”的关键词（页面出现这些即说明名额满/暂不可注册）
BLOCK_KEYWORDS = [
    "the server user limit has been reached",
    "registering a new account is currently not possible",
    "500 internal server error",
    "internal server error",
]


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=CHECK_TIMEOUT) as r:
            return r.read().decode("utf-8", "ignore"), r.status
    except Exception as e:
        return "ERR:%s" % e, 0


def is_open(html, status):
    if status != 200:
        return False
    low = html.lower()
    if any(kw in low for kw in BLOCK_KEYWORDS):
        return False
    # 正常注册页应有表单字段
    return ("name=" in low) and ("password" in low or "e-mail" in low or "email" in low)


def push_claw(message):
    """按配置推送微信。返回 True 表示已推送。"""
    # 兜底：通用 webhook 优先（若配置了）
    webhook = os.environ.get("CLAW_WEBHOOK", "").strip()
    if webhook:
        payload = json.dumps({
            "title": "Serv00 免费注册已开放",
            "content": message,
        }).encode("utf-8")
        req = urllib.request.Request(
            webhook, data=payload,
            headers={"Content-Type": "application/json"},
        )
        try:
            urllib.request.urlopen(req, timeout=CHECK_TIMEOUT)
            print("[推送] 已通过 CLAW_WEBHOOK 推送")
            return True
        except Exception as e:
            print("[推送] WEBHOOK 失败，转 ClawBot:", e)

    # 主通道：ClawBot（已绑定微信）
    token = os.environ.get("CLAW_BOT_TOKEN", "").strip()
    if token:
        return ilink_push(token, message)

    print("[推送] 未配置任何 claw 凭据（CLAW_BOT_TOKEN / CLAW_WEBHOOK）。仅打印不推送。")
    return False


def _ilink_headers(token):
    uin = base64.b64encode(struct.pack("<I", random.randint(0, 2 ** 32 - 1))).decode()
    return {
        "Content-Type": "application/json",
        "AuthorizationType": "ilink_bot_token",
        "Authorization": "Bearer " + token,
        "X-WECHAT-UIN": uin,
    }


def ilink_push(token, message):
    """经 ClawBot iLink API 推送到微信。"""
    base = "https://ilinkai.weixin.qq.com"
    hdr = _ilink_headers(token)

    to_user = os.environ.get("CLAW_TO_USER", "").strip()
    ctx = os.environ.get("CLAW_CONTEXT_TOKEN", "").strip()

    # 若没给 context_token / to_user，先用 getUpdates 取最近一条消息的上下文
    if not ctx or not to_user:
        body = json.dumps({
            "get_updates_buf": "",
            "base_info": {"channel_version": "1.0.2"},
        }).encode()
        req = urllib.request.Request(base + "/ilink/bot/getupdates", data=body, headers=hdr)
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=40).read())
            for m in resp.get("msgs", []):
                to_user = m.get("from_user_id", "")
                ctx = m.get("context_token", "")
                if to_user:
                    break
        except Exception as e:
            print("[iLink] getUpdates 失败:", e)

    if not to_user:
        print("[iLink] 仍缺少 to_user，无法推送。请先给 bot 发一条消息，或将 CLAW_TO_USER 写入 Secrets。")
        return False

    body = json.dumps({
        "msg": {
            "to_user_id": to_user,
            "client_id": "serv00mon-%d" % int(time.time()),
            "message_type": 2,
            "message_state": 2,
            "context_token": ctx,
            "item_list": [{"type": 1, "text_item": {"text": message}}],
        },
        "base_info": {"channel_version": "1.0.2"},
    }).encode()
    req = urllib.request.Request(base + "/ilink/bot/sendmessage", data=body, headers=hdr)
    try:
        urllib.request.urlopen(req, timeout=CHECK_TIMEOUT)
        print("[推送] 已通过 ClawBot 推送到微信")
        return True
    except Exception as e:
        print("[推送] iLink 推送失败:", e)
        return False


def main():
    html, status = fetch()
    if is_open(html, status):
        msg = (
            "Serv00 免费注册已开放！\n\n"
            "立刻前往 https://www.serv00.com/register-account/ 注册。\n\n"
            "提醒：免费版严禁跑代理/VPN/隧道（会封号），建站/SSH 练手可用；"
            "注册后 SSH 为 用户名@用户名.serv00.net:22；"
            "免费号 90 天不登录会被删，需定期登录保号。"
        )
        print("[开放] 检测到注册开放，推送通知...")
        push_claw(msg)
        sys.exit(0)
    else:
        print("[未开放] HTTP %s，10 分钟后重试" % status)
        sys.exit(0)


if __name__ == "__main__":
    main()
