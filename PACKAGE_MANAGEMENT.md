# PACKAGE_MANAGEMENT.md - Package Scripts & Dependencies

**[USER CONFIGURATION REQUIRED]**

This file documents package management, npm/pnpm/yarn scripts, and dependency management strategies. Agents reference this file when they need to understand build tools and package operations.

---

## 📦 Package Manager

**Purpose**: Document which package manager is used and why.

**What to include**:
- Package manager choice (npm, pnpm, yarn, bun)
- Version requirements
- Installation instructions
- Lock file information

**Example**:
```
Package Manager: [pnpm 8.x / npm 10.x / yarn 4.x / bun 1.x]

Why this choice:
- [Performance benefits / Disk space efficiency / Team preference]

Installation:
- Install: [npm install -g pnpm@8 / brew install pnpm]
- Verify: [pnpm --version]

Lock File: [pnpm-lock.yaml / package-lock.json / yarn.lock / bun.lockb]
- Committed to git: Yes
- Regenerate on: Dependency changes only
- Conflicts: Resolve by [regenerating / manual merge]
```

---

## 🚀 NPM Scripts

**Purpose**: Document all package.json scripts and their purposes.

**What to include**:
- Script name and purpose
- When to use each script
- Environment requirements
- Expected output

**Example**:
```
Development Scripts:
- `dev` - Start development server
  Usage: [npm run dev / pnpm dev]
  Port: [3000 / 5173 / configured in .env]
  Hot reload: [Yes/No]

- `dev:debug` - Start development server with debugger
  Usage: [npm run dev:debug]
  Debugger port: [9229]

Build Scripts:
- `build` - Build for production
  Usage: [npm run build]
  Output: [dist/ / build/ / .next/]
  Time: ~[30]s

- `build:analyze` - Build with bundle analysis
  Usage: [npm run build:analyze]
  Opens: Bundle analyzer in browser

Testing Scripts:
- `test` - Run all tests
  Usage: [npm test]
  Coverage: [yes/no]

- `test:unit` - Run unit tests only
  Usage: [npm run test:unit]

- `test:e2e` - Run end-to-end tests
  Usage: [npm run test:e2e]
  Requires: Development server running / Starts automatically

Quality Scripts:
- `lint` - Run ESLint
  Usage: [npm run lint]
  Auto-fix: Use `npm run lint:fix`

- `typecheck` - Run TypeScript type checking
  Usage: [npm run typecheck]
  No output = success

- `format` - Format code with Prettier
  Usage: [npm run format]

Database Scripts:
- `db:migrate` - Run database migrations
  Usage: [npm run db:migrate]

- `db:seed` - Seed database with test data
  Usage: [npm run db:seed]

- `db:studio` - Open database GUI
  Usage: [npm run db:studio]

Utility Scripts:
- `clean` - Clean build artifacts
  Usage: [npm run clean]
  Removes: [dist/, .next/, node_modules/.cache/, etc.]

- `install:clean` - Clean install dependencies
  Usage: [npm run install:clean]
  Process: Remove node_modules, clean cache, fresh install
```

---

## 📚 Dependencies

**Purpose**: Document major dependencies and their purposes.

**What to include**:
- Key production dependencies
- Development dependencies
- Peer dependencies
- Version constraints

**Example**:
```
Production Dependencies:

Framework:
- [react@18.x / vue@3.x / next@14.x / etc.] - Frontend framework
- [express@4.x / fastify@4.x] - Backend framework (if applicable)

Database & ORM:
- [prisma@5.x / typeorm@0.3.x / mongoose@8.x] - Database ORM
- [pg@8.x / mysql2@3.x / mongodb@6.x] - Database driver

UI Libraries:
- [tailwindcss@3.x / mui@5.x / chakra-ui@2.x] - UI framework
- [radix-ui@1.x / headlessui@1.x] - Component primitives

Utilities:
- [lodash@4.x / date-fns@3.x / zod@3.x] - Utility libraries

Development Dependencies:

Build Tools:
- [vite@5.x / webpack@5.x / turbopack] - Bundler
- [typescript@5.x] - Type system

Testing:
- [vitest@1.x / jest@29.x] - Unit test framework
- [playwright@1.x / cypress@13.x] - E2E testing
- [@testing-library/react@14.x] - Component testing utilities

Code Quality:
- [eslint@8.x] - Linting
- [prettier@3.x] - Code formatting
- [@typescript-eslint/...] - TypeScript ESLint rules

Version Pinning:
- Exact versions: [Yes for critical dependencies / No, use caret ^]
- Update strategy: [Automated via Dependabot / Manual quarterly review]
```

---

## 🔄 Dependency Management

**Purpose**: Document dependency update and management strategies.

**What to include**:
- Update frequency
- Testing procedures
- Security patch handling
- Deprecation strategy

**Example**:
```
Update Strategy:
- Minor updates: [Monthly / Quarterly]
- Major updates: [After testing in development]
- Security patches: [Immediately]

Update Process:
1. Check for updates: [npm outdated / pnpm outdated]
2. Review changelogs for breaking changes
3. Update in development branch
4. Run full test suite
5. Test in staging environment
6. Deploy to production

Automated Updates:
- Tool: [Dependabot / Renovate / None]
- Auto-merge: [Security patches only / Never]
- Frequency: [Weekly / Monthly]

Security:
- Audit command: [npm audit / pnpm audit]
- Audit frequency: [Weekly / On CI/CD]
- Fix command: [npm audit fix / pnpm audit --fix]
- Critical vulnerabilities: Address within [24] hours

Deprecated Dependencies:
- Policy: Replace within [90] days of deprecation notice
- Alternatives: Research and test before migrating
- Migration plan: Document breaking changes and migration path
```

---

## 🔧 Build Configuration

**Purpose**: Document build tool configuration.

**What to include**:
- Build tool and configuration files
- Build optimizations
- Environment-specific builds
- Output configuration

**Example**:
```
Build Tool: [Vite / Webpack / Turbopack / Rollup]

Configuration Files:
- [vite.config.ts / webpack.config.js / turbo.json]
- [tsconfig.json] - TypeScript configuration
- [postcss.config.js] - PostCSS plugins (if using Tailwind)

Build Optimizations:
- Code splitting: [Automatic / Manual via dynamic imports]
- Tree shaking: [Enabled]
- Minification: [Terser / SWC / esbuild]
- Source maps: [Production: hidden, Development: inline]

Environment-Specific:
- Development:
  * Hot module replacement: [Enabled]
  * Source maps: [Full]
  * Minification: [Disabled]

- Production:
  * Minification: [Enabled]
  * Source maps: [Hidden or external]
  * Bundle analysis: [Available via build:analyze]

Output:
- Directory: [dist/ / build/ / .next/ / out/]
- Assets: [dist/assets/]
- Chunks: [Vendor / App / Per-route]
```

---

## 🌲 Monorepo Configuration

**Purpose**: Document monorepo setup (if applicable).

**What to include**:
- Workspace configuration
- Shared dependencies
- Build orchestration
- Inter-package dependencies

**Example**:
```
Monorepo Tool: [pnpm workspaces / Nx / Turborepo / Lerna]

Workspace Structure:
packages/
  ├── app - Main application
  ├── shared - Shared utilities
  ├── ui - Component library
  └── [other-packages]

Configuration File: [pnpm-workspace.yaml / nx.json / turbo.json]

Shared Dependencies:
- Hoisted to root: [React, TypeScript, testing tools]
- Package-specific: Isolated in package directories

Build Order:
1. shared (no dependencies)
2. ui (depends on shared)
3. app (depends on shared, ui)

Commands:
- Install all: [pnpm install]
- Build all: [pnpm -r build]
- Build one: [pnpm --filter app build]
- Run in all: [pnpm -r [command]]

Note: If NOT using monorepo, delete this section.
```

---

## 🐳 Development Environment

**Purpose**: Document development environment setup beyond package installation.

**What to include**:
- Required system dependencies
- IDE/editor recommendations
- Pre-commit hooks
- Development tools

**Example**:
```
System Requirements:
- Node.js: [v18.x or later / v20.x LTS recommended]
- Package manager: [pnpm 8.x]
- [Other tools]: [Docker for local DB / etc.]

IDE Setup:
- Recommended: [VSCode / WebStorm]
- Extensions:
  * ESLint
  * Prettier
  * [Framework-specific extension]
  * [Database extension if applicable]

Git Hooks:
- Tool: [Husky / Lefthook / simple-git-hooks]
- Pre-commit: Lint staged files, type check
- Pre-push: Run tests (optional)
- Configuration: [.husky/ / lefthook.yml]

Development Tools:
- [Tool name]: [Purpose]
- [Tool name]: [Purpose]
```

---

## ⚡ Performance & Optimization

**Purpose**: Document package-related performance optimizations.

**What to include**:
- Bundle size targets
- Lazy loading strategies
- Code splitting patterns
- Dependency optimization

**Example**:
```
Bundle Size Targets:
- Main bundle: <[500]KB (gzipped)
- Vendor bundle: <[300]KB (gzipped)
- Individual routes: <[200]KB (gzipped)

Optimization Strategies:
- Dynamic imports for large dependencies
- Tree shaking enabled for all libraries
- Minimize use of large utility libraries (prefer specific imports)
- Regular bundle analysis to catch regressions

Code Splitting:
- Route-based: Automatic via [framework]
- Component-based: Manual via dynamic imports
- Libraries: Vendor chunk separate from app code

Dependency Optimization:
- Use [lodash-es] instead of [lodash] for tree shaking
- Replace large libraries with smaller alternatives:
  * [moment] → [date-fns] (saved [XKB])
  * [Library] → [Alternative] (saved [XKB])
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Document scripts as you add them to package.json
2. Update dependency sections when adding major dependencies
3. Review and update quarterly or when build setup changes
4. Keep bundle size targets updated based on actual measurements

**When agents reference this file**:
- code-writing-agent uses it to understand build commands and dependencies
- testing-agent uses it to run appropriate test commands
- debugging-agent uses it to understand build configuration
- planning-agent uses it to understand development environment constraints
