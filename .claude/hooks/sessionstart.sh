#!/bin/bash
# SessionStart hook - Project-specific session initialization
# Runs automatically when a new Claude Code session starts
#
# [USER CONFIGURATION REQUIRED]
#
# This hook is called at the beginning of each Claude Code session.
# Configure it to perform project-specific setup tasks such as:
# - Installing dependencies (npm install, pnpm install, etc.)
# - Setting up environment variables
# - Starting development servers
# - Initializing database connections
# - Verifying required tools are available
#
# Example setup tasks:
# - pnpm install
# - Verify database connection
# - Load environment variables
# - Check for required system dependencies
# - Initialize project-specific tooling

set -euo pipefail

# Get script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "📍 SessionStart hook location: $SCRIPT_DIR/sessionstart.sh"
echo "📂 Project root: $PROJECT_ROOT"
echo ""
echo "ℹ️  This hook can be configured for project-specific session initialization."
echo "   See comments in this file for setup examples."
echo ""
echo "✅ SessionStart hook executed (no custom initialization configured)"

exit 0
