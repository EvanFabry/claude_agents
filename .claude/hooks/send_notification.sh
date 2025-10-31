#!/bin/bash

# Unified notification script for Pushover (ntfy disabled)
# Usage: send_notification.sh "message" ["title"] ["priority"]

MESSAGE="${1:-Claude notification}"
TITLE="${2:-Claude Code}"
PRIORITY="${3:-0}"  # Pushover priority: -2 to 2

# Send to ntfy (DISABLED)
# if [ -n "$CLAUDE_NTFY_TOPIC" ]; then
#     curl -s -d "$MESSAGE" "ntfy.sh/$CLAUDE_NTFY_TOPIC" 2>/dev/null &
# fi

# Send to Pushover
if [ -n "$PUSHOVER_TOKEN" ] && [ -n "$PUSHOVER_USER" ] && [ "$PUSHOVER_USER" != "YOUR_USER_KEY_HERE" ]; then
    curl -s \
        --form-string "token=$PUSHOVER_TOKEN" \
        --form-string "user=$PUSHOVER_USER" \
        --form-string "message=$MESSAGE" \
        --form-string "title=$TITLE" \
        --form-string "priority=$PRIORITY" \
        https://api.pushover.net/1/messages.json 2>/dev/null &
fi

# Wait for background jobs to complete
wait

exit 0
