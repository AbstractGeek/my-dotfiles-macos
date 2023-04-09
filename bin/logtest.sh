#!/bin/sh
# A small shell script to test logging (for crontab)
LOG=$HOME/.local/logs/test.log
echo "*** $(date -R) ***" >> $LOG
