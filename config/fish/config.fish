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