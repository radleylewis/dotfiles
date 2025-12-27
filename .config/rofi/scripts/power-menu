#!/usr/bin/env python3

import subprocess
import os
from typing import List

shutdown_icon = ""
reboot_icon = ""
sleep_icon = "󰤄"
lock_icon = ""
logout_icon = "󰗽"
yes_icon = ""
no_icon = ""

CONFIG_DIR = os.environ.get("XDG_CONFIG_HOME", "")
LOCKSCREEN_WALLPAPER = f"{CONFIG_DIR}/qtile/assets/wallpapers/lock_screen.png"


def get_uptime() -> str:
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    return result.stdout.strip().replace("up ", "")


def main_menu() -> str:
    options: List[str] = [
        lock_icon,
        logout_icon,
        sleep_icon,
        shutdown_icon,
        reboot_icon,
    ]
    menu: str = "\n".join([f"{item}" for item in options])
    uptime = get_uptime()
    result = subprocess.run(
        [
            "rofi",
            "-dmenu",
            "-p",
            f"Uptime: {uptime}",
            "-mesg",
            f"Uptime: {uptime}",
            "-theme",
            f"{CONFIG_DIR}/rofi/common.rasi",
        ],
        input=menu,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return result.split("\n")[0]


def confirm() -> bool:
    options = [yes_icon, no_icon]
    menu: str = "\n".join([f"{item}" for item in options])
    result = subprocess.run(
        [
            "rofi",
            "-theme",
            f"{CONFIG_DIR}/rofi/common.rasi",
            "-theme-str",
            "listview {columns: 2; lines: 1;}",
            "-dmenu",
            "-p",
            "Confirmation",
            "-mesg",
            "Confirm?",
        ],
        input=menu,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return result == yes_icon


def power():
    selected = main_menu()

    action_map = {
        lock_icon: ["swaylock", "-i", LOCKSCREEN_WALLPAPER],
        sleep_icon: [os.path.expanduser("~/.config/qtile/scripts/sleep.sh")],
        shutdown_icon: ["systemctl", "poweroff"],
        reboot_icon: ["systemctl", "reboot"],
        logout_icon: ["pkill", "-KILL", "-u", os.environ["USER"]],
    }

    if action := action_map[selected]:
        if confirm():
            subprocess.run(action)


if __name__ == "__main__":
    power()
