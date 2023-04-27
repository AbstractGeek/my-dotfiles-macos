set -g VIRTUALFISH_HOME /Users/dinesh/.virtualenvs
set -g PROJECT_HOME /Users/dinesh/Codebank

set -g VIRTUALFISH_VERSION 2.5.4
set -g VIRTUALFISH_PYTHON_EXEC /Users/dinesh/.local/pipx/venvs/virtualfish/bin/python
source /Users/dinesh/.local/pipx/venvs/virtualfish/lib/python3.11/site-packages/virtualfish/virtual.fish
source /Users/dinesh/.local/pipx/venvs/virtualfish/lib/python3.11/site-packages/virtualfish/compat_aliases.fish
source /Users/dinesh/.local/pipx/venvs/virtualfish/lib/python3.11/site-packages/virtualfish/projects.fish
source /Users/dinesh/.local/pipx/venvs/virtualfish/lib/python3.11/site-packages/virtualfish/environment.fish
emit virtualfish_did_setup_plugins