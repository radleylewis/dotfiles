# dotfiles

## overview

These are my dotfiles for use on arch and ubuntu based linux distributions. My setup includes:

-   qtile ([submodule](https://github.com/radleylewis/qtile))  
-   neovim ([submodule](https://github.com/radleylewis/nvim))  
-   tmux
-   alacritty
-   zsh
-   rofi
-   lf
-   brave

Feel free to use any of the configurations herein as inspiration.

## setup

1. clone the repository

```bash
cd ~
```
```bash
git clone --bare git@github.com:radleylewis/dotfiles.git .dotfiles
```

2. include dotfiles alias in .bashrc / .zshrc

```bash
echo alias dotfiles=\'git --git-dir='$HOME'/.dotfiles --work-tree='$HOME'\' >> .bashrc
```
```bash
source ~/.bashrc
```
```bash
dotfiles config status.showUntrackedFiles no # don't track files noting $HOME work-tree
```
```bash
dotfiles checkout # populates dotfiles to their respective locations
```
```bash
cd ~/.config/nvim
```
```bash
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
