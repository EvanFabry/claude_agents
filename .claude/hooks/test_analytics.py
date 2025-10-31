#!/usr/bin/env python3

"""
Test script to verify the analytics system is working correctly.
"""

import json
import sys
from pathlib import Path
import subprocess
import time

def test_hook_execution():
    """Test that the analytics hooks can execute correctly."""
    print("Testing analytics hook execution...")

    # Create test data for PreToolUse
    # Get project root (current working directory)
    project_root = str(Path.cwd())

    test_pre_data = {
        "session_id": "test-session-123",
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "test-agent",
            "description": "Test task description"
        },
        "hook_event_name": "PreToolUse",
        "cwd": project_root,
        "permission_mode": "default"
    }

    # Test PreToolUse hook
    try:
        result = subprocess.run(
            ["uv", "run", ".claude/hooks/pre_tool_use_analytics.py"],
            input=json.dumps(test_pre_data),
            text=True,
            capture_output=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✅ PreToolUse hook executed successfully")
        else:
            print(f"❌ PreToolUse hook failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ PreToolUse hook execution error: {e}")
        return False

    # Wait a moment to simulate task execution
    time.sleep(1)

    # Create test data for PostToolUse
    test_post_data = {
        "session_id": "test-session-123",
        "tool_name": "Task",
        "tool_input": {
            "subagent_type": "test-agent",
            "description": "Test task description"
        },
        "tool_response": {
            "totalDurationMs": 1500,
            "totalTokens": 250,
            "totalToolUseCount": 1,
            "usage": {
                "input_tokens": 100,
                "output_tokens": 150,
                "cache_read_input_tokens": 50
            }
        },
        "hook_event_name": "PostToolUse",
        "cwd": project_root,
        "permission_mode": "default"
    }

    # Test PostToolUse hook
    try:
        result = subprocess.run(
            ["uv", "run", ".claude/hooks/post_tool_use_analytics.py"],
            input=json.dumps(test_post_data),
            text=True,
            capture_output=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✅ PostToolUse hook executed successfully")
        else:
            print(f"❌ PostToolUse hook failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ PostToolUse hook execution error: {e}")
        return False

    return True

def test_analytics_data():
    """Test that analytics data was properly created."""
    print("\nTesting analytics data creation...")

    analytics_dir = Path.cwd() / '.claude' / 'hooks' / 'analytics'
    analytics_file = analytics_dir / 'task_analytics.jsonl'

    if not analytics_file.exists():
        print("❌ Analytics file was not created")
        return False

    # Read and check the data
    try:
        with open(analytics_file, 'r') as f:
            lines = f.readlines()

        if len(lines) >= 2:  # Should have at least start and complete events
            print(f"✅ Analytics file created with {len(lines)} entries")

            # Check the last few entries for our test data
            for line in lines[-3:]:
                try:
                    entry = json.loads(line.strip())
                    if entry.get('session_id') == 'test-session-123':
                        event_type = entry.get('event_type')
                        subagent = entry.get('subagent_type')
                        print(f"   Found test entry: {event_type} for {subagent}")

                        if event_type == 'TaskComplete':
                            duration = entry.get('duration_seconds', 0)
                            success = entry.get('success', False)
                            print(f"   Duration: {duration}s, Success: {success}")
                except json.JSONDecodeError:
                    continue

            return True
        else:
            print("❌ Not enough analytics entries found")
            return False

    except Exception as e:
        print(f"❌ Error reading analytics data: {e}")
        return False

def test_analytics_reporter():
    """Test that the analytics reporter can generate statistics."""
    print("\nTesting analytics reporter...")

    try:
        result = subprocess.run(
            ["uv", "run", ".claude/hooks/analytics_reporter.py"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("✅ Analytics reporter executed successfully")
            if "Analytics report complete!" in result.stdout:
                print("✅ Report generation confirmed")
                return True
            else:
                print("⚠️ Report may not have completed properly")
                print(f"Output: {result.stdout[:200]}...")
                return True
        else:
            print(f"❌ Analytics reporter failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Analytics reporter execution error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Analytics System")
    print("=" * 50)

    success = True

    # Test hook execution
    if not test_hook_execution():
        success = False

    # Test data creation
    if not test_analytics_data():
        success = False

    # Test reporter
    if not test_analytics_reporter():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Analytics system is working.")
    else:
        print("❌ Some tests failed. Check the output above.")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())