# TECHNICAL LEADERSHIP FRAMEWORK

**Enterprise-Grade Code Quality Standards**  
**Owner**: Mr. Đức
**Established**: May 7, 2026 | **Version**: 1.0

---

## 📚 Documentation Index

This framework consists of 6 core documents:

### 1. **[00_TECHNICAL_LEAD_MANIFESTO.md](./00_TECHNICAL_LEAD_MANIFESTO.md)** ⭐ START HERE
**Core Principles & Standards**

- Philosophy: Simplicity, Practicality, Clean Code
- Code quality checklist (architecture, security, performance, testing)
- Quality gates for all tasks
- Pre-commit checklist

**Read if**: You want to understand what "quality" means  
**Time**: 20 minutes

---

### 2. **[06_QUICK_START_GUIDE.md](./06_QUICK_START_GUIDE.md)** ⭐ START HERE FIRST
**For Developers New to the Codebase**

- 5-minute overview
- Planning checklist for new tasks
- Common mistakes & solutions
- 30-day onboarding plan

**Read if**: You're new to the codebase  
**Time**: 10 minutes

---

### 3. **[05_GIT_WORKFLOW_RULES.md](./05_GIT_WORKFLOW_RULES.md)** ⭐ REQUIRED READING
**Git Branches, Commits, and Collaboration**

- Branch naming convention
- Atomic commit rule
- Commit message format with "Whys"
- Examples and anti-patterns

**Read if**: You're writing code and making commits  
**Time**: 30 minutes

---

### 4. **[03_4PLUS1_VIEW_MODEL.md](./03_4PLUS1_VIEW_MODEL.md)** ⭐ ARCHITECTURE THINKING
**System Design Across 5 Viewpoints**

- Why 4+1 View Model solves misalignment
- 5 views explained: Scenario, Logical, Development, Process, Physical
- When and how to apply
- Complete e-commerce example

**Read if**: You're designing a significant feature or system  
**Time**: 45 minutes

---

### 5. **[04_CODE_REVIEW_CHECKLIST.md](./04_CODE_REVIEW_CHECKLIST.md)** ⭐ FOR REVIEWERS
**What Code Reviewers Check**

- 7 categories of review
- Checklist for authors (before requesting review)
- Checklist for reviewers
- Red flags & decision guide

**Read if**: You're reviewing someone's code or want to know what to expect  
**Time**: 25 minutes

---

### 6. **[01_ADR_TEMPLATE.md](./01_ADR_TEMPLATE.md)** & **[02_RFC_TEMPLATE.md](./02_RFC_TEMPLATE.md)**
**Decision Documentation**

- **ADR** (Architecture Decision Record): Record decisions made
- **RFC** (Request for Comments): Propose decisions & gather feedback

**Use when**: Making architectural decisions  
**Time**: Reference as needed

---

## 🎯 Quick Navigation

### I need to...

**...understand what quality means**
→ Read: 00_TECHNICAL_LEAD_MANIFESTO.md

**...get started on coding**
→ Read: 06_QUICK_START_GUIDE.md → 05_GIT_WORKFLOW_RULES.md

**...design a major feature**
→ Read: 03_4PLUS1_VIEW_MODEL.md → ADR_TEMPLATE.md

**...review someone's code**
→ Read: 04_CODE_REVIEW_CHECKLIST.md

**...propose a big change**
→ Read: RFC_TEMPLATE.md

**...understand architecture decisions**
→ Read: ADR_TEMPLATE.md examples

---

## 📊 Framework Overview

### Core Principles

```
🎯 PHILOSOPHY
├── Simplicity First
├── Practical Impact
├── Clean & Sustainable Code
└── Reduce Misalignment

📐 ARCHITECTURE
├── 4+1 View Model (5 perspectives)
├── Clean Architecture (layered)
├── Domain-Driven Design (DDD)
└── Modular Monolith design

🔧 CODE QUALITY
├── Security (OWASP, no secrets)
├── Performance (p95 < 500ms)
├── Testing (70%+ coverage)
└── Maintainability (clear structure)

🌿 GIT WORKFLOW
├── Atomic commits (one change per commit)
├── Meaningful messages (explain "Why")
├── Clear branches (feature/fix/refactor)
└── Code review process

📋 DECISIONS
├── ADR = Record decisions made
├── RFC = Propose & discuss decisions
└── Transparency & documentation
```

---

## ✅ Quality Checklist Template

Use this for every task:

**Before you code:**
- [ ] Understand the business problem
- [ ] Identify which layers this touches
- [ ] Check existing patterns
- [ ] Find related ADR/RFC

**While coding:**
- [ ] Follow Clean Architecture layers
- [ ] Write tests as you code
- [ ] No security issues
- [ ] Clear naming

**Before committing:**
- [ ] Build passes
- [ ] Tests pass
- [ ] Lint passes
- [ ] No secrets
- [ ] Commits are atomic

**Before requesting review:**
- [ ] Self-review completed
- [ ] PR description links to issue
- [ ] Updated documentation
- [ ] Tested happy path + error cases

**Code Review:**
- [ ] Architecture respected
- [ ] Security verified
- [ ] Performance considered
- [ ] Tests adequate
- [ ] Commits atomic
- [ ] Message is clear

---

## 🚀 How to Use This Framework

### For Individual Contributors

1. **Day 1**: Read 06_QUICK_START_GUIDE.md
2. **Day 2-3**: Read 00_TECHNICAL_LEAD_MANIFESTO.md & 05_GIT_WORKFLOW_RULES.md
3. **On every task**: 
   - Plan using the checklist
   - Code following standards
   - Use 06_QUICK_START_GUIDE.md as reference
4. **Before each commit**: Use GIT_WORKFLOW_RULES.md template
5. **Before each PR**: Use CODE_REVIEW_CHECKLIST.md (author section)
6. **When designing**: Use 4PLUS1_VIEW_MODEL.md

### For Code Reviewers

1. Read 04_CODE_REVIEW_CHECKLIST.md
2. On every PR:
   - Use the checklist
   - Leave constructive feedback
   - Reference framework docs when giving guidance
3. When uncertain: Ask Tech Lead

### For Technical Leads

1. Own enforcement of standards
2. Use ADR/RFC templates for major decisions
3. Review quarterly: Do standards still fit?
4. Coach team members through examples
5. Update docs when standards evolve

### For Product Managers

1. Understand that quality = speed long-term
2. Budget for proper architecture & testing
3. Don't rush quality gates
4. Participate in RFC discussions

---

## 📈 Metrics & Success

### Code Quality Metrics

| Metric | Target | Measured By |
|--------|--------|------------|
| Test Coverage | 70%+ | npm test report |
| Build Success Rate | 95%+ | CI logs |
| Code Review Turnaround | < 24h | GitHub stats |
| Production Incidents | < 1/month | Incident tracking |
| Escaped Defects | < 2% | Post-release bugs |
| Security Issues | 0 critical | Security scanner |

### Developer Metrics

| Metric | Target |
|--------|--------|
| Atomic commits per PR | 3-7 |
| Commit message clarity | 100% follow template |
| Code review feedback turn time | < 24h |
| First-time PR approval rate | 80%+ (after learning period) |

### System Quality Metrics

| Metric | Target |
|--------|--------|
| p95 API latency | < 500ms |
| Error rate | < 0.1% |
| Uptime SLA | 99.9% |
| Deployment frequency | 1x per week minimum |
| MTTR (incident resolution) | < 30 minutes |

---

## 🎓 Learning Path

**Week 1**: Foundations
- Read: 06_QUICK_START_GUIDE.md (10 min)
- Read: 00_TECHNICAL_LEAD_MANIFESTO.md (20 min)
- Activity: Review 2 existing PRs

**Week 2**: Git & Commits
- Read: 05_GIT_WORKFLOW_RULES.md (30 min)
- Activity: Make 5 commits following the format
- Activity: Get feedback on commit messages

**Week 3**: Code Review
- Read: 04_CODE_REVIEW_CHECKLIST.md (25 min)
- Activity: Review 2 PRs using checklist
- Activity: Receive detailed feedback on your review

**Week 4**: Architecture
- Read: 03_4PLUS1_VIEW_MODEL.md (45 min)
- Activity: Sketch 4+1 views for your module
- Activity: Discuss architecture with Tech Lead

**Month 2+**: Mastery
- Participate in RFC discussions
- Lead code reviews
- Create ADRs for decisions
- Mentor new team members

---

## 🔗 Integration with Other Systems

This framework works alongside:

- **Build System**: Linting, testing, compilation (enforced via pre-commit hooks)
- **CI/CD**: Automated tests, security scanning (enforce on merge)
- **GitHub/GitLab**: PR checks, branch protection rules
- **Monitoring**: Incident tracking, performance monitoring
- **Documentation**: Wiki, architecture diagrams, runbooks

---

## 📞 Support & Questions

### Getting Help

| Question | Answer Source |
|----------|----------------|
| How should I structure this code? | Read: 03_4PLUS1_VIEW_MODEL.md or ask Tech Lead |
| What should my commit message look like? | Read: 05_GIT_WORKFLOW_RULES.md or use template |
| What's the code review looking for? | Read: 04_CODE_REVIEW_CHECKLIST.md |
| How do I propose a big change? | Read: RFC_TEMPLATE.md and create RFC |
| I don't understand the architecture | Read: 03_4PLUS1_VIEW_MODEL.md or pair with senior dev |

### Escalation

1. **Questions**: Ask your code reviewer or Tech Lead
2. **Blockers**: Create an RFC to discuss with team
3. **Process issues**: Talk to Engineering Manager
4. **Framework improvements**: Create an RFC to propose changes

---

## 🔄 Framework Evolution

This framework is **version 1.0** and will evolve:

- **Every quarter**: Review & update based on team feedback
- **Via RFC**: Propose major changes through RFC process
- **Transparently**: Document all decisions in ADRs

Last updated: May 7, 2026  
Next review: August 7, 2026

---

## 🎯 TL;DR (Too Long; Didn't Read)

If you have 2 minutes:

> **Quality comes from 5 things**:
> 1. **Clean Architecture** - Clear layers, clear boundaries
> 2. **Atomic Commits** - One logical change per commit, meaningful message
> 3. **Thorough Testing** - 70% coverage minimum
> 4. **Security First** - No shortcuts on security
> 5. **Documentation** - Why decisions matter, not just what code does

> **On every task**: Read → Plan → Code → Test → Commit → Review → Merge

---

## 📖 Document Relationships

```
06_QUICK_START_GUIDE.md (Start here)
    ↓
00_TECHNICAL_LEAD_MANIFESTO.md (Understand philosophy)
    ├→ 05_GIT_WORKFLOW_RULES.md (Learn git)
    ├→ 03_4PLUS1_VIEW_MODEL.md (Understand architecture)
    ├→ 04_CODE_REVIEW_CHECKLIST.md (Learn review)
    └→ 01_ADR_TEMPLATE.md & 02_RFC_TEMPLATE.md (Document decisions)
```

---

**Owner**: Mr. Đức (duch9707@gmail.com) | 0389 086 502
**Framework Version**: 1.0  
**Created**: May 9, 2026  
**Status**: Active & Enforced

---

## 🚀 Welcome!

You're now part of a team that values:
- **Quality over speed** (speed comes from quality)
- **Clarity over cleverness** (easy to maintain > hard to understand)
- **Collaboration over isolation** (code review is mentorship)
- **Documentation over assumptions** (decisions explained)

Let's build something great together.

---

**Ready to start?** → Read [06_QUICK_START_GUIDE.md](./06_QUICK_START_GUIDE.md)
