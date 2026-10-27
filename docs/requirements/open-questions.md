# Payroll Open Questions

| ID | Question | Why it matters | Owner | Status | Decision/evidence |
|---|---|---|---|---|---|
| Q-001 | Which HR and accounting systems and interfaces are in scope? | Integration scope, cost and schedule | Buyer/bidder | OPEN | |
| Q-002 | Which pay groups, calendars and cut-off rules apply? | Payroll correctness | Buyer | OPEN | |
| Q-003 | Which pension schemes and other deductions apply? | Statutory/policy configuration | Buyer/payroll reviewer | OPEN | |
| Q-004 | What are the approved overtime, allowance, benefit, bonus, loan and leave policies? | Calculation rules | Buyer | OPEN | |
| Q-005 | What are the source systems for employee, leave and cost-centre data? | Migration and reconciliation | Buyer | OPEN | |
| Q-006 | What hosting region, retention, RPO and RTO are required? | Privacy, security and continuity | Buyer/bidder | OPEN | |
| Q-007 | What bank schedule format is required? Payment execution remains outside scope unless separately agreed. | Payment boundary | Buyer | OPEN | |
| Q-008 | What acceptance tolerances, parallel-run periods and sign-off roles apply? | Release decision | Buyer | OPEN | |
| Q-009 | Which historical records must be migrated? | Migration scope | Buyer | OPEN | |
| Q-010 | What support hours, response targets and maintenance terms are required? | Support and recurring cost | Buyer/bidder | OPEN | |
| Q-011 | What monetary input precision and rounding rule apply to derived amounts, and how should residual cents be assigned in cost-centre splits? | Deterministic payroll results and independent test-vector approval | Buyer/payroll and finance reviewers | OPEN | Proposed engineering defaults are recorded in `payroll-calculation-spec.md` and `calculation-decision-register.md`; reviewer approval remains pending. |
| Q-012 | Which earning and deduction components are included in gross, taxable pay and the cost-allocation base, and what is the approved treatment for deductions exceeding net/gross pay? | Payroll correctness, statutory bases, cost-centre reconciliation and exception handling | Buyer/payroll and finance reviewers | OPEN | Arithmetic vectors define gross/net arithmetic only; they do not determine taxable bases, allocation-base policy, carry-forward, or recovery. See `calculation-decision-register.md`. |
| Q-013 | Are zero gross, empty earnings, zero deductions, and zero allocation base valid production cases? | Prevents missing data from being confused with legitimate zero-value cases | Buyer/payroll reviewer | OPEN | Draft register PD-011; do not infer production eligibility from synthetic tests. |
| Q-014 | What are the required calculation audit fields, immutable rule-version references, and rerun/correction controls? | Reproducibility, audit, and safe payroll corrections | Buyer payroll owner + security/audit owner | OPEN | Draft register PD-013 and PD-014; needs workflow and access-control approval. |
| Q-015 | Who is authorized to approve the calculation contract and independently validate expected outputs? | Establishes a defensible acceptance baseline | Buyer payroll owner | OPEN | Required reviewer template is in `calculation-decision-register.md`; no approval is implied. |
