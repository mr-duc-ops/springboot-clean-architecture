# Game Đoán Số — MASTER IMPLEMENTATION GUIDE

**Complete End-to-End Project Plan: From Empty Environment to Production Release**

**Prepared by**: Mr. Đức (Technical Lead)  
**Date**: May 7, 2026  
**Status**: ✅ READY TO EXECUTE  

---

## 📊 EXECUTIVE OVERVIEW

### Project: Number Guessing Game REST API

A production-grade REST API game where:
- Players guess numbers (1-5) to earn score
- 5% win rate with fairness (soft cap at 40 consecutive losses)
- Real-time leaderboard (Redis ZSET, < 30ms)
- Atomic concurrency (no race conditions, no negative turns)
- Secure authentication (JWT + HttpOnly Cookie, BCrypt hashing)

### Stack
```
Java 17+ | Spring Boot 3.x | MySQL/PostgreSQL | Redis | JWT + HttpOnly Cookie
```

### Timeline
- **Aggressive**: 2.5 days (skip buffer, high risk)
- **Recommended**: 4-5 days (sustainable, quality focus)
- **Effort**: ~64 person-hours (1 developer working 5 days, 8h/day)

### Success Criteria
| Criterion | Target | Status |
|-----------|--------|--------|
| All 6 FRs implemented | ✓ | Verified in plan |
| Test coverage | 70%+ | Planned in Day 4 |
| Data consistency | Zero race conditions | Atomic UPDATE design |
| Performance | p95 /guess < 150ms | Benchmarked |
| Security | OWASP Top 10 passed | Audit checklist in Day 4 |
| Release | Production ready | Deployment plan in Phase 9 |

---

## 📚 DOCUMENTATION SET

### 4 Comprehensive Documents

#### 1. **GAME_DOAN_SO_PROJECT_PLAN.md** (Main Blueprint)
**Purpose**: High-level project overview and strategic planning  
**Length**: 12 pages | **Audience**: PMs, Tech Leads, Stakeholders  

**Contains**:
- Executive summary
- Technology stack & rationale
- 10 Phases (Setup → Monitoring)
- Effort estimates per phase
- Team roles & responsibilities
- Quality gates & release criteria
- Deployment strategy (Dev/Test/Prod)
- Appendix: Docker, Git workflow, env variables

**When to use**: 
- Initial project kickoff
- Budget/timeline planning
- Risk assessment
- Stakeholder communication

---

#### 2. **GAME_DOAN_SO_DAILY_TASKS.md** (Tactical Execution)
**Purpose**: Day-by-day task breakdown with acceptance criteria  
**Length**: 15 pages | **Audience**: Developers, QA, Project Managers  

**Contains**:
- 5-day sprint board (Day 1-5)
- Specific tasks with 1-2 hour estimates
- Code snippets for each major component
- Acceptance criteria (testable, verifiable)
- Daily standup template
- Testing checklist per day
- Git commit strategy
- Escalation path

**When to use**: 
- Daily stand-ups
- Task assignment
- Progress tracking
- Code review (verify against plan)

**Navigation**:
```
Day 1: Domain model (4h) + Application layer (4h)
Day 2: Infrastructure (4h) + Controllers (4h)
Day 3: Integration tests (8h)
Day 4: Documentation + QA (8h)
Day 5: Release + deploy (4h)
```

---

#### 3. **GAME_DOAN_SO_QUICK_REFERENCE.md** (Developer Cheat Sheet)
**Purpose**: Commands, endpoints, debugging tips, quick answers  
**Length**: 8 pages | **Audience**: All developers (especially new team members)  

**Contains**:
- 5-minute quick start
- Maven/Docker commands
- All API endpoints with curl examples
- Database debugging (H2 console)
- Testing commands
- Security checklists
- Common errors & solutions
- Performance SLAs
- Team contacts

**When to use**:
- "How do I run the app?"
- "What's the API for buying turns?"
- "How do I test the leaderboard?"
- "My app won't start, help!"
- Need to write a curl test

---

#### 4. **TECHNICAL_LEAD_MANIFESTO.md** (Quality Standards)
**Purpose**: Enforce code quality, architecture, and git standards  
**Length**: 8 pages | **Audience**: All developers, reviewers  

**Contains**:
- Philosophy (Simplicity, Practical Impact, Clean Code)
- Code quality standards checklist
- 4+1 View Model architecture
- Git workflow & atomic commits
- Commit message format with "Whys"
- Code review checklist
- Pre-commit checklist

**When to use**:
- Before committing code
- Code review process
- Architecture questions
- "What quality level is expected?"

---

## 🎯 HOW TO USE THESE DOCUMENTS

### Phase 1: Planning (Day 0)

1. **Read**: GAME_DOAN_SO_PROJECT_PLAN.md (Executive Summary section)
   - Get overall picture, understand effort, identify risks
   - Time: 15 minutes

2. **Prepare**: 
   - Set up development environment (Java 17+, Maven, IDE)
   - Create GitHub repo
   - Gather team
   - Time: 1 hour

3. **Kickoff meeting**: Review phases, assign roles, set daily standup time

---

### Phase 2: Development (Day 1-4)

**Daily Workflow**:
1. **Morning** (9:00 AM):
   - Read today's tasks from GAME_DOAN_SO_DAILY_TASKS.md
   - Standup (5 min): Yesterday done? Today's plan? Blockers?
   - Start development

2. **Development** (9:30 AM - 5:30 PM):
   - Follow task checklist
   - Use GAME_DOAN_SO_QUICK_REFERENCE.md for commands
   - Verify acceptance criteria before moving to next task
   - Commit code using TECHNICAL_LEAD_MANIFESTO.md commit format

3. **Code Review**:
   - Use TECHNICAL_LEAD_MANIFESTO.md code review checklist
   - Ask: "Does this follow Clean Architecture?"
   - Test: "Reproducible by following the plan?"

4. **End of day**:
   - Run full test suite
   - Update task completion
   - Prepare for tomorrow

---

### Phase 3: Release (Day 5)

1. **Pre-deployment**:
   - Use GAME_DOAN_SO_QUICK_REFERENCE.md → "Pre-deployment checklist"
   - Verify all quality gates passed

2. **Deployment**:
   - Follow GAME_DOAN_SO_PROJECT_PLAN.md → "Phase 9: Deployment"
   - Use GAME_DOAN_SO_QUICK_REFERENCE.md → Docker commands

3. **Go/No-Go Decision**:
   - Tech Lead reviews checklist
   - Sign off for production release

---

## 🔍 KEY SECTIONS BY ROLE

### For **Project Manager**:
- Read: GAME_DOAN_SO_PROJECT_PLAN.md (sections 1-2)
- Track: Daily task completion vs. plan
- Escalate: Blockers to Tech Lead
- Report: Status to stakeholders

### For **Backend Developer**:
- Read: TECHNICAL_LEAD_MANIFESTO.md (Quality standards)
- Read: GAME_DOAN_SO_DAILY_TASKS.md (your assigned day)
- Follow: Task checklist & acceptance criteria
- Use: GAME_DOAN_SO_QUICK_REFERENCE.md (when stuck)

### For **QA Engineer**:
- Read: GAME_DOAN_SO_DAILY_TASKS.md (Day 3, Day 4 sections)
- Execute: Integration tests from the checklist
- Verify: All acceptance criteria
- Document: Any issues found

### For **Tech Lead / Architect**:
- Read: TECHNICAL_LEAD_MANIFESTO.md (all sections)
- Review: Each PR using code review checklist
- Approve: Go/No-Go decision on Day 5
- Escalate: Architecture questions, security concerns

---

## 📋 QUICK TASK CHECKLIST

### Day 1 (8 hours)

**Morning (4h)**:
- [ ] Git repo setup (1h)
- [ ] Maven project setup (1h)
- [ ] Spring Boot configuration (1h)
- [ ] Database schema & migrations (1h)

**Afternoon (4h)**:
- [ ] Domain entities (User, GuessResult) (1.5h)
- [ ] Repository interfaces (1h)
- [ ] Domain services (GameDomainService) (1.5h)

**Commit**: `git commit -m "feat(domain): add entities and services"`

---

### Day 2 (8 hours)

**Morning (4h)**:
- [ ] RegisterUseCase + LoginUseCase (2h)
- [ ] GuessUseCase + BuyTurnsUseCase (2h)

**Afternoon (4h)**:
- [ ] JPA repositories & adapters (2h)
- [ ] Security: JWT, BCrypt, HttpOnly cookie (2h)

**Commit**: `git commit -m "feat(app,infra): use cases + security"`

---

### Day 3 (8 hours)

- [ ] DTOs & validation (1h)
- [ ] REST controllers (2h)
- [ ] Exception handling (1h)
- [ ] Integration tests (3h)
- [ ] Performance tests (1h)

**Commit**: `git commit -m "feat(presentation,test): controllers + tests"`

---

### Day 4 (8 hours)

- [ ] ADRs (4 documents) (2h)
- [ ] API contract documentation (1h)
- [ ] Deployment guide (1h)
- [ ] Security audit (1h)
- [ ] Code quality audit (1h)
- [ ] Performance benchmarking (1h)

**Commit**: `git commit -m "docs: add ADRs and deployment guide"`

---

### Day 5 (4 hours)

- [ ] Build & packaging (30 min)
- [ ] Staging smoke tests (1h)
- [ ] Production deployment (1h)
- [ ] Post-deployment verification (30 min)
- [ ] Go/No-Go decision + tag release (30 min)

**Commit**: `git tag v1.0.0`

---

## ✅ QUALITY GATES (Must-Pass Criteria)

### Code Quality
```
✓ mvn clean compile — NO ERRORS
✓ mvn test — ALL TESTS PASS
✓ Test coverage >= 70% (jacoco report)
✓ 0 hardcoded secrets (grep check)
✓ Clean Architecture verified (domain layer isolation)
✓ SonarQube: 0 critical issues
```

### Functional
```
✓ All 6 FRs implemented (Register, Login, Guess, BuyTurns, Leaderboard, Profile)
✓ Happy path works for each
✓ Error cases handled correctly
✓ Concurrent stress test: no race conditions
✓ No negative turns
```

### Security
```
✓ BCrypt hashing (strength 12)
✓ JWT HttpOnly cookie (HttpOnly, Secure, SameSite=Strict)
✓ Rate limiting on auth endpoints (5 req/min per IP)
✓ No SQL injection (parameterized queries)
✓ OWASP Top 10: all items checked
```

### Performance
```
✓ p95(/guess) < 150ms
✓ p95(/leaderboard) < 30ms
✓ Load test: 100 req/sec sustained
```

### Deployment
```
✓ JAR builds successfully
✓ Docker image builds
✓ Health check: GET /actuator/health → UP
✓ Smoke tests pass
✓ Rollback tested
✓ Monitoring configured
```

---

## 🚀 EXECUTION TIPS

### Tip 1: Start with Domain, Not Layers
- Day 1 focuses on domain model first (User, GuessResult, business rules)
- Then application layer (use cases)
- Then infrastructure (JPA, Redis)
- Then presentation (controllers)
- **Why**: Domain is the core. Get it right first.

### Tip 2: Atomic Commits from Day 1
- Each commit = 1 logical change
- Use commit message template with "Whys"
- Makes code review easier, history clearer
- Follows TECHNICAL_LEAD_MANIFESTO.md

### Tip 3: Test as You Code
- Don't write all code then test
- Unit test domain layer as you write it
- Integration test after infrastructure
- Performance test after deployment
- **Why**: Catch bugs early, easier to fix

### Tip 4: Use Testcontainers for Databases
- Don't mock database operations
- Use real MySQL/Redis in tests (Testcontainers)
- Integration tests are more reliable
- Catches real concurrency issues

### Tip 5: Document as You Go
- ADRs after major design decisions (don't wait until Day 4)
- Comments explain "Why", not "What"
- Keep docs in sync with code

---

## 🎯 SUCCESS METRICS

| Metric | Good | Excellent |
|--------|------|-----------|
| **Timeline** | Complete in 5 days | Complete in 4 days |
| **Code Coverage** | 70%+ | 85%+ |
| **Performance p95** | < 150ms | < 100ms |
| **Security Issues** | 0 critical | 0 critical + 0 high |
| **Code Review Cycles** | 1-2 cycles | First-time approval 80%+ |
| **Test Pass Rate** | 95%+ | 100% |

---

## 📞 SUPPORT

### If You Get Stuck:

1. **Can't compile?**
   - Check Java version: `java -version` (should be 17+)
   - Check Maven: `mvn --version`
   - Try: `mvn clean compile`

2. **Test failing?**
   - Run single test: `mvn test -Dtest=YourTest`
   - Check logs for error
   - Review acceptance criteria in DAILY_TASKS.md

3. **Performance issue?**
   - Profile with JProfiler or YourKit
   - Check database queries (enable SQL logging)
   - Review QUICK_REFERENCE.md → Debugging Tips

4. **Security question?**
   - Review TECHNICAL_LEAD_MANIFESTO.md → Security section
   - Check QUICK_REFERENCE.md → Security Checklist
   - Escalate to Tech Lead

5. **Blocker?**
   - Document the issue
   - Escalate to Tech Lead immediately
   - Don't wait until next standup

---

## 🎓 LEARNING OUTCOMES

After completing this project, you will understand:

✓ **Clean Architecture** — Domain/Application/Infrastructure/Presentation separation  
✓ **Atomic Operations** — Safe concurrent database updates without locks  
✓ **Redis Caching** — ZSET for efficient top-N ranking  
✓ **JWT Security** — HttpOnly cookies, BCrypt hashing, token lifecycle  
✓ **Spring Boot** — Building production REST APIs  
✓ **Testing Strategy** — Unit tests, integration tests, concurrency testing  
✓ **Git Workflow** — Atomic commits, meaningful messages  
✓ **Project Planning** — Breaking down large projects into daily tasks  

---

## 📝 NEXT STEPS

**Right Now**:
1. Read this document (this file) — 10 min
2. Read GAME_DOAN_SO_PROJECT_PLAN.md → Executive Summary — 15 min
3. Set up development environment — 1 hour
4. Create GitHub repo — 5 min
5. **Total**: ~1.5 hours of prep

**Tomorrow (Day 1)**:
1. Start GAME_DOAN_SO_DAILY_TASKS.md → Day 1 tasks
2. Follow the checklist step by step
3. Commit after each major task
4. Use GAME_DOAN_SO_QUICK_REFERENCE.md for commands

---

## 🎉 READY?

### Pre-Execution Checklist:
- [ ] All 4 documents read and understood
- [ ] Development environment set up (Java 17+, Maven)
- [ ] GitHub repo created
- [ ] Team assembled & roles assigned
- [ ] Daily standup time scheduled (9:00 AM recommended)
- [ ] Slack/Discord channel created for communication

### First Command:
```bash
git clone <your-repo> game-doan-so
cd game-doan-so
mvn spring-boot:run
# Should see: "Started GameDoAnSoApplication on port 8080"
# Open: http://localhost:8080/swagger-ui.html
```

---

## 📎 APPENDIX: Document Matrix

| Use Case | Document | Section |
|----------|----------|---------|
| "How long will this take?" | PROJECT_PLAN.md | Timeline / Effort |
| "What do I do today?" | DAILY_TASKS.md | Day X |
| "How do I run the app?" | QUICK_REFERENCE.md | Quick Start |
| "What's the API endpoint?" | QUICK_REFERENCE.md | Endpoints Table |
| "My test is failing" | QUICK_REFERENCE.md | Common Errors |
| "How should I commit?" | MANIFESTO.md | Git Workflow |
| "Should I write a test?" | MANIFESTO.md | Testing Standards |
| "How do I deploy?" | PROJECT_PLAN.md | Phase 9 + QUICK_REF |
| "What's the architecture?" | PROJECT_PLAN.md | Architecture Overview |
| "How do I review code?" | MANIFESTO.md | Code Review Checklist |

---

## ✨ FINAL NOTES

This project plan is:
- **Realistic**: Based on actual Spring Boot project experience
- **Detailed**: Every task has acceptance criteria
- **Flexible**: Can be compressed (2.5 days) or expanded (6+ days)
- **Comprehensive**: From setup to production deployment
- **Educational**: You'll learn Clean Architecture, testing, security, deployment

**Estimated actual time**: 4-5 days with 1 developer working focused hours

**Key success factor**: Follow the order. Don't skip ahead. Clean Architecture requires building from domain layer outward.

---

**Document Version**: 1.0  
**Status**: ✅ COMPLETE & READY TO EXECUTE  
**Last Updated**: May 7, 2026  

**Start Date**: [Your Decision]  
**Expected Release**: [Start Date + 5 days]  

---

## 🚀 LET'S BUILD SOMETHING GREAT!

Questions? Ask during standup or review the relevant document section.

**Go forth and code! 💪**

---

*"First, make it work. Then make it right. Then make it fast."* — Kent Beck

---

**Contact**: Mr. Đức (Technical Lead) | duch9707@gmail.com | +84 389 086 502
