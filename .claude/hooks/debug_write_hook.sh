#!/bin/bash
# Debug hook to test if PostToolUse triggers for Write operations

# Get the project root (hooks run from project root in Claude Code)
PROJECT_ROOT="$(pwd)"
DEBUG_LOG="$PROJECT_ROOT/.claude/hooks/debug_write_hook.log"

echo "=== PostToolUse Hook Triggered ===" >> "$DEBUG_LOG"
echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")" >> "$DEBUG_LOG"
echo "Input data:" >> "$DEBUG_LOG"
cat | tee -a "$DEBUG_LOG"
echo "" >> "$DEBUG_LOG"
echo "==================" >> "$DEBUG_LOG"

# Return proper JSON format per Claude Code docs
cat <<EOF
{
  "suppressOutput": true,
  "continue": true
}
EOF
exit 0
