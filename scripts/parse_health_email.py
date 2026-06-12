#!/usr/bin/env python3
"""解析华为健康数据提取助手发来的邮件，写入健康追踪文件。

配合华为健康数据提取助手(Android APK)使用：
该工具每日定时通过Accessibility提取华为健康App数据，通过QQ邮箱发送。

配置要求：
  1. Android手机上安装APK
  2. 开启无障碍服务+配置QQ邮箱SMTP
  3. 每日定时发送到 7302282@qq.com

解析逻辑：
  检查收件箱 → 提取华为健康邮件 → 解析步数/睡眠/心率 → 写入追踪文件
"""

import sys, os, re, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.email_push import check_replies

TRACKING_FILE = os.path.expanduser("~/claude/deliverables/health/路线图/华为手表数据.md")
PROCESSED_LOG = "/tmp/health_email_ids.json"


def load_processed():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG) as f:
            return set(json.load(f))
    return set()


def save_processed(ids):
    with open(PROCESSED_LOG, "w") as f:
        json.dump(list(ids), f)


def parse_health_data(body: str) -> dict:
    """从邮件正文中提取健康数据"""
    data = {}
    patterns = {
        "步数": r"步数[：:]\s*(\d+)",
        "睡眠": r"睡眠[：:]\s*([\d.]+)h",
        "心率": r"心率[：:]\s*(\d+)",
        "血氧": r"血氧[：:]\s*(\d+)",
        "距离": r"距离[：:]\s*([\d.]+)km",
        "热量": r"热量[：:]\s*(\d+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, body)
        if match:
            data[key] = match.group(1)
    return data


def main():
    processed = load_processed()
    replies = check_replies(hours_back=48)

    for r in replies:
        msg_id = r.get("id", "")
        subject = r.get("subject", "")
        content = r.get("content", "")

        if msg_id in processed:
            continue
        # 识别华为健康邮件（主题或内容含"华为健康"关键字）
        if "华为健康" not in subject and "华为" not in content[:100]:
            continue

        data = parse_health_data(content)
        if data:
            from datetime import date
            today = date.today().isoformat()
            os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)

            # 写入追踪文件
            with open(TRACKING_FILE, "a") as f:
                f.write(f"\n## {today}\n")
                f.write("| 指标 | 数值 | 来源 |\n")
                f.write("|------|------|------|\n")
                f.write(f"| 步数 | {data.get('步数', '-')} | 华为健康 |\n")
                f.write(f"| 睡眠 | {data.get('睡眠', '-')}h | 华为健康 |\n")
                f.write(f"| 心率 | {data.get('心率', '-')}bpm | 华为健康 |\n")
                f.write(f"| 血氧 | {data.get('血氧', '-')}% | 华为健康 |\n")

            print(f"✅ 健康数据已记录 ({today}): 步数={data.get('步数','?')} 睡眠={data.get('睡眠','?')}h")
        processed.add(msg_id)

    save_processed(processed)


if __name__ == "__main__":
    main()
