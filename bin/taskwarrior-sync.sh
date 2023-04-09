#!/bin/sh
# source code from: https://www.berkeleytrue.com/posts/2022/06-june/01-taskwarrior-sync

TASK_BACKLOG=/Users/dinesh/.config/task/backlog.data
TASK_SHARE=/Users/dinesh/.local/share/task
SYNC_LOG=/Users/dinesh/.local/logs/taskwarrior-sync-cron.log
LOCK_FILE=$TASK_SHARE/SYNC.lock

if {
  # set C ensures redirect cannot overwrite a file.
  set -C
  # create lock file if it doesn't exist, pipe errors to /dev/null
  2>/dev/null >$LOCK_FILE
}; then
  # trap on exit to remove lockfile
  trap 'rm -f "$LOCK_FILE"' EXIT

  output=$(/opt/homebrew/bin/task sync)
  echo "$(date "+%F %T") - $output" >>$SYNC_LOG 2>&1
fi
exit
