#!/usr/bin/env python3

"""
PreToolUse Hook - Simple Payload Logger
Logs full payload from Task tool invocations to a file.
"""

import json
import sys
from pathlib import Path

def main():
    """Main hook logic - just log the full payload."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Set up log file
        log_dir = Path.cwd() / '.claude' / 'observability'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'pre_tool_use.jsonl'

        # Write full payload as a single line to the file
        with open(log_path, 'a') as f:
            f.write(json.dumps(input_data) + '\n')

        # Exit successfully to allow tool execution to proceed
        sys.exit(0)

    except Exception as e:
        print(f"[PRETOOLUSE ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()