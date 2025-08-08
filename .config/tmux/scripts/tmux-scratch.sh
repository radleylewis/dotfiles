#!/bin/bash

# Define session name for scratchpad
session="_popup_scratchpad"

# Create session if it doesn't exist
if ! tmux has -t "$session" 2>/dev/null; then
	session_id="$(tmux new-session -dP -s "$session" -F '#{session_id}')"
	tmux set-option -s -t "$session_id" key-table popup
	tmux set-option -s -t "$session_id" status off
	tmux set-option -s -t "$session_id" prefix None
	session="$session_id"
fi

# Attach to the scratchpad session inside the popup
exec tmux attach -t "$session" >/dev/null
