#!/bin/bash
# Debug hook to capture actual PostToolUse JSON format

# Read stdin to a variable
INPUT=$(cat)

# Append to debug log with timestamp
echo "=== PostToolUse Debug $(date) ===" >> /tmp/claude_hook_debug.log
echo "$INPUT" | jq . >> /tmp/claude_hook_debug.log
echo "" >> /tmp/claude_hook_debug.log

# Also output to stderr for visibility
echo "[DEBUG] PostToolUse input logged to /tmp/claude_hook_debug.log" >&2

# Pass through - don't block
echo '{"suppressOutput": true}'
exit 0
