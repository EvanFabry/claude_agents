# Agent Stub Section Completion Guide

When you encounter a **[STUB]** section during task execution, use this process to get the project-specific details you need.

---

## What This Means

The agent prompt you're executing has generalized sections that were intentionally stubbed to keep the system project-agnostic. These sections need project-specific details that vary by application architecture.

**Don't proceed with assumptions—get the right information.**

---

## How to Get Project-Specific Details

### Step 1: Request Agent-System-Optimizer Consultation

Ask the orchestrator to facilitate a conversation with agent-system-optimizer:

```
I've encountered stub section '[SECTION_NAME]' in [AGENT_NAME]. I need project-specific guidance to complete this task correctly.

Please facilitate a conversation with agent-system-optimizer to retrieve:
- Relevant architecture patterns from project documentation
- Performance requirements and benchmarks
- Integration requirements and constraints
- Known issues or gotchas related to this domain

Specifically for [describe what you're trying to accomplish].
```

**Example:**
```
I've encountered the 'Application-Specific Testing Patterns' stub in testing-agent. I need project-specific guidance for testing a data analysis feature.

Please facilitate a conversation with agent-system-optimizer to retrieve:
- Expected timing sequences and dependencies from @LIFECYCLE.md
- Expected log patterns from DEBUGGING.md
- Performance benchmarks for data processing
- Integration requirements with existing systems
```

### Step 2: Wait for agent-system-optimizer Response

The agent-system-optimizer will provide:
- **Documentation References**: Specific sections from project docs to review
- **Patterns & Best Practices**: Project-specific implementation patterns
- **Performance Targets**: Concrete benchmarks (e.g., "analysis must complete in <5s")
- **Integration Requirements**: How to connect with existing systems
- **Known Constraints**: Issues to avoid or work around

### Step 3: Use the Provided Information

Apply the project-specific guidance to complete your task with proper context. The information will be tailored to the actual application architecture, not generic assumptions.

---

## Why Stub Sections Exist

**Goal**: Keep the multi-agent system reusable across different projects and tech stacks.

**Problem Solved**: Without stubs, agent prompts would be filled with hardcoded details specific to one application (e.g., "API calls must complete in 2 seconds," "Database queries must use connection pooling"). This would make the system unusable for other projects.

**Solution**: Generalize agent prompts, stub application-specific sections, and use agent-system-optimizer as the knowledge authority for project details.

---

## What agent-system-optimizer Has Access To

The agent-system-optimizer can reference project-specific documentation:

**Common Documentation Files:**
- `@ARCHITECTURE.md` - System design patterns, integration flows
- `@LIFECYCLE.md` - Timing dependencies, component lifecycles (if exists)
- `@DEBUGGING.md` - Log patterns, troubleshooting procedures (if exists)
- `RECENT_GOTCHAS.md` - Known issues, workarounds (if exists)
- Other project-specific documentation in the repository

**If Documentation Doesn't Exist:**

If the agent-system-optimizer discovers that relevant documentation is missing, it will:
1. Ask the user to provide the necessary context
2. Help create documentation for future reference
3. Store the information appropriately

---

## Common Stub Section Types

### 1. Application-Specific Architecture Patterns
**Found In**: code-writing-agent, code-reviewer
**Provides**: System design patterns, integration requirements, component lifecycle rules

### 2. Application-Specific Testing Patterns
**Found In**: testing-agent
**Provides**: Expected timing sequences, log patterns, route-specific requirements

### 3. Application-Specific Log Patterns
**Found In**: debugging-agent
**Provides**: Log format references, expected sequences, timing chains

### 4. Application-Specific Planning Context
**Found In**: planning-agent
**Provides**: Architectural constraints, performance targets, integration requirements

### 5. Application-Specific Validation Criteria
**Found In**: critique-and-validation-agent
**Provides**: Success metrics, completion criteria, quality standards

### 6. Application-Specific Performance Standards
**Found In**: code-writing-agent
**Provides**: Performance benchmarks, optimization patterns, resource limits

---

## Universal Principles Preserved in Stubs

Each stub section retains **universal principles** that apply to ANY application:

- Generic error handling patterns
- Standard memory management practices
- Common performance optimization approaches
- Universal testing best practices
- General architectural guidelines

**Use these universal principles as a foundation**, then enhance with project-specific details from agent-system-optimizer.

---

## Quick Reference

| When you see... | Do this... |
|----------------|-----------|
| **[STUB] section during task** | Request agent-system-optimizer consultation via orchestrator |
| **Missing project documentation** | Agent-system-optimizer will ask user for details |
| **Generic examples in stub** | Use as reference, get specific details from agent-system-optimizer |
| **Universal principles in stub** | Apply immediately, enhance with project specifics |

---

**Remember**: Stub sections are a feature, not a limitation. They keep the system flexible while ensuring you get accurate, project-specific guidance when you need it.
