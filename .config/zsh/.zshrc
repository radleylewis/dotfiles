# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.config//zsh//.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# To customize prompt, run `p10k configure` or edit ~/.config//zsh//.p10k.zsh.
[[ ! -f ~/.config//zsh//.p10k.zsh ]] || source ~/.config//zsh//.p10k.zsh

SAVEHIST=10000000
HISTSIZE=11000000
HISTFILE="${XDG_CACHE_HOME:-$HOME/.cache}/zsh/history"

# load aliasrc if it exists
[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/zsh/aliasrc" ] && source "${XDG_CONFIG_HOME:-$HOME/.config}/zsh/aliasrc"
# load optionrc if it exists
[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/zsh/optionrc" ] && source "${XDG_CONFIG_HOME:-$HOME/.config}/zsh/optionrc"

# load plugins
source /usr/share/zsh/plugins/powerlevel10k/powerlevel10k.zsh-theme  2>/dev/null                                # powerlevel10k theme
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh 2>/dev/null                           # autosuggestions 
source /usr/share/zsh/plugins/fast-syntax-highlighting/fast-syntax-highlighting.plugin.zsh 2>/dev/null          # syntax highlighting 
source /usr/share/zsh/plugins/zsh-vi-mode/zsh-vi-mode.plugin.zsh 2>/dev/null                                    # vi mode
source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.plugin.zsh 2>/dev/null  # substring search

# colours
autoload -U colors && colors	      # colours
autoload -U compinit && compinit    # basic completion
autoload -U compinit colors zcalc   # theming

# tab completion
zstyle ':completion:*' matcher-list 'm:{[:lower:][:upper:]}={[:upper:][:lower:]}' # Case insensitive tab completion
zstyle ':completion:*' list-colors "${(s.:.)--color=auto}"                        # Colored completion (different colors for dirs/files/etc)
zstyle ':completion:*' rehash true                                                # automatically find new executables in path
zstyle ':completion:*' menu select                                                # Highlight menu selection

# Color man pages
export LESS_TERMCAP_mb=$'\E[01;32m'
export LESS_TERMCAP_md=$'\E[01;32m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;47;34m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;36m'
export LESS=-R

zmodload zsh/terminfo
# bindkey "$terminfo[kcuu1]" history-substring-search-up
# bindkey "$terminfo[kcud1]" history-substring-search-down
# bindkey '^[[A' history-substring-search-up
# bindkey '^[OA' history-substring-search-up
# bindkey '^[[B' history-substring-search-down
# bindkey '^[OB' history-substring-search-down
bindkey -M vicmd '^[[A' history-substring-search-up \
                 '^[OA' history-substring-search-up \
                 '^[[B' history-substring-search-down \
                 '^[OB' history-substring-search-down
bindkey -M viins '^[[A' history-substring-search-up \
                 '^[OA' history-substring-search-up \
                 '^[[B' history-substring-search-down \
                 '^[OB' history-substring-search-down
