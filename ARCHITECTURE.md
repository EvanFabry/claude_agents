# ARCHITECTURE.md - System Architecture Documentation

**[USER CONFIGURATION REQUIRED]**

This file should document your application's architecture, design patterns, and system integration flows. Agents reference this file when they need to understand how your system is structured.

---

## 🏗️ System Overview

**Purpose**: Provide a high-level overview of your application architecture.

**What to include**:
- Technology stack (frontend framework, backend, database, etc.)
- Core architectural principles
- Key design patterns used in your application
- Component relationships and dependencies

**Example**:
```
This application is a [React/Vue/Angular/etc.] frontend with a [Node.js/Python/Go] backend,
using [PostgreSQL/MongoDB/etc.] for data persistence. The architecture follows [MVC/MVVM/etc.]
patterns with [REST/GraphQL] API communication.

Core Principles:
1. [Principle 1 - e.g., "Separation of concerns"]
2. [Principle 2 - e.g., "Component reusability"]
3. [Principle 3 - e.g., "Performance-first design"]
```

---

## 🔄 Request Flow Architecture

**Purpose**: Document how requests flow through your system.

**What to include**:
- Complete request lifecycle diagrams
- Authentication/authorization flows
- API endpoint patterns
- Data flow between components

**Example**:
```
[Browser] → [Frontend Router] → [API Layer] → [Business Logic] → [Database]
     ↓              ↓                ↓              ↓              ↓
[UI Component] [Auth Check]    [Validation]   [Processing]   [Query/Update]
```

---

## 🗂️ Component Architecture

**Purpose**: Document major components and their responsibilities.

**What to include**:
- Frontend components/modules structure
- Backend services/controllers structure
- Shared utilities and libraries
- Third-party integrations

**Example**:
```
Frontend Components:
├── /components/common - Reusable UI components
├── /components/features - Feature-specific components
├── /hooks - Custom React hooks (if applicable)
└── /utils - Frontend utility functions

Backend Structure:
├── /routes - API route definitions
├── /controllers - Request handlers
├── /services - Business logic
├── /models - Data models
└── /middleware - Request/response middleware
```

---

## 🔐 Authentication & Authorization

**Purpose**: Document how authentication and authorization work in your application.

**What to include**:
- Authentication method (JWT, sessions, OAuth, etc.)
- Token management and storage
- Authorization patterns (RBAC, permissions, etc.)
- Protected route handling

**Example**:
```
Authentication: [JWT tokens / Session cookies / OAuth2]
Token Storage: [localStorage / httpOnly cookies / memory]
Authorization: [Role-based / Permission-based / Custom]
Protected Routes: [Frontend guards / Backend middleware]
```

---

## 🗄️ Data Architecture

**Purpose**: Document database design and data flow patterns.

**What to include**:
- Database schema overview
- Key relationships between entities
- Data access patterns
- Caching strategies (if applicable)

**Example**:
```
Database: [PostgreSQL/MongoDB/etc.]
Key Tables/Collections:
- users (id, email, role, created_at)
- [entity_name] (fields...)
- [entity_name] (fields...)

Relationships:
- users → [related_entity] (one-to-many)
- [entity] ↔ [entity] (many-to-many)
```

---

## 🔌 Integration Points

**Purpose**: Document external services and APIs your application integrates with.

**What to include**:
- Third-party services (payment, analytics, etc.)
- External APIs consumed
- Webhooks or event handlers
- Service communication patterns

**Example**:
```
External Services:
- [Service Name]: [Purpose] - [Integration method]
- [Service Name]: [Purpose] - [Integration method]

API Integrations:
- [API Name]: [Endpoint patterns] - [Authentication method]
```

---

## 📦 Build & Deployment

**Purpose**: Document build process and deployment architecture.

**What to include**:
- Build commands and outputs
- Environment configurations
- Deployment platforms and strategies
- CI/CD pipeline overview

**Example**:
```
Build Command: [npm run build / pnpm build / etc.]
Output Directory: [dist/ / build/ / .next/ / etc.]
Deployment: [Vercel / Netlify / AWS / Docker / etc.]
Environments: [development / staging / production]
```

---

## 🎯 Performance Considerations

**Purpose**: Document performance requirements and optimization strategies.

**What to include**:
- Performance targets (load time, API response time, etc.)
- Optimization techniques used
- Caching strategies
- Known performance bottlenecks

**Example**:
```
Targets:
- Page load: <3s
- API response: <500ms
- Database queries: <100ms

Optimizations:
- [Technique 1 - e.g., "Code splitting"]
- [Technique 2 - e.g., "Image optimization"]
- [Technique 3 - e.g., "API response caching"]
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Run `@.claude/prompts/setup-instructions.md` for guided configuration
2. Consult with agent-system-optimizer: `@agent-system-optimizer Help me document my application architecture`
3. Reference your existing architecture documentation (if available)
4. Update incrementally as your architecture evolves

**When agents reference this file**:
- planning-agent uses it to understand system constraints
- code-writing-agent uses it to maintain architectural consistency
- debugging-agent uses it to understand component interactions
- testing-agent uses it to validate integration points
