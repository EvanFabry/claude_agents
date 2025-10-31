#!/bin/bash
# SubagentStop hook for critique-and-validation-agent
# Level 3 Quality Gate: Provides complete quality status for completion determination
# NON-BLOCKING: Always exits 0 - provides information for validation decisions
# Part of three-level quality gate system
# Specification: /specs/active/three-level-quality-gate-system.yml

set -euo pipefail

TIMEOUT=30
APP_TYPE_STATUS=""
INFRA_TYPE_STATUS=""
APP_LINT_STATUS=""
INFRA_LINT_STATUS=""
HAS_TYPE_ERRORS=false
HAS_LINT_ISSUES=false

# Run application typecheck (CRITICAL for completion)
if ! APP_TYPE_OUTPUT=$(timeout ${TIMEOUT}s pnpm typecheck 2>&1); then
    APP_TYPE_STATUS="❌ Application type errors detected"
    HAS_TYPE_ERRORS=true
else
    APP_TYPE_STATUS="✅ Application typecheck clean"
fi

# Run testing infrastructure typecheck (CRITICAL for completion)
if ! INFRA_TYPE_OUTPUT=$(timeout ${TIMEOUT}s pnpm test:infra:typecheck 2>&1); then
    INFRA_TYPE_STATUS="❌ Testing infrastructure type errors detected"
    HAS_TYPE_ERRORS=true
else
    INFRA_TYPE_STATUS="✅ Testing infrastructure typecheck clean"
fi

# Run application lint (ADVISORY for completion)
if ! APP_LINT_OUTPUT=$(timeout ${TIMEOUT}s pnpm lint 2>&1); then
    APP_LINT_STATUS="⚠️  Application lint issues detected (advisory)"
    HAS_LINT_ISSUES=true
else
    APP_LINT_STATUS="✅ Application lint clean"
fi

# Run testing infrastructure lint (ADVISORY for completion)
if ! INFRA_LINT_OUTPUT=$(timeout ${TIMEOUT}s pnpm test:infra:lint 2>&1); then
    INFRA_LINT_STATUS="⚠️  Testing infrastructure lint issues detected (advisory)"
    HAS_LINT_ISSUES=true
else
    INFRA_LINT_STATUS="✅ Testing infrastructure lint clean"
fi

# Generate comprehensive quality status JSON (always exit 0)
if [ "$HAS_TYPE_ERRORS" = true ]; then
    cat <<EOF
{
  "additionalContext": "🔍 LEVEL 3 QUALITY STATUS - COMPLETION GATE

📊 TYPECHECK STATUS (BLOCKING):
$APP_TYPE_STATUS
$INFRA_TYPE_STATUS

📋 LINT STATUS (ADVISORY):
$APP_LINT_STATUS
$INFRA_LINT_STATUS

🚨 COMPLETION DECISION IMPACT:

⛔ TYPE ERRORS DETECTED - TASK COMPLETION MUST BE BLOCKED

According to the three-level quality gate system:
- Level 1: code-writing-agent and testing-agent should block on type errors
- Level 2: code-reviewer provides informational guidance
- Level 3: critique-and-validation-agent MUST NOT approve completion with type errors

✅ REQUIRED ACTIONS FOR COMPLETION:

1. All type errors MUST be fixed before task can be marked COMPLETE
2. If Level 1 agents completed despite type errors, this indicates a hook bypass
3. critique-and-validation-agent MUST set completion status to INCOMPLETE
4. Return to code-writing-agent or testing-agent to fix type errors
5. Re-run validation after fixes are applied

📊 COMPLETION CRITERIA:

For task completion approval, critique-and-validation-agent requires:
✅ Application typecheck: MUST be clean (MANDATORY)
✅ Testing infrastructure typecheck: MUST be clean (MANDATORY)
💡 Application lint: Noted if issues present (ADVISORY)
💡 Testing infrastructure lint: Noted if issues present (ADVISORY)

⚠️  CURRENT STATUS: COMPLETION BLOCKED DUE TO TYPE ERRORS

📚 REFERENCE:
- Specification: /specs/active/three-level-quality-gate-system.yml
- Documentation: AGENTS.md sections on quality gates
- Hook system: Three-level quality enforcement architecture

🔧 TYPE ERROR DETAILS:

Application Typecheck Output:
$APP_TYPE_OUTPUT

Testing Infrastructure Typecheck Output:
$INFRA_TYPE_OUTPUT",
  "suppressOutput": false
}
EOF
elif [ "$HAS_LINT_ISSUES" = true ]; then
    cat <<EOF
{
  "additionalContext": "🔍 LEVEL 3 QUALITY STATUS - COMPLETION GATE

📊 TYPECHECK STATUS (BLOCKING):
$APP_TYPE_STATUS
$INFRA_TYPE_STATUS

📋 LINT STATUS (ADVISORY):
$APP_LINT_STATUS
$INFRA_LINT_STATUS

✅ TYPE SAFETY VALIDATED - COMPLETION MAY PROCEED

According to the three-level quality gate system:
- Typecheck: CLEAN (completion not blocked)
- Lint issues: PRESENT but ADVISORY (completion not blocked)

💡 ADVISORY RECOMMENDATIONS:

While type safety is validated, lint issues are present. Consider:
1. Reviewing lint output for code quality improvements
2. Addressing lint issues to improve maintainability
3. Tracking lint trend for escalation if issues increase >20%

📊 COMPLETION CRITERIA STATUS:

✅ Application typecheck: CLEAN (MANDATORY - SATISFIED)
✅ Testing infrastructure typecheck: CLEAN (MANDATORY - SATISFIED)
⚠️  Application lint: Issues present (ADVISORY - NOT BLOCKING)
⚠️  Testing infrastructure lint: Issues present (ADVISORY - NOT BLOCKING)

✅ CURRENT STATUS: COMPLETION CRITERIA MET (lint issues advisory only)

📚 REFERENCE:
- Specification: /specs/active/three-level-quality-gate-system.yml
- Lint is tracked but not blocking per typecheck-only enforcement

💡 LINT DETAILS:

Application Lint Output:
$APP_LINT_OUTPUT

Testing Infrastructure Lint Output:
$INFRA_LINT_OUTPUT",
  "suppressOutput": false
}
EOF
else
    cat <<EOF
{
  "additionalContext": "✅ [LEVEL 3 QUALITY STATUS] All quality checks passed

📊 COMPLETE QUALITY VALIDATION:
$APP_TYPE_STATUS
$INFRA_TYPE_STATUS
$APP_LINT_STATUS
$INFRA_LINT_STATUS

✅ COMPLETION CRITERIA FULLY SATISFIED

All mandatory quality requirements met:
- Application typecheck: CLEAN
- Testing infrastructure typecheck: CLEAN
- Application lint: CLEAN
- Testing infrastructure lint: CLEAN

Task is eligible for COMPLETE status if all functional requirements are met.",
  "suppressOutput": true
}
EOF
fi

exit 0  # ALWAYS exit 0 (non-blocking - provides information only)
