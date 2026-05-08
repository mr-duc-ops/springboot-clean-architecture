# Technical Leadership Quick-Start Guide

**For developers starting work in this codebase**  
**Owner**: Mr. Đức | **Read Time**: 5 minutes

---

## 📖 What This Is

You're joining a codebase with enterprise-grade standards. This document helps you get started quickly.

---

## 🚀 Before You Start Coding

### 1. Read the Fundamentals (30 minutes)

- [ ] [00_TECHNICAL_LEAD_MANIFESTO.md](./00_TECHNICAL_LEAD_MANIFESTO.md) — Core principles
- [ ] [03_4PLUS1_VIEW_MODEL.md](./03_4PLUS1_VIEW_MODEL.md) — Architecture thinking

### 2. Understand the Git Workflow (15 minutes)

- [ ] [05_GIT_WORKFLOW_RULES.md](./05_GIT_WORKFLOW_RULES.md) — Branch & commit standards
- [ ] Key takeaway: **Atomic commits with meaningful "Why"**

### 3. Know the Code Review Standards (10 minutes)

- [ ] [04_CODE_REVIEW_CHECKLIST.md](./04_CODE_REVIEW_CHECKLIST.md) — What reviewers check
- [ ] **Key takeaway**: Optimize for clarity AND security AND performance

---

## 🎯 Your First Task Checklist

When given a coding task:

### ✅ Planning Phase (Before coding)

- [ ] **Understand the "Why"**: What business problem does this solve?
- [ ] **Check existing architecture**: Is there a pattern in the codebase?
- [ ] **Identify concerns**: What layer(s) does this touch? (Presentation, Application, Domain, Infrastructure)
- [ ] **Find related decisions**: Is there an ADR or RFC about this?
- [ ] **Plan commits**: How will you split this into atomic changes?

### ✅ Coding Phase

- [ ] **Follow project structure**: Files go in the right module/folder
- [ ] **Apply Clean Architecture**: Domain layer is pure business logic
- [ ] **Name clearly**: `processOrder` not `doThing` or `process`
- [ ] **Handle errors**: Don't ignore exceptions or edge cases
- [ ] **Add tests**: At least 1 test per function (target 70% coverage)
- [ ] **No secrets**: No API keys, passwords in code
- [ ] **Code builds**: `npm run build` or equivalent passes

### ✅ Commit Phase

- [ ] **One change per commit**: Atomic commits
- [ ] **Meaningful message**: Follow template (type/scope: description + Actions + Whys)
- [ ] **Review your own diff**: Any obvious issues?
- [ ] **Check lint**: `npm run lint` passes
- [ ] **Tests pass**: `npm test` passes

### ✅ Review Phase

- [ ] **Self-review first**: Use Code Review Checklist
- [ ] **Clear description**: PR explains what and why
- [ ] **Link to issue**: PR references the ticket/issue
- [ ] **Update docs**: README/API docs if user-facing
- [ ] **Request review**: From 1-2 senior engineers

---

## 📋 Copy-Paste Templates

### Creating a Branch

```bash
# For a new feature
git checkout -b feature/short-description

# Example
git checkout -b feature/add-payment-retry-logic
```

### Starting a Commit

```bash
git add src/path/to/affected/file.ts

# Open editor for full message
git commit

# Then type this template:
```

```
feat(payment): add retry logic for payment failures

Actions:
- Add PaymentRetryService with exponential backoff
- Update PaymentGateway to use retry service
- Add unit tests for retry scenarios

Whys:
- Reduces payment failures during network issues
- Implements resilient process design (Process View)
- Aligns with Payment Service architecture (ADR-008)

Notes / Impact:
- Max 3 retries, 2s initial delay
- Related: Issue #892
```

### Reviewing Before Push

```bash
# See what you've committed
git log origin/main..HEAD --oneline

# Make sure it looks good (should be 3-7 focused commits)
git diff origin/main | head -100

# Verify build and tests
npm run build
npm test
```

---

## 🏗️ Architecture Quick Reference

### The Layers (Clean Architecture)

```
API / Controller
     ↓
Application / Use Case (Orchestration)
     ↓
Domain / Business Logic (Pure, isolated)
     ↓
Infrastructure / Database / External APIs
```

**Rule**: Domain layer knows nothing about layers below it.

### The Views (4+1 Model)

| View | Answers | Audience |
|------|---------|----------|
| **Scenario** | What do users do? | Product, Business |
| **Logical** | What are the concepts? | Architect, Senior Dev |
| **Development** | How is code organized? | Developer, Architect |
| **Process** | How does it run? | Developer, DevOps |
| **Physical** | Where is it deployed? | DevOps, Operations |

---

## ⚠️ Common Mistakes to Avoid

### ❌ Mistake 1: Not Atomic Commits

```bash
# Wrong:
git add .
git commit -m "update code"

# Right:
git add src/modules/Auth/
git commit -m "feat(auth): add OAuth login"
git add src/modules/Auth/tests/
git commit -m "test(auth): add OAuth integration tests"
```

### ❌ Mistake 2: Vague Commit Message

```bash
# Wrong:
"fix stuff"
"update payment"
"wip"

# Right:
"fix(payment): handle gateway timeout and retry"
"refactor(order): extract validation into domain service"
```

### ❌ Mistake 3: Mixing Multiple Concerns

```bash
# Wrong:
# Bug fix + Refactor + New feature in one commit

# Right:
git commit -m "fix(auth): handle expired token"  # commit 1
git commit -m "refactor(auth): simplify middleware"  # commit 2
git commit -m "feat(auth): add 2FA support"  # commit 3
```

### ❌ Mistake 4: Violating Layer Boundaries

```typescript
// Wrong:
// Domain layer accessing database directly
export class Order {
  async save() {
    const result = await db.query("INSERT INTO orders...");
  }
}

// Right:
// Domain layer is pure
export class Order {
  constructor(orderId, customer, items) { ... }
  
  canBeCancelled(): boolean {
    return this.status === OrderStatus.PENDING;
  }
}

// Repository handles persistence
@Injectable()
export class OrderRepository {
  async save(order: Order): Promise<void> {
    await db.query("INSERT INTO orders...");
  }
}
```

### ❌ Mistake 5: No Tests

```typescript
// Wrong:
export function calculateOrderTotal(items): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
// (No test!)

// Right:
export function calculateOrderTotal(items): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

describe('calculateOrderTotal', () => {
  it('should sum item prices', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateOrderTotal(items)).toBe(30);
  });

  it('should handle empty items', () => {
    expect(calculateOrderTotal([])).toBe(0);
  });

  it('should apply tax correctly', () => {
    // More tests for edge cases...
  });
});
```

---

## 🔍 When to Ask for Help

### ✅ Ask if:
- "Is this the right place to put this code?"
- "Does this architecture decision make sense?"
- "How should I test this?"
- "Is there an existing pattern I should follow?"

### 🚫 Don't ask if:
- You haven't read the fundamental docs yet
- You haven't tried to understand the problem first
- You're looking for validation (do your best, then ask for review)

---

## 📊 Success Criteria (How You'll Be Evaluated)

✅ **Code Quality**
- Follows architectural principles
- Clear naming and structure
- Adequate tests (70%+ coverage)
- No security issues

✅ **Git Hygiene**
- Atomic commits
- Meaningful messages
- Clear PR descriptions
- Links to issues/decisions

✅ **Communication**
- Documents "Why" decisions
- Asks questions early
- Participates in code reviews
- Updates documentation

✅ **Reliability**
- Code doesn't break production
- Handles edge cases
- Tests pass consistently
- Rollback plan exists

---

## 📞 Getting Unblocked

| Problem | Solution |
|---------|----------|
| Don't understand architecture | Read 03_4PLUS1_VIEW_MODEL.md, ask Tech Lead |
| Don't know how to structure code | Look at existing modules with same concerns |
| Not sure about commit message | Use template in GIT_WORKFLOW_RULES.md |
| Feedback on code review seems harsh | It's about code quality, not you. Ask clarifying questions. |
| Unsure if this needs ADR/RFC | Ask: "Will this affect multiple teams?" If yes → RFC |

---

## 🎓 Recommended Reading Order

**Week 1**:
1. This file (5 min)
2. TECHNICAL_LEAD_MANIFESTO.md (20 min)
3. 4PLUS1_VIEW_MODEL.md (30 min)
4. Look at existing module structure (30 min)

**Week 2**:
1. GIT_WORKFLOW_RULES.md (20 min)
2. CODE_REVIEW_CHECKLIST.md (20 min)
3. ADR_TEMPLATE.md & RFC_TEMPLATE.md (skim, read when needed)

**Ongoing**:
- Read PRs from senior developers
- Ask questions about architectural decisions
- Contribute to RFC discussions

---

## 🚀 Your First PR Checklist

Before submitting first PR:

- [ ] Read TECHNICAL_LEAD_MANIFESTO.md
- [ ] Read GIT_WORKFLOW_RULES.md
- [ ] Code follows existing patterns in codebase
- [ ] All tests pass (`npm test`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] Commits are atomic (3-5 focused commits)
- [ ] Commit messages follow template
- [ ] PR description links to issue
- [ ] No sensitive data in code
- [ ] At least one reviewer assigned
- [ ] Ready to accept feedback and iterate

---

## 💡 Key Insights

### 1. Atomic Commits = Reversibility

If each commit is one logical change:
- Easy to revert if something breaks
- Easy to understand what changed and why
- Easy to bisect to find bugs
- Easy for code review

### 2. "Why" > "What"

Code shows WHAT. Comments/commits explain WHY.

```bash
# Bad:
git commit -m "add try-catch block"

# Good:
git commit -m "fix(payment): add timeout handling and retry logic

Whys:
- Payment timeouts causing 2% transaction failure rate
- Implement resilience pattern for external API calls"
```

### 3. Architecture = Constraints

Clean Architecture imposes constraints to make code:
- Testable (without database/network)
- Maintainable (easy to find code)
- Flexible (easy to replace components)

Don't fight the constraints. They exist for good reason.

### 4. Code Review = Learning

Feedback on PRs isn't criticism. It's:
- Mentorship
- Sharing patterns
- Catching mistakes early
- Improving team consistency

Appreciate it and improve.

---

## 🎯 30-Day Plan

**Day 1-2**: Read & understand core principles  
**Day 3-5**: Understand existing architecture  
**Day 6-10**: Complete first small task with guidance  
**Day 11-20**: Complete medium task independently  
**Day 21-30**: Lead smaller code review or architectural decision  

By day 30, you should be able to:
- Write atomic commits with meaningful messages
- Design code using Clean Architecture
- Participate in code reviews effectively
- Contribute to architectural decisions

---

## Questions?

**Technical**: Ask your code reviewer or Tech Lead  
**Process**: Create an RFC  
**Career**: Talk to Engineering Manager  

---

**Last Updated**: May 7, 2026  
**Owner**: Mr. Đức (Technical Lead)  
**Contact**: duch9707@gmail.com

Welcome to the team!
