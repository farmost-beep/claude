#!/usr/bin/env python3
"""QQ邮箱双通道——SMTP推送 + IMAP回传。

配置环境变量：
  export QQ_EMAIL="yourname@qq.com"
  export QQ_EMAIL_AUTH="你的QQ邮箱授权码"   # 设置→账户→POP3/SMTP服务→生成
  export QQ_EMAIL_RECIPIENT="yourname@qq.com"  # 收件人（默认同发送地址）

授权码获取：登录QQ邮箱 → 设置 → 账户 → POP3/SMTP服务 → 开启 → 生成授权码
"""

import os
import json
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.header import decode_header
from datetime import datetime, timedelta
from pathlib import Path

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587  # 备用端口 465 (SSL), 587 (TLS)
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INBOX_FILE = PROJECT_ROOT / ".bridge" / "inbox.md"


def get_config():
    addr = os.environ.get("QQ_EMAIL")
    auth = os.environ.get("QQ_EMAIL_AUTH")
    # 保险：从 .zshrc 读取
    if not addr or not auth:
        zshrc = Path.home() / ".zshrc"
        if zshrc.exists():
            for line in zshrc.read_text().split("\n"):
                if "export QQ_EMAIL=" in line and not addr:
                    addr = line.split("=", 1)[1].strip().strip("\"'")
                if "export QQ_EMAIL_AUTH=" in line and not auth:
                    auth = line.split("=", 1)[1].strip().strip("\"'")
    recipient = os.environ.get("QQ_EMAIL_RECIPIENT") or addr
    if not addr or not auth:
        return None
    return {"addr": addr, "auth": auth, "recipient": recipient}


def push(title: str, content: str) -> tuple[bool, str]:
    """通过QQ邮箱SMTP发送推送。支持自动重试。返回 (成功?, 消息)"""
    cfg = get_config()
    if not cfg:
        return False, "QQ邮箱未配置（设置 QQ_EMAIL + QQ_EMAIL_AUTH）"

    html = f"<h2>{title}</h2><pre style='font-size:14px;line-height:1.6'>{content}</pre>"
    msg = MIMEText(html, "html", "utf-8")
    msg["Subject"] = title
    msg["From"] = cfg["addr"]
    msg["To"] = cfg["recipient"]

    import time
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        # 冷却等待：QQ SMTP 有频率限制，每次发送前等待
        if attempt > 1:
            wait = attempt * 30
            time.sleep(wait)
        try:
            # 尝试 SSL (465), 失败则尝试 TLS (587)
            ports = [(SMTP_SERVER, 465, True), (SMTP_SERVER, 587, False)]
            last_error = None
            for host, port, use_ssl in ports:
                try:
                    if use_ssl:
                        server = smtplib.SMTP_SSL(host, port, timeout=15)
                    else:
                        server = smtplib.SMTP(host, port, timeout=15)
                        server.starttls()
                    server.login(cfg["addr"], cfg["auth"])
                    server.sendmail(cfg["addr"], [cfg["recipient"]], msg.as_string())
                    server.quit()
                    return True, f"邮件已发送到 {cfg['recipient']}"
                except Exception as e:
                    last_error = e
                    continue
            if attempt < max_retries:
                continue
            return False, f"SMTP发送失败: {last_error}"
        except Exception as e:
            if attempt < max_retries:
                continue
            return False, f"SMTP发送失败: {e}"


def check_replies(hours_back: int = 24) -> list[dict]:
    """检查收件箱，提取回复内容。返回 [{subject, from, body, date}, ...]"""
    cfg = get_config()
    if not cfg:
        return []

    replies = []
    QQ_SYSTEM_ADDRS = ("10000@qq.com", "service@qq.com", "notice@qq.com", "system@qq.com")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(cfg["addr"], cfg["auth"])
        mail.select("INBOX")

        # 搜索指定时间后的邮件
        since = (datetime.now() - timedelta(hours=hours_back)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{since}")')
        if status != "OK":
            return []

        for mid in messages[0].split()[-10:]:  # 最多取最近10封
            status, data = mail.fetch(mid, "(RFC822)")
            if status != "OK":
                continue
            raw = email.message_from_bytes(data[0][1])
            subject, encoding = decode_header(raw["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_addr = raw.get("From", "")
            date_str = raw.get("Date", "")

            # 跳过QQ系统邮件
            if any(a in from_addr for a in QQ_SYSTEM_ADDRS):
                continue

            body = ""
            if raw.is_multipart():
                for part in raw.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
            else:
                body = raw.get_payload(decode=True).decode("utf-8", errors="ignore")

            replies.append({
                "subject": subject,
                "from": from_addr,
                "body": body.strip()[:2000],
                "date": date_str,
            })

        mail.logout()
    except Exception:
        return []

    return replies


def save_replies_to_inbox(replies: list[dict]):
    """将回复写入 .bridge/inbox.md，供Claude读取"""
    if not replies:
        return

    Path(PROJECT_ROOT / ".bridge").mkdir(parents=True, exist_ok=True)
    existing = ""
    if INBOX_FILE.exists():
        existing = INBOX_FILE.read_text(encoding="utf-8")

    new_entries = []
    for r in replies:
        key = f"{r['subject']}|{r['date']}"
        if key not in existing:
            new_entries.append(f"## [{r['date']}] {r['subject']}\n**来自**: {r['from']}\n\n{r['body']}\n\n---\n")

    if new_entries:
        with open(INBOX_FILE, "w", encoding="utf-8") as f:
            f.write("# 📥 回传箱\n\n> Claude定期检查此文件。你在微信回复邮件后，内容会自动出现在这里。\n\n---\n\n")
            f.write("".join(new_entries))
            f.write(existing)
        print(f"📬 {len(new_entries)} 条新回复已写入 {INBOX_FILE}")
    else:
        print("📭 无新回复")


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 email_push.py [push|check] [内容]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "push":
        title = sys.argv[2] if len(sys.argv) > 2 else "来自Claude"
        content = sys.argv[3] if len(sys.argv) > 3 else "(空)"
        ok, msg = push(title, content)
        print(f"{'✅' if ok else '❌'} {msg}")
    elif mode == "check":
        replies = check_replies()
        save_replies_to_inbox(replies)
        for r in replies:
            print(f"  📩 [{r['date']}] {r['subject']} — {r['body'][:80]}...")
        if not replies:
            print("  📭 无新回复")


if __name__ == "__main__":
    main()
