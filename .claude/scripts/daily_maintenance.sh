#!/bin/bash
# Daily memory maintenance script
# Add to crontab: 0 2 * * * /path/to/daily_maintenance.sh

cd "."
/usr/local/bin/python3 .claude/scripts/memory_auto_update.py daily-cleanup
