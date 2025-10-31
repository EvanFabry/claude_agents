# Multi-Agent System Reference

**Document Organization**: Content ordered by criticality (I → II → III → IV → V)

---

## I. AGENT ECOSYSTEM

### Core Agent Definitions

<agents>

| Agent | Workflow Position | Role | Tools | Exclusive Domain | Handoff To |
|-------|------------------|------|-------|-----------------|------------|
| **planning-agent** 📋 | Step 3 (before Gate 1) | Strategic planning specialist | Bash, Read, Glob, Grep, WebFetch | Convert requirements to executable plans, analyze constraints, risk assessment | critique-and-validation-agent (Gate 1) |
| **critique-and-validation-agent** 🔍 | Gates 1 & 2 | Dual quality gate authority | Bash, Read, Glob, Grep, WebFetch | Plan validation (Gate 1), completion determination (Gate 2) | code-writing-agent (after Gate 1) OR User (after Gate 2) |
| **code-writing-agent** 💻 | Step 4 | Implementation specialist | Bash, Read, Edit, MultiEdit, Write, Glob, Grep, WebFetch | Implement approved plans, follow architectural patterns, maintain performance standards | code-reviewer (inline review) |
| **code-reviewer** 🔍 | Step 4 (inline) | Code quality specialist | Bash, Read, Glob, Grep, WebFetch | Line-by-line review, pattern validation, code smell detection, technical debt identification | testing-agent (Step 5) |
| **debugging-agent** 🐛 | Step 2 (verification) | Issue investigation | Bash, Read, Glob, Grep, Edit, MultiEdit, Write, WebFetch | Bug reproduction, log pattern analysis, baseline measurement collection | planning-agent (Step 3) |
| **testing-agent** 🌐 | Steps 2 & 5 | Testing and evidence collection | Bash, Read, Edit, MultiEdit, Write, Glob, Grep, WebFetch | **Step 2**: Bug verification, behavior reproduction \| **Step 5**: Test execution, evidence collection, validation support | critique-and-validation-agent (Gate 2) |

**When to Use Each Agent**:
- **planning-agent**: PROACTIVELY for medium/complex tasks requiring implementation plans
- **critique-and-validation-agent**: MUST USE at Gate 1 (plan approval) and Gate 2 (completion validation)
- **code-writing-agent**: PROACTIVELY after Gate 1 approval to implement code
- **code-reviewer**: MUST USE PROACTIVELY after code-writing-agent completes implementation
- **debugging-agent**: PROACTIVELY for bugs (reproduction required) and investigations (baseline data)
- **testing-agent**: MUST USE for behavior verification (Step 2) and testing/evidence (Step 5)

**Browser Automation Standards** (testing-agent):
- **Output Directories**: `testing_agent/outputs/` (results, screenshots, reports), `testing_agent/scripts/` (test scripts)
- **Browser Configuration**: Uses logged-in Chrome profile by default. Incognito ONLY when testing logged-out scenarios. See CLAUDE.md Section II for complete browser configuration details.
- **Error Recovery**: Report authentication failures immediately, document browser configuration used, learn from failures, preserve context, save scripts/results with timestamps

### Bash Access Control

**All agents have Bash access** with different permission levels:

**Orchestrator**:
- **Access Level**: FULL - unrestricted Bash access for all operations
- **Allowed**: Any command (pnpm, git, system commands)
- **Use Cases**: Coordination, system management, quality checks, version control

**Subagents** (all 6 agents):
- **Access Level**: RESTRICTED - pnpm and git only
- **Allowed Commands**: `pnpm`, `git`
- **Forbidden**: Other commands (npm, node, curl, ls, cat, rm), chained commands, pipes, redirects
- **Enforcement**: `.claude/hooks/pretooluse_bash_validation.py` blocks violations automatically

**Common Patterns**:
```bash
# Allowed (all agents)
Bash("pnpm typecheck")
Bash("pnpm exec tsx script.ts")
Bash("git status")
Bash("git commit -m 'message'")

# Forbidden (subagents only)
Bash("npm install")           # ❌ Wrong package manager
Bash("node script.js")        # ❌ Use pnpm exec tsx instead
Bash("pnpm build && pnpm test") # ❌ No chained commands
```

**Tool Access Policy**:
- **Orchestrator**: FULL Bash access - no restrictions
- **All Subagents**: RESTRICTED Bash access - pnpm and git only
- **Documentation**: See `.claude/tools/README.md` for complete Bash access control documentation

</agents>

---

## II. THE 5-STEP ADAPTIVE WORKFLOW

<workflow_overview>

### Single Unified Pattern for All Tasks

**All tasks follow this 5-step workflow, with depth adapting to complexity:**

```yaml
STEP 1: understand_and_spec
  Purpose: "Assess complexity and create specification"
  Adaptation: "Implicit (0-2) → Lightweight (3-5) → Comprehensive (6+)"
  Agent: "Orchestrator (with user input)"
  Output: "Specification OR clear understanding"

STEP 2: verify_if_needed
  Purpose: "Verify current behavior when relevant"
  Adaptation: "Skip for features | Required for bugs | Measure for investigations"
  Agents: "debugging-agent OR testing-agent"
  Output: "Evidence of current behavior OR skip confirmation"

STEP 3: plan_and_approve (QUALITY GATE 1)
  Purpose: "Create and validate implementation approach"
  Adaptation: "May skip (0-2) | Focused (3-5) | Comprehensive (6+)"
  Agents: "planning-agent → critique-and-validation-agent"
  Output: "Approved implementation plan"

STEP 4: implement_and_review
  Purpose: "Write code and validate quality inline"
  Adaptation: "Quick (0-2) | Standard (3-5) | Rigorous (6+)"
  Agents: "code-writing-agent → code-reviewer"
  Output: "Implemented, reviewed code"

STEP 5: validate_and_complete (QUALITY GATE 2)
  Purpose: "Test, collect evidence, validate completion"
  Adaptation: "Minimal (0-2) | Standard (3-5) | Comprehensive (6+)"
  Agents: "testing-agent → critique-and-validation-agent"
  Output: "Evidence-validated completion"
```

**Key Principles**:
- **Single Pattern**: One workflow for all tasks - depth adapts, not structure
- **Two Quality Gates**: Strategic placement for maximum efficiency (Gate 1: plan approval, Gate 2: completion validation)
- **Adaptive Specs**: Critical feature - spec depth matches task complexity
- **Conditional Steps**: Step 2 can be skipped, Step 3 can be skipped for simple tasks
- **Evidence Mandatory**: All tasks require evidence for completion validation

</workflow_overview>

<complexity_routing>

### Task Complexity Assessment & Adaptation Matrix

```yaml
complexity_factors:
  architectural_scope: "single=0 | multi=1 | system_wide=2"
  integration_points: "none=0 | few(1-2)=1 | many(3+)=2"
  risk_level: "low=0 | medium=1 | high=2"
  implementation_time: "minutes=0 | hours=1 | days=2"
  testing_requirements: "simple=0 | moderate=1 | comprehensive=2"
  performance_impact: "none=0 | minimal=1 | significant=2"
  planning_needed: "none=0 | lightweight=1 | comprehensive=2"

total_score: "Sum of all points"
workflow_depth_routing:
  0-2: "Simple - Implicit spec, may skip Step 3, minimal evidence"
  3-5: "Medium - Lightweight spec, full workflow, standard evidence"
  6+: "Complex - Comprehensive spec, full workflow, comprehensive evidence"
```

| Complexity | Score | Spec Approach | Gate 1 | Gate 2 Evidence | Example Tasks | Time |
|------------|-------|---------------|--------|----------------|---------------|------|
| **Simple** | 0-2 | Implicit (no file) | May skip | 1-2 screenshots | Fix typo, update config, add log | 5-15min |
| **Medium** | 3-5 | Lightweight (1-2 pg) | Focused | Screenshots + performance data + test results | Add component, optimize algorithm, fix complex bug | 30-90min |
| **Complex** | 6+ | Comprehensive (full template) | Thorough | Visual suite + detailed metrics + extensive logs | Architecture change, multi-system integration, performance overhaul | 2+ hrs |

**Workflow Adaptation by Complexity**:

```yaml
simple_0-2:
  step_1: "Implicit understanding - NO spec file created"
  step_2: "Skip for features, minimal for bugs"
  step_3: "MAY SKIP entirely for trivial changes"
  step_4: "Direct implementation, quick review"
  step_5: "Quick validation with minimal evidence"

medium_3-5:
  step_1: "Lightweight spec - 1-2 pages (5-10 min to create)"
  step_2: "As needed based on task type"
  step_3: "Focused planning with critique approval"
  step_4: "Careful implementation with standard review"
  step_5: "Standard testing with key evidence artifacts"

complex_6+:
  step_1: "Comprehensive spec - full template (15-30 min to create)"
  step_2: "Thorough verification with baseline data collection"
  step_3: "Comprehensive planning with thorough critique"
  step_4: "Iterative implementation with rigorous review"
  step_5: "Comprehensive testing with full evidence suite"
```

</complexity_routing>

<adaptive_specifications>

### Specification Requirements by Complexity

#### Simple Tasks (0-2 points): Implicit Understanding
- **Approach**: No formal specification file
- **Captured In**: Todo list items, inline comments, commit messages
- **Time Investment**: 0 minutes
- **Examples**: Fix typo in error message, update environment variable, add console log

#### Medium Tasks (3-5 points): Lightweight Specification
- **Approach**: Focused 1-2 page specification at `specs/active/`
- **Required Sections**: Overview (2-3 sentences), acceptance criteria (3-5 Gherkin scenarios), constraints, success criteria
- **Skip Sections**: Detailed technical design, comprehensive risk analysis, alternative approaches, rollback strategy
- **Time Investment**: 5-10 minutes
- **Examples**: Add new validation algorithm, optimize query performance, fix complex timing bug

#### Complex Tasks (6+ points): Comprehensive Specification
- **Approach**: Full specification using complete template at `specs/active/`
- **Required Sections**:
  - **P0 Critical**: Detailed overview with context, comprehensive acceptance criteria (10+ scenarios), evidence requirements, timing dependencies, integration points
  - **Medium Plus**: Dependency analysis, risk assessment with mitigation, alternative approaches, performance benchmarks
  - **Complex Only**: Phased implementation strategy, rollback and recovery plan, cross-system coordination, migration strategy
- **Time Investment**: 15-30 minutes
- **Examples**: Redesign data processing architecture, implement new service integration layer, refactor core system

</adaptive_specifications>

---

## III. AGENT COORDINATION

<coordination>

### Standard Handoff Protocol

1. **Context Preparation**: Gather relevant information from previous agents
2. **Clear Instructions**: Provide specific, actionable tasks in prompt
3. **Success Criteria**: Define what completion looks like
4. **Time Bounds**: Set reasonable expectations for response
5. **Escalation Path**: Define how to handle blockers or conflicts

### 5-Step Workflow Handoff Chain

| Handoff | From → To | Context Passed |
|---------|-----------|----------------|
| **Step 1 → Step 2** | Orchestrator → debugging-agent OR testing-agent | Spec + task type (bug/feature/investigation) + TODO state |
| **Step 2 → Step 3** | debugging-agent OR testing-agent → planning-agent | Spec + verified behavior evidence + TODO state |
| **Step 3 → Gate 1** | planning-agent → critique-and-validation-agent | Spec + implementation plan + progress updates |
| **Gate 1 → Step 4** | critique-and-validation-agent → code-writing-agent | Spec + approved plan + TODO state |
| **Step 4 Inline** | code-writing-agent → code-reviewer | Spec + plan + implementation + progress updates |
| **Step 4 → Step 5** | code-reviewer → testing-agent | Spec + plan + approved code + TODO state |
| **Step 5 → Gate 2** | testing-agent → critique-and-validation-agent | Spec + evidence package (screenshots, logs, metrics) + progress |
| **Gate 2 → Complete** | critique-and-validation-agent → Orchestrator + User | Validated completion OR identified issues + TODO updates |

### Browser Agent Configuration

**Browser Configuration Quick Reference** (see CLAUDE.md Section II for complete details):
- **Default**: Logged-in Chrome profile (99% of use cases) - prevents authentication loops
- **Incognito**: ONLY when explicitly testing logged-out scenarios
- **Pre-Call Checklist**: (1) Assess authentication needs, (2) Check previous failures, (3) Specify browser state, (4) Include failure context
- **Loop Prevention**: If testing-agent failed due to authentication → FORCE logged-in browser in next call

### Dynamic Quality Gates

| Complexity | Gate 1 (Plan Approval) | Gate 2 (Completion Validation) |
|------------|------------------------|-------------------------------|
| Simple (0-2) | May be skipped for trivial changes | Minimal evidence (1-2 screenshots) |
| Medium (3-5) | Focused plan validation | Standard evidence collection |
| Complex (6+) | Comprehensive plan validation | Full evidence suite |

### Agent Communication

All agents coordinate through prompt/response communication via Task tool:
- **Context in Prompts**: Each agent receives context through its prompt (including current TODO state)
- **Comprehensive Responses**: Agents provide detailed findings, recommendations, and progress updates
- **Progressive Context**: Each agent builds upon previous agent outputs
- **No Persistent State**: All context (including TODOs) passes through prompts and responses

### Multi-Agent Architecture Patterns

Beyond the primary orchestrator-worker pattern, several coordination patterns can be employed:

#### 1. Sequential Specialist Chain

**Definition**: Tasks flow through a series of specialized agents, each contributing specific expertise before passing to the next.

**Pattern Structure**:
```
User Query → Planning Agent → Validation Agent → Implementation Agent →
Review Agent → Testing Agent → Completion Validation Agent
```

**Advantages**:
- Clear quality gates at each stage
- Specialized expertise at each step
- Explicit validation checkpoints
- Traceable decision flow

**Disadvantages**:
- Higher latency (sequential not parallel)
- Context accumulation through chain
- Single point of failure at each stage

**Best Practices**:
- Pass complete context forward at each handoff
- Include rationale and decisions in handoffs
- Validate outputs before next stage
- Allow backward flow for corrections

#### 2. Hub-and-Spoke Pattern

**Definition**: Central coordination agent delegates to specialized agents and aggregates results.

**Use Cases**:
- Data gathering from multiple sources
- Multi-faceted analysis requiring different tools
- Consensus building across specialized perspectives
- Parallel research with synthesis

**Implementation**:
```yaml
hub_responsibilities:
  - "Query decomposition"
  - "Spoke agent selection"
  - "Parallel coordination"
  - "Result aggregation"
  - "Conflict resolution"

spoke_responsibilities:
  - "Focused task execution"
  - "Specialized tool usage"
  - "Independent operation"
  - "Structured result return"
```

#### 3. Advanced Patterns

**Hierarchical Multi-Level Orchestration**:
```
Top-Level Orchestrator
├── Feature Orchestrator A (spawns implementation agents)
├── Feature Orchestrator B (spawns testing agents)
└── Integration Orchestrator (coordinates A + B)
```
*Use Case*: Very large projects requiring multiple coordination levels

**Feedback Loop Pattern**:
```
Implementation Agent ↔ Review Agent (iterative refinement)
         ↓
  Validation Agent (final approval)
```
*Use Case*: Quality-critical implementations requiring iterative improvement

**Consensus Pattern**:
```
Multiple Expert Agents → Aggregator → Consensus Decision
```
*Use Case*: High-stakes decisions requiring multiple perspectives

### Pattern Selection Matrix

| Scenario | Recommended Pattern | Rationale |
|----------|-------------------|-----------|
| Complex feature development | Orchestrator-Worker | Parallel execution + specialization |
| Code quality assurance | Sequential Specialist | Clear quality gates |
| Multi-source research | Hub-and-Spoke | Parallel data gathering |
| Variable complexity tasks | Adaptive Delegation | Efficiency optimization |
| High-risk changes | Sequential with validation | Safety checkpoints |
| Independent modules | Parallel execution | Maximum speed |

### Parallel Execution Safety Criteria

**Safe Parallel Patterns**:
- Independent subtasks with no shared resources
- Data gathering from multiple sources
- Multi-perspective analysis
- Parallel research streams

**Risky Parallel Patterns** (avoid or serialize):
- Concurrent modifications to same files
- Dependent tasks with timing requirements
- Shared state manipulation
- Sequential quality gates

**Coordination Techniques**:
```yaml
parallel_spawning:
  method: "Orchestrator creates multiple subagent calls"
  tool: "Single message with multiple Task tool uses"
  benefit: "Maximum performance through concurrency"

result_aggregation:
  method: "Orchestrator collects all subagent outputs"
  processing: "Synthesize findings, resolve conflicts, integrate"
  output: "Unified response with multi-perspective insights"

timing_dependencies:
  method: "Orchestrator sequences dependent tasks"
  rule: "Only parallelize truly independent work"
  validation: "Check for shared resource conflicts"
```

### Agent-to-Agent Communication Protocols

**1. Prompt-Based Communication** (Current Standard):
- All context passes through prompts
- No persistent memory between agents
- Orchestrator mediates all communication
- Explicit handoff messages

**2. Structured JSON Handoffs** (Recommended for Complex Tasks):
```json
{
  "from_agent": "planning-agent",
  "to_agent": "code-writing-agent",
  "task_context": {
    "original_requirement": "Optimize data processing",
    "approved_plan": "...",
    "constraints": ["Maintain backward compatibility", "Performance target: <2s"],
    "success_criteria": "Processing time reduced by 50%"
  },
  "handoff_artifacts": {
    "plan_document": "path/to/plan.md",
    "risk_assessment": {...},
    "integration_points": [...]
  },
  "next_steps": ["Implement optimization", "Run benchmarks", "Validate performance"]
}
```

**3. Agent-to-Agent Protocol (A2A)** (Emerging Standard):
- Direct agent communication channel
- Standardized message formats
- Event-driven coordination
- Useful for complex multi-agent systems

### Coordination Anti-Patterns

**What NOT to Do**:

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Agent Overlap** | Multiple agents with overlapping responsibilities | Define clear, exclusive domains per agent |
| **Unclear Handoffs** | Implicit transitions without clear protocols | Use explicit handoff messages with complete context |
| **Context Loss** | Insufficient information passed between agents | Include all relevant context, decisions, and rationale |
| **Premature Optimization** | Complex patterns for simple tasks | Use complexity assessment to right-size workflow |
| **Circular Dependencies** | Agents waiting on each other | Design linear or tree-structured dependencies |
| **Monolithic Agents** | Single agent trying to do too much | Decompose into focused, specialized agents |
| **Uncontrolled Spawning** | Agents creating agents without limits | Orchestrator controls all agent creation |

</coordination>

---

## IV. APPLICATION-SPECIFIC INTEGRATION

<integration>

### Documentation References

**[USER CONFIGURATION REQUIRED]**

Agents should reference project-specific documentation when available. Common documentation files to create for your project:

| Document | Contents |
|----------|----------|
| **DEBUGGING.md** | Log patterns, troubleshooting procedures, expected behaviors |
| **ENVIRONMENT.md** | Environment configuration and setup |
| **DATABASE.md** | Database management and schema operations (if applicable) |
| **PACKAGE_MANAGEMENT.md** | Package scripts and dependencies |
| **ARCHITECTURE.md** | System design patterns, integration flows, authentication architecture |
| **LIFECYCLE.md** | Application timing, component lifecycles, initialization sequences |
| **TESTING_GUIDE.md** | Testing protocols, performance expectations, validation checklists |
| **RECENT_GOTCHAS.md** | Current known issues, workarounds, ongoing investigations |

**To create these documents**: Run `@.claude/prompts/setup-instructions.md` for guided documentation creation with agent-system-optimizer.

### Performance Requirements

**[USER CONFIGURATION REQUIRED]**

Document your application's performance requirements here. Examples:

| Stage | Timing Constraint | Notes |
|-------|------------------|-------|
| Initial Load | ≤Xs | First meaningful paint |
| API Response | ≤Xms | Typical API calls |
| Database Query | ≤Xms | Standard queries |
| Build Time | ≤Xs | Production build |

### Escalation Procedures

**User Escalation Triggers** (immediate consultation required):
- Ambiguous or contradictory requirements
- Scope changes exceeding original expectations
- High-risk changes requiring user approval
- Resource constraints beyond agent capabilities
- Irreconcilable quality vs timeline conflicts

**Escalation Communication Format**:
1. Context summary (brief overview of situation)
2. Specific issue (clear description of problem/decision needed)
3. Options analysis (2-3 viable approaches with pros/cons)
4. Recommendation (preferred approach with rationale)
5. Impact assessment (effects on timeline and quality)

</integration>

---

## V. TODO MANAGEMENT ARCHITECTURE

<todo_management>

### Critical Understanding: Subagent Context Isolation

**FUNDAMENTAL ARCHITECTURAL CONSTRAINT**: Subagents operate in completely isolated contexts and have NO access to:
- The orchestrator's TODO list
- TODOs created by other subagents
- Any persistent shared state

**TodoWrite Tool is CUSTOM** (not part of official Claude Code documentation):
- **Exclusively controlled by orchestrator** - subagents CANNOT share TODO state
- **Single source of truth**: Only orchestrator maintains persistent TODO list

### Context Injection Protocol (MANDATORY)

**For ALL subagent calls, orchestrator MUST inject current TODO state:**

```yaml
context_injection_requirement:
  mandatory: "Every subagent prompt MUST include current TODO state"
  format: |
    CURRENT TODO STATE:
    1. [Task description] - [status: pending/in_progress/completed]
    2. [Task description] - [status: pending/in_progress/completed]
    ...

    YOUR FOCUS: [Specific TODO item(s) this agent should address]
    RELEVANT CONTEXT: [Additional context from completed TODOs]

  timing: "Include in EVERY subagent call (planning, implementation, review, testing)"
  update_frequency: "Refresh TODO state before each new subagent invocation"
```

**Example Context Injection**:
```
CURRENT TODO STATE:
1. Create lightweight specification - completed
2. Plan implementation approach - completed
3. Implement optimization - in_progress
4. Review implemented code - pending
5. Validate with browser testing - pending

YOUR FOCUS: Implement optimization (TODO #3)
RELEVANT CONTEXT: Specification approved in specs/active/optimization.md, plan validated by critique agent with focus on caching and chunked processing.
```

### Subagent Progress Reporting Protocol

**Since subagents CANNOT modify orchestrator's TODO list, they MUST report progress in response text:**

```yaml
subagent_reporting_format:
  structure: |
    PROGRESS UPDATE:
    - Completed: [What work was accomplished]
    - TODO Updates Recommended: [Suggested changes to TODO list based on findings]
    - Next Steps: [What should happen next in workflow]
    - Blockers: [Any issues preventing progress]
```

**Example Progress Report (planning-agent)**:
```
PROGRESS UPDATE:
- Completed: Implementation plan created with 3 phases
- TODO Updates Recommended:
  * Mark "Plan implementation approach" as completed
  * Add "Phase 1: Core implementation" as pending
  * Add "Phase 2: Integration" as pending
  * Add "Phase 3: Performance validation" as pending
- Next Steps: Submit plan to critique-and-validation-agent for Gate 1 approval
- Blockers: None identified
```

### Orchestrator Responsibilities

```yaml
orchestrator_todo_management:
  maintain_canonical_list:
    - "Use TodoWrite to update single source of truth"
    - "Never allow subagents to modify TODO list directly"
    - "Preserve TODO state across entire conversation"

  inject_context_always:
    - "Include current TODO state in EVERY subagent prompt"
    - "Specify which TODO item(s) the subagent should address"
    - "Provide relevant context from completed TODOs"

  process_subagent_updates:
    - "Read subagent PROGRESS UPDATE sections in responses"
    - "Update TODO list via TodoWrite based on reported progress"
    - "Mark items completed only when subagent confirms completion"
    - "Add new items if subagent identifies additional work"

  track_progress_systematically:
    - "Monitor TODO completion across 5-step workflow"
    - "Ensure each workflow step has corresponding TODO items"
    - "Use TODO status to guide which agent to call next"
    - "Validate all TODOs completed before task conclusion"
```

### Tool Permission Matrix

| Tool | Orchestrator | All Subagents |
|------|-------------|---------------|
| **TodoWrite** | FULL ACCESS - maintains canonical TODO list | NO ACCESS - reports progress in response text |
| **Context Visibility** | Sees all TODOs (maintains them) | Sees ONLY what orchestrator includes in prompts |

### Common Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Subagent TodoWrite | TODOs created in isolated context, vanish when agent completes | Remove TodoWrite from subagent prompts, use progress reporting |
| Missing context injection | Subagent lacks task awareness, cannot align work with overall progress | ALWAYS include TODO state in subagent prompts |
| Ignoring progress updates | TODO list becomes stale, doesn't reflect actual progress | Read PROGRESS UPDATE sections, update TODOs via TodoWrite |
| Assuming TODO visibility | Subagent works without full context, misaligned with workflow | Explicitly inject TODO state in every subagent prompt |

### Why This Architecture Exists

**Technical Constraints**:
- Subagents run in isolated contexts by Claude Code design
- No persistent state between agent invocations
- TodoWrite is custom, not part of official Claude Code API

**Architectural Benefits**:
- Orchestrator maintains definitive TODO state (single source of truth)
- Impossible for subagents to create conflicting TODO updates
- All TODO changes flow through orchestrator (explicit coordination)
- Subagent progress explicitly reported, not implicit

</todo_management>

---

This multi-agent system ensures every aspect of development is handled by specialized expertise while maintaining coordination and quality throughout the entire process. The 5-step adaptive workflow provides a single unified pattern that scales from simple typo fixes to complex architectural changes, with specification depth adapting to match task complexity. TODO management maintains a single source of truth through the orchestrator while enabling all agents to communicate progress and maintain task awareness through explicit context injection.
