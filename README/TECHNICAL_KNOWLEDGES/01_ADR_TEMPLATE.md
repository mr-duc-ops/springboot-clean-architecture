# ADR Template - Architecture Decision Record

Use this template to document significant architectural decisions.

---

## ADR-XXX: [Tên quyết định, dùng động từ]

**Example names:**
- "Adopt PostgreSQL as Primary Database"
- "Use Modular Monolith for Phase 1"
- "Implement Multi-Tenant Architecture with Separate Databases"

---

## Metadata

| Field | Value |
|-------|-------|
| **Status** | `Proposed` / `Accepted` / `Rejected` / `Superseded` / `Deprecated` |
| **Date** | YYYY-MM-DD |
| **Owner** | [Name / Team] |
| **Decision Scope** | `System` / `Domain` / `Service` / `Platform` / `Org-wide` |
| **Priority** | `Critical` / `High` / `Medium` / `Low` |
| **Related ADRs** | ADR-001, ADR-014 |
| **Related RFCs** | RFC-XXX |
| **Tags** | #scalability, #security, #maintainability |

---

## 1. Executive Summary

**Problem**: [What problem are we solving?]

**Solution**: [What decision are we making?]

**Impact**: [Why matters? What changes?]

---

## 2. Context & Problem Statement

### Current State
- **System scale**: [Users, traffic, infrastructure]
- **Team size**: [# engineers, expertise]
- **Current architecture**: [Brief description]
- **Current pain points**: [Specific metrics: deploy time 45 min, MTTR 2h, incidents/month, etc.]

### Business Need
[What business driver requires this decision?]

### Why Now?
[What triggers this decision at this point?]

### Constraints
- Deadline: [date]
- Budget: [constraint]
- Team capacity: [people / hours available]
- Other: [breaking APIs, compliance requirements, etc.]

---

## 3. Stakeholders & Their Concerns

| Stakeholder | Concern | Success Criteria |
|-------------|---------|------------------|
| Product | [What matters to Product?] | [Measurable success] |
| Engineering | [What matters to Eng?] | [Measurable success] |
| Operations | [What matters to Ops?] | [Measurable success] |
| Security | [What matters to Security?] | [Measurable success] |

---

## 4. Decision Drivers (Ranking by importance)

| Driver | Priority | Definition |
|--------|----------|-----------|
| Scalability | High | System must handle 10x growth |
| Simplicity | High | Easy for team to maintain |
| Cost | Medium | CapEx + OpEx reasonable |
| Security | High | Minimize risk surface |
| Time-to-market | Medium | Feature velocity important |

---

## 5. Considered Options

### Option A: [Name]
**Description**: [What is this approach?]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Risks**:
- [Risk 1 - mitigation]
- [Risk 2 - mitigation]

**Cost Estimate**:
- Build: [effort / $ estimate]
- Run (annual): [$ estimate]
- Learning curve: [High / Medium / Low]

**Reversibility**: `Easy` / `Medium` / `Hard`

---

*(Repeat for Option B, C, etc.)*

---

## 6. Decision Matrix (Scoring)

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Scalability | 5 | 5 | 4 | 2 |
| Simplicity | 4 | 5 | 3 | 4 |
| Cost | 3 | 5 | 4 | 2 |
| **Total Score** | - | 45 | 35 | 24 |

---

## 7. Decision Outcome

**Chosen Option**: [Option name]

**Why This Option Wins**:
- [Key reason 1]
- [Key reason 2]
- [Trade-off accepted]

**Why Not Others**:
- Option B: [Reason eliminated]
- Option C: [Reason eliminated]

**Decision Confidence**: `High` / `Medium` / `Low`

---

## 8. Impact on 4+1 Views

| View | Impact |
|------|--------|
| **Scenario** | [How do user journeys change?] |
| **Logical** | [Domain model changes? New Bounded Contexts?] |
| **Development** | [Code structure changes? Module layout?] |
| **Process** | [Runtime behavior? Concurrency? Scaling changes?] |
| **Physical** | [Infrastructure changes? HA/DR strategy?] |

---

## 9. Consequences

**Positive**:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Negative**:
- [Drawback 1]
- [Drawback 2]

**Trade-offs Accepted**:
- [We accept X to gain Y]
- [Migration cost justified by long-term gain]

---

## 10. Risks & Mitigations

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|-----------|
| [Risk 1] | High | Medium | [Mitigation strategy] |
| [Risk 2] | Medium | High | [Mitigation strategy] |
| [Risk 3] | Low | Low | [Mitigation strategy] |

---

## 11. Rollout Plan

**Phase 1 - Validation** (2 weeks)
- POC or spike
- Establish baseline metrics
- Security review

**Phase 2 - Controlled Rollout** (2-4 weeks)
- Deploy to 5-10% of traffic
- Monitor closely
- Gather feedback

**Phase 3 - Full Adoption** (ongoing)
- Migrate remaining workload
- Decommission old system
- Document lessons learned

**Rollback Plan**: [How to revert if critical issue?]

---

## 12. Success Metrics

| Metric | Baseline | Target | How Measured |
|--------|----------|--------|--------------|
| [Metric 1] | [current] | [desired] | [method] |
| [Metric 2] | [current] | [desired] | [method] |
| [Metric 3] | [current] | [desired] | [method] |

---

## 13. Revisit Trigger

This decision should be revisited if:
- [Condition 1, e.g., traffic grows > 5x]
- [Condition 2, e.g., team doubles]
- [Condition 3, e.g., cost exceeds threshold]

**Review cadence**: Quarterly / Annually / Event-driven

---

## 14. Approvals

| Role | Name | Decision | Date |
|------|------|----------|------|
| Tech Lead | ... | Approve / Reject | YYYY-MM-DD |
| Engineering Manager | ... | Approve / Reject | YYYY-MM-DD |
| Product Manager | ... | Acknowledge | YYYY-MM-DD |
| Security Lead | ... | Approve / Reject | YYYY-MM-DD |

---

## 15. Changelog (Optional)

| Date | Change | By |
|------|--------|-----|
| YYYY-MM-DD | Status changed to Accepted | [Name] |
| YYYY-MM-DD | Superseded by ADR-XXX | [Name] |

---

**Owner**: [Name]  
**Last Updated**: YYYY-MM-DD  
**Document Location**: [Link to repo location]

---

**Contact**: Mr. Đức | duch9707@gmail.com | 0389 086 502