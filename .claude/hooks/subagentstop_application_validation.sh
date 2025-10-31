#!/bin/bash
# SubagentStop hook for testing-agent
# Level 1 Quality Gate: Validates browser automation scripts + test infrastructure
# BLOCKING: Script violations, all quality checks (eslint + typecheck + tests)
# Part of three-level quality gate system
# Specification: /specs/active/three-level-quality-gate-system.yml

set -euo pipefail

PROJECT_ROOT="$(pwd)"
SCRIPTS_DIR="$PROJECT_ROOT/testing_agent/scripts"
VIOLATIONS_FOUND=false
VIOLATION_DETAILS=""

# Scan all JS files in testing_agent/scripts/ for violations
while IFS= read -r script_file; do
  # Skip if not a .js file
  [[ ! "$script_file" =~ \.js$ ]] && continue

  SCRIPT_NAME=$(basename "$script_file")

  # CHECK 1: Direct playwright imports (EXISTING)
  if grep -q "import.*chromium.*from.*['\"]playwright['\"]" "$script_file"; then
    VIOLATIONS_FOUND=true
    VIOLATION_DETAILS+="
❌ VIOLATION in $SCRIPT_NAME:
   Direct playwright import detected
   FORBIDDEN: import { chromium } from 'playwright'
   "
  fi

  # CHECK 2: Incorrect import paths (NEW)
  if grep -q "import.*from.*['\"]\.\/common\.js['\"]" "$script_file"; then
    VIOLATIONS_FOUND=true
    VIOLATION_DETAILS+="
❌ VIOLATION in $SCRIPT_NAME:
   Incorrect import path detected
   FOUND: import ... from './common.js'
   REQUIRED: import ... from '../common.js'
   REASON: Scripts are in scripts/ subdirectory
   "
  fi

  # CHECK 3: Missing runBrowserTest (NEW - WARNING only)
  if ! grep -q "runBrowserTest" "$script_file"; then
    VIOLATION_DETAILS+="
⚠️  WARNING in $SCRIPT_NAME:
   Script does not use runBrowserTest()
   RECOMMENDED: Use runBrowserTest() for standardized Chrome setup
   "
  fi

  # CHECK 4: Server lifecycle validation (NEW)
  if grep -q "spawn.*vercel.*dev" "$script_file"; then
    # Script spawns server - check for proper lifecycle management
    has_shutdown_function=false
    has_log_file=false

    if grep -q "shutdownServer" "$script_file" || grep -q "serverProcess\.kill" "$script_file"; then
      has_shutdown_function=true
    fi

    if grep -q "LOG_FILE.*=.*path\.join.*outputs.*server-logs" "$script_file"; then
      has_log_file=true
    fi

    if [ "$has_shutdown_function" = false ]; then
      VIOLATIONS_FOUND=true
      VIOLATION_DETAILS+="
❌ VIOLATION in $SCRIPT_NAME:
   Server spawned without shutdown mechanism
   REQUIRED: shutdownServer() function or serverProcess.kill() calls
   REQUIRED: Signal handlers for SIGINT, SIGTERM, uncaughtException
   "
    fi

    if [ "$has_log_file" = false ]; then
      VIOLATION_DETAILS+="
⚠️  WARNING in $SCRIPT_NAME:
   Server spawned without correlation-tagged logging
   RECOMMENDED: LOG_FILE = path.join(__dirname, '../outputs', 'server-logs-\${correlationId}.log')
   RECOMMENDED: appendFileSync(LOG_FILE, ...) for server output
   "
    fi
  fi

done < <(find "$SCRIPTS_DIR" -type f \( -name "*.js" -o -name "*.ts" \) -mmin -60)  # Files modified in last 60 minutes

# Level 1 Quality Gate: Test infrastructure quality validation
# BLOCKING: All quality checks (eslint + typecheck + tests)
# Overall hook timeout budget: 90s (30s script checks + 60s full lint workflow)
INFRA_QUALITY_ERRORS=""

# Run full quality check for testing_agent (BLOCKING)
# pnpm test:infra:lint runs: eslint → typecheck → tests
if ! INFRA_LINT_OUTPUT=$(timeout 60s pnpm test:infra:lint 2>&1); then
    INFRA_QUALITY_ERRORS="${INFRA_QUALITY_ERRORS}

❌ TEST INFRASTRUCTURE QUALITY ERRORS (BLOCKING):
$INFRA_LINT_OUTPUT"
    VIOLATIONS_FOUND=true
fi

# Update VIOLATION_DETAILS to include infrastructure errors
if [ -n "$INFRA_QUALITY_ERRORS" ]; then
    VIOLATION_DETAILS+="
📦 TEST INFRASTRUCTURE QUALITY ISSUES:
$INFRA_QUALITY_ERRORS

✅ REQUIRED CORRECTIVE ACTIONS (BLOCKING):
1. Fix all quality issues: Run 'pnpm test:infra:lint'
2. Resolve ESLint errors, TypeScript errors, and test failures
3. testing-agent MUST complete with zero quality issues
"
fi

if [ "$VIOLATIONS_FOUND" = true ]; then
  cat <<EOF
{
  "additionalContext": "🚨 BROWSER AUTOMATION CONSTRAINT VIOLATIONS DETECTED

$VIOLATION_DETAILS

🔒 ENFORCED CONSTRAINTS:

1. NO DIRECT PLAYWRIGHT IMPORTS
   ❌ FORBIDDEN: import { chromium } from 'playwright'
   ✅ REQUIRED: import { runBrowserTest } from '../common.js'

2. CORRECT IMPORT PATHS
   ❌ FORBIDDEN: import ... from './common.js'
   ✅ REQUIRED: import ... from '../common.js'
   (scripts/ is a subdirectory)

3. USE runBrowserTest() FOR AUTOMATION
   ⚠️  Scripts should use runBrowserTest() for standardized setup
   ⚠️  Direct chromium.launch() bypasses authentication preservation

4. SERVER LIFECYCLE MANAGEMENT
   If spawning server (spawn('vercel', ['dev'])):
   ✅ MUST HAVE: shutdownServer() function
   ✅ MUST HAVE: Signal handlers (SIGINT, SIGTERM, uncaughtException)
   ✅ SHOULD HAVE: Correlation-tagged log file in outputs/

✅ CORRECT PATTERNS:

// Basic browser test (no server management)
import { runBrowserTest } from '../common.js';

runBrowserTest({
  url: 'http://localhost:3000/app/example',
  testFunction: async (page, client, metadata) => {
    // Your test logic here
  }
});

// Using templates for server lifecycle management
import { CANONICAL_SCRIPT_TEMPLATE, generateCorrelationId } from '../templates.js';

const script = CANONICAL_SCRIPT_TEMPLATE
  .replace('{correlationId}', generateCorrelationId())
  .replace('{targetSite}', 'example.com');
// ... save and execute

📚 DOCUMENTATION:
   See: @testing-agent.md
     - Lines 27: CRITICAL constraint
     - Lines 127-156: Mandatory workflow
     - Lines 229-237: Self-validation checklist

   See: @testing_agent/templates.js
     - CANONICAL_SCRIPT_TEMPLATE for server lifecycle
     - generateCorrelationId() for log correlation

🔧 CORRECTIVE ACTION:
   1. Review scripts in testing_agent/scripts/
   2. Fix import paths (use '../common.js' not './common.js')
   3. Replace direct playwright imports with runBrowserTest
   4. Add server lifecycle management if spawning server
   5. Use templates.js for canonical patterns
   6. Refer to existing conforming scripts as examples

⚠️ AUTHENTICATION IMPACT:
   Direct chromium.launch() creates LOGGED-OUT browser state
   This causes authentication failures for protected pages
   runBrowserTest() preserves login sessions automatically
",
  "suppressOutput": false
}
EOF
else
  # No violations - pass through silently
  echo '{"suppressOutput": true}'
fi

exit 0
