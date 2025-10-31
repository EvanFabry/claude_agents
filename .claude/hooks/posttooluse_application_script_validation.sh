#!/bin/bash
# PostToolUse hook for testing-agent agent
# Validates generated browser automation scripts follow mandatory patterns
# Blocks violations with detailed corrective guidance

# Parse tool result from stdin
TOOL_RESULT=$(cat)

# Extract tool name
TOOL_NAME=$(echo "$TOOL_RESULT" | jq -r '.tool_name // empty')

# Only validate Write operations
if [[ "$TOOL_NAME" != "Write" ]]; then
    # Pass through for other tools
    echo '{"suppressOutput": true}'
    exit 0
fi

# CORRECTED: Extract file path from tool_input (not parameters)
FILE_PATH=$(echo "$TOOL_RESULT" | jq -r '.tool_input.file_path // empty')

# Only validate JavaScript files in testing_agent/scripts/
if [[ ! "$FILE_PATH" =~ ^testing_agent/scripts/.*\.js$ ]]; then
    # Not a browser script, allow
    echo '{"suppressOutput": true}'
    exit 0
fi

# CORRECTED: Extract script content from tool_input (not parameters)
CONTENT=$(echo "$TOOL_RESULT" | jq -r '.tool_input.content // empty')

# VALIDATION #1: Check for direct playwright/chromium imports (BLOCKING)
if echo "$CONTENT" | grep -qE "import.*\{.*chromium.*\}.*from.*['\"]playwright['\"]"; then
    cat <<EOF
{
  "additionalContext": "🚨 BLOCKING CONSTRAINT VIOLATION DETECTED

❌ VIOLATION: Direct playwright import in ${FILE_PATH}
   Found: import { chromium } from 'playwright';
   Line: $(echo "$CONTENT" | grep -n "import.*chromium.*from.*playwright" | cut -d: -f1 | head -1)

🔒 ENFORCED CONSTRAINT:
   Browser automation scripts MUST use standardized functions from common.js
   Custom Playwright code is FORBIDDEN and will not execute correctly

✅ REQUIRED PATTERN:
   import { runBrowserTest, analyzeStylesWithCDP } from '../common.js';

   async function myTest(page, client, metadata) {
     // Your test logic here
     // page, client, metadata provided by runBrowserTest
   }

   runBrowserTest({
     url: 'http://localhost:3000/app/example',
     testFunction: myTest,
     waitForAnalysis: true,
     timeout: 60000
   });

📚 DOCUMENTATION:
   See: @testing-agent.md
     - Lines 27: CRITICAL constraint statement
     - Lines 127-156: Mandatory workflow pattern
     - Lines 164-176: Anti-patterns (what NOT to do)

💡 WHY THIS MATTERS:
   runBrowserTest() handles:
   - Chrome user profile configuration (preserves authentication)
   - Browser launch with correct settings
   - Page setup and navigation
   - Analysis completion detection
   - Proper cleanup and error handling

🔧 CORRECTIVE ACTION:
   1. Remove: import { chromium } from 'playwright'
   2. Add: import { runBrowserTest } from '../common.js'
   3. Wrap your test function in runBrowserTest()
   4. Let runBrowserTest handle all browser setup

📖 WORKING EXAMPLE:
   See: testing_agent/scripts/example-btn2-analysis.js
   This shows the correct standardized pattern in action.

⚠️ AUTHENTICATION IMPACT:
   Custom chromium.launch() creates LOGGED-OUT browser state
   This causes authentication failures for protected pages
   runBrowserTest() preserves login sessions automatically
",
  "suppressOutput": false,
  "continue": false,
  "stopReason": "Script violates mandatory constraint: no direct playwright imports. Must use runBrowserTest() from common.js"
}
EOF
    exit 0
fi

# VALIDATION #2: Check for runBrowserTest usage (WARNING if missing)
if ! echo "$CONTENT" | grep -q "runBrowserTest"; then
    cat <<EOF
{
  "additionalContext": "⚠️ MISSING MANDATORY PATTERN in ${FILE_PATH}

❓ ISSUE: Script does not use runBrowserTest() wrapper
   This may indicate custom browser automation code

🔍 EXPECTED PATTERN:
   All browser automation scripts should use:
   - runBrowserTest({ url, testFunction, ... })

   Your test function receives:
   - page: Configured Playwright page
   - client: Chrome DevTools Protocol client
   - metadata: Analysis metadata (if waitForAnalysis: true)

📋 STANDARD WORKFLOW:
   1. Import from common.js (never playwright directly)
   2. Define test function: async function test(page, client, metadata)
   3. Execute via: runBrowserTest({ url, testFunction })

📚 REFERENCE:
   @testing-agent.md lines 127-156

⚙️ IF YOU HAVE A GOOD REASON:
   In rare cases, specialized browser automation may be needed.
   If so, document WHY standard pattern doesn't work.
   Otherwise, please refactor to use runBrowserTest().
",
  "suppressOutput": false
}
EOF
    exit 0
fi

# VALIDATION #3: Check for custom browser.launch() patterns (WARNING)
if echo "$CONTENT" | grep -qE "(chromium\.launch|browser\.newContext|playwright\.)"; then
    cat <<EOF
{
  "additionalContext": "⚠️ CUSTOM BROWSER SETUP DETECTED in ${FILE_PATH}

❓ PATTERN: Found custom browser launch/context code
   - chromium.launch()
   - browser.newContext()
   - playwright.*

💡 RECOMMENDATION:
   runBrowserTest() handles all browser setup automatically:
   - Launches Chrome with persistent context (preserves auth)
   - Configures window size and viewport
   - Sets up console logging
   - Handles navigation and waits
   - Manages cleanup and timeouts

📋 BENEFITS OF STANDARDIZED PATTERN:
   - Authentication state preserved (no re-login)
   - Consistent browser configuration
   - Proper error handling and cleanup
   - Analysis completion detection built-in
   - Reduced code duplication

🔧 SUGGESTED REFACTOR:
   Replace custom setup with runBrowserTest() wrapper
   See: @testing-agent.md lines 127-156
",
  "suppressOutput": false
}
EOF
    exit 0
fi

# All validations passed
echo '{"suppressOutput": true}'
exit 0
