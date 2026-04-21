#!/bin/bash

DEVICE="/dev/nvme1n1p3"
APP_NAME="VeraCrypt"
UID_NUM=$(id -u)
GID_NUM=$(id -g)

# Check if already mounted
if sudo veracrypt --text --list | grep -q "$DEVICE"; then
    notify-send --app-name="$APP_NAME" --icon=dialog-warning "Already mounted!"
    exit 0
fi

# Get password using zenity
PASSWORD=$(zenity --password --title="Decrypt Documents (VeraCrypt)?")

# Check if password was entered
if [ -z "$PASSWORD" ]; then
    notify-send --app-name="$APP_NAME" --icon=dialog-warning "Mount cancelled: no password entered!"
    exit 1
fi

# Mount the partition - capture output for better error messages
MOUNT_OUTPUT=$(echo "$PASSWORD" | sudo veracrypt \
    --text \
    --non-interactive \
    --stdin \
    --fs-options=uid=$UID_NUM,gid=$GID_NUM \
    --slot=64 \
    "$DEVICE" 2>&1)
MOUNT_EXIT_CODE=$?

# Check if mount was successful
if [ $MOUNT_EXIT_CODE -eq 0 ]; then
    notify-send --app-name="$APP_NAME" --icon=emblem-default "Partition mounted successfully ✓"
else
    notify-send --app-name="$APP_NAME" --icon=dialog-warning "Failed to mount: $MOUNT_OUTPUT"
    exit 1
fi

unset PASSWORD
