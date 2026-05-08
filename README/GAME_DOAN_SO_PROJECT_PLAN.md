# Game Đoán Số — Comprehensive Project Plan
**From Empty Environment to Production Release**

**Owner**: Mr. Đức (Technical Lead)  
**Project**: Number Guessing Game REST API  
**Duration**: 2 Days (Estimated) | 5 Days (Recommended with Quality Buffer)  
**Status**: Planning Phase  
**Created**: May 7, 2026  

---

## 📋 EXECUTIVE SUMMARY

### Project Goal
Build a production-ready REST API game where players guess numbers (1-5) to earn score with controlled fairness, atomic concurrency safety, and real-time leaderboard.

### Success Criteria
- ✅ All 6 functional requirements implemented & tested
- ✅ Zero data inconsistencies under concurrent load
- ✅ p95 latency: /guess < 150ms, /leaderboard < 30ms  
- ✅ Security: JWT + HttpOnly Cookie, BCrypt hashing, rate limiting
- ✅ Code: Clean Architecture, 70%+ test coverage, all ADRs documented
- ✅ Deployment: Runnable in dev/test/prod environments

### Estimated Effort
| Phase | Days | FTE | Total Hours |
|-------|------|-----|-------------|
| Setup & Infrastructure | 0.5 | 1 | 4 |
| Core Backend Development | 1.0 | 1 | 8 |
| Testing & QA | 0.5 | 1 | 4 |
| Documentation & Release | 0.5 | 1 | 4 |
| **TOTAL (Aggressive)** | **2.5** | 1 | **20** |
| **TOTAL (Recommended)** | **4** | 1 | **32** |

---

## 🏗️ ARCHITECTURE OVERVIEW

### Technology Stack

```
┌─────────────────────────────────────────────┐
│  Frontend / Client (Out of scope)           │
└──────────────────┬──────────────────────────┘
                   │ HTTPS + HttpOnly Cookie
                   ▼
┌─────────────────────────────────────────────┐
│  API Gateway / Load Balancer                │
│  (Optional for v1, Single-node deployment) │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Spring Boot 3.x Application (Java 17+)     │
│  ├── REST Controllers (Presentation)        │
│  ├── Use Cases (Application)                │
│  ├── Domain Services (Domain)               │
│  └── Infrastructure                         │
│      ├── JPA Repositories                   │
│      ├── Redis Cache                        │
│      └── Security (JWT, BCrypt)             │
└──────────────────┬──────────────────────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
    ┌──────────┐       ┌──────────┐
    │ MySQL 8  │       │ Redis 7+ │
    │ or PgSQL │       │ (ZSET)   │
    └──────────┘       └──────────┘
```

### Key Technologies

| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Java 17+ | Strong typing, ecosystem, Spring support |
| Framework | Spring Boot 3.x | Rapid development, industry standard |
| Database | MySQL 8 / PostgreSQL 14+ | ACID compliance, atomic conditional UPDATE |
| Cache | Redis 7+ | ZSET for O(log N) leaderboard |
| Auth | JWT + HttpOnly Cookie | XSS protection, sessionless |
| Testing | JUnit 5 + Testcontainers | Isolated, reproducible tests |
| Build | Maven / Gradle | Dependency management |
| Documentation | Swagger/OpenAPI | Auto-generated API docs |
| CI/CD | GitHub Actions (optional) | Automated testing & deployment |

---

## 📅 PHASE BREAKDOWN

### PHASE 1: PROJECT SETUP & INFRASTRUCTURE (0.5 days)

#### 1.1 Repository & Development Environment
- [ ] Create GitHub repository (or local git repo)
- [ ] Clone repo to local machine
- [ ] Create `.gitignore` (Java/Maven/IDE patterns)
- [ ] Create standard folder structure
- [ ] Initialize Maven project with pom.xml

**Deliverable**: Clean git repo with correct structure
```
game-doan-so/
├── .git/
├── .gitignore
├── pom.xml
├── README.md
├── src/
│   ├── main/java/com/game/guess/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   ├── test/java/...
│   └── main/resources/
│       ├── application.yml
│       └── application-test.yml
└── docs/
    ├── SRS.md
    ├── ARCHITECTURE.md
    ├── API_CONTRACT.md
    └── ADR/
```

#### 1.2 Dependencies Setup (pom.xml)
Add dependencies:
```xml
<!-- Spring Boot -->
<spring-boot-starter-web>
<spring-boot-starter-data-jpa>
<spring-boot-starter-security>
<spring-boot-starter-redis>

<!-- Database -->
<mysql-connector-java>
<h2> <!-- For dev/test -->
<postgresql>

<!-- JWT -->
<jjwt>

<!-- Password -->
<spring-security-crypto> <!-- For BCrypt -->

<!-- Testing -->
<spring-boot-starter-test>
<testcontainers>
<testcontainers-mysql>
<testcontainers-postgresql>

<!-- API Docs -->
<springdoc-openapi-starter-webmvc-ui>

<!-- Logging -->
<logback>
```

**Deliverable**: pom.xml with all dependencies, builds successfully

#### 1.3 Application Configuration
Create configuration files:
- `application.yml` (common config)
- `application-dev.yml` (H2 in-memory DB)
- `application-test.yml` (Testcontainers)
- `application-prod.yml` (MySQL + Redis)

**Deliverable**: App starts without errors in dev mode

#### 1.4 Local Database Setup
- [ ] Install MySQL 8 (or PostgreSQL)
- [ ] Create database: `gamedoannso`
- [ ] Create `flyway/` or `liquibase/` migration folder
- [ ] Write initial schema migration (V1__initial_schema.sql)

**Deliverable**: `flyway/V1__initial_schema.sql` with tables: users, game_log

#### 1.5 Redis Setup (Local)
- [ ] Install Redis locally (or use Docker)
- [ ] Verify Redis connection
- [ ] Create `RedisConfig` Spring bean

**Deliverable**: Redis connection test passes

**Time**: 4 hours | **Owner**: Dev | **Quality Gate**: Build passes, DB accessible

---

### PHASE 2: DOMAIN LAYER & DATA MODEL (0.5 days)

#### 2.1 Database Schema Creation
Write initial migration: `V1__initial_schema.sql`

```sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  passwordHash VARCHAR(255) NOT NULL,
  score INT DEFAULT 0 NOT NULL CHECK(score >= 0),
  turns INT DEFAULT 0 NOT NULL CHECK(turns >= 0),
  consecutiveLosses INT DEFAULT 0,
  createdAt TIMESTAMP DEFAULT NOW(),
  version LONG DEFAULT 0
);

CREATE TABLE game_log (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  guess INT NOT NULL,
  serverNumber INT NOT NULL,
  outcome ENUM('WIN', 'LOSE') NOT NULL,
  turns_before INT NOT NULL,
  score_before INT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_created (user_id, created_at)
);

CREATE INDEX idx_username ON users(username);
```

**Deliverable**: Schema created, migrations runnable

#### 2.2 Domain Entities & Value Objects
Create in `domain/model/`:
- `User.java` — Core domain entity
- `GuessResult.java` — Immutable value object
- `WinRatePolicy.java` — Interface for win rate logic
- `TurnsWallet.java` — Value object for turns

**Key Rules**:
- Domain entities have NO Spring/JPA annotations
- All invariants enforced (turns >= 0, score >= 0)
- Immutable value objects

**Example** (User.java):
```java
public class User {
  private Long id;
  private String username;
  private String passwordHash;
  private Integer score;
  private Integer turns;
  
  // Invariants
  public void decrementTurns() {
    if (turns <= 0) throw new InsufficientTurnsException();
    turns--;
  }
  
  public void incrementScore() {
    score++;
  }
}
```

**Deliverable**: Clean domain entities, all tests pass

#### 2.3 Repository Interfaces
Create in `domain/repository/`:
- `IUserRepository.java`
- `ILeaderboardCache.java`
- `IGameLogRepository.java`

**Key**: Interfaces only, no implementations in domain layer

**Deliverable**: Interfaces defined, clean contract

**Time**: 4 hours | **Owner**: Dev | **Quality Gate**: Compiles, domain model valid

---

### PHASE 3: APPLICATION LAYER (0.75 days)

#### 3.1 Use Cases — Authentication
Create in `application/auth/`:
- `RegisterUseCase.java`
  - Validates username (3-50 chars, unique)
  - Validates password (min 8 chars)
  - Hashes with BCrypt (strength 12)
  - Saves user
  - Returns DTO (id, username, score, turns) — NO password
  
- `LoginUseCase.java`
  - Validates credentials
  - Generates JWT token (exp 1 hour)
  - Returns user DTO
  - Caller (SecurityConfig) sets HttpOnly cookie

**Deliverable**: RegisterUseCase + LoginUseCase with unit tests (80% coverage)

#### 3.2 Use Cases — Game
Create in `application/game/`:
- `GuessUseCase.java` (MOST CRITICAL)
  - Atomic conditional UPDATE: `UPDATE users SET turns = turns - 1 WHERE id = :id AND turns > 0`
  - Check affectedRows == 0 → 403 Forbidden
  - Inject WinRatePolicy, determine outcome
  - If WIN: update score + leaderboard cache (ZINCRBY)
  - Log to game_log table
  - Return GuessResultDTO
  
- `BuyTurnsUseCase.java`
  - Add 5 turns to user
  - Atomic UPDATE
  - Return updated turns

**Deliverable**: GuessUseCase with full concurrency testing

#### 3.3 Use Cases — User
Create in `application/user/`:
- `GetProfileUseCase.java` — Read from cache (10s TTL) or DB
- `GetLeaderboardUseCase.java` — Read from Redis ZSET (top 10)

**Deliverable**: All use cases with unit tests

#### 3.4 Application Services (DI Wiring)
Create `ApplicationServiceConfig.java`:
- Wire all use cases
- Inject repositories
- Inject caches

**Deliverable**: Spring context starts without errors

**Time**: 6 hours | **Owner**: Dev | **Quality Gate**: All use cases tested, 70%+ coverage

---

### PHASE 4: INFRASTRUCTURE LAYER (0.75 days)

#### 4.1 JPA Repositories & Entities
Create in `infrastructure/persistence/`:
- `UserJpaEntity.java` (JPA mapping of domain User)
- `GameLogJpaEntity.java`
- `UserJpaRepository.java` (extends JpaRepository)
- `GameLogJpaRepository.java`

**Custom Queries**:
```java
@Query("UPDATE UserJpaEntity u SET u.turns = u.turns - 1 "
       + "WHERE u.id = :id AND u.turns > 0")
int decrementTurnsIfAvailable(@Param("id") Long id);
```

**Deliverable**: JPA entities mapped correctly, queries tested

#### 4.2 Redis Cache Implementation
Create in `infrastructure/cache/`:
- `RedisLeaderboardCache.java`
  - `getTop10()` → ZREVRANGE
  - `incrementScore(username, delta)` → ZINCRBY
  
- `RedisUserProfileCache.java`
  - `get(userId)` → Cache-Aside pattern
  - `evict(userId)` → DEL

**Deliverable**: Redis operations tested with embedded Redis

#### 4.3 Security Implementation
Create in `infrastructure/security/`:
- `JwtProvider.java`
  - Generate token (HS256, exp 1 hour)
  - Validate token signature & expiry
  - Extract claims
  
- `PasswordEncoder.java`
  - Use BCryptPasswordEncoder (strength 12)
  
- `CookieUtil.java`
  - Create HttpOnly cookie (Secure, SameSite=Strict)
  - Extract JWT from cookie
  
- `SecurityConfig.java`
  - Configure Spring Security
  - Setup JWT filter
  - Enable CORS (if needed)
  
- `JwtFilter.java` (extends OncePerRequestFilter)
  - Extract JWT from HttpOnly cookie
  - Validate
  - Set SecurityContext

**Deliverable**: Security chain configured & tested

#### 4.4 Win Rate Policy Implementation
Create in `infrastructure/winrate/`:
- `ControlledWinRatePolicy.java` implements `WinRatePolicy`
  - 5% base probability
  - Soft cap: if consecutiveLosses >= 40, boost to 10%
  - Use ThreadLocalRandom for thread safety

**Deliverable**: Win rate logic tested (statistical validation)

**Time**: 6 hours | **Owner**: Dev | **Quality Gate**: Infrastructure tests pass

---

### PHASE 5: PRESENTATION LAYER & API (0.5 days)

#### 5.1 REST Controllers
Create in `presentation/controller/`:
- `AuthController.java`
  - POST /api/v1/auth/register
  - POST /api/v1/auth/login
  
- `GameController.java`
  - POST /api/v1/game/guess
  - POST /api/v1/game/buy-turns
  - GET /api/v1/game/leaderboard
  
- `UserController.java`
  - GET /api/v1/user/me

#### 5.2 DTOs & Validation
Create in `presentation/dto/`:
- `RegisterRequest.java` (@Valid, @NotNull, @Size)
- `LoginRequest.java`
- `GuessRequest.java`
- `GuessResponse.java`
- `UserProfileResponse.java`
- `LeaderboardResponse.java`

**Deliverable**: All endpoints functional

#### 5.3 Exception Handling
Create in `presentation/exception/`:
- `GlobalExceptionHandler.java` (@ControllerAdvice)
  - InsufficientTurnsException → 403
  - InvalidCredentialsException → 401
  - UserAlreadyExistsException → 409
  - ValidationException → 400

**Deliverable**: Error responses standardized

#### 5.4 API Documentation
- Add Swagger/OpenAPI annotations to controllers
- Auto-generate API docs at `/swagger-ui.html`

**Deliverable**: API docs accessible

**Time**: 4 hours | **Owner**: Dev | **Quality Gate**: All endpoints tested manually

---

### PHASE 6: INTEGRATION & CONCURRENCY TESTING (0.75 days)

#### 6.1 Integration Tests
Create in `test/java/com/game/guess/`:
- `AuthIntegrationTest.java`
  - Register → Login → Token in HttpOnly cookie
  - Invalid credentials → 401
  
- `GameIntegrationTest.java`
  - Happy path: guess with valid turns
  - Edge case: turn depletion
  - Edge case: concurrent guesses (ThreadPoolExecutor)
  
- `LeaderboardIntegrationTest.java`
  - Multiple users play, leaderboard updates

**Tools**: Testcontainers (MySQL + Redis), MockMvc

**Deliverable**: 15+ integration tests, all passing

#### 6.2 Concurrency Stress Test
Write test that simulates:
- 3 concurrent threads guessing simultaneously
- Verify exactly 3 turns deducted (no race condition)
- Verify no negative turns

**Deliverable**: Concurrency test passes, proves atomic UPDATE works

#### 6.3 Performance Testing
- Load test /guess endpoint: verify p95 < 150ms
- Load test /leaderboard: verify p95 < 30ms
- Use Apache JMeter or simple load test script

**Deliverable**: Performance baseline established

#### 6.4 Security Testing Checklist
- [ ] Verify JWT cannot be read from JavaScript (HttpOnly)
- [ ] Verify password never returned in response
- [ ] Verify rate limiting on /auth endpoints (Bucket4j)
- [ ] Verify CSRF protection (SameSite cookie)
- [ ] Verify no SQL injection in queries
- [ ] Verify no hardcoded secrets

**Deliverable**: Security checklist completed

**Time**: 6 hours | **Owner**: Dev + QA | **Quality Gate**: 70%+ test coverage, concurrency proven safe

---

### PHASE 7: DOCUMENTATION & ADRs (0.5 days)

#### 7.1 Architecture Decision Records (ADRs)
Create `docs/ADR/`:
- `ADR-001_ControlledWinRate.md` — Justifies 5% + soft cap algorithm
- `ADR-002_AtomicConditionalUpdate.md` — Concurrency strategy
- `ADR-003_HttpOnlyCookie.md` — JWT storage security
- `ADR-004_RedisZSet.md` — Leaderboard caching design

**Deliverable**: 4 ADRs documented

#### 7.2 API Contract Document
Create `docs/API_CONTRACT.md`:
- All 6 endpoints documented
- Request/response examples
- Error codes & meanings
- Rate limiting rules

**Deliverable**: API contract complete

#### 7.3 Deployment Guide
Create `docs/DEPLOYMENT.md`:
- Dev setup (H2 in-memory)
- Test setup (Testcontainers)
- Production setup (MySQL + Redis)
- Environment variables
- Health check endpoints

**Deliverable**: Deployment guide runnable

#### 7.4 README.md
- Project overview
- Quick start (5 minutes)
- Tech stack
- Architecture summary
- Link to docs/

**Deliverable**: README complete

**Time**: 4 hours | **Owner**: Dev + Tech Lead | **Quality Gate**: All docs reviewed

---

### PHASE 8: TESTING & QA (0.75 days)

#### 8.1 Final Integration Testing
- [ ] All 6 FRs implemented & working
- [ ] Happy path for each FR
- [ ] Error cases for each FR
- [ ] Concurrent load simulation

#### 8.2 Security Audit Checklist
- [ ] OWASP Top 10 reviewed
  - A01: Broken Access Control ✓ (JWT auth)
  - A02: Cryptographic Failures ✓ (HTTPS, BCrypt, HttpOnly)
  - A03: Injection ✓ (Parameterized queries)
  - A04: Insecure Design ✓ (Atomic operations)
  - A05: Security Misconfiguration ✓ (No hardcoded secrets)
  - A07: Identification & Authentication ✓ (JWT + password hashing)

#### 8.3 Code Quality Audit
- [ ] SonarQube / code review: 0 critical issues
- [ ] Test coverage >= 70%
- [ ] No hardcoded secrets
- [ ] Clean Architecture boundaries respected
- [ ] Domain layer has zero framework dependency

#### 8.4 Performance Benchmarks
| Endpoint | Baseline | Target | Status |
|----------|----------|--------|--------|
| POST /guess | ? | < 150ms p95 | Test |
| GET /leaderboard | ? | < 30ms p95 | Test |
| POST /register | ? | < 200ms p95 | Test |

**Deliverable**: All benchmarks within SLA

**Time**: 6 hours | **Owner**: QA + Dev | **Quality Gate**: All tests pass, all metrics met

---

### PHASE 9: DEPLOYMENT & RELEASE (0.5 days)

#### 9.1 Build & Package
- [ ] Create Docker image (optional but recommended)
- [ ] Generate JAR: `mvn clean package`
- [ ] Verify JAR runs: `java -jar game-doan-so.jar`

#### 9.2 Environment Setup
- [ ] Prod MySQL database created
- [ ] Prod Redis instance running
- [ ] Environment variables configured (`.env` or K8s secrets)
- [ ] Health check endpoint working

#### 9.3 Deployment Steps
```bash
# Build
mvn clean package -DskipTests

# Deploy (example)
java -jar target/game-doan-so.jar \
  --spring.profiles.active=prod \
  --spring.datasource.url=jdbc:mysql://prod-db:3306/gamedoannso
```

#### 9.4 Smoke Tests (Post-deployment)
- [ ] Health check: GET /actuator/health → UP
- [ ] Register & login: Works
- [ ] Guess endpoint: Works
- [ ] Leaderboard: Returns top 10
- [ ] Monitoring: Logs flowing

#### 9.5 Rollback Plan
If critical issue found:
- [ ] Revert to previous version
- [ ] Restore database from backup
- [ ] Clear Redis cache (manual or script)
- [ ] Verify service recovered

**Deliverable**: Service running in production

**Time**: 4 hours | **Owner**: DevOps + Dev | **Quality Gate**: Smoke tests pass

---

### PHASE 10: MONITORING & MAINTENANCE (Ongoing)

#### 10.1 Monitoring Setup
- [ ] Application logs (Logback, ELK or CloudWatch)
- [ ] Metrics (Prometheus or New Relic)
- [ ] Alerts (p95 latency > 500ms, error rate > 1%)
- [ ] Dashboards (Grafana)

#### 10.2 Incident Response
- [ ] Runbook for common issues
- [ ] On-call rotation (if applicable)
- [ ] Postmortem template for incidents

#### 10.3 Future Roadmap
- RFC-001: Payment gateway integration (VNPAY/MOMO)
- ADR-XXX: Multi-player game mode
- ADR-XXX: OAuth2 social login

**Deliverable**: Monitoring configured, team trained

---

## 📊 CONSOLIDATED TIMELINE

### Aggressive Schedule (2.5 days)
```
Day 1 Morning
├── Phase 1: Setup (2h)
├── Phase 2: Domain Model (2h)
└── Phase 3: Application Layer (2h)

Day 1 Afternoon
├── Phase 4: Infrastructure (3h)
├── Phase 5: Controllers (2h)
└── Phase 6: Integration Tests (1h)

Day 2 Morning
├── Phase 6: Concurrency Tests (2h)
├── Phase 7: Documentation (2h)
└── Phase 8: QA (1h)

Day 2 Afternoon
├── Phase 8: Final Testing (2h)
├── Phase 9: Deployment (2h)
└── Release! 🚀
```

### Recommended Schedule (4-5 days)
```
Day 1: Setup + Domain Model (6h)
Day 2: Application + Infrastructure (8h)
Day 3: Controllers + Tests (8h)
Day 4: Integration Testing + Documentation (8h)
Day 5: QA + Deployment (4h)
```

---

## ✅ QUALITY GATES (Release Criteria)

### Code Quality
- [ ] Test coverage >= 70%
- [ ] 0 critical SonarQube issues
- [ ] All ADRs documented
- [ ] Clean Architecture verified (domain layer isolation)

### Functional
- [ ] All 6 FRs implemented & tested
- [ ] Happy path + error cases for each
- [ ] Concurrent stress test passes
- [ ] No negative turns, no race conditions

### Security
- [ ] BCrypt hashing verified
- [ ] JWT HttpOnly cookie verified
- [ ] Rate limiting tested
- [ ] No hardcoded secrets
- [ ] OWASP Top 10 checklist passed

### Performance
- [ ] p95(/guess) < 150ms
- [ ] p95(/leaderboard) < 30ms
- [ ] Load test: 100 req/sec sustained

### Deployment
- [ ] Docker image builds
- [ ] Health checks passing
- [ ] Smoke tests pass
- [ ] Rollback tested

---

## 👥 TEAM ROLES & RESPONSIBILITIES

| Role | Responsibility | Hours |
|------|-----------------|-------|
| **Lead Developer** | Architecture, Core logic, Code review | 24 |
| **Backend Dev** | Controllers, Tests, Infrastructure | 16 |
| **QA Engineer** | Integration tests, Performance testing, Security audit | 12 |
| **DevOps** | Docker, Deployment, Monitoring (optional) | 4 |
| **Tech Lead** | ADRs, Architecture review, Release decision | 8 |
| **TOTAL** | - | **64 hours** (for 4-5 day timeline with 2 devs) |

---

## 🚀 DEPLOYMENT STRATEGY

### Dev Environment
- H2 in-memory database
- No Redis (optional)
- Runs locally on `localhost:8080`

### Test Environment
- Testcontainers MySQL
- Testcontainers Redis
- All tests automated

### Production Environment
- Managed MySQL (AWS RDS or similar)
- Managed Redis (AWS ElastiCache or similar)
- Docker image deployed to:
  - AWS ECS / EC2
  - Kubernetes
  - DigitalOcean App Platform
  - or simple VPS (Java + jar)

### Scaling (Future)
- Horizontal: Load balancer + multiple instances
- Database: Read replicas for leaderboard queries
- Cache: Redis Sentinel for HA

---

## 📋 CHECKLIST — READY FOR PRODUCTION

**Before Release Approval**:
- [ ] All phases completed
- [ ] All quality gates passed
- [ ] Security audit signed off
- [ ] Performance tested & within SLA
- [ ] Deployment tested in staging
- [ ] Rollback procedure tested
- [ ] Monitoring configured
- [ ] Runbook written
- [ ] Team trained
- [ ] Go/No-Go decision made by Tech Lead

---

## 🎓 LESSONS LEARNED & CONTINUOUS IMPROVEMENT

### After Release
- Collect metrics on actual performance vs. projections
- Document any unexpected challenges
- Update runbooks based on real incidents
- Plan improvements based on user feedback

### Version 1.1 Roadmap
- [ ] Multi-round game modes
- [ ] Social features (friends leaderboard)
- [ ] Advanced analytics dashboard
- [ ] Admin panel

---

## 📞 SUPPORT & ESCALATION

### During Development
- **Blocker**: Escalate to Tech Lead immediately
- **Question**: Post in tech discussion channel
- **Code Review**: Use GitHub PR process
- **Performance Issue**: Run profiler, investigate root cause

### Issues
Use GitHub Issues template:
```
Title: [FEAT/BUG/INFRA] Short description
Description:
- What happened?
- Expected behavior?
- Actual behavior?
- Steps to reproduce?
- Environment (dev/test/prod)?
```

---

## 📎 APPENDIX

### A. Git Workflow
```bash
# Setup
git clone <repo>
cd game-doan-so
git checkout -b feature/core-auth

# Commit (following framework standards)
git add src/...
git commit -m "feat(auth): implement register endpoint

Actions:
- Add RegisterUseCase with BCrypt hashing
- Add validation for username uniqueness
- Add unit tests (80% coverage)

Whys:
- Enforces Clean Architecture (business logic in domain layer)
- Prevents security vulnerabilities (no plaintext passwords)
- Atomic operation: username unique constraint at DB level

Notes / Impact:
- Breaking: None (new endpoint)
- Next: Implement login endpoint
- Related: ADR-003"

# Push & PR
git push origin feature/core-auth
# Create PR on GitHub with checklist
```

### B. Docker Setup (Optional but Recommended)
```dockerfile
FROM openjdk:17-slim
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
EXPOSE 8080
```

### C. Sample Environment Variables
```env
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/gamedoannso
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=password
SPRING_REDIS_HOST=localhost
SPRING_REDIS_PORT=6379
JWT_SECRET=your-secret-key-min-32-chars-long
JWT_EXPIRATION=3600000
BCRYPT_STRENGTH=12
RATE_LIMIT_MAX_ATTEMPTS=5
RATE_LIMIT_WINDOW_MINUTES=1
```

### D. Monitoring Queries (Prometheus/Grafana)
```promql
# Latency (p95)
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Throughput
rate(http_requests_total[5m])
```

---

**Document Version**: 1.0  
**Last Updated**: May 7, 2026  
**Status**: ✅ READY TO EXECUTE  

---

**Next Steps**: Print this plan, assign tasks, start Phase 1! 🚀
