"""微信推送封装 — 所有脚本通过此模块调用，避免每个脚本重复定义 push_to_wechat()."""
import subprocess
import hashlib
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SCRIPTS_DIR.parent
CHECKPOINT_DIR = PROJECT_ROOT / ".bridge" / "flywheel_checkpoints"


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


def push_incremental(flywheel_name: str, title: str, content: str, key_metric: str) -> bool:
    """增量推送：只在关键指标发生变化时才推送。

    flywheel_name: 飞轮名称（用于checkpoint文件名）
    key_metric: 本周的关键指标（如 "69.5%|待执行"）
    返回 True 表示已推送，False 表示无变化跳过。
    """
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    cp_file = CHECKPOINT_DIR / f"{flywheel_name}.txt"

    # 读取上次的指标
    last_metric = ""
    if cp_file.exists():
        last_metric = cp_file.read_text(encoding="utf-8").strip()

    # 如果指标没变，跳过推送
    if last_metric == key_metric.strip():
        print(f"  ⏭️ {flywheel_name} 无变化，跳过推送")
        return False

    # 指标变了 → 推送 + 更新checkpoint
    ok = push_to_wechat(title, content)
    cp_file.write_text(key_metric.strip(), encoding="utf-8")
    return ok
