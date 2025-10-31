#!/usr/bin/env python3

"""
Analytics Reporter - Task Duration and Success Rate Analysis
Analyzes collected task data and generates statistics tables.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
import argparse

def parse_iso_timestamp(timestamp_str):
    """Parse ISO timestamp string to datetime object."""
    try:
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        return datetime.fromisoformat(timestamp_str)
    except:
        return None

def load_analytics_data(analytics_file):
    """Load analytics data from JSONL file."""
    data = []
    if not analytics_file.exists():
        return data

    try:
        with open(analytics_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        # Parse timestamp
                        timestamp = parse_iso_timestamp(entry.get('timestamp', ''))
                        if timestamp:
                            entry['parsed_timestamp'] = timestamp
                            data.append(entry)
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Error loading analytics data: {e}", file=sys.stderr)

    return data

def filter_by_timeframe(data, hours=None):
    """Filter data by timeframe (last N hours, or all time if None)."""
    if hours is None:
        return data

    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    return [entry for entry in data if entry.get('parsed_timestamp', datetime.min.replace(tzinfo=timezone.utc)) >= cutoff_time]

def calculate_statistics(data):
    """Calculate comprehensive statistics from analytics data."""
    # Filter for task completion events only
    completion_events = [entry for entry in data if entry.get('event_type') == 'TaskComplete']

    if not completion_events:
        return {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'success_rate': 0.0,
            'avg_duration': 0.0,
            'median_duration': 0.0,
            'min_duration': 0.0,
            'max_duration': 0.0,
            'total_tokens': 0,
            'avg_tokens_per_task': 0.0,
            'by_agent': {},
            'by_description': {}
        }

    # Basic metrics
    total_tasks = len(completion_events)
    successful_tasks = sum(1 for event in completion_events if event.get('success', False))
    failed_tasks = total_tasks - successful_tasks
    success_rate = (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    # Duration metrics
    durations = [event.get('duration_seconds', 0) for event in completion_events if event.get('duration_seconds', 0) > 0]
    avg_duration = sum(durations) / len(durations) if durations else 0.0
    median_duration = sorted(durations)[len(durations) // 2] if durations else 0.0
    min_duration = min(durations) if durations else 0.0
    max_duration = max(durations) if durations else 0.0

    # Token metrics
    total_tokens = sum(event.get('metrics', {}).get('total_tokens', 0) for event in completion_events)
    avg_tokens_per_task = total_tokens / total_tasks if total_tasks > 0 else 0.0

    # By agent type
    by_agent = defaultdict(lambda: {'count': 0, 'success': 0, 'total_duration': 0.0, 'total_tokens': 0})
    for event in completion_events:
        agent = event.get('subagent_type', 'unknown')
        by_agent[agent]['count'] += 1
        if event.get('success', False):
            by_agent[agent]['success'] += 1
        by_agent[agent]['total_duration'] += event.get('duration_seconds', 0)
        by_agent[agent]['total_tokens'] += event.get('metrics', {}).get('total_tokens', 0)

    # Calculate agent averages
    for agent, stats in by_agent.items():
        if stats['count'] > 0:
            stats['success_rate'] = (stats['success'] / stats['count']) * 100
            stats['avg_duration'] = stats['total_duration'] / stats['count']
            stats['avg_tokens'] = stats['total_tokens'] / stats['count']

    # By description (top 10)
    description_counter = Counter(event.get('description', 'unknown') for event in completion_events)
    by_description = dict(description_counter.most_common(10))

    return {
        'total_tasks': total_tasks,
        'successful_tasks': successful_tasks,
        'failed_tasks': failed_tasks,
        'success_rate': success_rate,
        'avg_duration': avg_duration,
        'median_duration': median_duration,
        'min_duration': min_duration,
        'max_duration': max_duration,
        'total_tokens': total_tokens,
        'avg_tokens_per_task': avg_tokens_per_task,
        'by_agent': dict(by_agent),
        'by_description': by_description
    }

def format_duration(seconds):
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def print_statistics_table(stats, title):
    """Print formatted statistics table."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

    # Overall metrics
    print(f"📊 Overall Metrics:")
    print(f"   Total Tasks: {stats['total_tasks']}")
    print(f"   Successful:  {stats['successful_tasks']} ({stats['success_rate']:.1f}%)")
    print(f"   Failed:      {stats['failed_tasks']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")

    # Duration metrics
    print(f"\n⏱️  Duration Metrics:")
    print(f"   Average:  {format_duration(stats['avg_duration'])}")
    print(f"   Median:   {format_duration(stats['median_duration'])}")
    print(f"   Range:    {format_duration(stats['min_duration'])} - {format_duration(stats['max_duration'])}")

    # Token metrics
    print(f"\n🪙 Token Metrics:")
    print(f"   Total Tokens:     {stats['total_tokens']:,}")
    print(f"   Avg per Task:     {stats['avg_tokens_per_task']:.0f}")

    # By agent type
    if stats['by_agent']:
        print(f"\n🤖 By Agent Type:")
        print(f"   {'Agent':<25} {'Tasks':<8} {'Success':<10} {'Avg Duration':<12} {'Avg Tokens':<12}")
        print(f"   {'-'*25} {'-'*8} {'-'*10} {'-'*12} {'-'*12}")

        # Sort by task count
        sorted_agents = sorted(stats['by_agent'].items(), key=lambda x: x[1]['count'], reverse=True)
        for agent, agent_stats in sorted_agents:
            agent_name = agent[:24] + '...' if len(agent) > 24 else agent
            print(f"   {agent_name:<25} {agent_stats['count']:<8} "
                  f"{agent_stats['success_rate']:.1f}%{'':<6} "
                  f"{format_duration(agent_stats['avg_duration']):<12} "
                  f"{agent_stats['avg_tokens']:.0f}")

    # Top descriptions
    if stats['by_description']:
        print(f"\n📝 Top Task Descriptions:")
        for i, (desc, count) in enumerate(stats['by_description'].items(), 1):
            desc_short = desc[:50] + '...' if len(desc) > 50 else desc
            print(f"   {i:2}. {desc_short} ({count} tasks)")

def main():
    """Main analytics reporting function."""
    parser = argparse.ArgumentParser(description='Task Analytics Reporter')
    parser.add_argument('--export', action='store_true', help='Export data to JSON format')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    # Set up paths
    analytics_dir = Path.cwd() / '.claude' / 'hooks' / 'analytics'
    analytics_file = analytics_dir / 'task_analytics.jsonl'

    if not analytics_file.exists():
        print("No analytics data found. Run some tasks first to generate data.")
        return

    # Load data
    print("Loading analytics data...")
    all_data = load_analytics_data(analytics_file)

    if not all_data:
        print("No valid analytics data found.")
        return

    print(f"Loaded {len(all_data)} analytics entries")

    # Generate reports for different timeframes
    timeframes = [
        (5, "Last 5 Hours"),
        (24 * 7, "Last 7 Days"),  # 7 days in hours
        (None, "All Time")
    ]

    results = {}

    for hours, title in timeframes:
        filtered_data = filter_by_timeframe(all_data, hours)
        stats = calculate_statistics(filtered_data)
        results[title] = stats

        if stats['total_tasks'] > 0:
            print_statistics_table(stats, title)
        else:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}")
            print("No task data found for this timeframe.")

    # Export option
    if args.export:
        export_file = analytics_dir / 'analytics_report.json'
        with open(export_file, 'w') as f:
            json.dump({
                'generated_at': datetime.utcnow().isoformat() + 'Z',
                'timeframes': results
            }, f, indent=2)
        print(f"\n📁 Report exported to: {export_file}")

    print(f"\n{'='*60}")
    print("Analytics report complete!")

if __name__ == "__main__":
    main()