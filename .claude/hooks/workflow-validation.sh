#!/bin/bash

# Workflow Validation Hook - Runs after agent completion to validate workflow compliance
# Based on Anthropic's quality control patterns

AGENT_TYPE="$1"
SESSION_ID="$2"
TASK_CONTEXT="$3"

echo "[WORKFLOW VALIDATION] Validating $AGENT_TYPE completion for session $SESSION_ID"

# Parse task context to determine validation requirements
if echo "$TASK_CONTEXT" | jq -e '.complexity_score >= 3' > /dev/null 2>&1; then
    echo "[WORKFLOW VALIDATION] Complex task detected - validating agent workflow compliance"

    # Check if required agents were called for complex tasks
    REQUIRED_AGENTS=("planning-agent" "critique-and-validation-agent" "testing-agent")

    for required_agent in "${REQUIRED_AGENTS[@]}"; do
        if ! grep -q "Task.*$required_agent" /tmp/claude/session_${SESSION_ID}_agents.log 2>/dev/null; then
            echo "[WORKFLOW VALIDATION] ❌ COMPLIANCE FAILURE: Required agent $required_agent not called"
            echo "[WORKFLOW VALIDATION] Complex tasks must use full agent workflow"
            exit 1
        fi
    done

    echo "[WORKFLOW VALIDATION] ✅ Agent workflow compliance validated"
fi

# Validate evidence collection for verification tasks
if echo "$TASK_CONTEXT" | jq -e '.requires_browser_verification == true' > /dev/null 2>&1; then
    echo "[WORKFLOW VALIDATION] Browser verification required - checking evidence collection"

    # Check for required evidence artifacts
    PROJECT_ROOT="$(pwd)"
    EVIDENCE_DIR="$PROJECT_ROOT/testing_agent/outputs"
    if [ ! -d "$EVIDENCE_DIR" ] || [ -z "$(ls -A $EVIDENCE_DIR 2>/dev/null)" ]; then
        echo "[WORKFLOW VALIDATION] ❌ EVIDENCE FAILURE: No browser verification evidence found"
        echo "[WORKFLOW VALIDATION] Tasks requiring verification must collect evidence"
        exit 1
    fi

    echo "[WORKFLOW VALIDATION] ✅ Evidence collection validated"
fi

# Validate completion authority for complex tasks
if [[ "$AGENT_TYPE" != "critique-and-validation-agent" ]] && echo "$TASK_CONTEXT" | jq -e '.complexity_score >= 6' > /dev/null 2>&1; then
    echo "[WORKFLOW VALIDATION] ❌ COMPLETION AUTHORITY FAILURE: Complex task completion claimed by $AGENT_TYPE"
    echo "[WORKFLOW VALIDATION] Only critique-and-validation-agent can authorize complex task completion"
    exit 1
fi

echo "[WORKFLOW VALIDATION] ✅ All validation checks passed for $AGENT_TYPE"