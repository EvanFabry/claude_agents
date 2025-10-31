# TESTING_GUIDE.md - Testing Protocols & Validation

**[USER CONFIGURATION REQUIRED]**

This file documents testing strategies, protocols, and validation procedures. Agents reference this file when they need to understand how to test functionality.

---

## 🧪 Testing Strategy Overview

**Purpose**: Document overall testing approach and philosophy.

**What to include**:
- Testing pyramid/approach
- Test types and coverage goals
- When each test type is appropriate
- CI/CD integration

**Example**:
```
Testing Philosophy: [Test-driven / Behavior-driven / Pragmatic testing]

Test Pyramid:
- Unit Tests (70%): Fast, isolated, test individual functions/components
- Integration Tests (20%): Test component interactions
- E2E Tests (10%): Test complete user flows

Coverage Goals:
- Overall: >[80]%
- Critical paths: [100]%
- Utility functions: >[90]%
- UI components: >[70]%

Test Execution:
- Pre-commit: Unit tests (fast feedback)
- Pre-push: All tests (full validation)
- CI/CD: All tests + E2E on PR
- Production: Smoke tests after deployment
```

---

## 🎯 Unit Testing

**Purpose**: Document unit testing approach and tools.

**What to include**:
- Testing framework
- Test file organization
- Mocking strategies
- Common patterns

**Example**:
```
Framework: [Vitest / Jest / Mocha]

Test File Location:
- Co-located: [ComponentName.test.ts] next to [ComponentName.ts]
- Separate: [__tests__/ComponentName.test.ts]
- Convention: Use [*.test.ts / *.spec.ts]

Running Tests:
- All unit tests: [npm test / pnpm test]
- Specific file: [npm test path/to/file.test.ts]
- Watch mode: [npm test -- --watch]
- Coverage: [npm test -- --coverage]

Mocking:
- Module mocks: [vi.mock() / jest.mock()]
- Function mocks: [vi.fn() / jest.fn()]
- API calls: Mock at [fetch / axios / API client] level
- Database: Mock at [ORM / repository] level

Test Structure:
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should handle expected case', () => {
      // Arrange
      const input = /* setup */

      // Act
      const result = methodName(input)

      // Assert
      expect(result).toBe(expected)
    })
  })
})

Common Patterns:
- Use factories for test data creation
- Group related tests with describe blocks
- One assertion per test (when possible)
- Clear test names describing behavior
```

---

## 🔗 Integration Testing

**Purpose**: Document integration testing approach.

**What to include**:
- What constitutes an integration test
- Integration testing tools
- Database/API handling
- Common patterns

**Example**:
```
Integration Tests: Test component interactions without full E2E

Scope:
- API routes with database
- Multiple components working together
- Service layer interactions
- Third-party integrations (with mocks)

Tools:
- Test framework: [Same as unit tests / Separate framework]
- Test database: [SQLite in memory / Docker container / Dedicated test DB]
- API mocking: [MSW / Nock / Custom mocks]

Running:
- Command: [npm run test:integration]
- Database setup: [Automatic via beforeAll hooks / Manual setup required]
- Cleanup: [Automatic via afterAll hooks]

Database Testing:
- Strategy: [Transaction rollback / Database recreation / Isolated test DB]
- Seed data: Use factories, not production fixtures
- Cleanup: Always clean up after tests

Example:
describe('UserAPI', () => {
  beforeAll(async () => {
    // Setup test database
  })

  afterAll(async () => {
    // Cleanup
  })

  it('should create user and return with ID', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com' })

    expect(response.status).toBe(201)
    expect(response.body).toHaveProperty('id')
  })
})
```

---

## 🌐 E2E Testing

**Purpose**: Document end-to-end testing approach.

**What to include**:
- E2E framework
- Test scenarios
- Test data management
- Visual regression testing

**Example**:
```
Framework: [Playwright / Cypress / Puppeteer]

Test Scenarios:
- Critical user journeys: [Login → Main action → Logout]
- Happy paths for major features
- Key error scenarios
- Mobile vs Desktop (if applicable)

Running:
- Command: [npm run test:e2e]
- Headless: [npm run test:e2e]
- Headed: [npm run test:e2e:headed]
- UI mode: [npm run test:e2e:ui]

Test Environment:
- Server: [Starts automatically / Must be running]
- Database: [Test database / Seeded with fixtures]
- Authentication: [Test user accounts]

Test Data:
- Strategy: [Reset before each test / Isolated test data per test]
- Test users: [user1@test.com / admin@test.com]
- Cleanup: [Automatic / Manual]

Browser Configuration:
- Browsers tested: [Chromium / Firefox / WebKit]
- Viewport sizes: [Desktop: 1920x1080, Mobile: 390x844]
- Authenticated state: Uses logged-in browser profile (default)
- Incognito: ONLY for testing logged-out scenarios

Example:
test('user can complete purchase', async ({ page }) => {
  await page.goto('/products')
  await page.click('[data-testid="add-to-cart"]')
  await page.click('[data-testid="checkout"]')
  await page.fill('[name="card-number"]', '4242424242424242')
  await page.click('[data-testid="submit-payment"]')

  await expect(page).toHaveURL(/\/confirmation/)
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible()
})

Visual Regression:
- Tool: [Percy / Chromatic / Playwright screenshots]
- Baseline: [Git-tracked / Cloud service]
- Comparison: [Automatic on PR / Manual review]
```

---

## ⚡ Performance Testing

**Purpose**: Document performance testing and benchmarks.

**What to include**:
- Performance metrics
- Testing tools
- Benchmark targets
- Regression detection

**Example**:
```
Performance Metrics:
- Page load time: <[3]s
- Time to interactive: <[5]s
- First contentful paint: <[1.5]s
- Largest contentful paint: <[2.5]s
- API response time: <[500]ms (p95)

Tools:
- Lighthouse CI: [In CI/CD pipeline / Manual]
- Browser DevTools: Performance profiling
- [Other tools]: [k6 / Artillery / JMeter]

Running Performance Tests:
- Command: [npm run test:performance]
- Frequency: [On every PR / Weekly]
- Baseline: [Git-tracked performance budget]

Benchmarks:
test('API endpoint performance', async () => {
  const start = Date.now()
  await fetch('/api/endpoint')
  const duration = Date.now() - start

  expect(duration).toBeLessThan(500)
})

Performance Budget:
- JavaScript: <[500]KB
- CSS: <[100]KB
- Images: <[1]MB total
- Fonts: <[100]KB

Regression Detection:
- Alert if metrics degrade by >[10]%
- Block PR if exceeds hard limits
- Review report: [Link to dashboard]
```

---

## 🔍 Test Data Management

**Purpose**: Document test data creation and management.

**What to include**:
- Factories/fixtures
- Seed data
- Data cleanup
- PII handling

**Example**:
```
Test Data Creation:

Factories: [path/to/factories]
- UserFactory: Creates user with defaults
- [EntityFactory]: Creates [entity]
- Usage: const user = UserFactory.create({ email: 'custom@test.com' })

Fixtures: [path/to/fixtures]
- users.json: Standard test users
- [entity].json: Test [entities]
- Loading: Import and use in tests

Seed Scripts:
- Command: [npm run db:seed]
- Data: Creates [X] users, [Y] entities
- Reset: [npm run db:reset] drops and recreates

Data Cleanup:
- Unit tests: No database access, no cleanup needed
- Integration tests: Transaction rollback or database wipe
- E2E tests: Reset database before each test file

PII in Tests:
- Never use real user data
- Use clearly fake emails: test@example.com
- Use test credit cards: 4242424242424242
- Faker library for generated data: [faker.internet.email()]
```

---

## ✅ Test Validation Criteria

**Purpose**: Document what makes a test suite acceptable.

**What to include**:
- Quality criteria
- Code review checklist
- Coverage requirements
- Performance constraints

**Example**:
```
Test Quality Criteria:

1. Reliability:
   - Tests pass consistently (no flaky tests)
   - No random data causing intermittent failures
   - No race conditions or timing issues
   - Proper async/await usage

2. Readability:
   - Clear test names describing behavior
   - Arrange-Act-Assert structure
   - Minimal setup complexity
   - Good comments for complex scenarios

3. Maintainability:
   - DRY principle (shared test utilities)
   - No hardcoded values (use constants/factories)
   - Easy to update when code changes
   - Good separation of concerns

4. Performance:
   - Unit test suite: <[30]s
   - Integration test suite: <[2]min
   - E2E test suite: <[10]min
   - Individual E2E test: <[30]s

Code Review Checklist:
□ Tests cover happy path
□ Tests cover error cases
□ Tests cover edge cases
□ No commented-out tests
□ No .skip() or .only() left in
□ Coverage meets threshold
□ Tests are deterministic
□ Proper cleanup in afterEach/afterAll
```

---

## 🚨 Testing Anti-Patterns

**Purpose**: Document what to avoid in tests.

**What to include**:
- Common mistakes
- Bad practices
- How to fix them

**Example**:
```
Anti-Patterns to Avoid:

❌ Testing Implementation Details
Bad: expect(component.state.loading).toBe(true)
Good: expect(screen.getByText('Loading...')).toBeInTheDocument()

❌ Flaky Tests
Bad: await wait(1000) // Arbitrary wait
Good: await waitFor(() => expect(element).toBeInTheDocument())

❌ Tests Depending on Each Other
Bad: Test 2 depends on data created in Test 1
Good: Each test is independent and can run in any order

❌ Over-Mocking
Bad: Mock everything, test nothing real
Good: Mock external dependencies, test your code

❌ Brittle Selectors
Bad: page.click('.btn.btn-primary.mt-4')
Good: page.click('[data-testid="submit-button"]')

❌ Unclear Test Names
Bad: it('works')
Good: it('should display error message when email is invalid')

❌ Multiple Assertions on Unrelated Things
Bad: Test user creation AND deletion in one test
Good: Separate tests for creation and deletion
```

---

## 🔄 Continuous Integration

**Purpose**: Document CI/CD testing integration.

**What to include**:
- CI pipeline configuration
- Test parallelization
- Failure handling
- Reporting

**Example**:
```
CI Platform: [GitHub Actions / GitLab CI / CircleCI / etc.]

Pipeline Configuration: [.github/workflows/test.yml / .gitlab-ci.yml]

Test Jobs:
1. Unit & Integration Tests
   - Runs on: Every commit
   - Timeout: [10]min
   - Parallel: [Yes, split by file/spec]

2. E2E Tests
   - Runs on: Pull requests
   - Timeout: [20]min
   - Parallel: [Yes, split by browser/spec]
   - Retry failed: [1 time]

3. Performance Tests
   - Runs on: Pull requests to main
   - Timeout: [15]min
   - Comparison: Against main branch baseline

Test Matrix:
- Node versions: [18.x, 20.x]
- Browsers: [Chromium, Firefox, WebKit]
- OS: [ubuntu-latest / Windows / macOS if needed]

Failure Handling:
- Failed tests: Block merge
- Flaky test: Retry once, then report
- Timeout: Fail job
- Coverage drop: [Block merge / Warning only]

Reporting:
- Coverage reports: [Codecov / Coveralls]
- Test results: [Attached to PR / CI dashboard]
- Screenshots/videos: [For failed E2E tests]
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Run `@.claude/prompts/setup-instructions.md` for guided configuration
2. Document test patterns as you establish them
3. Update when adding new test types or tools
4. Review and refine based on actual test writing experience

**When agents reference this file**:
- testing-agent uses it to understand how to write and run tests
- code-writing-agent uses it to understand testability requirements
- debugging-agent uses it to understand test failures
- planning-agent uses it to plan testable implementations
