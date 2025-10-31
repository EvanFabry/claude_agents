# ENVIRONMENT.md - Environment Configuration

**[USER CONFIGURATION REQUIRED]**

This file documents environment variables, configuration management, and environment-specific settings. Agents reference this file when they need to understand environment setup.

---

## 🌍 Environment Overview

**Purpose**: Document the different environments in your application.

**What to include**:
- Environment names and purposes
- Environment-specific URLs/endpoints
- Configuration differences between environments
- Environment promotion flow

**Example**:
```
Environments:
1. development - Local development environment
   - URL: http://localhost:[PORT]
   - Database: Local instance
   - External Services: Mocked/sandbox

2. staging/preview - Pre-production testing
   - URL: https://staging.example.com
   - Database: Staging database
   - External Services: Sandbox/test mode

3. production - Live user-facing environment
   - URL: https://example.com
   - Database: Production database
   - External Services: Live credentials

Environment Flow:
development → staging → production
```

---

## 🔐 Environment Variables

**Purpose**: Document all environment variables used in your application.

**What to include**:
- Variable names and purposes
- Required vs optional variables
- Default values
- Security considerations

**Example**:
```
Required Variables:
- PORT - Server port number (default: 3000)
- DATABASE_URL - Database connection string
- API_KEY - [Service] API key for [purpose]
- NODE_ENV - Environment name (development/staging/production)

Optional Variables:
- LOG_LEVEL - Logging verbosity (default: info)
- CACHE_TTL - Cache time-to-live in seconds (default: 3600)
- MAX_UPLOAD_SIZE - Maximum file upload size (default: 10MB)

Security Variables (NEVER COMMIT):
- SECRET_KEY - Session encryption key
- API_SECRET - [Service] API secret
- DATABASE_PASSWORD - Database password (if not in DATABASE_URL)
- [OTHER_SECRET] - [Purpose]

Example .env file structure:
```
PORT=3000
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
NODE_ENV=development
LOG_LEVEL=debug
```

---

## 📂 Configuration Files

**Purpose**: Document configuration file locations and purposes.

**What to include**:
- Config file locations
- Config file formats
- What each config file controls
- Environment-specific config files

**Example**:
```
Configuration Files:
- .env - Environment variables (git-ignored)
- .env.example - Template with dummy values (committed)
- config/database.js - Database configuration
- config/[framework].config.js - Framework-specific config

Environment-Specific Configs:
- .env.development - Development overrides
- .env.staging - Staging configuration
- .env.production - Production configuration

Config Loading Order:
1. Default values in code
2. .env file (if exists)
3. .env.[environment] file (if exists)
4. Environment variables (highest priority)
```

---

## 🗄️ Database Configuration

**Purpose**: Document database setup and environment-specific settings.

**What to include**:
- Database connection details
- Connection pooling settings
- Schema/migration management
- Environment-specific database URLs

**Example**:
```
Database: [PostgreSQL / MySQL / MongoDB / etc.]

Connection Configuration:
- development: Local database at localhost:[port]
- staging: [Cloud provider] database instance
- production: [Cloud provider] with read replicas

Connection Pool:
- Min connections: [2]
- Max connections: [10]
- Idle timeout: [30]s

Migrations:
- Tool: [Prisma / TypeORM / Knex / etc.]
- Run automatically: [yes/no]
- Migration files: [path/to/migrations]

Environment Variable:
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
```

---

## 🔌 External Service Configuration

**Purpose**: Document external service integrations and their configuration.

**What to include**:
- Service names and purposes
- API endpoints (sandbox vs production)
- Authentication methods
- Rate limits and quotas

**Example**:
```
External Services:

1. [Service Name] - [Purpose, e.g., "Email delivery"]
   - Development: Sandbox API at https://sandbox.service.com
   - Production: Live API at https://api.service.com
   - Auth: API key in API_KEY env var
   - Rate Limit: [1000] requests/hour
   - Docs: [Link to API documentation]

2. [Service Name] - [Purpose]
   - Development: [Mock/local/sandbox]
   - Production: [Live endpoint]
   - Auth: [OAuth / API Key / etc.]
   - Configuration:
     * SERVICE_API_KEY=[key]
     * SERVICE_ENDPOINT=[url]

3. [Add more services as needed]
```

---

## 🏗️ Build & Deployment Configuration

**Purpose**: Document build-time and deployment-specific configuration.

**What to include**:
- Build commands and environment variables
- Deployment platform configuration
- CI/CD environment variables
- Build optimization settings

**Example**:
```
Build Configuration:
- Build command: [npm run build / pnpm build]
- Output directory: [dist / build / .next]
- Environment variables injected at build time:
  * PUBLIC_API_URL - API endpoint URL
  * APP_VERSION - Application version

Deployment Platform: [Vercel / Netlify / Docker / etc.]

Platform-Specific Configuration:
- [Config file]: [vercel.json / netlify.toml / Dockerfile]
- Environment variables set in platform dashboard:
  * [VAR_NAME] - [Purpose]
  * [VAR_NAME] - [Purpose]

CI/CD:
- Platform: [GitHub Actions / GitLab CI / CircleCI / etc.]
- Config file: [.github/workflows/*.yml / .gitlab-ci.yml]
- Secrets managed in: [CI platform secrets / external service]
```

---

## 🎯 Feature Flags & Conditional Config

**Purpose**: Document feature flags and environment-specific feature toggles.

**What to include**:
- Feature flag system
- Environment-specific enabled features
- Configuration conditionals
- Feature rollout strategy

**Example**:
```
Feature Flags: [LaunchDarkly / Custom / Environment variables]

Flags by Environment:
- ENABLE_BETA_FEATURES - true in development/staging, false in production
- USE_NEW_API - true in production, false elsewhere
- DEBUG_MODE - true in development, false elsewhere

Implementation:
if (process.env.ENABLE_BETA_FEATURES === 'true') {
  // Beta feature code
}

Feature Rollout:
1. Enable in development for testing
2. Enable in staging for QA
3. Gradual rollout in production (if supported)
4. Full production enablement
5. Remove flag and make permanent
```

---

## 🔒 Security Configuration

**Purpose**: Document security-related configuration and best practices.

**What to include**:
- Secret management
- CORS configuration
- SSL/TLS settings
- Security headers

**Example**:
```
Secret Management:
- Development: .env file (git-ignored)
- Staging/Production: [Cloud provider secrets / env vars in dashboard]
- Never commit secrets to version control
- Rotate secrets quarterly or after suspected exposure

CORS Configuration:
- Development: Allow all origins
- Staging: Allow staging.example.com
- Production: Allow example.com only

SSL/TLS:
- Development: HTTP (localhost)
- Staging/Production: HTTPS only, redirect HTTP → HTTPS

Security Headers:
- Content-Security-Policy: [Your policy]
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security: max-age=31536000
```

---

## 🚀 Quick Start

**Purpose**: Provide quick setup instructions for new developers.

**What to include**:
- First-time setup steps
- Required environment variables
- Common issues and solutions
- Verification steps

**Example**:
```
First-Time Setup:
1. Copy .env.example to .env:
   cp .env.example .env

2. Fill in required variables in .env:
   - DATABASE_URL (get from [source])
   - API_KEY (get from [service dashboard])
   - [OTHER_REQUIRED_VARS]

3. Install dependencies:
   [npm install / pnpm install / yarn]

4. Run database migrations:
   [npm run migrate / pnpm migrate]

5. Start development server:
   [npm run dev / pnpm dev]

6. Verify setup:
   - Open http://localhost:[PORT]
   - Check logs for errors
   - Test [basic functionality]

Common Issues:
- "Database connection failed" → Check DATABASE_URL format
- "Port already in use" → Change PORT in .env or kill process on that port
- [OTHER_COMMON_ISSUES]
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Run `@.claude/prompts/setup-instructions.md` for guided configuration
2. Document environment variables as you add them
3. Update when you add new external services
4. Review and update when deployment configuration changes

**When agents reference this file**:
- code-writing-agent uses it to understand available configuration options
- debugging-agent uses it to verify environment setup
- testing-agent uses it to configure test environments
- planning-agent uses it to understand environmental constraints
