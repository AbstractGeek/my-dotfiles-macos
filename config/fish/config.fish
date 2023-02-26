if status is-interactive
    # Commands to run in interactive sessions can go here
end
fish_add_path /opt/homebrew/bin
status --is-interactive; and rbenv init - fish | source

# pipx
set PATH $PATH /Users/dinesh/.local/bin
register-python-argcomplete --shell fish pipx >~/.config/fish/completions/pipx.fish

# sconfig and sfunctions
set fish_function_path $fish_function_path  /Users/dinesh/.config/fish/sfunctions
source /Users/dinesh/.config/fish/sconfig.fish

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
# eval /opt/homebrew/Caskroom/miniforge/base/bin/conda "shell.fish" "hook" $argv | source
# <<< conda initialize <<<

# additional env variables
set -gx GOPATH /Users/dinesh/.go