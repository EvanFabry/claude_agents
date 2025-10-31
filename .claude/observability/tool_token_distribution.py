#!/usr/bin/env python3
"""
Analyze token size and duration distribution for tool calls over the last 5 hours.
This script processes JSONL logs and shows per-tool statistics including token usage
and call duration distributions. Also tracks permission blocking time for tools that
require user approval and conversation compaction timing.
"""

import json
import os
import glob
import argparse
import numpy as np
from datetime import datetime, timedelta, timezone
from collections import Counter
from typing import Dict, List, Tuple

# Tools that typically require user permission approval
PERMISSION_SENSITIVE_TOOLS = {
    'ExitPlanMode',  # Always requires approval to exit plan mode
    'Bash',          # Most bash commands require approval (unless in allowed-tools)
    'Edit',          # File edits require approval
    'Write',         # File writes require approval
    'NotebookEdit',  # Notebook edits require approval
    'Task',          # Subagent tasks may require approval
    'MultiEdit',     # Multi-file edits require approval
    # Note: Tools like Read, Grep, Glob, WebSearch, WebFetch are typically auto-approved
}

# Threshold for detecting permission blocking (seconds)
# Tool calls longer than this for permission-sensitive tools are likely blocked on user approval
DEFAULT_PERMISSION_THRESHOLD = 5.0

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string to datetime object."""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def format_tool_call(tool_name: str, tool_input: dict) -> str:
    """
    Format tool call with relevant parameters for better analysis.
    Only expands Bash commands to show first argument, and Task to show subagent type.

    Args:
        tool_name: Name of the tool (e.g., "Bash", "Read", "Edit")
        tool_input: Input parameters dict for the tool

    Returns:
        Formatted string like "Bash(vercel...)" or "Task (agent-name)", plain tool name for others
    """
    if not tool_input:
        return tool_name

    try:
        if tool_name == 'Bash':
            # Extract first command word from bash command
            command = tool_input.get('command', '')
            if command:
                first_word = command.split()[0] if command.split() else command[:20]
                return f"Bash({first_word}...)"

        elif tool_name == 'Task':
            # For Task, include subagent type
            subagent_type = tool_input.get('subagent_type')
            if subagent_type:
                return f"Task ({subagent_type})"

    except Exception:
        # If any formatting fails, just return the tool name
        pass

    return tool_name

def extract_tool_token_data(filepath: str, tool_name: str | None, cutoff_time: datetime) -> Tuple[List[Dict], Dict[str, datetime], List[Dict]]:
    """
    Extract token usage data for a specific tool (or all tools if tool_name is None) from a JSONL file.
    Returns tuple of (tool_data list, tool_call_starts dict mapping tool_id to start timestamp, compaction_events list).
    """
    tool_data = []
    tool_call_starts = {}  # Map tool_id -> start timestamp
    compaction_events = []  # Track compaction events

    print(f"Analyzing: {os.path.basename(filepath)}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            line_count = 0
            prev_timestamp = None
            for line in f:
                line_count += 1
                try:
                    data = json.loads(line.strip())

                    # Extract timestamp
                    if 'timestamp' not in data:
                        continue

                    timestamp = parse_timestamp(data['timestamp'])
                    if timestamp < cutoff_time:
                        prev_timestamp = timestamp
                        continue

                    # Track compaction events
                    if (data.get('type') == 'system' and
                        data.get('subtype') == 'compact_boundary'):
                        compact_metadata = data.get('compactMetadata', {})
                        compaction_events.append({
                            'timestamp': timestamp,
                            'trigger': compact_metadata.get('trigger'),
                            'pre_tokens': compact_metadata.get('preTokens'),
                            'file_source': os.path.basename(filepath),
                            'prev_timestamp': prev_timestamp
                        })

                    # Look for tool usage in message content
                    if 'message' in data and isinstance(data['message'], dict):
                        content = data['message'].get('content', [])
                        if isinstance(content, list):
                            for item in content:
                                # Track tool_use (start of call)
                                if (isinstance(item, dict) and
                                    item.get('type') == 'tool_use' and
                                    (tool_name is None or item.get('name') == tool_name)):

                                    tool_id = item.get('id')
                                    if tool_id:
                                        tool_call_starts[tool_id] = timestamp

                                    # Extract usage info if available
                                    usage = None
                                    if 'usage' in data['message']:
                                        usage = data['message']['usage']
                                    elif 'usage' in data:
                                        usage = data['usage']

                                    if usage:
                                        input_tokens = usage.get('input_tokens', 0)
                                        cache_read_tokens = usage.get('cache_read_input_tokens', 0)
                                        output_tokens = usage.get('output_tokens', 0)
                                        total_tokens = input_tokens + cache_read_tokens + output_tokens

                                        # Format tool name with relevant parameters for better analysis
                                        base_tool_name = item.get('name')
                                        tool_input = item.get('input', {})
                                        effective_tool_name = format_tool_call(base_tool_name, tool_input)

                                        tool_data.append({
                                            'timestamp': timestamp,
                                            'tool_id': tool_id,
                                            'tool_name': effective_tool_name,
                                            'base_tool_name': base_tool_name,  # For permission analysis
                                            'input_tokens': input_tokens,
                                            'cache_read_input_tokens': cache_read_tokens,
                                            'output_tokens': output_tokens,
                                            'total_tokens': total_tokens,
                                            'duration_sec': None,  # Will be filled when we find tool_result
                                            'is_permission_sensitive': base_tool_name in PERMISSION_SENSITIVE_TOOLS,
                                            'file_source': os.path.basename(filepath)
                                        })

                                # Track tool_result (end of call) to calculate duration
                                elif (isinstance(item, dict) and
                                      item.get('type') == 'tool_result'):
                                    tool_id = item.get('tool_use_id')
                                    if tool_id and tool_id in tool_call_starts:
                                        start_time = tool_call_starts[tool_id]
                                        duration_sec = (timestamp - start_time).total_seconds()

                                        # Find the corresponding tool_data entry and update duration
                                        for tool_entry in reversed(tool_data):
                                            if tool_entry.get('tool_id') == tool_id:
                                                tool_entry['duration_sec'] = duration_sec
                                                break

                    prev_timestamp = timestamp

                except json.JSONDecodeError as e:
                    print(f"  Warning: Failed to parse line {line_count}: {e}")
                    continue
                except Exception as e:
                    print(f"  Warning: Error processing line {line_count}: {e}")
                    continue

    except Exception as e:
        print(f"  Error reading file: {e}")
        return [], {}, []

    if tool_name:
        print(f"  Found {len(tool_data)} {tool_name} calls with token data")
    else:
        print(f"  Found {len(tool_data)} tool calls with token data")
    if compaction_events:
        print(f"  Found {len(compaction_events)} compaction events")
    return tool_data, tool_call_starts, compaction_events

def calculate_distribution_stats(token_counts: List[int]) -> Dict:
    """Calculate distribution statistics for token counts."""
    if not token_counts:
        return {}

    token_array = np.array(token_counts)

    return {
        'count': len(token_counts),
        'min': int(np.min(token_array)),
        'max': int(np.max(token_array)),
        'mean': float(np.mean(token_array)),
        'median': float(np.median(token_array)),
        'std': float(np.std(token_array)),
        'p25': float(np.percentile(token_array, 25)),
        'p75': float(np.percentile(token_array, 75)),
        'p90': float(np.percentile(token_array, 90)),
        'p95': float(np.percentile(token_array, 95)),
        'p99': float(np.percentile(token_array, 99))
    }


def analyze_permission_blocking(tool_data: List[Dict], permission_threshold: float) -> Dict:
    """
    Analyze permission blocking time from tool call durations.

    Args:
        tool_data: List of tool call data with duration_sec and is_permission_sensitive fields
        permission_threshold: Minimum duration (seconds) to consider a permission block

    Returns:
        Dictionary with permission blocking statistics
    """
    permission_blocks = []

    for call in tool_data:
        # Only analyze permission-sensitive tools with valid durations
        if (call.get('is_permission_sensitive') and
            call.get('duration_sec') is not None and
            call['duration_sec'] >= permission_threshold):

            permission_blocks.append({
                'tool_name': call['tool_name'],
                'base_tool_name': call['base_tool_name'],
                'duration_sec': call['duration_sec'],
                'timestamp': call['timestamp'],
                'file_source': call['file_source']
            })

    if not permission_blocks:
        return {
            'total_blocks': 0,
            'total_blocking_time_sec': 0,
            'total_blocking_time_min': 0,
            'avg_blocking_time_sec': 0,
            'max_blocking_time_sec': 0,
            'blocks_by_tool': {},
            'individual_blocks': []
        }

    durations = [b['duration_sec'] for b in permission_blocks]
    total_time_sec = sum(durations)

    # Group by base tool name
    blocks_by_tool = {}
    for block in permission_blocks:
        base_name = block['base_tool_name']
        if base_name not in blocks_by_tool:
            blocks_by_tool[base_name] = {
                'count': 0,
                'total_time_sec': 0,
                'durations': []
            }
        blocks_by_tool[base_name]['count'] += 1
        blocks_by_tool[base_name]['total_time_sec'] += block['duration_sec']
        blocks_by_tool[base_name]['durations'].append(block['duration_sec'])

    # Calculate averages for each tool
    for tool_stats in blocks_by_tool.values():
        tool_stats['avg_time_sec'] = tool_stats['total_time_sec'] / tool_stats['count']

    return {
        'total_blocks': len(permission_blocks),
        'total_blocking_time_sec': total_time_sec,
        'total_blocking_time_min': total_time_sec / 60,
        'avg_blocking_time_sec': np.mean(durations),
        'max_blocking_time_sec': max(durations),
        'blocks_by_tool': blocks_by_tool,
        'individual_blocks': permission_blocks
    }


def analyze_compaction_timing(compaction_events: List[Dict]) -> Dict:
    """
    Analyze conversation compaction timing and derive duration estimates.

    Args:
        compaction_events: List of compaction events with timestamps

    Returns:
        Dictionary with compaction timing statistics
    """
    if not compaction_events:
        return {
            'total_compactions': 0,
            'total_compaction_time_sec': 0,
            'total_compaction_time_min': 0,
            'avg_compaction_time_sec': 0,
            'max_compaction_time_sec': 0,
            'compactions': []
        }

    # Sort by timestamp
    sorted_events = sorted(compaction_events, key=lambda x: x['timestamp'])

    # Calculate compaction durations by looking at the gap from prev_timestamp to compaction timestamp
    compactions_with_duration = []
    durations = []

    for event in sorted_events:
        if event.get('prev_timestamp'):
            # Duration is from previous message to compaction boundary
            duration_sec = (event['timestamp'] - event['prev_timestamp']).total_seconds()
            compactions_with_duration.append({
                'timestamp': event['timestamp'],
                'trigger': event.get('trigger'),
                'pre_tokens': event.get('pre_tokens'),
                'duration_sec': duration_sec,
                'file_source': event.get('file_source')
            })
            durations.append(duration_sec)
        else:
            # No previous timestamp available
            compactions_with_duration.append({
                'timestamp': event['timestamp'],
                'trigger': event.get('trigger'),
                'pre_tokens': event.get('pre_tokens'),
                'duration_sec': None,
                'file_source': event.get('file_source')
            })

    if not durations:
        return {
            'total_compactions': len(compaction_events),
            'total_compaction_time_sec': 0,
            'total_compaction_time_min': 0,
            'avg_compaction_time_sec': 0,
            'max_compaction_time_sec': 0,
            'compactions': compactions_with_duration
        }

    total_time_sec = sum(durations)

    return {
        'total_compactions': len(compaction_events),
        'compactions_with_duration': len(durations),
        'total_compaction_time_sec': total_time_sec,
        'total_compaction_time_min': total_time_sec / 60,
        'avg_compaction_time_sec': np.mean(durations),
        'median_compaction_time_sec': np.median(durations),
        'max_compaction_time_sec': max(durations),
        'min_compaction_time_sec': min(durations),
        'compactions': compactions_with_duration
    }


def main():
    parser = argparse.ArgumentParser(
        description='Analyze token size and duration distribution for tool calls'
    )
    parser.add_argument('tool_name', nargs='?', help='Name of the tool to analyze (e.g., "grep", "edit_files"). If omitted, analyzes all tools.')
    parser.add_argument('--hours', type=int, default=5,
                       help='Hours to look back (default: 5)')
    parser.add_argument('--permission-threshold', type=float, default=DEFAULT_PERMISSION_THRESHOLD,
                       help=f'Threshold in seconds for detecting permission blocks (default: {DEFAULT_PERMISSION_THRESHOLD})')
    parser.add_argument('--permission-only', action='store_true',
                       help='Show only permission blocking analysis')
    parser.add_argument('--show-blocked-calls', action='store_true',
                       help='List individual permission-blocked calls with timestamps')
    parser.add_argument('--compaction-only', action='store_true',
                       help='Show only conversation compaction analysis')
    parser.add_argument('--show-compactions', action='store_true',
                       help='List individual compaction events with timestamps')

    args = parser.parse_args()

    # Get all JSONL files
    # Default to current project's Claude logs directory
    # Override with CLAUDE_LOG_DIR environment variable if set
    default_log_dir = os.path.expanduser("~/.claude/projects")
    log_dir = os.environ.get('CLAUDE_LOG_DIR', default_log_dir)

    # If using default, try to auto-detect project directory
    if log_dir == default_log_dir:
        # List all project directories and use the most recent one
        project_dirs = glob.glob(os.path.join(log_dir, "*"))
        if project_dirs:
            # Sort by modification time and use most recent
            log_dir = max(project_dirs, key=os.path.getmtime)
            print(f"Auto-detected log directory: {log_dir}")

    jsonl_files = glob.glob(os.path.join(log_dir, "*.jsonl"))
    
    if not jsonl_files:
        print(f"No JSONL files found in {log_dir}")
        return
    
    print(f"Found {len(jsonl_files)} JSONL files")
    if args.tool_name:
        print(f"Analyzing '{args.tool_name}' calls in the last {args.hours} hours")
    else:
        print(f"Analyzing all tool calls in the last {args.hours} hours")
    print("=" * 60)
    
    # Calculate cutoff time
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(hours=args.hours)
    
    print(f"Current time: {now}")
    print(f"Cutoff time: {cutoff_time}")
    print()
    
    # Extract all tool token data and compaction events
    all_tool_data = []
    all_compaction_events = []
    for filepath in jsonl_files:
        tool_data, _, compaction_events = extract_tool_token_data(filepath, args.tool_name, cutoff_time)
        all_tool_data.extend(tool_data)
        all_compaction_events.extend(compaction_events)
    
    if not all_tool_data:
        if args.tool_name:
            print(f"No {args.tool_name} calls found in the specified time period")
        else:
            print(f"No tool calls found in the specified time period")
        return

    # Count calls by tool
    tool_counts = Counter(call['tool_name'] for call in all_tool_data)

    print(f"\nTotal tool calls found: {len(all_tool_data)}")
    print(f"Unique tools: {len(tool_counts)}")

    # Group data by tool
    tools_to_analyze = [args.tool_name] if args.tool_name else sorted(tool_counts.keys())

    # Collect summary data for table
    summary_rows = []

    for tool_name in tools_to_analyze:
        tool_data = [call for call in all_tool_data if call['tool_name'] == tool_name]

        if not tool_data:
            continue

        total_tokens_list = [call['total_tokens'] for call in tool_data]
        duration_list = [call['duration_sec'] for call in tool_data if call['duration_sec'] is not None]

        token_stats = calculate_distribution_stats(total_tokens_list)
        duration_stats = calculate_distribution_stats(duration_list) if duration_list else None

        # Calculate total tokens consumed for sorting
        total_tokens_consumed = sum(total_tokens_list)

        summary_rows.append({
            'tool_name': tool_name,
            'calls': len(tool_data),
            'latency_p50': duration_stats['median'] if duration_stats else None,
            'latency_mean': duration_stats['mean'] if duration_stats else None,
            'latency_p99': duration_stats['p99'] if duration_stats else None,
            'tokens_p50': token_stats['median'] if token_stats else None,
            'tokens_mean': token_stats['mean'] if token_stats else None,
            'tokens_p95': token_stats['p95'] if token_stats else None,
            'total_tokens_consumed': total_tokens_consumed,
        })

    # Sort by total tokens consumed (descending)
    summary_rows.sort(key=lambda x: x['total_tokens_consumed'], reverse=True)

    # Print summary table (skip if --permission-only or --compaction-only is specified)
    if not args.permission_only and not args.compaction_only:
        print("\n" + "=" * 175)
        print("TOOL PERFORMANCE SUMMARY")
        print("=" * 175)
        print(f"{'Tool':<45} {'Calls':>7} {'Total Tok':>12} {'Tok P50':>10} {'E(Tok)':>10} {'Tok P95':>10} {'Lat P50':>10} {'E(Lat)':>10} {'Lat P99':>10}")
        print(f"{'':45} {'':>7} {'':>12} {'':>10} {'':>10} {'':>10} {'(sec)':>10} {'(sec)':>10} {'(sec)':>10}")
        print("-" * 175)

        for row in summary_rows:
            tool_name = row['tool_name']
            if len(tool_name) > 44:
                tool_name = tool_name[:41] + "..."

            total_tok = f"{row['total_tokens_consumed']:,}"
            tok_p50 = f"{row['tokens_p50']:,.0f}" if row['tokens_p50'] is not None else "N/A"
            tok_mean = f"{row['tokens_mean']:,.0f}" if row['tokens_mean'] is not None else "N/A"
            tok_p95 = f"{row['tokens_p95']:,.0f}" if row['tokens_p95'] is not None else "N/A"
            lat_p50 = f"{row['latency_p50']:.2f}" if row['latency_p50'] is not None else "N/A"
            lat_mean = f"{row['latency_mean']:.2f}" if row['latency_mean'] is not None else "N/A"
            lat_p99 = f"{row['latency_p99']:.2f}" if row['latency_p99'] is not None else "N/A"

            print(f"{tool_name:<45} {row['calls']:>7} {total_tok:>12} {tok_p50:>10} {tok_mean:>10} {tok_p95:>10} {lat_p50:>10} {lat_mean:>10} {lat_p99:>10}")

        print("=" * 175)

    # Perform permission blocking analysis (skip if --compaction-only is specified)
    if not args.compaction_only:
        permission_stats = analyze_permission_blocking(all_tool_data, args.permission_threshold)
    else:
        permission_stats = {'total_blocks': 0}

    if permission_stats['total_blocks'] > 0 or args.permission_only:
        print("\n" + "=" * 120)
        print("PERMISSION BLOCKING ANALYSIS")
        print("=" * 120)
        print(f"Permission Threshold: {args.permission_threshold}s (tool calls >= this duration are considered permission-blocked)")
        print(f"Total Permission Blocks: {permission_stats['total_blocks']} calls")
        print(f"Total Blocking Time: {permission_stats['total_blocking_time_min']:.2f} minutes ({permission_stats['total_blocking_time_sec']:.1f} seconds)")

        if permission_stats['total_blocks'] > 0:
            print(f"Average Approval Time: {permission_stats['avg_blocking_time_sec']:.1f} seconds")
            print(f"Longest Block: {permission_stats['max_blocking_time_sec']:.1f} seconds")

            # Show per-tool breakdown
            if permission_stats['blocks_by_tool']:
                print("\n" + "-" * 120)
                print("TOP PERMISSION-BLOCKING TOOLS:")
                print(f"{'Tool':<25} {'Blocks':>8} {'Total Time':>12} {'Avg Time':>12} {'Max Time':>12}")
                print(f"{'':25} {'':>8} {'(min)':>12} {'(sec)':>12} {'(sec)':>12}")
                print("-" * 120)

                # Sort by total blocking time
                sorted_tools = sorted(
                    permission_stats['blocks_by_tool'].items(),
                    key=lambda x: x[1]['total_time_sec'],
                    reverse=True
                )

                for tool_name, stats in sorted_tools:
                    total_min = stats['total_time_sec'] / 60
                    avg_sec = stats['avg_time_sec']
                    max_sec = max(stats['durations'])

                    print(f"{tool_name:<25} {stats['count']:>8} {total_min:>12.2f} {avg_sec:>12.1f} {max_sec:>12.1f}")

            # Show individual blocked calls if requested
            if args.show_blocked_calls:
                print("\n" + "-" * 120)
                print("INDIVIDUAL PERMISSION-BLOCKED CALLS:")
                print(f"{'Timestamp':<28} {'Tool':<30} {'Duration':<12} {'Source File':<40}")
                print("-" * 120)

                # Sort by duration (longest first)
                sorted_blocks = sorted(
                    permission_stats['individual_blocks'],
                    key=lambda x: x['duration_sec'],
                    reverse=True
                )

                for block in sorted_blocks:
                    ts_str = block['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    duration_str = f"{block['duration_sec']:.1f}s"
                    tool_name = block['tool_name']
                    if len(tool_name) > 29:
                        tool_name = tool_name[:26] + "..."
                    source_file = block['file_source']
                    if len(source_file) > 39:
                        source_file = source_file[:36] + "..."

                    print(f"{ts_str:<28} {tool_name:<30} {duration_str:<12} {source_file:<40}")

        print("=" * 120)

    # Perform conversation compaction analysis
    compaction_stats = analyze_compaction_timing(all_compaction_events)

    if compaction_stats['total_compactions'] > 0 or args.compaction_only:
        print("\n" + "=" * 120)
        print("CONVERSATION COMPACTION ANALYSIS")
        print("=" * 120)
        print(f"Total Compaction Events: {compaction_stats['total_compactions']}")
        print(f"Compactions with Duration Data: {compaction_stats.get('compactions_with_duration', 0)}")
        print(f"Total Compaction Time: {compaction_stats['total_compaction_time_min']:.2f} minutes ({compaction_stats['total_compaction_time_sec']:.1f} seconds)")

        if compaction_stats.get('compactions_with_duration', 0) > 0:
            print(f"Average Compaction Duration: {compaction_stats['avg_compaction_time_sec']:.1f} seconds")
            print(f"Median Compaction Duration: {compaction_stats['median_compaction_time_sec']:.1f} seconds")
            print(f"Min Compaction Duration: {compaction_stats['min_compaction_time_sec']:.1f} seconds")
            print(f"Max Compaction Duration: {compaction_stats['max_compaction_time_sec']:.1f} seconds")

            # Show individual compaction events if requested
            if args.show_compactions:
                print("\n" + "-" * 120)
                print("INDIVIDUAL COMPACTION EVENTS:")
                print(f"{'Timestamp':<28} {'Trigger':<10} {'Pre-Tokens':>12} {'Duration':<12} {'Source File':<40}")
                print("-" * 120)

                # Sort by duration (longest first)
                sorted_compactions = sorted(
                    [c for c in compaction_stats['compactions'] if c.get('duration_sec') is not None],
                    key=lambda x: x['duration_sec'],
                    reverse=True
                )

                for compaction in sorted_compactions:
                    ts_str = compaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    trigger = compaction.get('trigger', 'N/A')
                    pre_tokens = f"{compaction.get('pre_tokens', 0):,}"
                    duration_str = f"{compaction['duration_sec']:.1f}s"
                    source_file = compaction['file_source']
                    if len(source_file) > 39:
                        source_file = source_file[:36] + "..."

                    print(f"{ts_str:<28} {trigger:<10} {pre_tokens:>12} {duration_str:<12} {source_file:<40}")

        print("=" * 120)

if __name__ == "__main__":
    main()