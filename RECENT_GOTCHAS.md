# RECENT_GOTCHAS.md - Current Issues & Workarounds

**[USER CONFIGURATION REQUIRED]**

This is a **living document** tracking current known issues, workarounds, and ongoing investigations. Unlike other documentation files, this file should be updated frequently as issues are discovered and resolved.

---

## 📋 How to Use This File

**Purpose**: Track temporary issues and their solutions in a central location.

**Lifecycle**:
1. **Add** an entry when you discover an issue with a workaround
2. **Update** the entry as you learn more or find better workarounds
3. **Move to DEBUGGING.md** if the issue becomes a permanent pattern
4. **Delete** the entry when the issue is fully resolved

**Update Frequency**: Every time you encounter or resolve an issue (daily/weekly)

**Target Audience**:
- debugging-agent uses this to avoid known issues
- code-writing-agent uses this to implement workarounds
- All agents reference this before diving deep into debugging

---

## 🔴 Critical Issues (P0)

**Purpose**: Issues that block development or cause major functionality loss.

**Format**:
```markdown
### [Issue Title]
**Status**: [Open / In Progress / Blocked / Resolved]
**Discovered**: YYYY-MM-DD
**Impact**: [What's broken and who it affects]
**Workaround**: [Temporary solution]
**Root Cause**: [Known / Under investigation / Unknown]
**Tracking**: [Link to issue tracker / Internal discussion]
**Notes**: [Additional context]
```

**Example**:
```markdown
### Example: Database Connection Pool Exhaustion
**Status**: In Progress
**Discovered**: 2025-01-15
**Impact**: Application becomes unresponsive after ~1 hour of heavy traffic. Affects all users.
**Workaround**: Restart server every hour via cron job until fix is deployed
**Root Cause**: Connection leak in [specific module] - identified via profiling
**Tracking**: Issue #123
**Notes**: Fix in PR #456, deploying to staging for testing
```

---

## 🟡 High Priority Issues (P1)

**Purpose**: Issues that significantly impact development or user experience.

**Example**:
```markdown
### Example: Search Not Returning Results for Special Characters
**Status**: Open
**Discovered**: 2025-01-14
**Impact**: Users can't search for terms with special characters (e.g., "C++", "user@domain")
**Workaround**: URL encode search terms before sending: encodeURIComponent(searchTerm)
**Root Cause**: Backend doesn't handle URL-encoded special characters properly
**Tracking**: Issue #120
**Notes**: Affects ~5% of searches. Need backend fix.
```

---

## 🟢 Medium Priority Issues (P2)

**Purpose**: Issues that are annoying but have acceptable workarounds.

**Example**:
```markdown
### Example: Hot Reload Slow on Large Component Changes
**Status**: Open
**Discovered**: 2025-01-10
**Impact**: HMR takes 5-10 seconds instead of instant on changes to large files
**Workaround**: Split large files into smaller components
**Root Cause**: Vite HMR struggles with files >500 lines
**Tracking**: None (known limitation)
**Notes**: Not urgent, but consider refactoring [ComponentName] eventually
```

---

## 🔵 Low Priority / Informational (P3)

**Purpose**: Minor issues, quirks, or things to be aware of.

**Example**:
```markdown
### Example: Console Warning About PropTypes in Development
**Status**: Open
**Discovered**: 2025-01-08
**Impact**: Harmless console warning in development only
**Workaround**: Ignore (doesn't affect functionality)
**Root Cause**: Third-party library [LibraryName] using deprecated PropTypes
**Tracking**: Reported upstream, waiting for library update
**Notes**: Will resolve when library updates to v3.x
```

---

## ✅ Recently Resolved

**Purpose**: Keep resolved issues for 30 days for reference, then delete.

**Example**:
```markdown
### Example: Build Failing on CI Due to TypeScript Errors
**Status**: Resolved
**Discovered**: 2025-01-05
**Resolved**: 2025-01-06
**Impact**: All CI builds failing, blocking deployments
**Solution**: Updated TypeScript from 5.2 to 5.3, fixed type errors in [files]
**Root Cause**: TypeScript 5.3 has stricter type checking for [specific pattern]
**Notes**: Delete this entry after 2025-02-06 (30 days from resolution)
```

---

## 🔍 Under Investigation

**Purpose**: Issues we know exist but haven't found root cause or workaround yet.

**Example**:
```markdown
### Example: Intermittent 500 Errors on API Endpoint
**Status**: Under Investigation
**Discovered**: 2025-01-12
**Impact**: ~1% of API calls to /api/data fail with 500 error
**Workaround**: Client retry works (error doesn't repeat)
**Investigation Progress**:
- 2025-01-12: Added detailed logging
- 2025-01-13: Appears to correlate with high traffic times
- 2025-01-14: Monitoring database query times
**Next Steps**: Profile database queries under load
**Notes**: Cannot reproduce locally
```

---

## 🌐 Environment-Specific Issues

**Purpose**: Issues that only occur in specific environments.

**Example**:
```markdown
### Example: Auth Cookies Not Persisting in Safari
**Status**: Open
**Discovered**: 2025-01-11
**Impact**: Safari users (desktop & mobile) must log in on every page load
**Environment**: Safari only (Chrome/Firefox work fine)
**Workaround**: Use session storage instead of cookies for Safari (user agent detection)
**Root Cause**: Safari's cookie privacy settings blocking third-party cookies
**Tracking**: Issue #118
**Notes**: May need to reconsider auth strategy for Safari compatibility
```

---

## 🐛 Known Dependencies Issues

**Purpose**: Issues in third-party libraries that affect our application.

**Example**:
```markdown
### Library: [LibraryName] v2.3.4
**Issue**: Memory leak in [specific feature]
**Impact**: Application memory grows over time in production
**Workaround**:
  - Option 1: Downgrade to v2.3.3 (no memory leak)
  - Option 2: Restart application nightly
**Status**: Reported to library maintainers (issue #789)
**Timeline**: Fix expected in v2.3.5 (ETA 2025-02-01)
**Notes**: Currently using Option 1 (downgraded)
```

---

## 🔧 Configuration Gotchas

**Purpose**: Non-obvious configuration issues that took time to figure out.

**Example**:
```markdown
### Gotcha: Environment Variables Not Loading in [Context]
**Issue**: .env variables not available in [server components / build scripts / etc.]
**Solution**: Must prefix with NEXT_PUBLIC_ (for Next.js) or VITE_ (for Vite) or load explicitly in [file]
**Context**: [When this applies]
**Date Discovered**: 2025-01-09
**Notes**: Document this in ENVIRONMENT.md once stable
```

---

## 🎯 Testing Gotchas

**Purpose**: Issues specific to testing that aren't bugs in application code.

**Example**:
```markdown
### Gotcha: E2E Tests Failing Due to Auth State
**Issue**: Tests intermittently fail because logged-out browser profile is used
**Solution**: ALWAYS explicitly specify browser configuration in testing-agent prompts
**Correct Pattern**: "Use logged-in Chrome profile (default)"
**Incorrect Pattern**: Omitting browser configuration (defaults vary)
**Date Discovered**: 2025-01-07
**Reference**: CLAUDE.md Section II (Browser Configuration)
```

---

## 📊 Performance Gotchas

**Purpose**: Performance issues and their solutions.

**Example**:
```markdown
### Gotcha: Slow Queries on [Table] Without Index
**Issue**: Queries filtering by [column] take 5+ seconds
**Solution**: Add index: CREATE INDEX idx_[table]_[column] ON [table]([column])
**Impact**: Query time reduced to <50ms
**Date Discovered**: 2025-01-06
**Notes**: Migration created (migrations/YYYYMMDD_add_index.sql)
```

---

## 📝 Maintenance Notes

**Cleanup Schedule**:
- Review this file weekly
- Move persistent patterns to DEBUGGING.md
- Delete resolved issues after 30 days
- Archive critical historical issues to docs/ if needed

**Size Limit**:
- Keep file under 500 lines
- If exceeding, archive old resolved issues

**Format Standards**:
- Always include Date Discovered
- Always include Status
- Always include Workaround (even if "None known yet")
- Use consistent formatting

---

## 🚀 Quick Reference Template

**Copy this template when adding new issues**:

```markdown
### [Clear, Descriptive Title]
**Status**: [Open / In Progress / Blocked / Resolved / Under Investigation]
**Discovered**: YYYY-MM-DD
**Impact**: [What's broken and severity]
**Workaround**: [Temporary solution or "None known"]
**Root Cause**: [Known / Under investigation / Unknown]
**Tracking**: [Issue #XXX / PR #XXX / None]
**Notes**: [Additional context, next steps, etc.]
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Start empty (no example issues)
2. Add issues as you discover them during development
3. Update issues as you learn more
4. Clean up regularly (weekly review)
5. Move stable patterns to DEBUGGING.md

**When agents reference this file**:
- debugging-agent checks this FIRST before deep investigation
- code-writing-agent uses this to avoid known pitfalls
- testing-agent uses this to understand test failures
- planning-agent uses this to assess risk of similar issues

**Important**: This is the ONLY documentation file that should change frequently (daily/weekly). All other files document stable patterns.
