# dotfiles

## overview

These are my dotfiles for use on arch and ubuntu based linux distributions including:

-   tmux
-   neovim
-   alacritty

Feel free to use any of the configurations herein as inspiration.

## setup

1. clone the repository

```bash
cd ~
git clone --bare https://github.com/radleylewis/dotfiles.git .dotfiles
```

2. include dotfiles alias in .bashrc / .zshrc

```bash
echo alias dotfiles=\'git --git-dir='$HOME'/.dotfiles --work-tree='$HOME'\' >> .bashrc
source ~/.bashrc
dotfiles config status.showUntrackedFiles no # don't track files noting $HOME work-tree
dotfiles checkout # populates dotfiles to their respective locations
cd ~/.config/nvim
dotfiles submodule update # clones the submodule nvim which may not happen automatically
```

## usage

Once setup, useful commands include:

```bash
dotfiles status
dotfiles add <filename> # add a new dotfile
dotfiles add -u # add unstaged files
```

## author

Radley E. Sidwell-Lewis
