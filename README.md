# World Concern Payroll

**Status:** Initial scaffold only. This is not a complete, certified, or production-ready payroll application.

## Repository boundary
- This repository owns the payroll requirements, application, statutory-rule decisions, payroll-specific tests, deployment, security controls, and release evidence.
- `Kimiti4/autonomous-API-Gen` remains the separate ESAP generation platform.
- ESAP may provide versioned generated artifacts and provenance manifests. This repository independently reviews, builds, and tests them.
- The deployed payroll application must not require ESAP at runtime unless separately justified and approved.

## First priorities
1. Baseline the original TOR and trace every requirement to tests and acceptance evidence.
2. Resolve buyer questions about policies, integrations, statutory scope, hosting, security, and acceptance.
3. Prepare independently reviewed payroll calculation vectors before implementing statutory rules.
4. Define architecture and threat model.
5. Establish repository-local CI and reproducible builds.
6. Generate candidate implementations with ESAP only against the same reviewed specification and tests.
7. Compare candidates on payroll-specific correctness, security, maintainability, and operational fit.
8. Block production release until all agreed gates pass and World Concern signs off.

## Evidence vocabulary
`PASS`, `FAIL`, `NOT_RUN`, `NOT_APPLICABLE` (with justification). Missing, skipped, simulated, or stale evidence is not a pass.

Never commit real employee data, bank details, production exports, credentials, or secrets. Use synthetic fixtures.
