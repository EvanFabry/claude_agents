#!/usr/bin/env python3
"""
Analyze tool call frequency per agent type to identify which agents are making excessive tool calls.
Processes JSONL logs to count tool calls within each agent session.
"""

import json
import os
import glob
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Dict, List

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string to datetime object."""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def format_tool_call(tool_name: str, tool_input: dict) -> str:
    """
    Format tool call with relevant parameters for better analysis.
    Only expands Bash commands to show first argument.

    Args:
        tool_name: Name of the tool (e.g., "Bash", "Read", "Edit")
        tool_input: Input parameters dict for the tool

    Returns:
        Formatted string like "Bash(vercel...)" for Bash, plain tool name for others
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

    except Exception:
        # If any formatting fails, just return the tool name
        pass

    return tool_name

def analyze_agent_tool_calls(filepath: str, cutoff_time: datetime) -> Dict:
    """
    Extract tool call patterns per agent session.
    Returns dict mapping agent_type -> list of (tool_calls_count, session_info)
    """
    agent_sessions = defaultdict(list)
    current_agent = None
    current_session_tools = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())

                    if 'timestamp' not in data:
                        continue

                    timestamp = parse_timestamp(data['timestamp'])
                    if timestamp < cutoff_time:
                        continue

                    # Check for agent session markers
                    if 'message' in data and isinstance(data['message'], dict):
                        role = data['message'].get('role')
                        content = data['message'].get('content', [])

                        # Look for Task tool calls (agent delegation)
                        if isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and item.get('type') == 'tool_use':
                                    tool_name = item.get('name')

                                    # Track when Task tool is called (agent delegation starts)
                                    if tool_name == 'Task':
                                        # Save previous agent session if exists
                                        if current_agent and current_session_tools:
                                            agent_sessions[current_agent].append({
                                                'tool_count': len(current_session_tools),
                                                'tools': current_session_tools.copy(),
                                                'timestamp': timestamp
                                            })

                                        # Extract subagent type from parameters
                                        params = item.get('input', {})
                                        current_agent = params.get('subagent_type', 'unknown')
                                        current_session_tools = []

                                    # Track tool calls within current agent session
                                    elif current_agent:
                                        tool_input = item.get('input', {})
                                        formatted_tool = format_tool_call(tool_name, tool_input)
                                        current_session_tools.append(formatted_tool)

                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    continue

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return {}

    # Save final session if exists
    if current_agent and current_session_tools:
        agent_sessions[current_agent].append({
            'tool_count': len(current_session_tools),
            'tools': current_session_tools,
            'timestamp': timestamp
        })

    return agent_sessions

def main():
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

    print(f"Analyzing {len(jsonl_files)} JSONL files for agent tool call patterns")
    print("=" * 80)

    # Analyze last 72 hours
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=72)

    all_agent_sessions = defaultdict(list)

    for filepath in jsonl_files:
        file_sessions = analyze_agent_tool_calls(filepath, cutoff_time)
        for agent_type, sessions in file_sessions.items():
            all_agent_sessions[agent_type].extend(sessions)

    if not all_agent_sessions:
        print("No agent sessions found in the analyzed period")
        return

    # Calculate statistics per agent type
    print("\n" + "=" * 80)
    print("TOOL CALL FREQUENCY BY AGENT TYPE (Last 72 Hours)")
    print("=" * 80)

    agent_stats = []

    for agent_type, sessions in all_agent_sessions.items():
        tool_counts = [s['tool_count'] for s in sessions]

        if not tool_counts:
            continue

        avg_tools = sum(tool_counts) / len(tool_counts)
        max_tools = max(tool_counts)
        min_tools = min(tool_counts)

        # Count tool usage frequency
        all_tools = []
        for s in sessions:
            all_tools.extend(s['tools'])

        from collections import Counter
        tool_freq = Counter(all_tools)
        top_tools = tool_freq.most_common(5)

        agent_stats.append({
            'agent': agent_type,
            'sessions': len(sessions),
            'avg_tools': avg_tools,
            'max_tools': max_tools,
            'min_tools': min_tools,
            'top_tools': top_tools
        })

    # Sort by average tool count (descending)
    agent_stats.sort(key=lambda x: x['avg_tools'], reverse=True)

    print(f"\n{'Agent Type':<40} {'Sessions':<10} {'Avg Tools':<12} {'Max':<8} {'Min':<8}")
    print("-" * 80)

    for stat in agent_stats:
        print(f"{stat['agent']:<40} {stat['sessions']:<10} {stat['avg_tools']:<12.1f} {stat['max_tools']:<8} {stat['min_tools']:<8}")

    # Show top tools per agent
    print("\n" + "=" * 80)
    print("TOP TOOLS USED BY EACH AGENT")
    print("=" * 80)

    for stat in agent_stats:
        print(f"\n{stat['agent']}:")
        for tool, count in stat['top_tools']:
            print(f"  {tool:<30} {count:>5} calls")

    # Summary
    print("\n" + "=" * 80)
    print("FINDINGS")
    print("=" * 80)

    high_tool_agents = [s for s in agent_stats if s['avg_tools'] > 20]
    if high_tool_agents:
        print(f"\n⚠️  Agents with >20 average tool calls per session:")
        for stat in high_tool_agents:
            print(f"  - {stat['agent']}: {stat['avg_tools']:.1f} avg tools ({stat['sessions']} sessions)")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
