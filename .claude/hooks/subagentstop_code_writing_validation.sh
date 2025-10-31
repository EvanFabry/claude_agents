#!/bin/bash
# SubagentStop hook for code-writing-agent
# Level 1 Quality Gate: Blocks on lint failures (eslint + typecheck + tests) (BLOCKING)
# Part of three-level quality gate system
# Specification: /specs/active/three-level-quality-gate-system.yml

set -euo pipefail

TIMEOUT=90
LINT_ERRORS=""
EXIT_CODE=0

# Run full quality validation (BLOCKING)
# pnpm lint runs: eslint → typecheck → tests
if ! LINT_OUTPUT=$(timeout ${TIMEOUT}s pnpm lint 2>&1); then
    LINT_ERRORS="$LINT_OUTPUT"
    EXIT_CODE=1
fi

# Generate structured JSON output
# Using heredoc for safe multi-line JSON generation
if [ $EXIT_CODE -eq 1 ]; then
    cat <<EOF
{
  "additionalContext": "🚨 LEVEL 1 QUALITY GATE: QUALITY ERRORS DETECTED

QUALITY CHECK FAILURES:
$LINT_ERRORS

🔒 BLOCKING ENFORCEMENT:

This code cannot be accepted due to quality check failures. The code-writing-agent
MUST fix all issues before completing the task.

✅ REQUIRED CORRECTIVE ACTIONS:

1. Review all errors above carefully (ESLint, TypeCheck, Test failures)
2. Fix all issues in the relevant files
3. Run 'pnpm lint' locally to verify fixes
4. Ensure no new issues are introduced

📊 SELF-CORRECTION PROTOCOL:

- Iteration 1: Analyze errors, apply standard fixes
- Iteration 2: If errors persist, review type definitions, lint rules, test logic
- Iteration 3: If still failing, escalate to user with detailed error context

⚠️ IMPORTANT:

- ESLint rules enforce code quality and consistency
- Type safety is NON-NEGOTIABLE (prevents runtime bugs)
- All tests must pass (validates functionality)
- Address root causes, not just quick fixes

🔧 COMMON ERROR PATTERNS:

- ESLint: Unused variables, import issues, code style violations
- TypeCheck: Missing properties, incorrect types, null/undefined cases
- Tests: Logic errors, missing edge cases, timing issues

📚 DOCUMENTATION:

See /specs/active/three-level-quality-gate-system.yml for quality gate system details.
Quality gates ensure code reliability and maintainability.",
  "suppressOutput": false
}
EOF
else
    cat <<EOF
{
  "additionalContext": "✅ [LEVEL 1 QUALITY GATE] All quality checks passed (eslint + typecheck + tests)",
  "suppressOutput": true
}
EOF
fi

exit $EXIT_CODE
