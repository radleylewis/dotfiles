# tmux

A tmux configuration with vim keybindings, session management, and popup utilities.

*Author: Radley E. Sidwell-Lewis*

## Requirements

- tmux `3.3` or later
- [TPM](https://github.com/tmux-plugins/tpm) (tmux plugin manager)
- `fzf` (for the session and SSH popups)
- `lazygit` (for the lazygit popup)
- `wl-clipboard` (tmux-yank copies with `wl-copy` on Wayland)
- A [Nerd Font](https://www.nerdfonts.com/) (JetBrains Mono Nerd Font, as in the rest of the setup)

## Installation

i. Clone this config:

```bash
mkdir -p ~/.config/tmux && curl -fsSL https://raw.githubusercontent.com/radleylewis/dotfiles/master/.config/tmux/tmux.conf -o ~/.config/tmux/tmux.conf
```

ii. Install TPM:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.config/tmux/plugins/tpm
```

iii. Start tmux and install plugins with `prefix + I` (capital i).

## Plugins

| Plugin | Purpose |
|--------|---------|
| `vim-tmux-navigator` | Seamless navigation between tmux panes and vim splits |
| `tmux-resurrect` | Save and restore tmux sessions across reboots |
| `tmux-continuum` | Automatic session saving every minute |
| `tmux-yank` | System clipboard integration in copy mode |

## Keybindings

**Prefix key:** `Ctrl + a`

### Panes

| Shortcut | Action |
|----------|--------|
| `prefix + \|` | Split pane horizontally |
| `prefix + -` | Split pane vertically |
| `prefix + h/j/k/l` | Resize pane left/down/up/right |
| `prefix + m` | Zoom pane (toggle fullscreen) |

### Windows

| Shortcut | Action |
|----------|--------|
| `prefix + c` | New window (in current path) |
| `prefix + Space` | Switch to last window |
| `prefix + b` | Break pane into its own window |
| `prefix + x` | Kill pane (no confirmation) |

### Copy Mode

| Shortcut | Action |
|----------|--------|
| `prefix + [` | Enter copy mode |
| `v` | Begin selection |
| `y` | Copy selection to clipboard |

### Popups

| Shortcut | Action |
|----------|--------|
| `prefix + w` | Session switcher |
| `prefix + T` | Scratchpad terminal |
| `prefix + g` | LazyGit |
| `prefix + S` | SSH to a host from `~/.ssh/config` (new window) |

Inside the scratchpad (it has no prefix): `T` closes it, `C-[` enters copy mode.

### General

| Shortcut | Action |
|----------|--------|
| `prefix + r` | Reload config |
