# RFC Template - Request for Comments

Use this template to propose changes and gather team feedback BEFORE making decisions.

---

## RFC-XXX: [Tên đề xuất rõ ràng, dùng động từ]

**Example names:**
- "Introduce Modular Monolith Architecture"
- "Migrate to OAuth2 Authentication"
- "Adopt Kubernetes for Deployment"
- "Standardize API Error Format"

---

## Metadata

| Field | Value |
|-------|-------|
| **Status** | `Draft` / `Review` / `Accepted` / `Rejected` / `Withdrawn` / `Implemented` |
| **Author** | [Name / Team] |
| **Date Created** | YYYY-MM-DD |
| **Target Release** | [Sprint / Quarter] |
| **Priority** | `Critical` / `High` / `Medium` / `Low` |
| **Review Deadline** | YYYY-MM-DD |
| **Stakeholders** | Product, Backend, Frontend, Security, DevOps |
| **Related ADRs** | ADR-XXX |
| **Related RFCs** | RFC-XXX |

---

## 1. Executive Summary

Answer these 5 questions in 1-2 paragraphs:
- **Problem**: What's broken or missing?
- **Proposal**: What do we suggest?
- **Why**: What's the benefit?
- **Cost**: What's the effort/risk?
- **Ask**: What decision do we need?

---

## 2. Problem Statement

### Current State (Metrics)
- Deploy time: [X minutes]
- Incidents/month: [X]
- Team size: [X engineers]
- Current bottleneck: [Specific pain]

### Business Impact
- [How does problem hurt the business?]
- [Revenue impact? Churn risk? Velocity blocked?]

### If We Do Nothing
- [What happens in 6 months?]
- [Technical debt grows? System bottleneck?]
- [Market window closes?]

---

## 3. Goals & Non-Goals

### Goals (IN scope)
- ✅ [Goal 1 - specific and measurable]
- ✅ [Goal 2]
- ✅ [Goal 3]

### Non-Goals (OUT of scope)
- ❌ [Not included in this proposal]
- ❌ [Future consideration]
- ❌ [Explicitly excluded]

---

## 4. Context & Constraints

### Constraints
- Deadline: [date or "flexible"]
- Budget: [amount or "cost-neutral"]
- Team capacity: [X people for Y weeks]
- Breaking changes allowed? [Yes/No]

### Assumptions
- [Assumption 1 - verify this?]
- [Assumption 2 - verify this?]
- [Assumption 3 - verify this?]

---

## 5. Stakeholders & Their Concerns

| Stakeholder | Concern | Success Criteria |
|-------------|---------|------------------|
| Product | Time to new features | Weekly releases possible |
| Engineering | Code maintainability | Easy onboarding < 1 day |
| Operations | System stability | SLA 99.9% |
| Security | Data protection | Pass security audit |
| Finance | Cost efficiency | Within 20% budget increase |

---

## 6. Proposal (Main Idea)

### What We Propose
[Clear, concise description of the solution]

### Key Components
- Component A: [What it is, why needed]
- Component B: [What it is, why needed]
- Component C: [What it is, why needed]

### Architecture Sketch
```
[ASCII diagram or high-level flow]

Example:
User → Load Balancer → Pod A
                    → Pod B (autoscale)
                    → Pod C
       → Shared DB (PostgreSQL)
       → Cache (Redis)
```

---

## 7. Alternatives Considered

### Option A: [Name]
**Description**: [What is this?]

**Pros**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]

**Cons**:
- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]

**Why not chosen**: [Reason, or "Maybe future consideration"]

---

*(Repeat for Option B, C, etc.)*

---

## 8. Decision Matrix (Transparent Evaluation)

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Scalability | 5 | 5 | 4 | 2 |
| Simplicity | 4 | 3 | 5 | 2 |
| Cost | 3 | 4 | 3 | 5 |
| **Total Score** | - | 38 | 37 | 21 |

**Note**: Matrix is for transparency, not final decision. Technical judgment > scores.

---

## 9. Detailed Design

### Architecture Changes
[How does the system architecture change?]

### Data Flow
```
[Show major data flows]
```

### Security Considerations
- [ ] Authentication: [How handled?]
- [ ] Authorization: [How enforced?]
- [ ] Data encryption: [Transit & at rest?]
- [ ] Secrets management: [How stored?]

### Performance Considerations
- [ ] Query optimization: [Strategy?]
- [ ] Caching: [Where and how?]
- [ ] Scaling strategy: [Horizontal / Vertical?]
- [ ] Expected latency: [p95 < X ms?]

---

## 10. Rollout Plan

### Phase 1: POC / Validation (Week 1-2)
- [ ] Spike or proof-of-concept
- [ ] Establish baseline metrics
- [ ] Identify unknowns
- [ ] Estimated effort: [X person-weeks]

### Phase 2: Controlled Rollout (Week 3-6)
- [ ] Deploy to staging or limited production (5-10% traffic)
- [ ] Monitor key metrics
- [ ] Gather team feedback
- [ ] Estimated effort: [X person-weeks]

### Phase 3: Full Adoption (Week 7+)
- [ ] Migrate remaining workload
- [ ] Decommission old system
- [ ] Run post-mortem
- [ ] Document lessons learned

### Rollback Plan
If critical issue discovered:
- [ ] Detect: [Alerting criteria? Manual check?]
- [ ] Decide: [Who decides to rollback?]
- [ ] Execute: [Steps to rollback]
- [ ] Estimated time: [X minutes]

---

## 11. Operational Impact

### For Development Team
- [ ] New skills needed: [Training plan?]
- [ ] Development workflow changes: [How?]
- [ ] New tools to learn: [Tooling support?]

### For Operations / DevOps
- [ ] New responsibilities: [What?]
- [ ] Runbook updates: [How?]
- [ ] On-call training: [When?]

### For Infrastructure
- [ ] New resources needed: [Server count, DB capacity?]
- [ ] Cost impact: [Estimated monthly increase?]
- [ ] Capacity planning: [6-month forecast?]

---

## 12. Metrics of Success

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| Deploy time | 40 min | < 10 min | CI/CD log timestamps |
| Incident rate | 6/month | < 2/month | Incident tracking system |
| Feature velocity | 8 stories/sprint | 12 stories/sprint | Sprint tracker |
| Team satisfaction | 6/10 | 8/10 | Quarterly survey |
| Infrastructure cost | $5K/month | $4K/month | Cloud billing |

---

## 13. Open Questions

- [ ] [Question 1? → Who can answer?]
- [ ] [Question 2? → Who can answer?]
- [ ] [Question 3? → Who can answer?]

---

## 14. Review Requests

We need feedback from:

- **Product Team**: [Specific questions?]
- **Backend Team**: [Specific questions?]
- **Frontend Team**: [Specific questions?]
- **Security Team**: [Specific questions?]
- **DevOps Team**: [Specific questions?]

**Please comment by**: YYYY-MM-DD

---

## 15. Related Documentation

- **RFC-XXX**: [Related RFC, if any]
- **ADR-YYY**: [Related ADR, if any]
- **Issue #ZZZ**: [Related GitHub issue]

---

## 16. Implementation Plan (If Approved)

### Timeline
- Week 1-2: POC
- Week 3-4: Phase 1 implementation
- Week 5-6: Phase 2 rollout
- Week 7+: Full adoption + monitoring

### Ownership
- Tech Lead: [Name] - Final decision & architecture
- Implementation Lead: [Name] - Day-to-day execution
- QA Lead: [Name] - Testing strategy

### Success Criteria Tracking
- Dashboard: [Link or description]
- Weekly review: [Day/Time]
- Escalation path: [Who decides if go/no-go?]

---

## 17. Approval & Sign-off

| Role | Name | Status | Date | Notes |
|------|------|--------|------|-------|
| Tech Lead | ... | [ ] Approve | ... | ... |
| Product Manager | ... | [ ] Acknowledge | ... | ... |
| Engineering Lead | ... | [ ] Approve | ... | ... |
| Security Lead | ... | [ ] Approve | ... | ... |

---

## 18. Writing Tips

**RFC Done Well**:
- ✅ Clear problem statement with metrics
- ✅ Multiple options considered transparently
- ✅ Rollout plan with rollback strategy
- ✅ Real metrics of success (not vague goals)
- ✅ Actively solicits feedback
- ✅ Shows clear thinking

**RFC Done Poorly**:
- ❌ Only 1 option presented
- ❌ Vague problem ("improve performance")
- ❌ No cost/effort estimates
- ❌ No rollback plan
- ❌ Presented as done deal, not feedback request
- ❌ No clear owner

> **Golden Rule**: RFC is not to prove you're right. RFC is to find the right answer together through structured thinking.

---

**Author**: [Name]  
**Created**: YYYY-MM-DD  
**Status**: [Status]  
**Document Location**: [Link]

---

**Contact**: Mr. Đức | duch9707@gmail.com | 0389 086 502
