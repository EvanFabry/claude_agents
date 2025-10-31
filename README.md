# Claude Code Multi-Agent System

> A production-ready orchestrator-workers pattern implementation for Claude Code with intelligent complexity assessment, adaptive workflows, and evidence-based validation.

## Origin Story

This repository was created to extract and generalize a production multi-agent system from a specific project implementation. The goal was to create a reusable, public-facing framework that others could adapt to their own Claude Code projects.

### Creation Process

The initial version was generated using the following process (executed by the `agent-system-optimizer` agent):

**Original Directive:**
```
Act as the agent-system-optimizer agent and for each agent within the repository:

1. Read each section of the documentation. Remove anything unique to the original
   project infrastructure.

2. Assess the degree of section overlap across prompts. Re-organize so that:
   a. Each section has low overlap in content coverage
   b. Section order/numbering reflects importance (most to least critical)
   c. All project-specific logic is stubbed out with user guidance
   d. Resulting agent prompts are ~500 lines (ideally less)

3. Perform a second pass as agent-system-optimizer to validate conditions are met

4. Final validation pass as critique-and-validation-agent

SUCCESS CRITERIA: Both agent-system-optimizer and critique-and-validation-agent
can confidently assess the work is complete and production-ready.
```

This multi-pass process with dual agent validation ensured:
- Clean separation of concerns across agents
- Removal of project-specific implementation details
- Maintainable prompt sizes
- Clear guidance for customization
- Production-ready generalization

## Overview

This repository provides a complete multi-agent system for Claude Code that implements Anthropic's recommended orchestrator-workers pattern. It features a primary orchestrator that intelligently coordinates specialized sub-agents to handle tasks ranging from simple queries to complex multi-step workflows.

**Key Features:**

- **Intelligent Mode Selection**: Automatically routes between direct handling and multi-agent coordination based on task complexity
- **Adaptive Workflows**: Specification depth and workflow rigor scale proportionally with task complexity (0-2: implicit, 3-5: lightweight, 6+: comprehensive)
- **Evidence-Based Validation**: Mandatory evidence collection and dual quality gates prevent premature completion claims
- **Specialized Agents**: Purpose-built agents for planning, implementation, code review, debugging, testing, and validation
- **Anti-Loop Safeguards**: Built-in protections against repeated failures and authentication loops
- **Tool Access Control**: Hook-based enforcement of agent-specific tool permissions

## Architecture

### Orchestrator-Workers Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                   Primary Orchestrator                       │
│  - Complexity assessment (0-2 / 3-5 / 6+ scoring)           │
│  - Mode selection (Direct vs Multi-Agent)                    │
│  - Context passing between agents                            │
│  - TODO state management                                     │
│  - Evidence validation                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
┌─────────────┐         ┌─────────────┐
│   Direct    │         │ Multi-Agent │
│   Mode      │         │   Workflow  │
└─────────────┘         └──────┬──────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
              ┌──────────┬─────────┬──────────┐
              │ Planning │  Code   │ Testing  │
              │  Agent   │ Writing │  Agent   │
              │          │  Agent  │          │
              └────┬─────┴────┬────┴─────┬────┘
                   │          │          │
                   └────┬─────┴─────┬────┘
                        ▼           ▼
                  ┌──────────┬──────────┐
                  │  Code    │ Critique │
                  │ Reviewer │   & Val  │
                  └──────────┴──────────┘
```

### The 5-Step Adaptive Workflow

All tasks follow this unified pattern, with depth adapting to complexity:

1. **Understand & Spec**: Assess complexity, create specification (implicit/lightweight/comprehensive)
2. **Verify (if needed)**: Verify current behavior for bugs, skip for features, measure for investigations
3. **Plan & Approve** (Quality Gate 1): Planning-agent → critique-and-validation-agent approval
4. **Implement & Review**: Code-writing-agent → code-reviewer inline validation
5. **Validate & Complete** (Quality Gate 2): Testing-agent → critique-and-validation-agent final approval

**Complexity-Driven Adaptation:**

| Score | Spec Type | Time Investment | Example |
|-------|-----------|----------------|---------|
| 0-2 | Implicit (no file) | 0 min | Fix typo, update config |
| 3-5 | Lightweight (1-2 pages) | 5-10 min | Add component, optimize algorithm |
| 6+ | Comprehensive (full template) | 15-30 min | Architectural change, system integration |

## Specialized Agents

### Primary Orchestrator
**Prompt**: `CLAUDE.md`
**Role**: Intelligent task routing, complexity assessment, agent coordination, TODO management

**Key Capabilities:**
- Complexity scoring (7 factors: scope, integration, risk, time, testing, performance, planning)
- Direct mode handling for simple tasks
- Multi-agent workflow coordination
- Context injection and progress tracking
- Evidence-based completion validation

### Sub-Agents

#### Planning Agent
**Location**: `.claude/agents/planning-agent.md`
**Exclusive Capabilities**: Strategic planning, architectural design, task breakdown
**Workflow Role**: Step 3 (plan creation before Gate 1)

#### Critique & Validation Agent
**Location**: `.claude/agents/critique-and-validation-agent.md`
**Exclusive Capabilities**: Plan validation, completion determination, quality gate authority
**Workflow Role**: Gates 1 & 2 (dual quality gate oversight)

#### Code Writing Agent
**Location**: `.claude/agents/code-writing-agent.md`
**Exclusive Capabilities**: Production code implementation, pattern adherence
**Workflow Role**: Step 4 (implementation phase)

#### Code Reviewer
**Location**: `.claude/agents/code-reviewer.md`
**Exclusive Capabilities**: Line-by-line code review, technical debt identification
**Workflow Role**: Step 4 (inline review during implementation)

#### Debugging Agent
**Location**: `.claude/agents/debugging-agent.md`
**Exclusive Capabilities**: Systematic debugging, log pattern analysis
**Workflow Role**: Step 2 (verification for bugs/investigations)

#### Testing Agent
**Location**: `.claude/agents/testing-agent.md`
**Exclusive Capabilities**: Browser automation, Playwright testing, evidence collection
**Workflow Role**: Steps 2 & 5 (verification + testing/evidence)

**Special Note**: Testing agent has exclusive authority over ALL browser automation, server management, and screenshot capture. Never perform these tasks directly.

## System Components

### Complete Agent Inventory

**Primary Orchestrator** (`CLAUDE.md`)
- Intelligent task routing and complexity assessment
- Mode selection (Direct vs Multi-Agent)
- Context passing between agents
- Canonical TODO state management
- Evidence-based completion validation
- Full Bash access for system coordination

**Specialized Sub-Agents** (`.claude/agents/`)

1. **planning-agent.md** (699 lines)
   - Strategic planning and architectural design
   - Lightweight and comprehensive planning modes
   - Task breakdown and phased implementation
   - Risk assessment and testing strategy
   - Tools: Bash (restricted), Read, Glob, Grep, WebFetch
   - Bash Access: pnpm and git only

2. **critique-and-validation-agent.md** (323 lines)
   - Dual quality gate authority (Gates 1 & 2)
   - Plan validation and approval
   - Completion determination with evidence review
   - Generalization compliance enforcement
   - Complexity-appropriate critique depth
   - Tools: Bash (restricted), Read, Glob, Grep, WebFetch
   - Bash Access: pnpm and git only

3. **code-writing-agent.md** (699 lines)
   - Production code implementation
   - Architectural pattern adherence
   - Error handling and performance optimization
   - Integration correctness
   - Tools: Bash (restricted), Read, Write, Edit, MultiEdit, Glob, Grep, WebFetch
   - Bash Access: pnpm and git only

4. **code-reviewer.md** (446 lines)
   - Line-by-line code quality review
   - Generalization compliance validation
   - Technical debt identification
   - Performance pattern assessment
   - Type checking and linting integration
   - Tools: Bash (restricted), Read, Glob, Grep, WebFetch
   - Bash Access: pnpm and git only

5. **debugging-agent.md** (374 lines)
   - Systematic investigation and diagnosis
   - Log pattern analysis
   - Timing dependency debugging
   - Strategic instrumentation (console.log)
   - Root cause identification
   - Tools: Bash (restricted), Read, Write, Edit, MultiEdit, Glob, Grep, WebFetch
   - Bash Access: pnpm and git only

6. **testing-agent.md** (518 lines)
   - Exclusive browser automation authority
   - Playwright test creation and execution
   - Server lifecycle management
   - Evidence collection (screenshots, logs, metrics)
   - Visual and technical validation
   - Tools: Bash (restricted), Read, Write, Edit, MultiEdit, Glob, Grep, WebFetch
   - Bash Access: pnpm and git only

### Hooks & Enforcement (`.claude/hooks/`)

**Quality Gate Hooks:**
- `evidence-validation.sh` - Validates evidence collection for task completion
- `workflow-validation.sh` - Enforces 5-step workflow compliance
- `subagentstop_validation_quality_status.sh` - Quality gate validation on agent completion
- `subagentstop_code_reviewer_guidance.sh` - Code review guidance and standards
- `subagentstop_code_writing_validation.sh` - Code writing agent output validation
- `subagentstop_application_validation.sh` - Application-specific validation rules

**Tool Access Control:**
- `pretooluse_bash_validation.py` - Enforces Bash restrictions (pnpm/git only for subagents)
- `pretooluse_application_agent_file_validation.sh` - File access validation
- `pretooluse_application_agent_scope_validation.sh` - Agent scope enforcement

**Analytics & Observability:**
- `pre_tool_use_analytics.py` - Task start tracking
- `post_tool_use_analytics.py` - Task completion and duration tracking
- `analytics_reporter.py` - Statistics generation and reporting
- `test_analytics.py` - Analytics system test suite
- `analytics/` directory - JSONL data storage and reports

**Session Management:**
- `sessionstart.sh` - Session initialization and environment setup
- `send_notification.sh` - Pushover notification integration

**Development Tools:**
- `debug_posttooluse.sh` - PostToolUse hook debugging
- `debug_write_hook.sh` - Write hook debugging
- `debug_write_hook.log` - Write hook debug output

### Tool Access Control (`.claude/tools/`)

**Documentation** (`README.md`)
- Complete Bash access control architecture
- Orchestrator: Full Bash access (unrestricted)
- Subagents: Restricted Bash access (pnpm and git only)
- Hook-based enforcement via `pretooluse_bash_validation.py`
- Security patterns and migration guide
- Historical context: Deprecated MCP tools (PnpmTool, GitTool)

**Enforcement Mechanism:**
- Hook intercepts all Bash tool calls
- Validates agent identity (orchestrator vs subagent)
- Blocks unauthorized commands with helpful error messages
- Allows complex operations via script creation pattern

### Guided Setup (`.claude/prompts/`)

**setup-instructions.md**
- Automated 4-phase configuration process
- Discovery & Analysis phase
- Information Gathering phase
- Configuration Execution phase
- Validation & Confirmation phase
- Integration with agent-system-optimizer

**complete-stub-sections.md**
- Referenced by all [STUB] sections in agent prompts
- Instructions for consulting agent-system-optimizer
- Example queries for different stub types
- Why stubs exist and how to complete them
- Universal patterns provided for common scenarios

### Supporting Documentation

**Core System Documentation:**
- `AGENTS.md` - Complete agent ecosystem, workflow coordination, browser configuration, and TODO management architecture

**Project-Specific Documentation Templates:**
- `DEBUGGING.md` - Log patterns and troubleshooting procedures (to be configured)
- `LIFECYCLE.md` - Application timing and component lifecycles (to be configured)
- `ARCHITECTURE.md` - System design and request flows (to be configured)
- `RECENT_GOTCHAS.md` - Current issues and workarounds (to be configured)

### Analytics & Observability

**Analytics System** (`.claude/hooks/analytics/`)
- Task duration tracking by agent type
- Success/failure rate monitoring
- Token usage and efficiency metrics
- Performance trends (5hrs, 7 days, all-time)
- JSONL storage format for efficient querying

**Reporter Commands:**
```bash
# Generate analytics report
uv run .claude/hooks/analytics_reporter.py

# Export to JSON
uv run .claude/hooks/analytics_reporter.py --export

# Detailed output
uv run .claude/hooks/analytics_reporter.py --verbose

# Test the system
uv run .claude/hooks/test_analytics.py
```

**Tracked Metrics:**
- Overall success rates and task counts
- Duration metrics (avg, median, min, max)
- Token consumption patterns
- Performance breakdown by agent type
- Most frequent task descriptions

## Getting Started

### Quick Start

**First Time Setup** (Automated):
```
Run the setup instructions prompt:
@.claude/prompts/setup-instructions.md

This will guide you through automated configuration with agent-system-optimizer.
```

### Manual Installation

1. **Copy the repository structure** into your Claude Code project:
   ```bash
   # Copy everything
   cp -r .claude /path/to/your/project/
   cp CLAUDE.md AGENTS.md /path/to/your/project/
   ```

2. **Configure for your project**:

   **Option A (Recommended)**: Use the automated setup
   ```
   Run: @.claude/prompts/setup-instructions.md
   ```

   **Option B**: Manual configuration
   - Edit CLAUDE.md: Replace `[YOUR_DEV_COMMAND]`, `[YOUR_DEV_PORT]`, etc.
   - Complete [STUB] sections in agent prompts as you encounter them
   - See `.claude/prompts/complete-stub-sections.md` for guidance

### User-Specific Configuration

#### Pushover Notifications (Optional)

Get notified when long-running agent tasks complete.

**Prerequisites:**
- Pushover account ($4.99 one-time after 7-day trial)
- Mobile app (iOS/Android)

**Setup Steps:**

1. **Create Account**: Visit https://pushover.net and sign up

2. **Get User Key**:
   - Login to dashboard at https://pushover.net
   - Find your User Key (30-character string)

3. **Register Application**:
   - Go to https://pushover.net/apps/build
   - Create new application
   - Get API Token (30-character string)

4. **Configure Environment Variables**:
   ```bash
   export PUSHOVER_TOKEN="your_api_token_here"
   export PUSHOVER_USER="your_user_key_here"
   ```

5. **Verify Setup**:
   ```bash
   ./.claude/hooks/send_notification.sh "Test message" "Test Title"
   ```

**Documentation**: https://pushover.net/api

**Free Tier**: 10,000 messages per month

#### Browser Profile Configuration

The testing-agent uses your logged-in browser profile for authenticated testing.

**Default Configuration:**
- **macOS**: `~/Library/Application Support/Google/Chrome/Default`
- **Linux**: `~/.config/google-chrome/Default`

**To Use Custom Profile:**
1. Find your profile path: `chrome://version` → Profile Path
2. Update in CLAUDE.md `<browser_configuration>` section
3. Restart Claude Code

**Why This Matters**: Preserves authentication sessions, prevents login loops during testing.

#### Application-Specific Configuration

**[USER CONFIGURATION REQUIRED]**

This system is designed to be project-agnostic. Configure for your specific stack:

1. **Development Server**:
   - Command: [e.g., `npm run dev`, `pnpm dev`, `yarn dev`]
   - Port: [your dev server port]

2. **Build System**:
   - Build command: [e.g., `npm run build`, `vite build`]
   - Output directory: [e.g., `dist/`, `build/`]

3. **Testing Framework** (if applicable):
   - Test command: [e.g., `npm test`, `pytest`]
   - Test directory: [e.g., `tests/`, `__tests__/`]

**Automated Setup**: Run `@.claude/prompts/setup-instructions.md` to configure automatically.

### Basic Usage

The orchestrator automatically selects the appropriate mode based on your request:

**Direct Mode** (Simple tasks):
```
User: "How does the authentication system work?"
Claude: [Reads relevant files and explains directly]
```

**Multi-Agent Mode** (Complex tasks):
```
User: "Add a new caching layer with Redis integration"
Claude:
  - Complexity Score: 7 points (Complex workflow)
  - Creating comprehensive specification...
  - Step 1: Understanding and spec creation
  - Step 2: Skipping verification (new feature)
  - Step 3: Calling planning-agent...
  - [Coordinates full 5-step workflow with quality gates]
```

### Complexity Assessment

The orchestrator uses a 7-factor scoring system:

```yaml
factors:
  architectural_scope: "single=0 | multi=1 | system_wide=2"
  integration_points: "none=0 | few(1-2)=1 | many(3+)=2"
  risk_level: "low=0 | medium=1 | high=2"
  implementation_time: "minutes=0 | hours=1 | days=2"
  testing_requirements: "simple=0 | moderate=1 | comprehensive=2"
  performance_impact: "none=0 | minimal=1 | significant=2"
  planning_needed: "none=0 | lightweight=1 | comprehensive=2"
```

**Total Score Routing:**
- **0-2**: Direct handling allowed
- **3-5**: Medium workflow (lightweight spec, standard gates)
- **6+**: Complex workflow (comprehensive spec, maximum rigor)

## Evidence-Based Validation

### Completion Blocking Rules

The system enforces strict completion requirements:

```yaml
completion_requirements:
  for_ui_css_browser_tasks:
    - testing_agent_called: true
    - evidence_artifacts_collected: true
    - critique_agent_final_approval: true
    - no_outstanding_issues: true

forbidden_patterns:
  - self_declaring_success: "Never allowed for complexity 3+"
  - bypassing_agent_workflow: "Never allowed"
  - claiming_success_without_evidence: "Never allowed"
```

### Quality Gates

**Gate 1** (Plan Approval):
- Planning-agent creates implementation plan
- Critique-and-validation-agent reviews and approves
- Blocks implementation until plan is validated

**Gate 2** (Completion Validation):
- Testing-agent collects evidence (screenshots, logs, results)
- Critique-and-validation-agent validates completion
- Final authority on task completion

## Anti-Loop Safeguards

The system includes built-in protections against repeated failures:

### Browser Configuration
- Default: Uses logged-in Chrome profile (preserves authentication)
- Testing-agent automatically uses authenticated sessions
- Incognito mode ONLY for explicit auth testing scenarios

### Progressive Context Accumulation
- Tracks all sub-agent calls and their configurations
- Documents authentication failures and causes
- Prevents identical calls without corrective context
- Escalates to user after 2+ identical failures

See `CLAUDE.md` Section II for complete browser configuration details.

## Tool Access Control

Agents have role-appropriate tool permissions enforced via hooks:

| Agent | Bash Access | File Operations | Browser Automation |
|-------|-------------|----------------|-------------------|
| Orchestrator | Full (all commands) | Full | Via testing-agent |
| Planning | pnpm, git only | Read, Grep, Glob | No |
| Code Writing | pnpm, git only | Full (Write, Edit, MultiEdit) | No |
| Code Reviewer | pnpm, git only | Read, Grep, Glob | No |
| Debugging | pnpm, git only | Read, Write, Edit, MultiEdit | No |
| Testing | pnpm, git only | Read, Write, Edit, MultiEdit | Exclusive |

Hook enforcement: `.claude/hooks/pretooluse_bash_validation.sh`

## TODO Management Architecture

**Critical**: The orchestrator maintains the canonical TODO state. Sub-agents operate in isolated contexts and cannot modify the orchestrator's TODO list.

### Orchestrator Responsibilities

1. **Maintain TODO list** via TodoWrite throughout conversation
2. **Inject TODO context** into EVERY sub-agent call:
   ```
   CURRENT TODO STATE:
   1. [Task] - [status: pending/in_progress/completed]
   2. [Task] - [status]

   YOUR FOCUS: [Specific TODO this agent addresses]
   ```
3. **Process progress updates** from sub-agent responses
4. **Update TODO state** based on reported completion

See `AGENTS.md` Section VI for complete architecture.

## Documentation

- **CLAUDE.md**: Primary orchestrator prompt and system overview
- **AGENTS.md**: Complete agent ecosystem, workflow coordination, browser configuration, and TODO management architecture
- **.claude/agents/**: Individual agent prompts
- **.claude/hooks/**: Tool access validation hooks
- **.claude/tools/**: Tool access control documentation

## Customization Guide

### Adapting to Your Project

1. **Review Stub Sections**: Agent prompts contain `[STUB]` markers for project-specific logic
2. **Complete Stubs**: When Claude encounters a stub, follow the guided conversation with `agent-system-optimizer`
3. **Add Application Knowledge**: Update `<application_knowledge>` sections with your:
   - Critical timing requirements
   - Known issues and workarounds
   - Documentation references
   - System-specific constraints

4. **Configure Hooks**: Adjust tool access rules in `.claude/hooks/` for your security requirements

5. **Customize Agents**: Modify agent prompts in `.claude/agents/` to add domain-specific capabilities

### Example Customization

```markdown
<!-- In CLAUDE.md <application_knowledge> section -->

### Critical Timing Requirements
- [YOUR_SYSTEM]: [Specific timing constraints]
- [YOUR_COMPONENT]: [Lifecycle dependencies]

### Known Issues and Workarounds
- [YOUR_ISSUE_1]: [Workaround description]
- [YOUR_ISSUE_2]: [Workaround description]

### Documentation Integration
- [YOUR_DOC_1.md]: [Purpose]
- [YOUR_DOC_2.md]: [Purpose]
```

## Best Practices

### For Orchestrator Use

1. **Trust the Complexity Assessment**: Don't override the scoring system without good reason
2. **Respect Agent Boundaries**: Each agent has exclusive capabilities - use them appropriately
3. **Maintain Context Chains**: Always pass complete context when calling sub-agents
4. **Validate Completion**: Never skip critique-and-validation-agent for complex tasks
5. **Collect Evidence**: Testing-agent evidence is mandatory for UI/browser/CSS tasks

### For Agent Customization

1. **Keep Prompts Focused**: Each agent should have clear, non-overlapping responsibilities
2. **Document Exclusivity**: Be explicit about what ONLY this agent can do
3. **Maintain Size Limits**: Aim for <500 lines per agent prompt
4. **Use Stubs Appropriately**: Mark project-specific sections clearly
5. **Test Agent Boundaries**: Ensure tool access restrictions work correctly

### For Workflow Design

1. **Start Simple**: Use Direct Mode for simple tasks, escalate when needed
2. **Scale Appropriately**: Let complexity score drive workflow depth
3. **Enforce Quality Gates**: Both gates are critical for complex tasks
4. **Track Progress**: Maintain TODO state throughout multi-step workflows
5. **Communicate Transparently**: Show orchestration decisions to users

## Contributing

Contributions are welcome! This is a living framework that can benefit from:

- Additional specialized agents for specific domains
- Improved complexity assessment heuristics
- Enhanced anti-loop safeguards
- Better evidence collection patterns
- Workflow optimization strategies

Please submit issues or pull requests with clear descriptions of improvements.

## License

[Your chosen license]

## Acknowledgments

Built on Anthropic's orchestrator-workers pattern recommendations for Claude Code. Inspired by production needs in complex web application development across various frontend and backend technologies.

---

**Ready to get started?** Copy the repository structure into your project and let Claude guide you through completing the stub sections for your specific use case.
