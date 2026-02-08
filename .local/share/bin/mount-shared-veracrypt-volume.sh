#!/bin/bash

DEVICE="/dev/nvme0n1p3"
MOUNT_POINT="/home/rad/Documents"
APP_NAME="VeraCrypt"

# Check if already mounted
if sudo veracrypt --text --list | grep -q "$DEVICE"; then
    notify-send --app-name="$APP_NAME" --icon=dialog-warning "Already mounted!"
    exit 0
fi

# Get password using zenity (or rofi if you prefer)
PASSWORD=$(zenity --password --title="Decrypt Documents (VeraCrypt)?")

# Check if password was entered
if [ -z "$PASSWORD" ]; then
    notify-send --app-name="$APP_NAME" --icon=dialog-warning "Mount cancelled: no password entered!"
    exit 1
fi

# Mount the partition
echo "$PASSWORD" | sudo veracrypt --text --non-interactive --pim=0 --stdin "$DEVICE" "$MOUNT_POINT"

# Check if mount was successful
if [ $? -eq 0 ]; then
    chown -R rad:rad "$MOUNT_POINT"
    notify-send --app-name="$APP_NAME" --icon=emblem-default "Partition mounted successfully ✓"
else
    notify-send --app-name="$APP_NAME" --icon=dialog-warning "Failed to mount: incorrect password? ✗"
    exit 1
fi
