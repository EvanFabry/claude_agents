# Multi-Agent System Setup Instructions

You are Claude, helping a user configure this multi-agent development system for their specific project.

---

## Overview

This multi-agent system is designed to be **project-agnostic**. Before it can be used effectively, it needs to be configured with your project's specific:
- Architecture patterns
- Development environment
- Performance requirements
- Testing infrastructure
- Integration requirements

This automated setup process will guide you through configuration.

---

## Setup Process

### Phase 1: Discovery & Analysis

**Your Task**: Use the agent-system-optimizer to scan the entire repository and identify all configuration requirements.

**What to Find:**

1. **Stub Sections in Agent Prompts**
   - Search `.claude/agents/*.md` for `[STUB]` markers
   - Document which agents have which stubs
   - Note what type of information each stub needs

2. **User Configuration Requirements in CLAUDE.md**
   - Search for `[USER CONFIGURATION REQUIRED]` markers
   - Search for `[YOUR_*]` placeholder patterns
   - Identify all application-specific assumptions

3. **Environment Variable Requirements**
   - Check `.claude/hooks/send_notification.sh` for notification config
   - Check other hooks for environment dependencies
   - Document all required environment variables

4. **Application-Specific References**
   - Find references to specific frameworks (Remix, Next.js, etc.)
   - Identify hardcoded commands (development servers, build tools)
   - Note any port numbers, paths, or tool-specific assumptions

**Deliverable**: Comprehensive list of all items requiring configuration, organized by category.

---

### Phase 2: Information Gathering

**Your Task**: Present findings to the user and collect necessary information.

**Information to Collect:**

#### A. Project Basics
```yaml
questions:
  - "What type of project is this? (React, Vue, Next.js, Remix, Node.js API, etc.)"
  - "What package manager do you use? (npm, pnpm, yarn, bun)"
  - "What is your project's root directory path?"
```

#### B. Development Environment
```yaml
questions:
  - "What command starts your development server? (e.g., npm run dev, pnpm dev, vite)"
  - "What port does your development server use? (e.g., 3000, 5173, 8080)"
  - "Do you use any special architecture patterns (service workers, middleware, etc.)? If yes, describe."
  - "What command builds your project for production?"
```

#### C. Testing Infrastructure
```yaml
questions:
  - "Do you have browser testing set up? (Playwright, Cypress, none)"
  - "What command runs your tests?"
  - "Are there any test-specific environment requirements?"
  - "What browser profile should testing use? (default logged-in profile, incognito, custom)"
```

#### D. Architecture Patterns
```yaml
questions:
  - "Do you have specific architectural constraints? (microservices, monolith, serverless, etc.)"
  - "Are there critical timing dependencies we should know about? (component lifecycles, API sequences)"
  - "What are your performance requirements? (page load times, API response times, etc.)"
  - "Do you have integration with external services? Which ones?"
```

#### E. Documentation
```yaml
questions:
  - "Do you have existing documentation we should reference? (ARCHITECTURE.md, README.md, etc.)"
  - "Should we create documentation files for patterns we discuss? (recommended: yes)"
  - "Are there known issues or gotchas we should document?"
```

#### F. Notifications (Optional)
```yaml
questions:
  - "Do you want to set up Pushover notifications for agent task completion?"
  - "If yes, do you have Pushover account? (needs user key + API token)"
```

**Deliverable**: Complete answers to all questions, organized and ready for configuration.

---

### Phase 3: Configuration Execution

**Your Task**: Start a new thread with agent-system-optimizer to apply all configurations.

**Agent-System-Optimizer Instructions:**

In a new thread, provide agent-system-optimizer with:
```
I need you to configure the multi-agent system with the following project details:

[Paste all collected information from Phase 2]

Please update the following files:

1. Update all stub sections in agent prompts:
   - code-writing-agent.md (Application Architecture, Performance Standards stubs)
   - testing-agent.md (Application Testing Patterns stub)
   - code-reviewer.md (Application Code Review stub)
   - planning-agent.md (Application Planning Context stub)
   - debugging-agent.md (Log Patterns, Timing Dependency stubs)
   - critique-and-validation-agent.md (Application Validation stub)

2. Update CLAUDE.md:
   - Replace [YOUR_DEV_COMMAND] with actual command
   - Replace [YOUR_DEV_PORT] with actual port
   - Replace [YOUR_FRAMEWORK] with actual framework
   - Update browser configuration section with correct paths
   - Replace any other placeholders

3. Create/Update documentation files:
   - Create ARCHITECTURE.md if needed (with project architecture patterns)
   - Create LIFECYCLE.md if timing dependencies exist
   - Create DEBUGGING.md with expected log patterns
   - Update RECENT_GOTCHAS.md with known issues

4. Update environment setup in README.md:
   - Add project-specific environment variables
   - Document development setup steps
   - Include correct server commands

For each stub section, replace generic guidance with project-specific details based on the information provided. Keep universal principles, but add concrete examples and requirements specific to this project.
```

**What Agent-System-Optimizer Will Do:**
1. Read each file requiring updates
2. Replace placeholders with actual values
3. Enhance stub sections with project-specific guidance
4. Create new documentation files as needed
5. Verify all references and links work correctly

---

### Phase 4: Validation & Confirmation

**Agent-System-Optimizer Must Verify:**

#### A. Completeness Check
- [ ] All stub sections now contain project-specific guidance (no generic placeholders)
- [ ] All [USER CONFIGURATION REQUIRED] markers replaced
- [ ] All [YOUR_*] placeholders replaced with actual values
- [ ] Environment variables documented in README.md
- [ ] Development commands are correct

#### B. Consistency Check
- [ ] References between files are valid (e.g., @ARCHITECTURE.md references work)
- [ ] Port numbers consistent across all files
- [ ] Framework names consistent
- [ ] No contradictory information

#### C. Documentation Check
- [ ] New documentation files created where needed
- [ ] Existing documentation updated with new patterns
- [ ] Cross-references between docs work correctly

#### D. Testing Check
- [ ] Browser configuration matches user's environment
- [ ] Test commands are correct
- [ ] Output directories exist or will be created

**Deliverable**: Agent-system-optimizer confirms:

```
✅ System configuration complete and validated

Summary of changes:
- Updated 6 agent prompts with project-specific guidance
- Configured CLAUDE.md for [PROJECT_TYPE] development
- Created [X] new documentation files
- Updated README.md with environment setup
- All placeholders replaced
- All references validated

The multi-agent system is now configured for:
  Project: [PROJECT_NAME]
  Framework: [FRAMEWORK]
  Dev Server: [COMMAND] on port [PORT]
  Testing: [TESTING_SETUP]

Ready for use.
```

---

## Success Criteria

The setup is complete when:

✅ **All stub sections have project-specific guidance**
- No generic "consult agent-system-optimizer" text remains in stubs
- Concrete examples match actual project architecture
- Performance requirements are specific numbers, not generic advice

✅ **All environment variables documented**
- README.md has complete environment setup section
- Each variable has description and example value
- Optional vs required variables are clearly marked

✅ **CLAUDE.md references correct application architecture**
- Development server commands are accurate
- Port numbers match actual configuration
- Framework-specific patterns are correct

✅ **Browser configuration matches user's environment**
- Browser profile paths are correct for user's OS
- Testing configuration matches actual setup
- Authentication requirements documented

✅ **agent-system-optimizer confirms completion**
- Explicit "System configuration complete and validated" message
- Summary of all changes made
- Confirmation that system is ready for use

---

## Troubleshooting

### If Setup Fails or Is Incomplete

1. **Missing Information**: Go back to Phase 2, collect more details
2. **Invalid Paths**: Verify all file paths and directories exist
3. **Conflicting Requirements**: Clarify with user, document resolution
4. **Documentation Gaps**: Create minimal documentation to proceed

### After Setup

- **Test the system**: Try a simple task to verify agent coordination works
- **Update as needed**: Configuration can be refined as you use the system
- **Document learnings**: Add to RECENT_GOTCHAS.md as you discover patterns

---

## Next Steps After Setup

1. **Test basic workflow**: Ask orchestrator to handle a simple task
2. **Verify agent coordination**: Check that agents pass context correctly
3. **Validate evidence collection**: Ensure testing-agent can capture logs/screenshots
4. **Review notifications**: Test Pushover setup if configured

---

**Remember**: This setup process runs once per project. After completion, the multi-agent system will work seamlessly with your specific application architecture.
