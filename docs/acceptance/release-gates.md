# Payroll Verification and Release Gates

**Status:** Proposed gates. World Concern must approve contractual acceptance criteria and tolerances.

1. Requirements baseline: TOR traceability complete; scope, policies and exclusions dispositioned.
2. Calculation correctness: independently reviewed vectors cover salary components, deductions, rounding, arrears, loans, leave inputs, cost-centre allocations and required frequencies.
3. Statutory correctness: dated authoritative sources, effective-dated rules, independent review and boundary/historical-period tests.
4. Migration: source-to-target counts, exception report and signed control-total reconciliation.
5. Authorization/privacy: role-negative tests, separation of duties, employee data isolation, audit coverage and agreed security tests.
6. Integrations: contract tests, failure/retry and duplicate handling, reconciliation.
7. Parallel payroll: two consecutive agreed runs reconciled against the approved reference process; material variances resolved or formally dispositioned.
8. Payslips/reports: content, access and totals reconciled.
9. Backup/restore: witnessed restore against agreed RPO/RTO.
10. Training/documentation: users trained; guides and runbooks delivered.
11. Release: no release-blocking defects; evidence reviewed; authorized buyer sign-off recorded.

CI passing alone is not acceptance. Use synthetic test data unless a separate secure, lawful and approved process requires otherwise.
