# Manifesto
**Version 1.0** | **Owner**: Mr. Đức | **Last Updated**: May 9, 2026

---

## 🎯 Core Philosophy

### Guiding Principles
1. **Simplicity First**: Solve with the simplest effective solution. Complexity only when necessary.
2. **Practical Impact**: Technology is a tool. Prioritize real business value and user needs.
3. **Clean & Sustainable Code**: Write maintainable, scalable code that others can build upon.
4. **Reduce Misalignment**: Use 4+1 View Model to ensure all stakeholders understand the system the same way.
5. **Quality as Non-Negotiable**: Code quality, security, and performance are not optional.

---

## 📋 Code Quality Standards

### Every Coding Task Must Satisfy

#### ✅ Architecture Quality
- [ ] Follows 4+1 View Model (Scenario, Logical, Development, Process, Physical views are clear)
- [ ] Clear domain boundaries (Bounded Context per DDD)
- [ ] Clean Architecture layers (don't violate dependency rules)
- [ ] Low coupling, high cohesion
- [ ] No circular dependencies

#### ✅ Code Quality
- [ ] Consistent naming conventions (PascalCase classes, camelCase methods/variables, UPPER_SNAKE_CASE constants)
- [ ] Module responsibility is single and clear
- [ ] Max file size: 400 lines (encourage smaller, focused files)
- [ ] Functions: ≤30 lines ideally
- [ ] No god objects or utility dumping grounds
- [ ] Proper error handling with meaningful messages

#### ✅ Security
- [ ] No hardcoded secrets
- [ ] Input validation on all boundaries
- [ ] SQL injection prevention (parameterized queries)
- [ ] CORS/CSRF protection where applicable
- [ ] Authentication & authorization properly separated
- [ ] Follow OWASP Top 10 principles

#### ✅ Performance
- [ ] Database queries optimized (no N+1 problems)
- [ ] Caching strategy considered
- [ ] API response time target: p95 < 500ms (adjust per domain)
- [ ] No unnecessary loops or repeated computations
- [ ] Proper indexing for database queries

#### ✅ Testing
- [ ] Unit tests for business logic (minimum 70% coverage)
- [ ] Integration tests for contracts
- [ ] Regression tests for critical paths
- [ ] Happy path + error path coverage
- [ ] All tests pass before merge

#### ✅ Documentation
- [ ] README with setup instructions
- [ ] Architecture decisions documented (ADR)
- [ ] Complex logic has inline comments explaining "why"
- [ ] API endpoints documented (OpenAPI/Swagger preferred)
- [ ] Deployment runbook available

#### ✅ Git & Commits
- [ ] Branch naming follows convention: `feature/`, `fix/`, `refactor/`, `docs/`, `test/`, `chore/`
- [ ] Atomic commits (one logical change per commit)
- [ ] Commit messages follow format: `<type>(<scope>): <description>` + Actions + Whys + Notes
- [ ] No "fix typo" or "wip" commits on main branch

#### ✅ Code Review
- [ ] Self-review before requesting review
- [ ] Review checklist completed
- [ ] Addressed all feedback before merge
- [ ] At least 1 approval (2 for critical path)

---

## 🏗️ Architecture Approach

### 4+1 View Model (MANDATORY for significant changes)

Every substantial feature/system must be designed across 5 views:

1. **Scenario View** → Business use cases, user journeys
2. **Logical View** → Domain model, Bounded Contexts, Business rules
3. **Development View** → Code structure, modules, layers
4. **Process View** → Runtime behavior, concurrency, queues, scalability
5. **Physical View** → Deployment topology, infrastructure, HA/DR

**Why**: Prevents misalignment between Product, Engineering, Ops, and Architecture teams.

### Clean Architecture Layers (REQUIRED)

```
┌─────────────────────────────────────────┐
│     Presentation / API Layer            │  (Controllers, REST endpoints)
├─────────────────────────────────────────┤
│     Application Layer                   │  (Use Cases, Orchestration)
├─────────────────────────────────────────┤
│     Domain Layer                        │  (Entities, Value Objects, Business Rules)
├─────────────────────────────────────────┤
│     Infrastructure Layer                │  (Databases, APIs, External Services)
└─────────────────────────────────────────┘
```

**Dependency Rule**: Inner layers don't know outer layers. Domain is pure business logic.

---

## 🔄 Git Workflow & Commit Standards

### Branch Naming (MANDATORY)

```
<prefix>/<scope>-<description>
```

**Prefixes**:
- `feature/` → New features
- `fix/` → Bug fixes
- `refactor/` → Code restructuring
- `test/` → Tests only
- `docs/` → Documentation
- `chore/` → Maintenance, dependencies
- `spike/` → Research/POC (never merge to main)
- `infra/` → Infrastructure, CI/CD

**Example**: `feature/multi-tenant-domain-isolation`, `fix/auth-token-expiry`, `refactor/payment-gateway-abstraction`

### Commit Message Format (MANDATORY)

```
<type>(<scope>): <strong, specific description>

Actions:
- Concrete action 1
- Concrete action 2

Whys:
- Strategic or architectural reason.
- Link to Bounded Context / Clean Architecture / Domain principle.
- Why NOT other approaches.

Notes / Impact:
- Trade-offs accepted.
- Breaking changes (if any).
- Next steps.
- Related ADR / Issue #.
```

**Example**:
```
refactor(auth): decouple Auth from global UI state management

Actions:
- Extract Login/Register components to `modules/Auth/components/`
- Move auth state to Redux slice: `modules/Auth/store/authSlice.ts`
- Create Auth Boundary Contract at `modules/Auth/types.ts`

Whys:
- Enforces Bounded Context (Clean Architecture principle).
- Prevents Product domain from directly mutating Auth state → reduces misalignment.
- Global UI layer remains purely presentational.
- Eases future integration with OAuth2/SAML.

Notes / Impact:
- Breaking: Auth exports change from `@/store/auth` → `@/modules/Auth`
- Next step: Implement API adapter to fully decouple from global Axios.
- Related: ADR-002 (Modular Monolith Boundaries)
```

### Atomic Commit Rule (MANDATORY)

- **One logical change per commit** (reversible independently).
- Use `git diff` to verify each commit contains related changes only.
- Never commit `console.logs`, debugging code, or unrelated refactors.
- Small commits = easier review, easier rollback, clearer history.

---

## 📊 ADR & RFC Process

### When to Write ADR (Architecture Decision Record)

**Write ADR for:**
- Database choice (PostgreSQL vs MongoDB)
- Microservices vs Monolith
- Auth model decision
- Multi-tenant strategy
- Cloud provider selection
- Framework or library selection (if system-wide impact)

**ADR is a record of DECISION MADE.** Template: [See ADR_TEMPLATE.md](./ADR_TEMPLATE.md)

### When to Write RFC (Request for Comments)

**Write RFC BEFORE deciding:**
- Major refactoring
- New architecture pattern
- Framework migration
- API contract change
- Security policy change
- Deployment strategy change

**RFC is a DISCUSSION space.** Template: [See RFC_TEMPLATE.md](./RFC_TEMPLATE.md)

### Workflow

1. **RFC Draft** → Propose to team
2. **RFC Review** → 5 working days for feedback
3. **RFC Decision** → Tech Lead approves or modifies
4. **ADR Created** → Records final decision
5. **Implementation** → Team executes ADR

---

## 🛡️ Code Review Checklist

**Reviewer MUST verify:**

- [ ] Code meets all quality standards above
- [ ] Follows project naming and structure conventions
- [ ] No security vulnerabilities
- [ ] Tests pass and coverage maintained
- [ ] Commit messages are clear and atomic
- [ ] No hardcoded values or credentials
- [ ] Performance impact considered
- [ ] Documentation updated
- [ ] Architecture decisions documented (if significant)
- [ ] At least one alternative was considered

**Reviewer Should Ask:**
- "Why this approach over alternatives?"
- "Will this scale to 10x usage?"
- "Can someone onboard in 1 hour?"
- "Is error handling complete?"
- "Are there edge cases missed?"

---

## 📈 SDLC Governance

### Roles & Responsibilities

| Role | Responsibilities |
|------|-------------------|
| **Technical Lead** | Architecture decisions, quality gates, mentoring, ADR/RFC approval |
| **Senior BA** | Requirement clarity, acceptance criteria, scope traceability |
| **Developer** | Implementation within standards, code quality, tests |
| **QA/Tester** | Test strategy, acceptance testing, regression verification |
| **DevOps/SRE** | Infrastructure, monitoring, deployment, incident response |

### Mandatory Reporting

For each significant task:
- [ ] Task Execution Report (status, risks, metrics)
- [ ] Daily Status (blockers, progress, next steps)
- [ ] Weekly Governance Report (portfolio KPIs)
- [ ] Release Readiness Report (before production)
- [ ] Incident Report (if applicable)

---

## 🤖 AI-Era Code Standards (2026+)

Your code will be read by **AI Agents** too. Optimize for both humans and machines:

### For AI Readability:
- [ ] Explicit > Implicit (avoid magic)
- [ ] Consistent patterns (same problem solved same way always)
- [ ] Clear contracts (typed DTOs, schemas, API specs)
- [ ] Contracts everywhere (no implicit assumptions)
- [ ] Fast feedback loops (tests, linting, CI)

### Anti-patterns to Avoid:
- ❌ Ambiguous naming
- ❌ Hidden side effects
- ❌ Module boundaries unclear
- ❌ Convention changes frequently
- ❌ No tests or weak tests
- ❌ Inconsistent error handling

---

## ✅ Pre-Commit Checklist (MANDATORY)

Before pushing, verify:

```bash
# 1. Code builds
npm run build  # or equivalent

# 2. Tests pass
npm test

# 3. Linter passes
npm run lint

# 4. No secrets in code
git diff --cached | grep -E "(password|secret|key|token)" # should be empty

# 5. Commits are atomic and messages are clear
git log --oneline origin/main..HEAD  # review last few commits

# 6. Branch name follows convention
# feature/, fix/, refactor/, test/, docs/, chore/, infra/

# 7. Self-review completed
# Does this code pass all the quality standards above?
```

---

## 🎓 Continuous Learning

- Review architecture decisions quarterly
- Participate in code reviews (reviewer + reviewee)
- Document lessons learned in ADRs
- Share knowledge with team (pair programming, tech talks)
- Stay updated on security best practices

---

## Questions?

Contact: **Mr. Đức** (duch9707@gmail.com) | 0389 086 502
LinkedIn: linkedin.com/in/mr-duc  
GitHub: github.com/mr-duc-ops
Website: https://duc-huynh-2003.vercel.app