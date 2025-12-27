import subprocess
import os

from datetime import datetime
from typing import Optional


def timestamp_file(prefix: str, ext: str, folder) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{folder}/{prefix}_{ts}.{ext}"


def take_screenshot():
    IMAGE_DIR = os.path.expanduser("~/Pictures/Screenshots")
    os.makedirs(IMAGE_DIR, exist_ok=True)
    out = timestamp_file("screenshot", "png", IMAGE_DIR)

    subprocess.Popen(["grim", out])

    notify("Screenshot Taken", out)


def notify(
    title: str,
    message: str,
    replace_id: Optional[int] = None,
    app_name: Optional[str] = "",
    expire_time: int = 1_200,
    urgency: str = "normal",
):
    cmd = ["notify-send"]
    if replace_id:
        cmd.append(f"--replace-id={replace_id}")
    if app_name:
        cmd.append(f"--app-name={app_name}")

    cmd.append(f"--urgency={urgency}")
    cmd.append(f"--expire-time={expire_time}")

    subprocess.run(cmd + [title, message], check=False)


def get_audio_input_device():
    """Return the current default audio input (microphone) using pactl."""
    try:
        result = subprocess.run(
            ["pactl", "get-default-source"],
            capture_output=True,
            text=True,
            check=True,
        )
        source = result.stdout.strip()

        # Get human-readable description
        desc = subprocess.run(
            ["pactl", "list", "sources"],
            capture_output=True,
            text=True,
        ).stdout

        for block in desc.split("Source #"):
            if source in block:
                for line in block.splitlines():
                    if "Description:" in line:
                        return line.split("Description:")[1].strip()

        return source  # fallback
    except Exception:
        return "No Mic"
