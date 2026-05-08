# Git Workflow & Commit Rules
**Enterprise-Grade Standard** | **Enforced by Technical Leadership** | **Last Updated**: May 7, 2026

---

## 📋 Overview

This document enforces atomic commits, meaningful messages, and clear branch strategy to maintain code quality and reduce misalignment.

**Key principle**: Every commit should be reversible, understandable, and valuable on its own.

---

## 🌿 Branch Strategy

### Repository Structure

```
main (production, always deployable)
  ├── release/* (release candidates)
  ├── feature/* (new features)
  ├── fix/* (bug fixes)
  ├── refactor/* (code restructuring)
  ├── test/* (test additions)
  ├── docs/* (documentation)
  ├── chore/* (dependencies, config)
  ├── infra/* (CI/CD, infrastructure)
  └── spike/* (R&D, never merged)
```

### Branch Naming Convention

```
<prefix>/<scope>-<description>

Examples:
  feature/auth-oauth2-integration
  feature/multi-tenant-isolation
  fix/payment-timeout-handling
  fix/memory-leak-in-cache
  refactor/order-service-boundaries
  refactor/extract-validation-layer
  test/e2e-checkout-flow
  docs/api-authentication-guide
  chore/upgrade-nodejs-v20
  chore/update-dependencies-july
  infra/setup-kubernetes-deployment
  infra/add-datadog-monitoring
  spike/evaluate-event-sourcing
  spike/benchmark-database-options
```

### Rules

✅ **DO**:
- Use lowercase and hyphens (kebab-case)
- Be specific and descriptive
- Include ticket number if applicable: `feature/jira-123-auth-oauth2`

❌ **DON'T**:
- Use spaces or underscores: `feature/auth oauth2` ❌
- Use vague names: `feature/update` ❌
- Use abbreviations: `feat/auth-o2` ❌
- Mix multiple concerns: `feature/auth-and-payment` ❌

---

## 🎯 Commit Strategy - The Atomic Commit Rule

### What is an Atomic Commit?

**One logical, reversible, understandable change.**

If you do `git revert <commit>`, the code should still be:
- Compilable
- Testable
- Deployable

### How to Create Atomic Commits

#### Step 1: Plan the Changes

Before typing `git add`, analyze what changes you need:

```bash
# See what you've changed
git diff

# Check what's staged
git diff --cached

# Review complete diff
git status
```

#### Step 2: Stage Selectively (NOT git add .)

```bash
# Add specific files related to one change
git add src/modules/Auth/components/LoginForm.tsx
git add src/modules/Auth/components/RegisterForm.tsx
git add src/modules/Auth/styles/form.css

# Commit this logical group
git commit -m "feat(auth): create login and register form components"

# Then stage next change
git add src/modules/Auth/store/authSlice.ts
git commit -m "feat(auth): initialize Redux auth slice for state management"
```

#### Step 3: Use Interactive Staging When Necessary

```bash
# Stage parts of files (not whole files)
git add -p

# This shows each change and asks "stage this? y/n/s/d"
# s = split this hunk further
```

#### Step 4: Verify Before Committing

```bash
# Review what you're about to commit
git diff --cached

# Make sure it compiles
npm run build

# Run tests
npm test

# Now commit
git commit
```

### Commit Size Guidelines

| Size | When to Use | Example |
|------|------------|---------|
| 1-5 lines | Very focused change | Fix typo, add constant |
| 5-30 lines | One method/function | Add new validation function |
| 30-100 lines | One component/class | Create new entity class |
| 100-300 lines | One feature piece | New API endpoint + handler |
| 300+ lines | Red flag | Consider splitting |

### Anti-patterns

❌ **Mistake**: One massive commit with 20 files changed
```bash
git add .
git commit -m "Update code"  # ❌ Bad
```

❌ **Mistake**: Mixed concerns in one commit
```bash
# Fixed bug + refactored database + upgraded dependency ❌
```

❌ **Mistake**: Incomplete commits
```bash
# Auth module + Payment module + Inventory module in one commit ❌
```

✅ **Correct**: Atomic, focused commits
```bash
git commit -m "refactor(auth): extract LoginForm into separate component"
git commit -m "refactor(auth): move auth state to Redux slice"
git commit -m "test(auth): add unit tests for LoginForm"
git commit -m "feat(auth): integrate OAuth2 login button"
```

---

## 💬 Commit Message Format

### Template

```
<type>(<scope>): <strong, specific description>

Actions:
- Concrete action 1
- Concrete action 2
- Concrete action 3

Whys:
- Strategic reason / business value
- Architectural principle / DDD concept
- Misalignment prevention
- Reference to domain boundary or design principle

Notes / Impact:
- Trade-offs accepted
- Breaking changes (if any)
- Next steps
- Related ADR / Issue #
```

### Type (MANDATORY)

Must be one of:
- **feat** → New feature
- **fix** → Bug fix
- **refactor** → Code restructuring (behavior unchanged)
- **test** → Add or update tests
- **docs** → Documentation only
- **chore** → Maintenance, dependencies, build config
- **style** → Code formatting (rare - usually auto-formatted)
- **ci** → CI/CD pipeline changes

### Scope (HIGHLY RECOMMENDED)

The module or area affected:
- `auth`, `payment`, `order`, `inventory`, `user`
- `api`, `database`, `cache`, `queue`
- `frontend`, `backend`, `infra`

### Subject Line (REQUIRED)

- First line, summary
- 50 characters max (enforced by linters)
- Imperative mood: "add" not "added" or "adds"
- No period at end
- Specific, not vague

| ❌ Bad | ✅ Good |
|--------|---------|
| "fix bug" | "fix(auth): handle expired token refresh" |
| "update stuff" | "refactor(payment): simplify gateway adapter" |
| "wip" | "feat(order): add order status tracking" |

### Example: Complete Commit Messages

#### Example 1: Feature Commit

```
feat(auth): decouple auth from global UI state management

Actions:
- Extract Login and Register components from src/components/ into src/modules/Auth/components/
- Create Redux slice: src/modules/Auth/store/authSlice.ts
- Create Auth boundary contract: src/modules/Auth/types.ts
- Update tests for new component structure

Whys:
- Enforces Bounded Context (Clean Architecture principle).
- Prevents Product domain from directly mutating Auth state.
- Reduces misalignment between Auth and UI concerns.
- Makes auth testable and reusable independently.
- Prepares for future OAuth2/SAML integration.

Notes / Impact:
- BREAKING: Auth imports change from @/store/auth → @/modules/Auth/store
- Next step: Implement API adapter to fully decouple from Axios.
- Related: ADR-002 (Modular Monolith Architecture)
- Issue: #427
```

#### Example 2: Bug Fix Commit

```
fix(payment): handle payment timeout and retry appropriately

Actions:
- Add timeout detection in PaymentGateway adapter
- Implement exponential backoff retry strategy (3 attempts)
- Update Order status to PAYMENT_PENDING on timeout
- Add logging for troubleshooting

Whys:
- Production incident: 5 orders failed due to payment timeout
- Root cause: No timeout handling in synchronous payment flow
- Solution: Timeout marks order as PENDING, retry in background job
- Aligns with resilient process design (Process View in 4+1 Model)

Notes / Impact:
- User experience: Customer sees "Payment processing..." instead of error
- Database: adds payment_last_retry_at column for migration
- Monitoring: Add alert if > 50 timeouts/hour
- Related: Issue #892
```

#### Example 3: Refactor Commit

```
refactor(order-service): extract validation into domain service

Actions:
- Create OrderValidator domain service
- Move validation rules from OrderService to OrderValidator
- Update OrderService to call validator
- Add unit tests for OrderValidator

Whys:
- Violation of Single Responsibility Principle (OrderService was doing too much)
- Prepares for API versioning (different versions may have different validation)
- Improves testability: OrderValidator is pure domain logic
- Aligns with Clean Architecture (business rules belong in Domain layer)

Notes / Impact:
- No breaking changes: OrderService interface remains same
- Performance: No impact (validation still O(1))
- Maintainability: +150 lines in OrderValidator, -100 lines in OrderService
- Related: ADR-007 (Clean Architecture Layers)
```

#### Example 4: Test Commit

```
test(auth): add unit tests for login flow

Actions:
- Add LoginForm.test.tsx with 8 test cases
- Add LoginForm submission test
- Add OAuth2 failure handling test
- Add accessibility tests (a11y)

Whys:
- Current coverage: 42%. Target: 70%.
- LoginForm is user-critical, high-risk change.
- Improves confidence in Auth refactoring (feat commit).
- Prepares for future regression detection by AI agents.

Notes / Impact:
- Test execution time: +2 seconds (acceptable)
- Coverage after: 65% (getting closer to target)
- All tests pass locally and in CI
```

---

## 🔍 Commit Message Review Checklist

Before committing, verify:

- [ ] **Type is correct**: feat/fix/refactor/test/docs/chore
- [ ] **Scope specified**: auth, payment, etc.
- [ ] **Subject is clear**: 50 chars, specific, imperative mood
- [ ] **Actions are concrete**: Not vague descriptions
- [ ] **Whys reference architecture**: DDD, Clean Architecture, 4+1, etc.
- [ ] **Impact documented**: Breaking changes, side effects
- [ ] **Related issue linked**: Issue #123
- [ ] **Related ADR/RFC linked**: ADR-001 / RFC-003
- [ ] **Commit is reversible**: `git revert` would be safe

---

## 🛠️ Workflow Example: Implementing a Feature

### Scenario: Add PaymentGateway Abstraction

#### Step 1: Plan the Feature

```bash
# Create branch
git checkout -b feature/payment-gateway-abstraction

# Understand current state
git log --oneline -10
git diff main...HEAD
```

#### Step 2: Create Atomic Commits

**Commit 1**: Create the interface

```bash
git add src/modules/Payment/ports/PaymentGateway.ts
git commit -m "feat(payment): add PaymentGateway port interface

Actions:
- Create PaymentGateway interface in ports/ (Clean Architecture boundary)
- Define contract: charge(), refund(), getTransactionStatus()

Whys:
- Establishes payment processing boundary
- Allows multiple implementations (Stripe, PayPal, etc.)
- Enables testing via mocks

Notes / Impact:
- No implementation yet, just contract
- Next: Implement Stripe adapter
- Related: ADR-004 (Payment Service Design)"
```

**Commit 2**: Implement Stripe adapter

```bash
git add src/modules/Payment/adapters/StripePaymentGateway.ts
git add src/modules/Payment/adapters/StripePaymentGateway.test.ts
git commit -m "feat(payment): implement Stripe payment gateway adapter

Actions:
- Create StripePaymentGateway implementing PaymentGateway interface
- Add charge() implementation with error handling
- Add unit tests for success/failure cases

Whys:
- Concrete implementation of PaymentGateway port
- Encapsulates Stripe API details in adapter
- Testable via dependency injection

Notes / Impact:
- Requires STRIPE_API_KEY env variable
- No breaking changes to existing code
- Tests use Stripe sandbox keys"
```

**Commit 3**: Integrate into Order Service

```bash
git add src/modules/Order/application/PlaceOrderUseCase.ts
git commit -m "feat(order): inject PaymentGateway into OrderService

Actions:
- Update PlaceOrderUseCase constructor to accept PaymentGateway
- Remove hardcoded Stripe dependency
- Update tests to pass mock PaymentGateway

Whys:
- Completes Clean Architecture dependency injection
- Order Service no longer directly depends on Stripe
- Improves testability and flexibility

Notes / Impact:
- Breaking change: OrderService constructor signature changed
- Migration: Existing instantiation code must pass PaymentGateway
- Related: ADR-004"
```

**Commit 4**: Migrate existing code

```bash
git add src/index.ts
git add src/modules/Order/index.ts
git commit -m "chore(payment): migrate existing code to use gateway abstraction

Actions:
- Update app initialization to create Stripe adapter instance
- Pass PaymentGateway to OrderService
- Remove old hardcoded payment logic

Whys:
- Completes migration from hardcoded to abstracted pattern
- No functional change, just structure

Notes / Impact:
- Completes the architecture migration
- All tests pass
- Ready to add alternative payment providers"
```

**Commit 5**: Tests and documentation

```bash
git add test/integration/payment-gateway.integration.test.ts
git add docs/ARCHITECTURE.md
git commit -m "test(payment): add integration tests for payment gateway

Actions:
- Add integration test: charge success flow
- Add integration test: charge failure handling
- Update architecture documentation

Whys:
- Validates real Stripe integration
- Documents new payment abstraction for future maintainers

Notes / Impact:
- Integration tests use Stripe sandbox
- Documentation links to ADR-004"
```

#### Step 3: Create Pull Request

```bash
git push origin feature/payment-gateway-abstraction

# On GitHub:
Title: "feat(payment): add payment gateway abstraction (Stripe)"
Description:
  Closes #123
  
  ## Changes
  - New PaymentGateway port interface
  - Stripe adapter implementation
  - Order Service now uses injected gateway
  
  ## Commits
  - Atomic commits, each independently reviewable
  
  ## Testing
  - Unit tests: src/modules/Payment/adapters/*.test.ts
  - Integration tests: test/integration/payment-gateway.integration.test.ts
  - All tests pass locally and in CI
  
  ## Related
  - ADR-004: Payment Service Architecture
  - Resolves #123
```

#### Step 4: Code Review & Merge

Reviewer checks each commit independently using the Code Review Checklist.

---

## 📊 Git Commands Cheat Sheet

### Viewing Commits

```bash
# View commit history
git log --oneline

# View commits with diff
git log -p

# View commits for specific file
git log -- src/modules/Auth/

# View specific commit details
git show <commit-hash>

# View who changed each line
git blame src/modules/Auth/Login.tsx
```

### Staging & Committing

```bash
# Add specific files
git add src/modules/Auth/Login.tsx src/modules/Auth/Register.tsx

# Add parts of files interactively
git add -p

# See what's staged
git diff --cached

# Commit with editor (for detailed messages)
git commit

# Commit with inline message
git commit -m "feat(auth): add login form"

# Amend last commit (if not pushed yet)
git commit --amend
```

### Reviewing Before Push

```bash
# Compare with main branch
git diff main...HEAD

# View all commits in this branch
git log main..HEAD --oneline

# Count commits
git log main..HEAD --oneline | wc -l
```

### Reverting Changes

```bash
# Revert a commit (creates new commit)
git revert <commit-hash>

# Reset to previous state (destructive, only if not pushed)
git reset --hard <commit-hash>

# Unstage a file
git reset HEAD <file>

# Discard changes to a file
git checkout -- <file>
```

---

## 🚨 Common Mistakes & How to Fix Them

### Mistake 1: Committed to Wrong Branch

```bash
# You committed to main instead of feature/auth

# Create the correct branch with your commits
git branch feature/auth-fix

# Reset main to previous state
git reset --hard origin/main

# Switch to your branch
git checkout feature/auth-fix

# Create PR from feature/auth-fix
```

### Mistake 2: Committed Too Much (Not Atomic)

```bash
# You committed auth + payment + inventory in one commit

# Reset to before commit (keeps changes as unstaged)
git reset HEAD~1

# Now stage and commit separately
git add src/modules/Auth/
git commit -m "feat(auth): ..."

git add src/modules/Payment/
git commit -m "feat(payment): ..."

git add src/modules/Inventory/
git commit -m "feat(inventory): ..."

# Push all commits
git push
```

### Mistake 3: Sensitive Data in Commit

```bash
# You accidentally committed API key

# Remove from commit history (if not pushed yet)
git reset --soft HEAD~1
git reset HEAD sensitive-file.txt
# Remove the secret
git commit -m "feat(auth): add oauth integration"

# If already pushed (more complex)
# Use git-filter-branch or GitHub secret scanning
```

### Mistake 4: Bad Commit Message

```bash
# You wrote "wip" as commit message

# Amend the last commit (if not pushed yet)
git commit --amend -m "feat(auth): add login validation"

# If already pushed to remote
git push --force-with-lease origin feature/auth-fix
# (use cautiously, only with team agreement)
```

---

## 🔒 Pre-push Checklist

Before `git push`:

```bash
# 1. Verify all commits are atomic and meaningful
git log origin/main..HEAD --oneline
# (Should see 3-7 focused commits, not 1 huge or 20 tiny)

# 2. Verify branch builds
npm run build

# 3. Verify tests pass
npm test

# 4. Verify no secrets
git diff origin/main | grep -E "(password|secret|key|token)"
# (Should output nothing)

# 5. Verify commit messages are good
git log origin/main..HEAD --pretty=fuller
# (Read each message - does it make sense?)

# 6. Only then push
git push origin feature/my-feature
```

---

## 🎓 Further Reading

- **Conventional Commits**: https://www.conventionalcommits.org/
- **Clean Code**: Chapters on naming and functions
- **A successful Git branching model**: https://nvie.com/posts/a-successful-git-branching-model/

---

**Questions?** Contact your Tech Lead  
**Want to improve these standards?** Create an RFC

