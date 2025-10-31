#!/bin/bash

# Evidence Validation Hook - Validates that required evidence is collected
# Implements Anthropic's "robust tool interface" pattern

AGENT_TYPE="$1"
SESSION_ID="$2"
TASK_CONTEXT="$3"

echo "[EVIDENCE VALIDATION] Validating evidence collection for $AGENT_TYPE"

# Only validate evidence for agents that should collect it
if [[ "$AGENT_TYPE" == "testing-agent" ]]; then
    echo "[EVIDENCE VALIDATION] Validating browser verification evidence"

    PROJECT_ROOT="$(pwd)"
    EVIDENCE_DIR="$PROJECT_ROOT/testing_agent/outputs"
    SCRIPTS_DIR="$PROJECT_ROOT/testing_agent/scripts"

    # Check for required evidence artifacts based on task type
    if echo "$TASK_CONTEXT" | jq -e '.task_type == "css_variable_injection"' > /dev/null 2>&1; then
        echo "[EVIDENCE VALIDATION] CSS variable injection task - checking required artifacts"

        # Required artifacts for CSS verification
        REQUIRED_ARTIFACTS=(
            "cdp-computed-styles"
            "before-screenshot"
            "after-screenshot"
            "console-logs"
            "test-results"
        )

        for artifact in "${REQUIRED_ARTIFACTS[@]}"; do
            if ! ls "$EVIDENCE_DIR"/*"$artifact"* > /dev/null 2>&1; then
                echo "[EVIDENCE VALIDATION] ❌ MISSING ARTIFACT: $artifact not found in evidence"
                echo "[EVIDENCE VALIDATION] CSS verification requires: ${REQUIRED_ARTIFACTS[*]}"
                exit 1
            fi
        done

        # Validate CDP inspection results contain expected data
        if ls "$EVIDENCE_DIR"/*cdp-computed-styles*.json > /dev/null 2>&1; then
            CDP_FILE=$(ls "$EVIDENCE_DIR"/*cdp-computed-styles*.json | head -1)
            if ! jq -e '.results | length > 0' "$CDP_FILE" > /dev/null 2>&1; then
                echo "[EVIDENCE VALIDATION] ❌ INVALID CDP DATA: No computed styles found"
                exit 1
            fi

            # Check for var() references in computed styles
            if ! jq -r '.results[].computedStyles[].value' "$CDP_FILE" | grep -q "var(" 2>/dev/null; then
                echo "[EVIDENCE VALIDATION] ⚠️  WARNING: No var() references found in computed styles"
                echo "[EVIDENCE VALIDATION] This may indicate CSS variable injection did not work"
            fi
        fi

        echo "[EVIDENCE VALIDATION] ✅ All required artifacts collected and validated"
    fi

elif [[ "$AGENT_TYPE" == "critique-and-validation-agent" ]]; then
    echo "[EVIDENCE VALIDATION] Validating completion evidence for complex tasks"

    if echo "$TASK_CONTEXT" | jq -e '.complexity_score >= 6' > /dev/null 2>&1; then
        # For complex tasks, ensure browser verification was completed
        PROJECT_ROOT="$(pwd)"
        if ! ls "$PROJECT_ROOT/testing_agent/outputs/"*.json > /dev/null 2>&1; then
            echo "[EVIDENCE VALIDATION] ❌ COMPLETION BLOCKED: No browser verification evidence"
            echo "[EVIDENCE VALIDATION] Complex tasks require browser verification before completion"
            exit 1
        fi
    fi
fi

echo "[EVIDENCE VALIDATION] ✅ Evidence validation passed for $AGENT_TYPE"