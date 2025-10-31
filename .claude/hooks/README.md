# Claude Analytics System

A Python-based analytics solution for tracking agent task durations, success rates, and performance metrics.

## Overview

This system replaces the previous shell-based metrics collector with a more robust Python implementation that tracks:

- **Task Durations**: How long each agent task takes to complete
- **Success Rates**: Success/failure rates by agent type
- **Token Usage**: Token consumption patterns and efficiency
- **Performance Trends**: Analytics over different time periods (5hrs, 7 days, all time)

## Components

### 1. Analytics Hooks

- **`pre_tool_use_analytics.py`**: Tracks task start times for duration calculation
- **`post_tool_use_analytics.py`**: Tracks task completion and calculates durations

These hooks automatically capture:
- Session ID and agent type
- Task descriptions and timestamps
- Token usage and response metrics
- Success/failure status

### 2. Analytics Reporter

- **`analytics_reporter.py`**: Generates comprehensive statistics tables

**Usage:**
```bash
# Generate analytics report
uv run .claude/hooks/analytics_reporter.py

# Export to JSON format
uv run .claude/hooks/analytics_reporter.py --export

# Show detailed output
uv run .claude/hooks/analytics_reporter.py --verbose
```

### 3. Test Suite

- **`test_analytics.py`**: Comprehensive test suite to verify system functionality

**Usage:**
```bash
# Test the analytics system
uv run .claude/hooks/test_analytics.py
```

## Data Format

Analytics data is stored in `.claude/hooks/analytics/task_analytics.jsonl` with the following structure:

### TaskStart Events
```json
{
  "timestamp": "2025-01-23T10:30:45.123Z",
  "event_type": "TaskStart",
  "session_id": "abc123",
  "subagent_type": "code-writing-agent",
  "description": "Fix TypeScript errors",
  "hook_event_name": "PreToolUse",
  "tool_name": "Task",
  "cwd": "/path/to/project",
  "permission_mode": "default"
}
```

### TaskComplete Events
```json
{
  "timestamp": "2025-01-23T10:30:47.456Z",
  "event_type": "TaskComplete",
  "session_id": "abc123",
  "subagent_type": "code-writing-agent",
  "description": "Fix TypeScript errors",
  "duration_seconds": 2.333,
  "start_timestamp": "2025-01-23T10:30:45.123Z",
  "end_timestamp": "2025-01-23T10:30:47.456Z",
  "success": true,
  "metrics": {
    "total_duration_ms": 2500,
    "total_tokens": 1250,
    "total_tool_use_count": 3,
    "input_tokens": 800,
    "output_tokens": 450,
    "cache_read_input_tokens": 200
  }
}
```

## Hook Integration

The system is integrated via `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_tool_use_analytics.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/post_tool_use_analytics.py"
          }
        ]
      }
    ]
  }
}
```

## Analytics Output

The reporter generates tables showing:

### Overall Metrics
- Total tasks executed
- Success/failure counts and rates
- Success rate percentage

### Duration Metrics
- Average, median, min, max durations
- Human-readable format (seconds, minutes, hours)

### Token Metrics
- Total token consumption
- Average tokens per task
- Input/output token breakdown

### By Agent Type
- Performance breakdown by agent
- Success rates per agent
- Average duration and tokens per agent

### Top Task Descriptions
- Most frequently executed task types
- Task frequency analysis

## File Locations

```
.claude/hooks/
├── pre_tool_use_analytics.py    # PreToolUse hook
├── post_tool_use_analytics.py   # PostToolUse hook
├── analytics_reporter.py        # Statistics generator
├── test_analytics.py           # Test suite
├── analytics/                  # Data directory
│   ├── task_analytics.jsonl   # Main analytics data
│   └── analytics_report.json  # Exported reports
└── README.md                   # This file
```

## Migration from Old System

This system replaces:
- `metrics_collector_robust.sh` - Replaced by Python hooks
- `analyze_metrics_robust.py` - Replaced by `analytics_reporter.py`

All SubagentStop hooks have been simplified to remove metrics collection overhead while preserving quality checking functionality.

## Performance

The system is designed for minimal overhead:
- Lightweight Python hooks with fast execution
- Efficient JSONL storage format
- Automatic cleanup of temporary files
- Background processing with timeout protection

## Troubleshooting

### No Data Found
If the reporter shows "No analytics data found":
1. Ensure hooks are properly configured in settings.json
2. Run some tasks to generate data
3. Check `.claude/hooks/analytics/task_analytics.jsonl` exists

### Hook Execution Errors
If hooks fail to execute:
1. Verify Python scripts are executable (`chmod +x`)
2. Check that `uv` is available in PATH
3. Review error output in Claude logs

### Test the System
Run the test suite to verify everything works:
```bash
uv run .claude/hooks/test_analytics.py
```

This will test hook execution, data creation, and report generation.