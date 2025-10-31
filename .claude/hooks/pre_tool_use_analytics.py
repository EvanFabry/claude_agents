#!/usr/bin/env python3

"""
PreToolUse Analytics Hook - Task Duration Tracking
Tracks the start time of Task tool invocations for analytics.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def main():
    """Log task start times for duration analysis."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        print(f"{{\"systemMessage\": \"Running {input_data.get('tool_name')}...\"}}")

        # Only track Task tool events
        if input_data.get('tool_name') != 'Task':
            sys.exit(0)

        # Extract key data
        session_id = input_data.get('session_id', 'unknown')
        tool_input = input_data.get('tool_input', {})
        subagent_type = tool_input.get('subagent_type', 'unknown')
        description = tool_input.get('description', 'unknown')
        timestamp = datetime.utcnow().isoformat() + 'Z'

        # Set up analytics directory
        analytics_dir = Path.cwd() / '.claude' / 'hooks' / 'analytics'
        analytics_dir.mkdir(parents=True, exist_ok=True)

        # Convert absolute path to relative path for privacy
        cwd = input_data.get('cwd', '')
        try:
            # Try to convert to relative path from project root
            cwd_path = Path(cwd)
            project_root = Path.cwd()
            if cwd_path.is_relative_to(project_root):
                cwd = str(cwd_path.relative_to(project_root))
            else:
                # If not within project, use basename
                cwd = cwd_path.name
        except (ValueError, AttributeError):
            # Fallback: use as-is or just directory name
            cwd = Path(cwd).name if cwd else ''

        # Create analytics entry
        analytics_entry = {
            'timestamp': timestamp,
            'event_type': 'TaskStart',
            'session_id': session_id,
            'subagent_type': subagent_type,
            'description': description,
            'hook_event_name': input_data.get('hook_event_name'),
            'tool_name': input_data.get('tool_name'),
            'cwd': cwd,
            'permission_mode': input_data.get('permission_mode', 'default')
        }

        # Write to analytics log
        analytics_log = analytics_dir / 'task_analytics.jsonl'
        with open(analytics_log, 'a') as f:
            f.write(json.dumps(analytics_entry) + '\n')

        # Create start tracking file for duration calculation
        start_file = analytics_dir / f'.task_start_{session_id}_{subagent_type}'
        start_data = {
            'start_timestamp': timestamp,
            'session_id': session_id,
            'subagent_type': subagent_type,
            'description': description
        }

        with open(start_file, 'w') as f:
            json.dump(start_data, f)

        # Exit successfully
        sys.exit(0)

    except Exception as e:
        print(f"[ANALYTICS PRE ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()