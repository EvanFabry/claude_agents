#!/bin/bash
# SubagentStop hook for code-reviewer
# Level 2 Quality Gate: Provides quality status guidance (INFORMATIONAL, NON-BLOCKING)
# Part of three-level quality gate system
# Always exits 0 - guidance only, not enforcement
# Note: Level 1 already blocks on quality issues (eslint + typecheck + tests)
# Specification: /specs/active/three-level-quality-gate-system.yml

set -euo pipefail

TIMEOUT=90  # Increased timeout since lint now includes typecheck + tests
QUALITY_STATUS=""
QUALITY_OUTPUT=""
HAS_ISSUES=false

# Run comprehensive quality check (lint now includes: eslint + typecheck + tests)
# Note: pnpm lint runs eslint → typecheck → test:run sequentially
if ! QUALITY_OUTPUT=$(timeout ${TIMEOUT}s pnpm lint 2>&1); then
    QUALITY_STATUS="⚠️  Quality issues detected"
    HAS_ISSUES=true

    # Provide helpful context about what might have failed
    if echo "$QUALITY_OUTPUT" | grep -q "error TS"; then
        QUALITY_STATUS="$QUALITY_STATUS
   - Type errors found (should have been caught by Level 1 gate)"
    fi
    if echo "$QUALITY_OUTPUT" | grep -q "eslint"; then
        QUALITY_STATUS="$QUALITY_STATUS
   - ESLint issues found (should have been caught by Level 1 gate)"
    fi
    if echo "$QUALITY_OUTPUT" | grep -q "FAIL\|failed"; then
        QUALITY_STATUS="$QUALITY_STATUS
   - Test failures found (should have been caught by Level 1 gate)"
    fi
else
    QUALITY_STATUS="✅ All quality checks passed (eslint + typecheck + tests)"
fi

# Generate informational JSON (always exit 0)
if [ "$HAS_ISSUES" = true ]; then
    cat <<EOF
{
  "additionalContext": "📊 LEVEL 2 QUALITY STATUS (Informational - Non-Blocking)

$QUALITY_STATUS

🔍 QUALITY CHECK RESULTS:
   pnpm lint now runs: ESLint → Typecheck → Unit Tests

ℹ️  CONTEXT:

- ESLint: Should be clean (Level 1 blocks on lint errors)
- Typecheck: Should be clean (Level 1 blocks on type errors)
- Tests: Should be passing (Level 1 blocks on test failures)

💡 RECOMMENDATIONS:

1. If ANY issues present: Investigate why Level 1 didn't catch them
2. This indicates a potential gap in the Level 1 quality gate
3. Review code-writing-agent output for quality gate execution
4. Run 'pnpm lint' for complete quality check output
5. Run individual checks to isolate issues:
   - 'pnpm lint:only' (ESLint only)
   - 'pnpm typecheck' (TypeScript only)
   - 'pnpm test:run' (Tests only)

📊 QUALITY GATE SYSTEM:

- Level 1 (code-writing-agent): BLOCKS on all quality issues (eslint + typecheck + tests)
- Level 2 (code-reviewer): INFORMATIONAL guidance (this hook - should see clean results)
- Level 3 (critique-agent): Evidence validation at completion

See /specs/active/three-level-quality-gate-system.yml for details.

⚠️  NOTE: This is informational only - workflow continues regardless",
  "suppressOutput": false
}
EOF
else
    cat <<EOF
{
  "additionalContext": "✅ [LEVEL 2 QUALITY STATUS] All quality checks passed (eslint + typecheck + tests)",
  "suppressOutput": true
}
EOF
fi

exit 0  # ALWAYS exit 0 (non-blocking by design)
