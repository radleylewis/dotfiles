"""Shared helpers for the rofi scripts (kept out of scripts/ so rofi doesn't list it as a mode)."""

import json
import os
import subprocess
import time
from datetime import datetime
from typing import Optional

CONFIG_DIR = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
ROFI_DIR = os.path.join(CONFIG_DIR, "rofi")


def timestamp_file(prefix: str, ext: str, folder) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{folder}/{prefix}_{ts}.{ext}"


def take_screenshot():
    image_dir = os.path.expanduser("~/Pictures/Screenshots")
    os.makedirs(image_dir, exist_ok=True)
    out = timestamp_file("screenshot", "png", image_dir)
    # Short delay so the rofi menu has closed before grim captures the screen.
    subprocess.Popen(
        [
            "sh",
            "-c",
            'sleep 0.3 && grim "$1" && wl-copy --type image/png < "$1"'
            ' && notify-send "Screenshot Taken" "$1\nCopied to clipboard"',
            "sh",
            out,
        ],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


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


# ─────────────────────────────────────────────
#  Audio devices (sinks = outputs, sources = inputs)
# ─────────────────────────────────────────────


def list_audio_devices(kind: str) -> list[tuple[str, str]]:
    """(name, description) for kind "sinks" or "sources"; monitor sources are skipped."""
    out = subprocess.run(
        ["pactl", "-f", "json", "list", kind], capture_output=True, text=True
    ).stdout
    devices = []
    for d in json.loads(out or "[]"):
        if d.get("monitor_source") and kind == "sources":
            continue  # "Monitor of ..." entries are outputs, not microphones
        devices.append((d["name"], d.get("description") or d["name"]))
    return devices


def cards() -> list[dict]:
    out = subprocess.run(
        ["pactl", "-f", "json", "list", "cards"], capture_output=True, text=True
    ).stdout
    return json.loads(out or "[]")


def _profile_for_port(card: dict, port: dict) -> Optional[str]:
    """Best available profile exposing this output port, preferring one that keeps the
    card's current input (so switching to the monitor doesn't drop the laptop mic)."""
    profiles = card["profiles"]
    candidates = [n for n in port.get("profiles", []) if profiles.get(n, {}).get("available")]
    if not candidates:
        return None
    current_input = card["active_profile"].partition("+")[2]  # e.g. "input:analog-stereo"
    keeps_input = [n for n in candidates if current_input and n.endswith("+" + current_input)]
    pool = keeps_input or candidates
    return max(pool, key=lambda n: profiles[n].get("priority", 0))


def switchable_outputs(port_prefix: str = "") -> list[tuple[str, str, str]]:
    """(card, profile, description) for connected outputs that need a card profile
    switch to appear, e.g. a monitor's HDMI/DisplayPort audio while on the analog
    profile. port_prefix limits it to e.g. "hdmi-output" or "analog-output"."""
    outputs = []
    for card in cards():
        active = card["active_profile"]
        for port_name, port in card.get("ports", {}).items():
            # pactl reports no direction; output ports are named e.g. "hdmi-output-0"
            if "-output" not in port_name or not port_name.startswith(port_prefix):
                continue
            if port.get("availability") == "not available" or active in port.get("profiles", []):
                continue
            profile = _profile_for_port(card, port)
            if profile:
                desc = port.get("description", port_name)
                product = port.get("properties", {}).get("device.product.name")
                outputs.append((card["name"], profile, f"{product} ({desc})" if product else desc))
    return outputs


def switch_card_profile(card: str, profile: str, wait: float = 3.0) -> Optional[str]:
    """Switch a card's profile and make its new output the default; returns the sink."""
    subprocess.run(["pactl", "set-card-profile", card, profile], check=False)
    deadline = time.monotonic() + wait
    while time.monotonic() < deadline:  # the new sink appears shortly after the switch
        out = subprocess.run(
            ["pactl", "-f", "json", "list", "sinks"], capture_output=True, text=True
        ).stdout
        for sink in json.loads(out or "[]"):
            props = sink.get("properties", {})
            if props.get("device.name") == card and profile.startswith(
                "output:" + props.get("device.profile.name", "?")
            ):
                subprocess.run(["pactl", "set-default-sink", sink["name"]], check=False)
                return sink["name"]
        time.sleep(0.2)
    return None


def default_audio_device(kind: str) -> str:
    cmd = "get-default-sink" if kind == "sinks" else "get-default-source"
    return subprocess.run(["pactl", cmd], capture_output=True, text=True).stdout.strip()


def get_audio_input_device() -> str:
    """Human-readable name of the current default microphone."""
    current = default_audio_device("sources")
    for name, desc in list_audio_devices("sources"):
        if name == current:
            return desc
    return current or "No Mic"


def show_audio_menu(kind: str, icon: str, prompt: str, message: str) -> None:
    """Print a rofi script-mode menu of audio devices, marking the current one."""
    current = default_audio_device(kind)
    devices = list_audio_devices(kind)
    current_desc = next((d for n, d in devices if n == current), current)

    print(f"\0prompt\x1f{prompt}")
    print(f"\0message\x1f{message}: {current_desc}")
    for name, desc in devices:
        label = f"[current] {desc}" if name == current else desc
        print(f"{icon} {label}\0info\x1f{name}|{desc}")
    if kind == "sinks":
        # outputs hidden behind another card profile (e.g. the monitor's speakers)
        for card, profile, desc in switchable_outputs():
            print(f"{icon} {desc}\0info\x1fcard|{card}|{profile}|{desc}")


def set_audio_device(kind: str, selection: str, title: str) -> None:
    """Apply a selection made from show_audio_menu (ROFI_INFO is "name|description")."""
    if selection.startswith("card|"):
        _, card, profile, desc = selection.split("|", 3)
        switch_card_profile(card, profile)
        notify(title, f"Now using: {desc}", expire_time=3_000)
        return
    name, desc = selection.split("|", 1)
    cmd = "set-default-sink" if kind == "sinks" else "set-default-source"
    subprocess.run(["pactl", cmd, name], check=False)
    notify(title, f"Now using: {desc}", expire_time=3_000)
