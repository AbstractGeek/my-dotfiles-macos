if status is-interactive
    # Commands to run in interactive sessions can go here
end
fish_add_path /opt/homebrew/bin
status --is-interactive; and rbenv init - fish | source

# pipx
set PATH $PATH /Users/dinesh/.local/bin
#register-python-argcomplete --shell fish pipx >~/.config/fish/completions/pipx.fish

# sconfig and sfunctions
set fish_function_path $fish_function_path /Users/dinesh/.config/fish/sfunctions
source /Users/dinesh/.config/fish/sconfig.fish

## >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
#if test -f /opt/homebrew/Caskroom/miniforge/base/bin/conda
#    eval /opt/homebrew/Caskroom/miniforge/base/bin/conda "shell.fish" "hook" $argv | source
#else
#    if test -f "/opt/homebrew/Caskroom/miniforge/base/etc/fish/conf.d/conda.fish"
#        . "/opt/homebrew/Caskroom/miniforge/base/etc/fish/conf.d/conda.fish"
#    else
#        set -x PATH "/opt/homebrew/Caskroom/miniforge/base/bin" $PATH
#    end
#end
## <<< conda initialize <<<

# additional env variables
set -gx GOPATH /Users/dinesh/.go
set -gx EDITOR /usr/bin/nano

# taskwarrior
#if [ "$(defaults read -g AppleInterfaceStyle)" = Dark ]
#    set -gx TASK_THEME dark-256.theme
#else
#    set -gx TASK_THEME light-256.theme
#end

# taskwarrior functions
#source /Users/dinesh/.config/fish/conf.d/task_funcs.fish

# Added by LM Studio CLI (lms)
set -gx PATH $PATH /Users/dinesh/.lmstudio/bin

# starship
starship init fish | source