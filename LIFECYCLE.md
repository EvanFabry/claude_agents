# LIFECYCLE.md - Application Timing & Component Lifecycles

**[USER CONFIGURATION REQUIRED]**

This file documents timing dependencies, component lifecycles, and initialization sequences in your application. Agents reference this file when they need to understand timing-critical behavior.

---

## ⏱️ Application Initialization Sequence

**Purpose**: Document the order and timing of application startup.

**What to include**:
- Initialization steps and their order
- Timing dependencies between steps
- Async operations and their completion requirements
- Bootstrap process details

**Example**:
```
1. [Step 1] - Load configuration (synchronous)
2. [Step 2] - Initialize database connection (~500ms)
3. [Step 3] - Register middleware (synchronous)
4. [Step 4] - Start server on port [PORT] (~100ms)
5. [Step 5] - [Other initialization step]

Critical Timing:
- [Component A] MUST complete before [Component B] starts
- [Service X] waits for [Event Y] before processing requests
```

---

## 🔄 Component Lifecycle Patterns

**Purpose**: Document lifecycle patterns for major components (if applicable).

**What to include**:
- Component mount/unmount sequences
- State initialization timing
- Event listener registration/cleanup
- Resource acquisition and release

**Example (for React/Vue/etc.)**:
```
Standard Component Lifecycle:
1. Constructor/Setup - Initialize local state
2. Mount - Attach to DOM, fetch initial data
3. Update - Re-render on prop/state changes
4. Unmount - Cleanup listeners, cancel requests

Critical Components:
- [ComponentName]:
  * Mounts after [dependency] is ready
  * Requires [data/service] before rendering
  * Cleanup: [specific cleanup actions]
```

**Example (for Backend Services)**:
```
Service Lifecycle:
1. Registration - Service registered with DI container
2. Initialization - Database connections, cache warming
3. Ready - Accepting requests
4. Shutdown - Graceful connection closure, pending request completion
```

---

## 🎯 Page/Route Lifecycle

**Purpose**: Document page load and route transition timing.

**What to include**:
- Page load sequence
- Data fetching patterns
- Loading states and skeleton screens
- Transition animations timing

**Example**:
```
Page Load Sequence:
1. Route match and component selection
2. Layout render (immediate)
3. Data fetch initiation (async)
4. Loading state display (~0ms)
5. Data received and content render (~500-2000ms)
6. Page interactive state

Data Fetching:
- [Page/Route]: Fetches [data] from [source] (~[time]ms)
- [Page/Route]: Requires [authentication/authorization] check first
- [Page/Route]: Uses [caching strategy]
```

---

## ⚡ Event Handling & Timing

**Purpose**: Document event-driven timing and dependencies.

**What to include**:
- Critical event sequences
- Event debouncing/throttling
- User interaction timing
- Real-time update patterns (if applicable)

**Example**:
```
Event Timing:
- User input: Debounced at [300]ms
- Auto-save: Triggered [5]s after last change
- Real-time updates: Polling every [30]s / WebSocket push
- Animation duration: [300]ms (match this in tests)

Critical Event Sequences:
- [Event A] must fire before [Event B]
- [Action X] triggers [async operation] with [timeout]
```

---

## 🔌 Async Operations & Promises

**Purpose**: Document async operation patterns and timing requirements.

**What to include**:
- API call timeouts
- Retry strategies
- Concurrent operation limits
- Race condition prevention

**Example**:
```
API Calls:
- Timeout: [5]s for standard requests, [30]s for heavy operations
- Retry: [3] attempts with exponential backoff
- Concurrent: Maximum [5] parallel requests

Race Condition Prevention:
- [Operation]: Uses [locking/debouncing/queue] to prevent conflicts
- [Operation]: Cancels previous requests when new one starts
```

---

## 🗄️ Database Operation Timing

**Purpose**: Document database-related timing patterns (if applicable).

**What to include**:
- Connection pool configuration
- Query timeout settings
- Transaction lifecycle
- Migration timing

**Example**:
```
Database Connections:
- Pool size: [min] to [max] connections
- Connection timeout: [10]s
- Query timeout: [30]s

Transactions:
- Isolation level: [READ COMMITTED / SERIALIZABLE / etc.]
- Timeout: [10]s
- Retry on deadlock: [yes/no]

Migrations:
- Run during: [startup / manually / CI/CD]
- Timeout: [5]min
```

---

## 🚦 State Management Lifecycle

**Purpose**: Document state management patterns and timing.

**What to include**:
- Global state initialization
- State persistence timing
- Cache invalidation patterns
- State synchronization across components

**Example**:
```
State Management: [Redux / MobX / Vuex / Context / etc.]

Initialization:
- Store created during [app bootstrap / lazy load]
- Persisted state rehydrated from [localStorage / IndexedDB]
- Initial data fetch: [synchronous / async]

State Updates:
- Actions dispatched [synchronously / asynchronously]
- Updates propagate to components [immediately / batched]
- Side effects triggered via [middleware / watchers / effects]
```

---

## ⏲️ Performance Timing Targets

**Purpose**: Document expected timing for performance-sensitive operations.

**What to include**:
- Page load targets
- Component render targets
- API response time expectations
- Database query time expectations

**Example**:
```
Performance Targets:
- Initial page load: <[3]s
- Route transitions: <[500]ms
- Component interactions: <[100]ms (to feel instant)
- API responses: <[1]s typical, <[3]s worst case
- Database queries: <[100]ms simple, <[500]ms complex
```

---

## 🔧 Testing Considerations

**Purpose**: Document timing considerations for testing.

**What to include**:
- Wait times in tests
- Timing-sensitive assertions
- Mock timing requirements
- Async operation handling in tests

**Example**:
```
Test Timing:
- Wait for [component] mount: ~[100]ms
- Wait for API response: ~[500]ms (mocked)
- Animation completion: [300]ms (match actual timing)
- Debounced input: Wait [350]ms after typing

Timing-Sensitive Tests:
- [Test scenario]: Must wait for [specific event/timing]
- [Test scenario]: Uses polling with [timeout]
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Run `@.claude/prompts/setup-instructions.md` for guided configuration
2. Profile your application to measure actual timing
3. Document timing failures you've encountered and their solutions
4. Update as you discover timing-sensitive behavior

**When agents reference this file**:
- code-writing-agent uses it to avoid introducing timing bugs
- debugging-agent uses it to identify timing-related issues
- testing-agent uses it to set appropriate wait times and assertions
- planning-agent uses it to understand timing constraints
