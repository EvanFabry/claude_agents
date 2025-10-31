# DATABASE.md - Database Management & Schema

**[USER CONFIGURATION REQUIRED]**

This file documents database schema, queries, and data management procedures. Agents reference this file when they need to understand data storage and retrieval patterns.

---

## 🗄️ Database Overview

**Purpose**: Document database technology and connection details.

**What to include**:
- Database type and version
- Connection information
- Access patterns
- Data organization philosophy

**Example**:
```
Database: [PostgreSQL 15 / MySQL 8 / MongoDB 6 / etc.]
ORM/Query Builder: [Prisma / TypeORM / Sequelize / Mongoose / Raw SQL]

Connection:
- Development: localhost:[port]
- Staging: [cloud-instance-url]
- Production: [cloud-instance-url] with read replicas

Access Patterns:
- Primary: Read-write operations on main instance
- Replicas: Read-only queries for reporting/analytics (if applicable)

Philosophy:
- [Normalized / Denormalized for performance]
- [Event sourcing / Traditional CRUD]
- [Single database / Microservices with separate databases]
```

---

## 📊 Schema Overview

**Purpose**: Document database schema and relationships.

**What to include**:
- Table/collection names and purposes
- Key relationships
- Indexes
- Constraints

**Example**:
```
Tables/Collections:

1. users
   - id (primary key, auto-increment/UUID)
   - email (unique, not null)
   - password_hash (not null)
   - role (enum: admin, user, guest)
   - created_at (timestamp)
   - updated_at (timestamp)
   - Indexes: email (unique), role
   - Foreign Keys: none

2. [table_name]
   - id (primary key)
   - user_id (foreign key → users.id)
   - [other_fields]
   - created_at (timestamp)
   - Indexes: user_id, created_at
   - Foreign Keys: user_id → users.id (ON DELETE CASCADE)

3. [Add more tables as needed]

Relationships:
- users → [table] (one-to-many)
- [table] ↔ [table] (many-to-many via junction table)
```

---

## 🔄 Migrations

**Purpose**: Document migration strategy and procedures.

**What to include**:
- Migration tool
- Migration workflow
- Rollback procedures
- Environment-specific considerations

**Example**:
```
Migration Tool: [Prisma Migrate / TypeORM / Knex / Flyway / etc.]

Migration Files Location: [prisma/migrations / migrations / db/migrate]

Creating Migrations:
- Command: [npm run migrate:create / pnpm migrate:create]
- Naming: [timestamp_description.sql / YYYYMMDDHHMMSS_description.ts]
- Review: Always review generated SQL before committing

Running Migrations:
- Development: [npm run migrate:dev / automatic on dev server start]
- Staging: [npm run migrate:deploy / CI/CD pipeline]
- Production: [npm run migrate:deploy / manual trigger with approval]

Rollback:
- Command: [npm run migrate:rollback]
- Strategy: [Keep previous migration / Manual rollback SQL]
- Testing: Always test rollback in staging first

Best Practices:
- Never edit committed migrations
- Always make migrations reversible when possible
- Test migrations in development before staging
- Backup production database before major migrations
```

---

## 🔍 Query Patterns

**Purpose**: Document common query patterns and optimizations.

**What to include**:
- Frequently used queries
- Query optimization strategies
- N+1 query prevention
- Pagination patterns

**Example**:
```
Common Queries:

1. Get user with related data:
   [ORM syntax or SQL]
   Performance: ~[50]ms, uses index on user_id
   Optimization: Includes [related_table] to avoid N+1

2. List items with pagination:
   [ORM syntax or SQL]
   Performance: ~[100]ms for 20 items
   Pagination: Cursor-based / Offset-based
   Index: created_at DESC

3. [Add more common queries]

Query Optimization:
- Use select() to fetch only needed columns
- Use eager loading to prevent N+1 queries
- Add indexes for frequently filtered/sorted columns
- Use database-level aggregation when possible

N+1 Prevention:
- Use includes/joins to load related data
- Batch queries with DataLoader pattern (if applicable)
- Monitor query counts in development
```

---

## 🚀 Performance & Optimization

**Purpose**: Document database performance tuning and optimization strategies.

**What to include**:
- Index strategy
- Query performance targets
- Caching strategy
- Connection pooling

**Example**:
```
Performance Targets:
- Simple queries: <[50]ms
- Complex queries: <[500]ms
- Bulk operations: <[2]s per 1000 records

Indexes:
- Primary keys: Auto-created
- Foreign keys: Index all foreign key columns
- Unique constraints: users.email, [others]
- Composite indexes: [(column1, column2) for queries filtering on both]

Query Performance:
- Use EXPLAIN ANALYZE to understand query plans
- Watch for sequential scans on large tables
- Ensure indexes are actually being used

Caching:
- Query results cached for [duration] in [Redis / memory]
- Cache invalidation on [write operations / TTL expiry]
- Cache warming strategy: [On startup / On first request]

Connection Pooling:
- Min connections: [2-5]
- Max connections: [10-20]
- Idle timeout: [30]s
- Connection reuse: Enabled
```

---

## 📝 Data Management

**Purpose**: Document data maintenance procedures.

**What to include**:
- Backup strategy
- Data retention policies
- Data cleanup procedures
- Archival strategies

**Example**:
```
Backups:
- Frequency: [Daily / Hourly]
- Retention: [30] days for daily, [7] days for hourly
- Location: [Cloud storage / Separate region]
- Recovery time objective (RTO): [4] hours
- Recovery point objective (RPO): [24] hours
- Test restores: [Monthly]

Data Retention:
- User data: Retain until account deletion + [30] days
- Logs: Retain for [90] days, then archive
- Analytics: Aggregate and retain for [2] years
- [Other data types]: [Retention policy]

Data Cleanup:
- Soft deletes: Mark deleted_at timestamp, physical delete after [30] days
- Automated cleanup: Cron job runs [daily] to remove old records
- Manual cleanup: [Procedure for manual data removal]

Compliance:
- GDPR: Support data export and deletion requests
- Data sovereignty: [Geographic data storage requirements]
```

---

## 🔒 Security & Access Control

**Purpose**: Document database security and access patterns.

**What to include**:
- Access credentials management
- User permissions
- Sensitive data handling
- Audit logging

**Example**:
```
Access Control:
- Application user: Read/write access to application tables
- Migration user: Schema modification permissions
- Readonly user: Read-only access for analytics/reporting
- Admin user: Full access (use sparingly)

Credentials:
- Stored in: [Environment variables / Secrets manager]
- Rotation: [Quarterly / After incidents]
- Access: Granted via [IAM / Database users]

Sensitive Data:
- Passwords: Hashed with [bcrypt / Argon2]
- PII: Encrypted at rest with [encryption method]
- Payment data: [Tokenized / Not stored]
- API keys: Encrypted before storage

Audit Logging:
- Track: [Schema changes / Data modifications / Access patterns]
- Retention: [1] year
- Review: [Monthly / After incidents]
```

---

## 🧪 Testing Database

**Purpose**: Document test database setup and seeding.

**What to include**:
- Test database configuration
- Seed data procedures
- Test data cleanup
- Factory/fixture patterns

**Example**:
```
Test Database:
- Separate database: [test_database_name]
- Reset before each test suite: [yes/no]
- Transaction rollback: [yes/no - for individual tests]

Seed Data:
- Location: [prisma/seed.ts / seeds / fixtures]
- Command: [npm run seed / pnpm seed]
- Data included: [Users, test entities, relationships]

Test Data Creation:
- Factories: [path/to/factories] (if using factory pattern)
- Fixtures: [path/to/fixtures] (if using fixtures)
- Pattern: [Factory pattern / Raw inserts / ORM creates]

Cleanup:
- Between tests: [Transaction rollback / Database wipe]
- After suite: [Drop and recreate / Leave for inspection]
```

---

## 📈 Monitoring & Alerts

**Purpose**: Document database monitoring setup.

**What to include**:
- Monitored metrics
- Alert thresholds
- Slow query logging
- Performance dashboards

**Example**:
```
Monitored Metrics:
- Connection count: Alert if >[80]% of pool
- Query duration: Alert if p95 >[1]s
- Disk usage: Alert if >[80]% full
- CPU usage: Alert if >[80]% sustained for [5]min
- Replication lag: Alert if >[10]s behind

Slow Query Logging:
- Threshold: Queries taking >[1]s
- Log location: [database logs / monitoring service]
- Review: [Weekly / After performance issues]

Dashboards:
- Database performance: [Link to dashboard]
- Query analytics: [Link to query analyzer]
- Connection pool: [Link to connection metrics]
```

---

## 📝 Configuration Guide

**To populate this file**:

1. Document schema as you design it
2. Update when you add migrations
3. Document query patterns as you discover optimization needs
4. Review and update when database structure changes significantly

**When agents reference this file**:
- code-writing-agent uses it to write database queries correctly
- debugging-agent uses it to understand data-related issues
- testing-agent uses it to set up test data appropriately
- planning-agent uses it to understand data model constraints
