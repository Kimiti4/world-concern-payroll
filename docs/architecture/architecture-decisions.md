# Architecture Decision Records

## ADR-0001: Separate payroll repository from ESAP
- **Status:** Proposed
- **Context:** ESAP is a generic generation platform; payroll has buyer-specific compliance, data and acceptance obligations.
- **Decision:** Keep payroll requirements, accepted application source, payroll tests, deployment and release evidence here. Keep ESAP separate.
- **Handoff:** Transfer versioned generated artifacts with provenance manifest, hashes, dependency lockfiles and test outputs.
- **Runtime boundary:** The payroll application must not require ESAP at runtime unless separately justified and approved.
- **Acceptance:** A clean checkout can build/test the payroll artifact without checking out ESAP; imported artifacts are pinned and independently verified.
