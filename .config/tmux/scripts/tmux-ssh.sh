#!/usr/bin/env sh

host=$(grep '^Host ' ~/.ssh/config | awk '{print $2}' | grep -v '\*' | fzf --prompt="SSH: ")

[ -z "$host" ] && exit 0

tmux new-window -n "$host" "ssh $host"
