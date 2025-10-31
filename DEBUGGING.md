# DEBUGGING.md - Log Patterns & Troubleshooting

**[USER CONFIGURATION REQUIRED]**

This file documents log patterns, error messages, and troubleshooting procedures for your application. Agents reference this file when debugging issues.

---

## 📋 Log Format & Patterns

**Purpose**: Document your application's logging structure.

**What to include**:
- Log format/structure
- Log levels used (error, warn, info, debug)
- Timestamp formats
- Log output destinations

**Example**:
```
Log Format:
[TIMESTAMP] [LEVEL] [COMPONENT] Message

Example:
2025-01-15T10:30:45.123Z [INFO] [AuthService] User logged in: user@example.com
2025-01-15T10:30:46.456Z [ERROR] [DatabaseService] Query failed: Connection timeout

Log Levels:
- ERROR: Critical failures requiring immediate attention
- WARN: Potential issues, degraded functionality
- INFO: Normal operational messages
- DEBUG: Detailed diagnostic information

Log Destinations:
- Console: [enabled in development/staging/production]
- File: [path/to/logs/*.log]
- External Service: [e.g., Datadog, Sentry, CloudWatch]
```

---

## 🔍 Common Error Patterns

**Purpose**: Document frequent error messages and their meanings.

**What to include**:
- Error message patterns
- Root causes
- Common solutions
- Error codes (if applicable)

**Example**:
```
ERROR: "[Specific error message pattern]"
Cause: [What triggers this error]
Solution: [How to fix it]
Prevention: [How to avoid it in the future]

ERROR: "[Another error message pattern]"
Cause: [Root cause]
Solution: [Fix steps]
Related: [Link to issue tracker / documentation]
```

---

## 🔎 Diagnostic Procedures

**Purpose**: Document step-by-step debugging approaches for common issues.

**What to include**:
- Systematic debugging steps
- Where to look for issues
- How to reproduce problems
- Diagnostic commands or tools

**Example**:
```
Issue: [Problem description, e.g., "Slow page load"]

Diagnostic Steps:
1. Check [specific log file/console] for [error pattern]
2. Verify [configuration/service] is running
3. Test [specific functionality] in isolation
4. Review [metrics/profiler] for bottlenecks
5. Check [dependency/service] status

Commands:
- `[command to check logs]`
- `[command to verify service status]`
- `[command to run diagnostics]`
```

---

## 🚨 Error Categories & Priority

**Purpose**: Classify errors by severity and required response.

**What to include**:
- Error categorization system
- Response time expectations
- Escalation procedures
- Impact assessment

**Example**:
```
Critical (P0):
- Service completely down
- Data loss or corruption
- Security breach
Response: Immediate (drop everything)

High (P1):
- Major feature broken
- Significant performance degradation
- User-facing errors affecting many users
Response: Within 1 hour

Medium (P2):
- Minor feature issues
- Edge case errors
- Non-critical warnings
Response: Within 1 day

Low (P3):
- Cosmetic issues
- Informational warnings
- Nice-to-have improvements
Response: Next sprint
```

---

## 🔧 Debugging Tools & Techniques

**Purpose**: Document available debugging tools and how to use them.

**What to include**:
- Browser DevTools specific features
- Backend debugging tools
- Profiling tools
- Logging utilities

**Example**:
```
Frontend Debugging:
- Browser DevTools: [Chrome/Firefox/etc.] - [Specific features you use]
- React DevTools: [If applicable]
- Network tab: Check for [specific patterns]
- Performance profiler: Look for [bottlenecks]

Backend Debugging:
- Debugger: [Node inspector / Python pdb / etc.]
- Log analysis: [grep patterns / log aggregator queries]
- Performance profiling: [Tool name and usage]
- Database query analysis: [EXPLAIN / query profiler]

Debugging Commands:
- `[command to enable debug logging]`
- `[command to profile performance]`
- `[command to inspect state]`
```

---

## 📊 Performance Debugging

**Purpose**: Document how to diagnose performance issues.

**What to include**:
- Performance metrics to monitor
- Profiling procedures
- Bottleneck identification
- Optimization verification

**Example**:
```
Metrics to Monitor:
- Page load time: Target <[3]s
- API response time: Target <[500]ms
- Database query time: Target <[100]ms
- Memory usage: Watch for leaks
- CPU usage: Normal range [X-Y]%

Profiling:
1. Use [profiling tool] to capture [metric]
2. Look for [specific patterns indicating issues]
3. Compare to baseline: [expected values]
4. Identify top [3-5] slowest operations

Common Bottlenecks:
- [Issue]: Usually caused by [reason] - Fix: [solution]
- [Issue]: Check [specific component/query] - Fix: [solution]
```

---

## 🐛 Known Issues & Workarounds

**Purpose**: Document current known issues (reference RECENT_GOTCHAS.md for active issues).

**What to include**:
- Persistent bugs being tracked
- Temporary workarounds
- Root cause understanding
- Fix timeline

**Example**:
```
Known Issue: [Description]
Status: [Open / In Progress / Planned]
Workaround: [Temporary solution]
Root Cause: [Technical explanation]
Fix ETA: [Timeline or "Unknown"]
Tracking: [Issue #123 / RECENT_GOTCHAS.md]

Known Issue: [Description]
[...]
```

---

## 📈 Monitoring & Alerts

**Purpose**: Document monitoring setup and alert conditions.

**What to include**:
- What is monitored
- Alert thresholds
- Alert destinations
- On-call procedures (if applicable)

**Example**:
```
Monitoring Tools: [Datadog / New Relic / CloudWatch / etc.]

Monitored Metrics:
- Uptime: Alert if down for >[1]min
- Error rate: Alert if >[5]% of requests fail
- Response time: Alert if p95 >[2]s
- Memory usage: Alert if >[80]% of available
- Disk space: Alert if >[85]% full

Alert Channels:
- Email: [team@example.com]
- Slack: [#alerts channel]
- PagerDuty: [For critical alerts]

Response Procedure:
1. Check alert details in [monitoring dashboard]
2. Follow runbook for specific alert type
3. Escalate to [person/team] if unresolved in [X] minutes
```

---

## 🔄 Debugging Workflow

**Purpose**: Document the systematic debugging approach.

**What to include**:
- Standard debugging process
- When to use each debugging tool
- Escalation paths
- Documentation requirements

**Example**:
```
Standard Debugging Process:
1. Reproduce the issue consistently
2. Check logs for error messages
3. Isolate the failing component
4. Add diagnostic logging if needed
5. Test potential fixes
6. Verify fix resolves issue
7. Document findings (update this file or RECENT_GOTCHAS.md)

When to Escalate:
- Issue blocks critical functionality: Escalate immediately
- Issue persists after [2 hours] investigation: Ask for help
- Security-related issue: Escalate immediately
- Unknown error pattern: Consult team before proceeding
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Document errors as you encounter them
2. Update log patterns when you change logging
3. Keep RECENT_GOTCHAS.md for active issues (this file for persistent patterns)
4. Review and update quarterly or when debugging processes change

**When agents reference this file**:
- debugging-agent uses it to understand log patterns and diagnostic procedures
- code-writing-agent uses it to add appropriate error handling
- testing-agent uses it to verify error conditions are handled correctly
- planning-agent uses it to understand system failure modes
