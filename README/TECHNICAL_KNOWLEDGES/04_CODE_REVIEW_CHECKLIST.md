# Code Review Checklist

**Reviewer**: Use this checklist for every code review.  
**Author**: Use this before requesting review.

---

## Pre-Review (For Code Author)

**Before requesting review, author must verify:**

- [ ] **Build passes**: `npm run build` or equivalent succeeds
- [ ] **Tests pass**: `npm test` passes with >= 70% coverage
- [ ] **Linting passes**: `npm run lint` returns no errors
- [ ] **No secrets in code**: No passwords, API keys, tokens visible
- [ ] **Commits are atomic**: Each commit is one logical change
- [ ] **Commit messages clear**: Follow format (type/scope: description)
- [ ] **Self-review done**: Read own diff, any obvious issues?
- [ ] **Branch naming correct**: `feature/`, `fix/`, `refactor/`, etc.
- [ ] **No unnecessary files**: Removed console.logs, debug code, node_modules
- [ ] **Updated relevant docs**: README, API docs, or architecture docs if applicable

---

## Review Checklist (For Code Reviewer)

### 1️⃣ SCOPE & INTENT

- [ ] **Scope is clear**: What problem does this PR solve?
- [ ] **One concern per PR**: Not mixing refactor + feature + bug fix
- [ ] **Size is reasonable**: < 400 lines changed (prefer smaller PRs)
- [ ] **Related to issue/ticket**: PR description links to issue
- [ ] **Related ADR/RFC**: If architectural change, related documentation exists

**Questions to Ask**:
- "Is this the minimal change to solve the problem?"
- "Could this be split into multiple PRs?"
- "Is there unnecessary refactoring in here?"

---

### 2️⃣ CODE QUALITY

#### 🏗️ Architecture & Design
- [ ] **Follows project structure**: Files in correct location/module
- [ ] **No circular dependencies**: A → B → C, not A ← → B
- [ ] **Respects layer boundaries**: Domain doesn't know about Infra
- [ ] **Bounded Contexts separated**: Order logic doesn't contaminate Payment
- [ ] **Interfaces/contracts clear**: Types are explicit, not inferred
- [ ] **No public members that should be private**: Encapsulation respected

**Questions to Ask**:
- "Why is this class/module here?"
- "Could this logic go in Domain layer?"
- "Does this violate any boundary?"
- "Is the 4+1 view still consistent?"

#### 📝 Naming & Readability
- [ ] **Names are clear**: Variables, functions, classes have intent
- [ ] **No abbreviations**: `orderService` not `ordSvc` or `os`
- [ ] **Consistent naming**: Similar concepts named similarly
- [ ] **No misleading names**: Name matches actual behavior
- [ ] **Naming follows convention**: camelCase for variables, PascalCase for classes
- [ ] **Comments explain "why"**: Not "what" (code shows what)

**Questions to Ask**:
- "Does the name reflect what this does?"
- "Will someone understand this in 6 months?"
- "Is this name consistent with codebase?"

#### 🔄 Logic & Flow
- [ ] **Logic is correct**: No off-by-one errors, null checks missing
- [ ] **No dead code**: All variables/functions are used
- [ ] **No duplicate logic**: Not copy-pasted from elsewhere
- [ ] **Complexity is justified**: Complex algorithms explained
- [ ] **Edge cases handled**: Null, empty, boundary conditions
- [ ] **No hard-coded values**: Magic numbers extracted to constants

**Questions to Ask**:
- "Is there a simpler way to write this?"
- "What if input is null/empty?"
- "What if this runs 1000 times?"
- "Does this match the business rule?"

#### 🔒 Security
- [ ] **No SQL injection**: Uses parameterized queries
- [ ] **No secrets in code**: No API keys, passwords, tokens
- [ ] **Input validation**: All external input validated
- [ ] **Authorization checked**: Only permitted users can access
- [ ] **Sensitive data handled**: Passwords hashed, PII encrypted
- [ ] **No CORS bypass**: CORS config is restrictive
- [ ] **Dependencies safe**: No known vulnerabilities in deps

**Questions to Ask**:
- "Could an attacker exploit this?"
- "Is user identity verified?"
- "Is data encrypted in transit?"
- "Are there dependency security issues?"

#### ⚡ Performance
- [ ] **No N+1 queries**: Database queries optimized
- [ ] **Caching used appropriately**: Not over-caching
- [ ] **No blocking operations**: Async used where appropriate
- [ ] **No memory leaks**: Resources released properly
- [ ] **No infinite loops**: Bounded iterations
- [ ] **Response time acceptable**: p95 < target SLA

**Questions to Ask**:
- "Will this scale to 10x users?"
- "Are there database queries in loops?"
- "Is caching missing where needed?"
- "Could this hang in production?"

---

### 3️⃣ TESTING

- [ ] **Tests added/updated**: New code has test coverage
- [ ] **Tests pass**: All tests green before merge
- [ ] **Coverage maintained**: Coverage didn't decrease
- [ ] **Test names clear**: Describe what's being tested
- [ ] **Happy path tested**: Normal flow works
- [ ] **Error path tested**: Exception handling tested
- [ ] **Edge cases tested**: Boundary conditions covered
- [ ] **No skip/xdescribe**: No temporarily disabled tests left
- [ ] **Mocks appropriate**: Not over-mocked, integration tested too

**Questions to Ask**:
- "What breaks if I change this code?"
- "Are tests testing implementation or behavior?"
- "Is error handling actually tested?"
- "Would these tests catch a regression?"

---

### 4️⃣ GIT & COMMITS

- [ ] **Commits are atomic**: One logical change per commit
- [ ] **Commit messages clear**: Follow format with "Why"
- [ ] **No WIP commits**: No "fix", "wip", "debug" commits
- [ ] **No console.logs**: Debug code cleaned up
- [ ] **No merged main**: Branch rebased on latest main
- [ ] **Conventional Commits format**: Followed (feat/fix/refactor/etc)

**Questions to Ask**:
- "Does each commit tell a story?"
- "Could I revert one commit safely?"
- "Is the message clear to someone reading history?"

---

### 5️⃣ DOCUMENTATION

- [ ] **Code comments when needed**: Explains "why", not "what"
- [ ] **API documented**: If public API, documented
- [ ] **Complex logic explained**: Non-obvious algorithms have comments
- [ ] **README updated**: If user-facing feature
- [ ] **Deprecations marked**: Old code marked as deprecated
- [ ] **ADR/RFC created**: If architectural decision
- [ ] **Inline docs accurate**: Comments match code

**Questions to Ask**:
- "Will someone understand this without talking to author?"
- "Are there any gotchas documented?"
- "Is the architecture decision recorded?"

---

### 6️⃣ TEAM STANDARDS

- [ ] **Follows .eslintrc/.editorconfig**: Linting passes
- [ ] **No style wars**: Adheres to team conventions
- [ ] **Error handling consistent**: Same pattern as codebase
- [ ] **Logging consistent**: Same format, appropriate level
- [ ] **Constants management**: Used shared constants, not local magic numbers
- [ ] **Type safety**: Types used properly (TypeScript/Java/etc)

---

### 7️⃣ FINAL CHECKS

- [ ] **Resolves the issue**: Does PR accomplish what issue requested?
- [ ] **No unrelated changes**: Everything is relevant to scope
- [ ] **Backwards compatible**: No breaking changes (unless documented)
- [ ] **No package-lock conflicts**: Dependencies resolved cleanly
- [ ] **CI passes**: All automated checks pass
- [ ] **Ready for main branch**: Would be safe to merge now

---

## Decision Guide

### ✅ Approve If:
- All checks above pass
- Code quality meets team standards
- Tests adequate
- No security issues
- Clear architectural coherence

### 🤝 Approve with Minor Comments:
- Small issues noted but acceptable
- Author can fix in follow-up
- Not blocking merge

### 🔄 Request Changes If:
- Missing tests
- Security concern
- Architecture violation
- Unresolved design question
- Performance issue

### ❌ Reject & Request Rewrite If:
- Fundamentally wrong approach
- Security vulnerability
- Major architecture violation
- Unmaintainable code

---

## Reviewer Notes

### Constructive Feedback Template

```
🎯 **Goal**: [Why this matters to codebase/team]

❓ **Question**: [Specific question about the approach]

💡 **Suggestion**: [Alternative approach or improvement]

✅ **Positive**: [What's good about this PR]

⚠️ **Concern**: [Risk or potential issue]

🚀 **Nice-to-have**: [Optional improvement, not blocking]
```

### Example Good Comments

❌ **Bad**: "This is wrong"  
✅ **Good**: "This approach won't scale if N > 1000 due to O(n²) algorithm. Consider using a hash map instead (O(1) lookup)."

❌ **Bad**: "Naming is bad"  
✅ **Good**: "`processData` is vague. Based on the logic, this looks like it's validating and normalizing orders. How about `normalizeOrderFields` instead?"

❌ **Bad**: "Missing test"  
✅ **Good**: "What happens if `user` is null? Can we add a test case for unauthorized access?"

---

## Review Time Estimates

| Change Size | Estimated Review Time |
|-------------|----------------------|
| < 50 lines | 5-10 minutes |
| 50-200 lines | 15-30 minutes |
| 200-500 lines | 30-60 minutes |
| 500+ lines | 60+ minutes (consider requesting split) |

**Rule**: If review takes > 60 min, ask author to split PR into smaller changes.

---

## Red Flags (Always Investigate)

🚩 Large refactor + feature in one PR  
🚩 No tests for new code  
🚩 SQL queries visible in code (not parameterized)  
🚩 Error handling missing  
🚩 Vague commit messages  
🚩 Code style wildly different from codebase  
🚩 Performance not considered  
🚩 Comments don't match code  
🚩 Secrets or sensitive data visible  
🚩 Breaking API changes undocumented  

---

## Post-Merge Checklist

After PR is merged:
- [ ] Monitor for regressions
- [ ] Verify deployment is clean
- [ ] Update related documentation
- [ ] Close related issues
- [ ] Tag reviewers if incident occurs

---

**For questions**: Ask Tech Lead  
**For process improvements**: Create an RFC
