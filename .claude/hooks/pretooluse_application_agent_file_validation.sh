#!/bin/bash
# Enhanced PreToolUse hook for testing-agent agent
# Uses Claude Code 2.0 structured JSON responses for richer feedback
# Validates file creation patterns before tool execution

# Parse tool use from stdin
TOOL_USE=$(cat)

# Extract tool name
TOOL_NAME=$(echo "$TOOL_USE" | jq -r '.tool_name // empty')

# Check if this is a Bash command
if [ "$TOOL_NAME" = "Bash" ]; then
    COMMAND=$(echo "$TOOL_USE" | jq -r '.parameters.command // empty')

    # Detect file creation patterns in bash commands
    # Matches: cat >, echo >, > file.js, << EOF (heredoc)
    if echo "$COMMAND" | grep -qE '(cat[^|]*>|echo[^|]*>|\s>\s*["\047]?[\w/.-]+\.(js|ts|json|md|txt|sh)|<<\s*["\047]?[A-Z_]+)'; then
        # Return structured JSON denial
        cat <<EOF
{
  "permissionDecision": "deny",
  "permissionDecisionReason": "File creation must use Write tool, not Bash. Bash should only execute existing files.",
  "systemMessage": "⚠️ TOOL CONSTRAINT VIOLATION DETECTED\n\n❌ Attempted: Bash file creation\n✅ Required Pattern:\n   Step 1: Write(file_path='testing_agent/scripts/test.js', content='...')\n   Step 2: Bash(command='node testing_agent/scripts/test.js')\n\n🚫 Blocked command:\n   ${COMMAND}\n\nℹ️ Use Write tool first to create files, then Bash to execute them.\nSee @testing-agent.md lines 68-77 for details.",
  "suppressOutput": false
}
EOF
        exit 0  # Exit 0 with JSON denial
    fi
fi

# Allow tool use - return success JSON
cat <<EOF
{
  "permissionDecision": "allow",
  "permissionDecisionReason": "Tool use validated - no file creation detected",
  "suppressOutput": true
}
EOF
exit 0