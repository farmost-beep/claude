"""微信推送封装 — 所有脚本通过此模块调用，避免每个脚本重复定义 push_to_wechat()."""
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent


def push_to_wechat(title: str, content: str) -> bool:
    """推送消息到微信（通过 wechat_push.py）。
    返回 True 表示推送成功，False 表示失败。
    """
    script = SCRIPTS_DIR / "wechat_push.py"
    result = subprocess.run(
        ["python3", str(script), title, content],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0


def push_file(title: str, filepath: str) -> bool:
    """推送文件内容到微信。"""
    script = SCRIPTS_DIR / "wechat_push.py"
    result = subprocess.run(
        ["python3", str(script), title, "--file", filepath],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0
