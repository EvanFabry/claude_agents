#!/usr/bin/env python3

import sys
import json

# Read JSON input from stdin
try:
    hook_input = json.load(sys.stdin)
except json.JSONDecodeError:
    # If JSON parsing fails, allow the command (fail open)
    sys.exit(0)

# Extract tool information
tool_name = hook_input.get('tool_name', '')
tool_input = hook_input.get('tool_input', {})
bash_command = tool_input.get('command', '')

# Only validate Bash tool calls
if tool_name != 'Bash':
    sys.exit(0)

# Extract base command (first word) for early checking
base_command = bash_command.split()[0] if bash_command else ''

# Allow git and gh commands without further validation
# (they may contain dev server commands in commit messages or PR descriptions)
if base_command in ['git', 'gh']:
    sys.exit(0)

# Check for common dev server commands (server management)
# Add your project's dev server command here
dev_server_patterns = [
    'npm run dev',
    'pnpm dev',
    'yarn dev',
    'bun dev',
    # Add your custom dev command here if different
]

if any(pattern in bash_command for pattern in dev_server_patterns):
    error_message = f"""❌ BLOCKED: Bash("{bash_command}")

Error: Development server management forbidden
- Command: {bash_command}
- Reason: Development server management should only be performed by our testing infrastructure, never done directly

Development servers are managed by:
  ✅ testing-agent automatically handles server lifecycle
  ✅ Server starts/stops/restarts managed by testing infrastructure
  ✅ Port management and cleanup handled automatically

Forbidden patterns:
  ❌ Bash("npm run dev")
  ❌ Bash("pnpm dev")
  ❌ Bash("[YOUR_DEV_COMMAND]")

If you need to test the application:
  - Use testing-agent which manages server lifecycle automatically
  - testing-agent starts server, runs tests, and stops server
  - No manual server management required

See CLAUDE.md Section II for browser configuration and testing infrastructure details.
"""

    # Write error to stderr and exit with code 2 to block execution
    sys.stderr.write(error_message)
    sys.exit(2)

# Check other disallowed commands
disallowed_commands = ['cd', 'npm', 'node', 'cat']
if base_command in disallowed_commands:
    error_message = f"""❌ BLOCKED: Bash("{bash_command}")

Error: Forbidden Bash command
- Command: {bash_command}
- Reason: Only 'pnpm' and 'git' commands allowed

Allowed patterns:
  ✅ Bash("pnpm typecheck")
  ✅ Bash("pnpm exec tsx script.ts")
  ✅ Bash("git status")
  ✅ Bash("git commit -m 'message'")

Forbidden patterns:
  ❌ Bash("cd directory")
  ❌ Bash("npm install")
  ❌ Bash("node script.js")
  ❌ Bash("cat file.txt")

Use specialized tools instead:
  - File operations: Read, Write, Edit, Glob tools
  - Network: WebFetch tool
  - Complex operations: Write a .ts script, execute with 'pnpm exec tsx script.ts'

See .claude/tools/README.md for complete documentation.
"""

    # Write error to stderr and exit with code 2 to block execution
    sys.stderr.write(error_message)
    sys.exit(2)

# Allow all other commands with exit code 0
sys.exit(0)
