# Payroll Calculation Decision Register

**Document version:** draft-0.1  
**Status:** Proposed decisions for review; none are buyer-approved.  
**Applies to:** `docs/requirements/payroll-calculation-spec.md` draft-0.1 and synthetic fixtures only.  
**Rule:** No item in this register becomes payroll policy until the named authorized reviewer records an explicit decision and effective date. These proposed engineering defaults are not legal advice and do not define Kenyan statutory calculations.

## Decision record

| ID | Topic | Draft proposal for review | Why it is proposed | Required decision owner | Status |
|---|---|---|---|---|---|
| PD-001 | Money representation | Continue to accept canonical non-negative decimal strings only; KES values have at most two fractional digits. Reject JSON numbers, signs, exponent notation, commas, and whitespace. | Avoid binary floating-point and ambiguous parsing. | Payroll/finance reviewer + technical lead | PROPOSED |
| PD-002 | Derived line rounding | Multiply quantity by unit rate using exact decimal arithmetic; round each derived earning line once to two decimals with ROUND_HALF_UP; sum rounded lines without rounding running totals. | Deterministic cross-language arithmetic. | Payroll/finance reviewer | PROPOSED |
| PD-003 | Quantity precision | Permit up to four fractional digits for quantities; rates remain monetary strings with two decimal places maximum. | A bounded, testable input contract; does not assert overtime policy. | Payroll reviewer + relevant operations owner | PROPOSED |
| PD-004 | Gross | Gross is the sum of earning lines already determined by approved component rules. Component labels alone do not determine taxability or statutory bases. | Keeps arithmetic separate from tax/legal classification. | Payroll reviewer | PROPOSED |
| PD-005 | Taxable/statutory bases | Do not infer taxable, pensionable, SHIF, NSSF, housing levy, or other statutory bases from gross or labels. Each requires its own effective-dated, source-backed rule and independent expected cases. | Prevents undocumented statutory assumptions. | Authorized payroll/statutory reviewer | BLOCKED — SOURCE/RULE REVIEW |
| PD-006 | Net pay | For this arithmetic-only contract, reject when explicit deductions exceed gross; do not cap, carry forward, or silently recover the difference. Production exceptions require a separately approved workflow. | Prevents silent alteration of inputs. | Payroll/finance reviewer | PROPOSED |
| PD-007 | Cost-centre allocation base | Require an explicit allocation base supplied by the caller. Do not assume it is gross, basic salary, taxable pay, or net pay. | Allocation basis is an accounting policy choice. | Finance owner + payroll reviewer | OPEN — BUYER DECISION |
| PD-008 | Allocation rounding | Convert the supplied base to integer cents, use largest-remainder allocation, break ties by ascending cost-centre ID using ordinal case-sensitive order, and sort outputs by ID. | Allocations reconcile exactly and are deterministic. | Finance reviewer + technical lead | PROPOSED |
| PD-009 | Negative corrections/reversals | Reject negative earning and deduction amounts in this contract. Model reversals, refunds, overpayment recovery, and correction runs as a separately specified workflow with audit history. | Avoids ambiguous sign semantics in the initial contract. | Payroll/finance reviewer | PROPOSED |
| PD-010 | Pay periods | Validate inclusive ISO start/end dates and frequency label only. Do not infer pay dates, working days, cut-offs, proration, or calendar boundaries from the frequency. | Separates arithmetic contract from calendar/employment policy. | Payroll operations owner | PROPOSED |
| PD-011 | Empty/zero cases | Require reviewer decision on whether zero gross, empty earnings, zero deductions, and zero allocation base are valid in production; until decided, fixtures can test arithmetic behavior but must not define operational eligibility. | These cases may be legitimate or may indicate missing input. | Payroll reviewer | OPEN — BUYER DECISION |
| PD-012 | Error precedence | Preserve the documented validation order and return one stable error code with no partial result. Add vectors for inputs containing multiple defects to lock precedence. | Enables consistent behavior across generated candidates. | Technical lead + independent test reviewer | PROPOSED |
| PD-013 | Rule versioning | Every production calculation must identify the versioned rule set, effective date, input snapshot/reference, and calculation result; reruns must not silently use changed rules. | Enables audit and reproducibility. | Payroll owner + security/audit owner | PROPOSED |
| PD-014 | Approval and locking | Define distinct prepare, review, approve, lock, reverse, and rerun permissions; record actor, timestamp, action, rule version, and reason for changes. | Prevents a calculation result being mistaken for an approved payroll. | Buyer payroll owner + security owner | OPEN — BUYER DECISION |

## Required reviewer response

For each decision, record one of: **APPROVED**, **REJECTED**, or **REVISE**. Do not mark a decision approved by inference from silence or from passing tests.

- Decision ID:
- Outcome:
- Approved wording or replacement:
- Rationale / source reference:
- Effective date (if applicable):
- Reviewer name and role:
- Review date:
- Evidence or ticket reference:

## Gate to specification baseline

Do not mark the calculation specification buyer-approved until all production-affecting decisions are resolved, statutory rules have authoritative source records and effective dates, expected results have been independently prepared or checked, and the authorized reviewer has signed the decision record. Passing the test suite demonstrates consistency with the current draft contract only.
