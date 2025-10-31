#!/bin/bash
# PreToolUse hook for testing-agent agent
# Validates Write/Edit operations are scoped to testing_agent/ directory only
# Prevents accidental modification of application code, configs, or documentation

# Parse tool use from stdin
TOOL_USE=$(cat)

# Extract tool name
TOOL_NAME=$(echo "$TOOL_USE" | jq -r '.tool_name // empty')

# Check if this is a Write, Edit, or MultiEdit operation
if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]] || [[ "$TOOL_NAME" == "MultiEdit" ]]; then
    # Extract file path (handle both single file and array of files)
    FILE_PATH=$(echo "$TOOL_USE" | jq -r '.parameters.file_path // .parameters.files[0] // empty')

    # Normalize path (remove leading ./ if present)
    FILE_PATH="${FILE_PATH#./}"

    # Check if file path is outside testing_agent/ directory
    if [[ ! "$FILE_PATH" =~ ^testing_agent/ ]]; then
        # Return structured JSON denial
        cat <<EOF
{
  "permissionDecision": "deny",
  "permissionDecisionReason": "Browser agent can only modify files in testing_agent/ directory. Application code, configs, and docs are off-limits.",
  "systemMessage": "⚠️ DIRECTORY SCOPE VIOLATION DETECTED\n\n❌ Attempted file operation: ${TOOL_NAME}\n📁 Target file: ${FILE_PATH}\n✅ Allowed directory: testing_agent/\n\n🔒 Security Constraint:\nBrowser agent is restricted to test scripts and outputs only.\nApplication code modification requires code-writing-agent.\n\nℹ️ Valid operations:\n  - testing_agent/scripts/*.js (test scripts)\n  - testing_agent/outputs/*.{json,png,txt} (test results)\n\nSee @testing-agent.md lines 48-67 for details.",
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
  "permissionDecisionReason": "File operation within allowed testing_agent/ scope",
  "suppressOutput": true
}
EOF
exit 0