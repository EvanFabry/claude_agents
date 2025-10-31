#!/usr/bin/env python3

"""
PostToolUse Analytics Hook - Task Duration Completion
Calculates task duration and logs completion data for analytics.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import glob

def parse_iso_timestamp(timestamp_str):
    """Parse ISO timestamp string to datetime object."""
    try:
        # Handle both with and without Z suffix
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        return datetime.fromisoformat(timestamp_str)
    except:
        # Fallback to current time if parsing fails
        return datetime.now(timezone.utc)

def calculate_duration_seconds(start_time, end_time):
    """Calculate duration in seconds between two timestamps."""
    try:
        start_dt = parse_iso_timestamp(start_time)
        end_dt = parse_iso_timestamp(end_time)
        return (end_dt - start_dt).total_seconds()
    except:
        return 0

def main():
    """Log task completion and calculate duration."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Only track Task tool events
        if input_data.get('tool_name') != 'Task':
            sys.exit(0)

        # Extract key data
        session_id = input_data.get('session_id', 'unknown')
        tool_input = input_data.get('tool_input', {})
        tool_response = input_data.get('tool_response', {})
        subagent_type = tool_input.get('subagent_type', 'unknown')
        description = tool_input.get('description', 'unknown')
        end_timestamp = datetime.utcnow().isoformat() + 'Z'

        # Extract response metrics
        total_duration_ms = tool_response.get('totalDurationMs', 0)
        total_tokens = tool_response.get('totalTokens', 0)
        total_tool_use_count = tool_response.get('totalToolUseCount', 0)
        usage = tool_response.get('usage', {})

        # Set up analytics directory
        analytics_dir = Path.cwd() / '.claude' / 'hooks' / 'analytics'
        analytics_dir.mkdir(parents=True, exist_ok=True)

        # Look for corresponding start file
        start_pattern = f'.task_start_{session_id}_{subagent_type}'
        start_files = list(analytics_dir.glob(start_pattern))

        start_timestamp = None
        duration_seconds = 0

        if start_files:
            start_file = start_files[0]  # Take the first match
            try:
                with open(start_file, 'r') as f:
                    start_data = json.load(f)
                    start_timestamp = start_data.get('start_timestamp')
                    if start_timestamp:
                        duration_seconds = calculate_duration_seconds(start_timestamp, end_timestamp)

                # Clean up start file
                start_file.unlink(missing_ok=True)
            except Exception as e:
                print(f"[ANALYTICS] Error processing start file: {e}", file=sys.stderr)

        # Determine success status based on tool response
        success = not bool(tool_response.get('error'))  # No error means success

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

        # Create completion analytics entry
        analytics_entry = {
            'timestamp': end_timestamp,
            'event_type': 'TaskComplete',
            'session_id': session_id,
            'subagent_type': subagent_type,
            'description': description,
            'duration_seconds': duration_seconds,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'success': success,
            'metrics': {
                'total_duration_ms': total_duration_ms,
                'total_tokens': total_tokens,
                'total_tool_use_count': total_tool_use_count,
                'input_tokens': usage.get('input_tokens', 0),
                'output_tokens': usage.get('output_tokens', 0),
                'cache_read_input_tokens': usage.get('cache_read_input_tokens', 0),
                'cache_creation_input_tokens': usage.get('cache_creation_input_tokens', 0)
            },
            'hook_event_name': input_data.get('hook_event_name'),
            'tool_name': input_data.get('tool_name'),
            'cwd': cwd,
            'permission_mode': input_data.get('permission_mode', 'default')
        }

        # Write to analytics log
        analytics_log = analytics_dir / 'task_analytics.jsonl'
        with open(analytics_log, 'a') as f:
            f.write(json.dumps(analytics_entry) + '\n')

        # Clean up any orphaned start files older than 1 hour
        try:
            import time
            current_time = time.time()
            for start_file in analytics_dir.glob('.task_start_*'):
                if current_time - start_file.stat().st_mtime > 3600:  # 1 hour
                    start_file.unlink(missing_ok=True)
        except Exception:
            pass  # Ignore cleanup errors

        # Exit successfully
        sys.exit(0)

    except Exception as e:
        print(f"[ANALYTICS POST ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()