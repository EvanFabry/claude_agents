# Bash Access Control for Multi-Agent Workflows

This document describes the Bash access control system used across the multi-agent architecture.

## Overview

**Current System**: All agents use Bash with different permission levels:
- **Orchestrator**: FULL Bash access (unrestricted)
- **Subagents**: RESTRICTED Bash access (pnpm and git only)

**Enforcement**: `.claude/hooks/pretooluse_bash_validation.sh` hook blocks unauthorized commands before execution.

---

## Agent Access Levels

### Orchestrator (Full Access)

**Permissions**: Unrestricted - can run any Bash command

**Use Cases**:
- System coordination and management
- Complex multi-step operations
- Package management (pnpm install, etc.)
- Version control (all git operations)
- Quality checks (typecheck, lint, test)

**Examples**:
```bash
Bash("pnpm install")                  # ✅ Package installation
Bash("pnpm exec tsx script.ts")       # ✅ Script execution
Bash("git commit -m 'message'")       # ✅ Version control
Bash("ls -la testing_agent/outputs")  # ✅ File system operations
Bash("killport 5373")                 # ✅ Process management
```

### Subagents (Restricted Access)

**Allowed Commands**: `pnpm`, `git` only

**Forbidden**:
- ❌ Other commands (npm, node, curl, ls, cat, rm, mv, cp)
- ❌ Chained commands (`&&`, `||`, `;`)
- ❌ Pipes (`|`)
- ❌ Redirects (`>`, `>>`, `<`)
- ❌ Background processes (`&`)

**Allowed Patterns**:
```bash
# Quality Checks
Bash("pnpm typecheck")       # ✅ Type checking
Bash("pnpm lint")            # ✅ Linting
Bash("pnpm test")            # ✅ Testing

# Script Execution
Bash("pnpm exec tsx script.ts")  # ✅ TypeScript execution
Bash("pnpm exec playwright test") # ✅ Playwright tests

# Version Control
Bash("git status")           # ✅ Repository status
Bash("git add .")            # ✅ Stage changes
Bash("git commit -m 'msg'")  # ✅ Commit changes
Bash("git diff --staged")    # ✅ View changes
```

**Forbidden Patterns**:
```bash
# Wrong Package Manager
Bash("npm install")          # ❌ Use pnpm instead

# Direct Node Execution
Bash("node script.js")       # ❌ Use pnpm exec tsx instead

# Chained Commands
Bash("pnpm build && pnpm test")  # ❌ No chained commands

# Pipes
Bash("git log | grep 'feat'")    # ❌ No pipes

# Redirects
Bash("pnpm typecheck > output.txt")  # ❌ No redirects

# File System Operations
Bash("ls -la")               # ❌ Use Glob/Read tools instead
Bash("cat file.txt")         # ❌ Use Read tool instead
Bash("rm file.txt")          # ❌ Use Edit/Write tools instead
```

**Complex Operations**: For multi-step operations, create a `.ts` script with Write tool, then execute with `Bash("pnpm exec tsx script.ts")`

---

## Enforcement Mechanism

### Pretooluse Hook

**Location**: `.claude/hooks/pretooluse_bash_validation.sh`

**Function**: Intercepts all Bash tool calls before execution and validates against agent permissions

**Validation Logic**:
1. Identify calling agent (orchestrator vs subagent)
2. If orchestrator: Allow all commands (exit 0)
3. If subagent: Check if command starts with `pnpm` or `git`
4. If allowed: Allow execution (exit 0)
5. If forbidden: Block execution (exit 1) with helpful error message

**Error Messages**:
```bash
# Example blocked command
❌ BLOCKED: Bash("npm install")

Error: Subagent attempted forbidden Bash command
- Agent: code-writing-agent
- Command: npm install
- Reason: Only 'pnpm' and 'git' commands allowed for subagents
- Allowed: Bash("pnpm install") or use orchestrator for npm commands
```

---

## Migration from Custom Tools

**Previous System**: Custom MCP tools (PnpmTool, GitTool) provided restricted execution
**New System**: Bash with hook-based validation

**Migration Benefits**:
- ✅ Simpler syntax: `Bash("pnpm test")` vs `PnpmTool.executeScript({ script: "test" })`
- ✅ Less tooling overhead: No MCP server management
- ✅ More flexible: Orchestrator has full system access
- ✅ Clearer permissions: Simple allow/deny rules
- ✅ Better error messages: Hook provides immediate, contextual feedback

**Migration Complete**: All agent prompts and documentation updated to use Bash patterns

---

## Security Architecture

### Defense in Depth

**Layer 1 - Hook Validation**: Pretooluse hook blocks unauthorized commands before execution
**Layer 2 - Agent Design**: Agent prompts explicitly document restrictions
**Layer 3 - Code Review**: code-reviewer validates Bash usage in implementations

### Command Injection Prevention

**Restriction Strategy**: Limiting subagents to `pnpm` and `git` reduces attack surface significantly

**Safe Commands**:
- `pnpm`: Package manager - controlled via package.json scripts
- `git`: Version control - restricted to safe operations (no push/force)

**Dangerous Commands Blocked**:
- Shell utilities (rm, mv, cp) - use Read/Write/Edit tools instead
- Network tools (curl, wget) - use WebFetch tool instead
- Process management (kill, killall) - orchestrator only

---

## Agent-Specific Guidance

All 6 subagents have identical Bash restrictions documented in their prompts:
- planning-agent
- critique-and-validation-agent
- code-writing-agent
- code-reviewer
- debugging-agent
- testing-agent

See individual agent files in `.claude/agents/` for complete tool access documentation.

---

## Troubleshooting

### "Forbidden Bash command" errors

**Problem**: Subagent attempted to use a command other than pnpm/git

**Solution**:
1. Check if operation truly needs the forbidden command
2. If yes: Use Write tool to create a script, execute with `pnpm exec tsx`
3. If no: Restructure to use pnpm/git or alternative tools (Read, Glob, etc.)

### Complex multi-step operations

**Problem**: Need to run multiple commands in sequence

**Solution**: Create a TypeScript script
```typescript
// Write tool creates: scripts/multi-step-operation.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function multiStepOperation() {
  await execAsync('command1');
  await execAsync('command2');
  await execAsync('command3');
}

multiStepOperation();
```

Then execute: `Bash("pnpm exec tsx scripts/multi-step-operation.ts")`

### Hook not enforcing restrictions

**Problem**: Forbidden commands executing without being blocked

**Solution**:
1. Verify hook is registered in `.claude/config.json`
2. Check hook script has execute permissions: `chmod +x .claude/hooks/pretooluse_bash_validation.sh`
3. Test hook manually: `.claude/hooks/pretooluse_bash_validation.sh testing-agent 'Bash("npm install")'`

---

## Historical Context: Custom MCP Tools (DEPRECATED)

**Note**: The content below describes the DEPRECATED PnpmTool/GitTool MCP implementation. This system was replaced with Bash access control in January 2025.

**Why Deprecated**: MCP tools added complexity (server management, TypeScript APIs) while Bash with hook validation provides equivalent security with simpler syntax.

**Historical Value**: This documentation remains as reference for understanding the evolution of the tool access system.

---

# Claude Code Custom Tools (DEPRECATED - January 2025)

This directory previously contained custom MCP tools (PnpmTool, GitTool) that provided secure, constrained alternatives to the Bash tool for multi-agent workflows. These tools have been deprecated in favor of Bash with hook-based validation.

## Overview (Historical)

**Purpose**: Replace broad Bash access with purpose-built tools that enforce security constraints and provide clear operational boundaries.

**Security Model**: Allowlist-based execution, command validation, argument sanitization, no shell access.

---

## Available Tools

### PnpmTool

**Purpose**: Safe pnpm operations for package management and script execution

**Allowed Operations**:

- `executeCommand()` - Run pnpm exec commands (tsx, playwright, node)
- `executeScript()` - Run package.json scripts (typecheck, lint, test, etc.)

**Security Constraints**:

- ✅ Allowlist-based: Only approved commands and scripts
- ✅ No shell access: Direct spawn, no shell metacharacter processing
- ✅ Argument sanitization: Prevents command injection
- ✅ Timeout enforcement: Prevents runaway processes
- ❌ Denies arbitrary commands
- ❌ Denies package installation/removal (pnpm add/remove)

**Usage Example**:

```typescript
// Execute TypeScript script
const result = await PnpmTool.executeCommand({
  command: "tsx",
  args: ["testing_agent/scripts/test-feature.ts"],
});

// Run package.json script
const result = await PnpmTool.executeScript({
  script: "typecheck",
});

// Check capabilities
const allowedCommands = PnpmTool.getAllowedCommands();
// ['node', 'playwright', 'tsx']

const allowedScripts = PnpmTool.getAllowedScripts();
// ['build', 'dev', 'lint', 'test', 'test:infra:lint', 'test:infra:typecheck', 'typecheck']
```

**Typical Users**: testing-agent, code-writing-agent (for quality checks)

---

### GitTool

**Purpose**: Safe git operations with commit support, no branch switching or pushing

**Allowed Operations**:

- **Read**: status, log, diff, show, blame, reflog, etc.
- **Write**: add, commit, reset (soft), restore, rm, mv, stash

**Denied Operations**:

- ❌ Branch operations: checkout, switch, merge, rebase
- ❌ Remote operations: push, pull, fetch, clone
- ❌ Repository operations: init, submodule
- ❌ Dangerous flags: --force, --hard, --delete

**Security Constraints**:

- ✅ Category-based allowlist: Clear read/write/denied boundaries
- ✅ Flag validation: Denies destructive flags like --force, --hard
- ✅ Commit message enforcement: Requires -m flag
- ✅ No shell access: Direct spawn, no shell metacharacter processing
- ✅ Argument sanitization: Prevents command injection

**Usage Example**:

```typescript
// Check status
const result = await GitTool.execute({
  command: "status",
});

// Stage files
const result = await GitTool.execute({
  command: "add",
  args: ["app/components/Button.tsx"],
});

// Commit changes
const result = await GitTool.execute({
  command: "commit",
  args: ["-m", "Add Button component\n\n🤖 Generated with Claude Code"],
});

// View diff
const result = await GitTool.execute({
  command: "diff",
  args: ["--staged"],
});

// Check capabilities
const capabilities = GitTool.getAllowedCommands();
// {
//   read: ['status', 'log', 'diff', ...],
//   write: ['add', 'commit', 'reset', ...],
//   denied: {
//     branch: ['checkout', 'merge', ...],
//     remote: ['push', 'pull', ...]
//   }
// }

// Check if command allowed
GitTool.isCommandAllowed("status"); // true
GitTool.isCommandAllowed("push"); // false
```

**Typical Users**: Orchestrator (for commits), code-writing-agent (for git status/diff)

---

## Tool Result Format

All tools return a consistent result format:

```typescript
interface ToolResult {
  success: boolean; // true if exitCode === 0
  stdout: string; // Standard output
  stderr: string; // Standard error
  exitCode: number; // Process exit code
  command: string; // Full command that was executed
  duration: number; // Execution time in milliseconds
}
```

**Example**:

```typescript
{
  success: true,
  stdout: "TypeScript 5.3.3\n",
  stderr: "",
  exitCode: 0,
  command: "pnpm exec tsx --version",
  duration: 245
}
```

---

## Security Architecture

### Defense in Depth

Tools implement multiple security layers:

1. **Allowlist Validation**: Command/script must be in approved list
2. **Argument Sanitization**: Shell metacharacters detected and rejected
3. **Flag Validation**: Dangerous flags (--force, --hard, etc.) denied
4. **No Shell Execution**: Direct spawn, not shell, prevents injection
5. **Timeout Enforcement**: Runaway processes killed after timeout

### Command Injection Prevention

```typescript
// ❌ BLOCKED: Shell metacharacters
PnpmTool.executeCommand({
  command: "tsx",
  args: ["script.ts", ";", "rm", "-rf", "/"],
});
// Throws: "Argument contains suspicious pattern"

// ❌ BLOCKED: Directory traversal
PnpmTool.executeCommand({
  command: "tsx",
  args: ["../../etc/passwd"],
});
// Throws: "Argument contains suspicious pattern"

// ✅ ALLOWED: Safe arguments
PnpmTool.executeCommand({
  command: "tsx",
  args: ["testing_agent/scripts/test.ts"],
});
```

### Destructive Operation Prevention

```typescript
// ❌ BLOCKED: Dangerous git operations
GitTool.execute({
  command: "reset",
  args: ["--hard", "HEAD~1"],
});
// Throws: "git reset --hard is not allowed"

GitTool.execute({
  command: "push",
  args: ["--force", "origin", "main"],
});
// Throws: "Remote operation 'push' not allowed"

// ✅ ALLOWED: Safe operations
GitTool.execute({
  command: "reset",
  args: ["HEAD"], // Soft reset, just unstages
});

GitTool.execute({
  command: "commit",
  args: ["-m", "Fix bug"],
});
```

---

## Testing

Run unit tests to validate security constraints:

```bash
# Test both tools
pnpm test .claude/tools/__tests__/PnpmTool.test.ts
pnpm test .claude/tools/__tests__/GitTool.test.ts

# Test specific security scenarios
pnpm test .claude/tools/__tests__/ --testNamePattern="security validation"
```

**Test Coverage**:

- ✅ Allowlist enforcement
- ✅ Command injection prevention
- ✅ Dangerous flag detection
- ✅ Timeout handling
- ✅ Error handling
- ✅ Argument sanitization

---

## Agent Integration

### Update Agent Tool Access

**Remove Bash, add custom tools in agent YAML frontmatter**:

```yaml
# .claude/agents/testing-agent.md
---
tools: PnpmTool, Read, Write, Edit, Glob, Grep # NO Bash
---
```

### Update Agent Prompts

**Replace Bash references with tool usage**:

```markdown
# Before

Use the Bash tool to execute tests:

- `Bash("pnpm exec tsx testing_agent/scripts/test.ts")`

# After

Use the PnpmTool to execute tests:

- `PnpmTool.executeCommand({ command: "tsx", args: ["testing_agent/scripts/test.ts"] })`
```

---

## Extending Allowlists

To add new allowed commands/scripts, update the allowlist in the tool implementation:

### PnpmTool

Edit `.claude/tools/PnpmTool.ts`:

```typescript
const ALLOWED_COMMANDS = new Set([
  "tsx",
  "playwright",
  "node",
  "your-new-command", // Add here
]);

const ALLOWED_SCRIPTS = new Set([
  "typecheck",
  "lint",
  "test",
  "your-new-script", // Add here
]);
```

### GitTool

Edit `.claude/tools/GitTool.ts`:

```typescript
const GIT_OPERATIONS = {
  READ: new Set([
    "status",
    "log",
    "your-new-read-operation", // Add here
  ]),
  WRITE: new Set([
    "add",
    "commit",
    "your-new-write-operation", // Add here
  ]),
};
```

**After updating**: Run tests to ensure security constraints still hold.

---

## Troubleshooting

### "Command not allowed" errors

**Problem**: Agent trying to use a command not in allowlist

**Solution**:

1. Verify command is necessary for agent's role
2. If necessary, add to allowlist in tool implementation
3. If not necessary, update agent prompt to use allowed alternative

### "Suspicious pattern" errors

**Problem**: Arguments contain shell metacharacters or dangerous patterns

**Solution**:

1. Check if arguments are actually safe (e.g., commit messages may contain special chars)
2. If safe, update sanitization logic to allow specific use case
3. If not safe, agent should restructure command to avoid dangerous patterns

### Timeout errors

**Problem**: Command exceeds default timeout (2 minutes for Pnpm, 1 minute for Git)

**Solution**:

1. Increase timeout parameter if operation legitimately needs more time
2. Investigate if command is hanging (infinite loop, waiting for input)
3. Consider breaking operation into smaller steps

---

## Migration Guide

### From Bash to PnpmTool

```typescript
// Before: Bash
Bash("pnpm exec tsx script.ts");
Bash("pnpm typecheck");

// After: PnpmTool
PnpmTool.executeCommand({ command: "tsx", args: ["script.ts"] });
PnpmTool.executeScript({ script: "typecheck" });
```

### From Bash to GitTool

```typescript
// Before: Bash
Bash("git status");
Bash("git add .");
Bash("git commit -m 'message'");
Bash("git diff --staged");

// After: GitTool
GitTool.execute({ command: "status" });
GitTool.execute({ command: "add", args: ["."] });
GitTool.execute({ command: "commit", args: ["-m", "message"] });
GitTool.execute({ command: "diff", args: ["--staged"] });
```

---

## Architecture Decision Records

### Why Not Use Bash with Allowlist?

**Considered**: Restrict Bash to allowlist (e.g., `Bash(git status *)`)

**Rejected because**:

- ❌ Allowlist complexity: Need patterns for every command variation
- ❌ Shell metacharacter risk: Harder to prevent injection in shell context
- ❌ Less explicit: Harder for agents to discover capabilities
- ❌ Maintenance burden: Permission patterns complex and error-prone

**Dedicated tools win because**:

- ✅ Explicit API: Clear method signatures, discoverable
- ✅ Type safety: TypeScript interfaces for parameters
- ✅ No shell: Direct spawn eliminates injection vectors
- ✅ Simple security: Allowlist is just a Set, easy to audit
- ✅ Better errors: Clear messages when operation denied

### Why Not Scripts Instead of Tools?

**Considered**: Agent writes script file, tool executes script file

**Rejected because**:

- ❌ Two-step friction: Write → Execute slows workflow
- ❌ Script proliferation: Hundreds of .sh/.ts files
- ❌ Cleanup complexity: Delete scripts? Keep them? Version control?
- ❌ Still needs execution: Doesn't eliminate Bash, just indirects it

**Direct tool calls win because**:

- ✅ Single step: Call tool directly
- ✅ No file clutter: No intermediate script files
- ✅ Familiar pattern: testing-agent already writes Playwright scripts via Write
- ✅ Simpler debugging: Fewer indirection layers

---

## Future Enhancements

Potential additions based on usage patterns:

- **ServerTool**: Manage dev server lifecycle (if needed beyond TypeScript modules)
- **ProcessTool**: Manage background processes (if killport pattern emerges)
- **NpmTool**: Separate from pnpm if npm-specific operations needed
- **FileSystemTool**: If complex file operations beyond Read/Write/Edit/Glob needed

**Principle**: Add tools based on observed need, not speculation. Start minimal, extend when patterns emerge.

---

## Support

**Documentation**:

- Tool implementations: `.claude/tools/PnpmTool.ts`, `.claude/tools/GitTool.ts`
- Unit tests: `.claude/tools/__tests__/`
- Usage examples: See AGENTS.md Section II (agent definitions)

**Issues**:

- Security concerns: Review tool implementation, add tests for new scenarios
- Missing capabilities: Consider if truly needed, then extend allowlist
- Performance issues: Adjust timeout parameters, investigate command efficiency

**Contact**: See project CLAUDE.md for escalation procedures
