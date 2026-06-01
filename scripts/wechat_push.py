#!/usr/bin/env python3
"""将 Claude Code 产出推送到微信，通过 PushPlus/Server酱 渠道。

使用方式：
  python3 scripts/wechat_push.py "标题" "内容"
  python3 scripts/wechat_push.py "标题" --file /path/to/markdown.md
  echo "内容" | python3 scripts/wechat_push.py "标题" --stdin

配置方式（任选一种）：
  1. WxPusher（免费推荐）: 注册 wxpusher.zjiecode.com → 创建应用获取 appToken → 扫码关注获取UID
     export WECHAT_WXPUSHER_TOKEN="your_app_token"
     export WECHAT_WXPUSHER_UID="your_uid"
  2. 企业微信机器人: 企业微信创建群机器人 → 获取 webhook URL（企业微信用户免费）
     export WECHAT_WEBHOOK="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
  3. PushPlus: 注册 pushplus.plus → 获取 token（需实名认证）
     export WECHAT_PUSH_TOKEN="your_pushplus_token"
  4. Server酱: 注册 sct.ftqq.com → 获取 SendKey
     export WECHAT_SENDKEY="your_sendkey"
"""

import os
from lib.email_push import push as push_email, get_config as email_configured
import sys
import json
import argparse
import urllib.request


def push_wxpusher(token: str, uid: str, title: str, content: str) -> bool:
    """通过 WxPusher 推送到微信（免费，无需实名）"""
    url = "http://wxpusher.zjiecode.com/api/send/message"
    # 合并标题和内容
    full_content = f"# {title}\n\n{content}"
    data = json.dumps({
        "appToken": token,
        "content": full_content,
        "contentType": 3,  # 3=Markdown
        "uids": [uid],
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result.get("code") == 1000
    except Exception as e:
        print(f"WxPusher 发送失败: {e}", file=sys.stderr)
        return False


def push_pushplus(token: str, title: str, content: str) -> bool:
    """通过 PushPlus 推送到微信"""
    url = "http://www.pushplus.plus/send"
    data = json.dumps({
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown" if any(c in content for c in '#*`-') else "txt",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result.get("code") == 200
    except Exception as e:
        print(f"PushPlus 发送失败: {e}", file=sys.stderr)
        return False


def push_serverchan(sendkey: str, title: str, content: str) -> bool:
    """通过 Server酱 推送到微信"""
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    data = urllib.parse.urlencode({
        "title": title,
        "desp": content[:50000],  # Server酱限制 50KB
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result.get("code") == 0
    except Exception as e:
        print(f"Server酱 发送失败: {e}", file=sys.stderr)
        return False


def push_wecom_webhook(webhook: str, title: str, content: str) -> bool:
    """通过企业微信机器人 Webhook 推送"""
    # 企业微信 markdown 消息限制 4096 字节，超长截断
    text = f"## {title}\n\n{content[:3500]}"
    data = json.dumps({
        "msgtype": "markdown",
        "markdown": {"content": text},
    }).encode("utf-8")
    req = urllib.request.Request(webhook, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result.get("errcode") == 0
    except Exception as e:
        print(f"企业微信发送失败: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="推送内容到微信")
    parser.add_argument("title", help="消息标题")
    parser.add_argument("content", nargs="?", default="", help="消息内容（可选，与 --file/--stdin 互斥）")
    parser.add_argument("--file", help="从文件读取内容")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取内容")
    args = parser.parse_args()

    content = args.content
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.stdin:
        content = sys.stdin.read()

    if not content.strip():
        print("错误：内容不能为空", file=sys.stderr)
        sys.exit(1)

    wxpusher_token = os.environ.get("WECHAT_WXPUSHER_TOKEN")
    wxpusher_uid = os.environ.get("WECHAT_WXPUSHER_UID")
    pushplus_token = os.environ.get("WECHAT_PUSH_TOKEN")
    sendkey = os.environ.get("WECHAT_SENDKEY")
    webhook = os.environ.get("WECHAT_WEBHOOK")
    email_cfg = email_configured()

    if email_cfg:
        ok = push_email(args.title, content)
    elif wxpusher_token and wxpusher_uid:
        ok = push_wxpusher(wxpusher_token, wxpusher_uid, args.title, content)
    elif webhook:
        ok = push_wecom_webhook(webhook, args.title, content)
    elif pushplus_token:
        ok = push_pushplus(pushplus_token, args.title, content)
    elif sendkey:
        ok = push_serverchan(sendkey, args.title, content)
    else:
        print("错误：未配置推送渠道。请设置以下任一环境变量组合：",
              file=sys.stderr)
        print("  QQ邮箱（推荐）: 登录QQ邮箱→设置→账户→生成授权码 → export QQ_EMAIL=xxx QQ_EMAIL_AUTH=xxx",
              file=sys.stderr)
        print("  企业微信机器人: 创建群机器人 → export WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/...",
              file=sys.stderr)
        print("  PushPlus: pushplus.plus → export WECHAT_PUSH_TOKEN=xxx",
              file=sys.stderr)
        print("  Server酱: sct.ftqq.com → export WECHAT_SENDKEY=xxx",
              file=sys.stderr)
        sys.exit(1)

    if ok:
        print("微信推送成功")
    else:
        print("微信推送失败，请检查配置", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
