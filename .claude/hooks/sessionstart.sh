#!/bin/bash
# SessionStart hook - Ensures development environment is fully initialized
# Runs automatically when a new Claude Code session starts
#
# This hook performs essential setup to ensure all development functionality works:
# 1. Install dependencies (pnpm install)
# 2. Link to Vercel project (if not already linked)
# 3. Pull Vercel development environment variables
# 4. Generate Prisma client with environment-specific schema
# 5. Persist environment variables to CLAUDE_ENV_FILE for session
# 6. Verify critical tools are available

set -euo pipefail

# Get project root from script location (portable across environments)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

# Tee all output to sessionStart.output file (visible in console AND saved to file)
exec > >(tee "${PROJECT_ROOT}/sessionStart.output")

echo "🚀 SessionStart: Initializing development environment..."
echo "📂 Project root: $PROJECT_ROOT"

# Step 1: Install dependencies
echo ""
echo "📦 Step 1/6: Installing dependencies..."
if pnpm install --silent > /dev/null 2>&1; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Step 2: Link to Vercel project (if not already linked)
echo ""
echo "🔗 Step 2/6: Linking to Vercel project..."

# Check if already linked
if [ -d ".vercel" ]; then
    echo "✅ Project already linked to Vercel (.vercel/ exists)"
else
    echo "📡 Linking project to Vercel..."
    # Use vercel wrapper which handles VERCEL_TOKEN automatically
    if ./scripts/vercel-wrapper.sh link --yes > /dev/null 2>&1; then
        echo "✅ Successfully linked to Vercel project"
    else
        echo "⚠️  Warning: Could not link to Vercel project"
        echo "    This may be expected if VERCEL_TOKEN is not set or network is unavailable"
        echo "    Development can continue, but environment variable pull may not work"
    fi
fi

# Step 3: Pull Vercel development environment variables
echo ""
echo "🌍 Step 3/6: Loading environment variables..."

# Check if development env file already exists
if [ -f ".env.development.local" ]; then
    echo "✅ Development environment file already exists (.env.development.local)"
else
    echo "📥 Pulling development environment from Vercel..."
    # Use load-env.js which automatically pulls from Vercel if file doesn't exist
    # This will create .env.development.local with all necessary variables
    if node scripts/load-env.js --mode=development > /dev/null 2>&1; then
        echo "✅ Environment variables loaded from Vercel"
    else
        echo "⚠️  Warning: Could not pull from Vercel (may be offline or not authenticated)"
        echo "    Development may continue with existing environment variables"
    fi
fi

# Step 4: Generate Prisma client with environment-specific schema
echo ""
echo "🗄️  Step 4/6: Setting up environment-specific Prisma schema..."

# Load environment variables and regenerate Prisma client with correct schema name
# This updates the schema.prisma file with the correct environment-specific schema name
# and regenerates the Prisma client - same process as 'pnpm dev' but standalone
if ./scripts/load-env.sh mode=development 2>/dev/null | while read -r _env; do
    eval "$_env pnpm _prisma:generate" > /dev/null 2>&1
done; then
    echo "✅ Environment-specific Prisma client generated successfully"
else
    echo "⚠️  Warning: Environment-specific Prisma generation had issues"
    echo "    This is expected if not connected to Vercel or database"
    echo "    Development may continue with limited database functionality"
fi

# Step 5: Persist environment variables to CLAUDE_ENV_FILE
echo ""
echo "💾 Step 5/6: Persisting environment variables to Claude session..."

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
    # Load environment variables and write to CLAUDE_ENV_FILE
    # This makes all environment variables available in all subsequent Bash commands
    ENV_VARS=$(./scripts/load-env.sh mode=development 2>/dev/null | tail -1 || echo "")

    if [ -n "$ENV_VARS" ]; then
        # Convert space-separated KEY=VALUE pairs to export statements
        for var in $ENV_VARS; do
            # Skip if it's not a valid KEY=VALUE pair
            if [[ "$var" == *"="* ]]; then
                echo "export $var" >> "$CLAUDE_ENV_FILE"
            fi
        done
        echo "✅ Environment variables persisted to Claude session"
        echo "   All Bash commands will have access to: DATABASE_URL, PRISMA_SCHEMA, etc."
    else
        echo "⚠️  Warning: No environment variables to persist"
    fi
else
    echo "⚠️  Warning: CLAUDE_ENV_FILE not available (not running in SessionStart context?)"
fi

# Step 6: Verify critical tools
echo ""
echo "🔧 Step 6/6: Verifying development tools..."

TOOLS_OK=true

# Check vercel wrapper
if [ -x "./scripts/vercel-wrapper.sh" ]; then
    echo "✅ Vercel wrapper script available"
else
    echo "❌ Vercel wrapper script missing or not executable"
    TOOLS_OK=false
fi

# Check killport wrapper
if [ -x "./scripts/killport.sh" ]; then
    echo "✅ Killport script available"
else
    echo "❌ Killport script missing or not executable"
    TOOLS_OK=false
fi

# Check pnpm
if command -v pnpm &> /dev/null; then
    echo "✅ pnpm available ($(pnpm --version))"
else
    echo "❌ pnpm not found in PATH"
    TOOLS_OK=false
fi

# Check node
if command -v node &> /dev/null; then
    echo "✅ Node.js available ($(node --version))"
else
    echo "❌ Node.js not found in PATH"
    TOOLS_OK=false
fi

echo ""
if [ "$TOOLS_OK" = true ]; then
    echo "✅ SessionStart complete - Development environment ready!"
    echo ""
    echo "📝 Quick Start Commands:"
    echo "   pnpm dev              - Start development server"
    echo "   pnpm lint             - Run quality checks"
    echo "   pnpm test             - Run tests"
    echo "   ./scripts/killport.sh [PORT] - Clear port if needed"
else
    echo "⚠️  SessionStart complete with warnings - Some tools may not work correctly"
fi

echo ""
echo "🌐 Environment variables are now available in all Bash commands during this session"

# Return success - non-critical warnings shouldn't block session start
exit 0
