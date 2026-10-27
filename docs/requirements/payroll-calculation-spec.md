# Payroll Calculation Specification

**Version:** draft-0.1  
**Status:** Proposed, not buyer-approved.  
**Purpose:** Define a deterministic, implementation-neutral arithmetic contract for synthetic payroll test cases. This document does not define Kenyan statutory rules or constitute a production payroll specification.

## 1. Scope and explicit non-goals

The calculation contract covers:

- Earnings entered as fixed monetary amounts or derived from a non-negative quantity multiplied by a monetary unit rate.
- Positive arrears or back-pay entries treated as earnings in the selected pay period.
- Deductions supplied as monetary amounts, including synthetic externally calculated statutory amounts.
- Gross, deduction total and net pay.
- Optional allocation of a supplied monetary base among cost centres using integer basis-point weights.
- Deterministic validation failures for invalid amounts, duplicate line IDs, deductions exceeding gross, and invalid allocation weights.

It does **not** calculate PAYE, NSSF, SHIF, Affordable Housing Levy, pension, taxable benefits, overtime entitlement, leave entitlement, loan schedules, prorating, or any other legal or employer policy. Statutory amounts in examples are synthetic fixtures only. A future payroll implementation may use these vectors only after an authorized reviewer approves the applicable rules and expected results.

## 2. Numeric representation

- Currency is KES in the current project scope. Monetary inputs and outputs are decimal strings, never binary floating-point values.
- A monetary value is non-negative and has at most two fractional digits. Negative earnings, deductions, and allocations are rejected. Corrections, reversals, refunds, and recovery of overpayments need a separately approved workflow and are out of scope here.
- A calculated line may have more than two fractional digits internally. Round that line once, to two decimal places, using decimal `ROUND_HALF_UP`, before adding it to a payroll total.
- Do not round a running total after each addition; sum already rounded line amounts exactly.
- A quantity has at most four fractional digits and a unit rate is a non-negative monetary amount with at most two fractional digits.
- Reject JSON numeric values for money, quantities, and rates. Accept canonical decimal strings only; do not silently coerce floats, commas, exponent notation, whitespace, or negative values.

## 3. Period and frequency

Every calculation names an ISO-8601 inclusive period start and end, with frequency `weekly`, `biweekly`, or `monthly`. The dates must parse and end on or after start. This arithmetic contract does not infer a calendar, pay date, cut-off, number of workdays, proration rule, or statutory period from the frequency. Those are approved payroll-policy inputs.

## 4. Earnings

Each earning has a unique, non-empty ID, a type, and exactly one of:

1. `amount`: a non-negative KES amount with no more than two decimal places; or
2. `quantity` and `unit_rate`: quantity multiplied by unit rate, rounded once to two decimal places using `ROUND_HALF_UP`.

The line type is descriptive, not a rule. Salary, allowance, bonus, overtime, arrears, and back pay are all amounts already determined under separately approved policies. A positive arrears/back-pay amount is included in gross in this period. Negative adjustments are rejected under this contract.

`gross = sum(rounded earning line amounts)`.

## 5. Deductions and net pay

Each deduction has a unique, non-empty ID, a type, a non-negative KES amount, and an explicit tax-treatment label:

- `pre_tax`
- `post_tax`
- `externally_calculated_statutory`

The label is metadata only in this contract. No tax base or statutory amount is derived from it. Production use of `externally_calculated_statutory` requires a separately approved, effective-dated source/rule record and independent expected cases.

`deductions_total = sum(deduction line amounts)`  
`net = gross - deductions_total`

Reject the calculation if deductions exceed gross; do not emit negative net pay, silently cap a deduction, or carry a balance forward. A future policy may define such cases explicitly.

## 6. Cost-centre allocation

Allocation is optional and does not change gross, deductions, or net. When present:

- The caller supplies an `allocation_base` as a non-negative KES amount. The buyer-approved policy must define which earnings that base includes; the calculator does not infer it.
- Each unique cost-centre ID has a positive integer `basis_points` weight. The weights must sum to exactly 10,000 (100%).
- Convert the base to integer cents. For each centre, compute `base_cents * basis_points / 10000`; initially assign the floor of each exact share.
- Distribute any remaining cents in descending fractional-remainder order. Resolve equal remainders by ascending cost-centre ID using ordinal, case-sensitive order.
- Output allocations in ascending cost-centre ID order. Their sum must equal the supplied base exactly.

This method is deterministic for all compiler/backend candidates. Whether the base is gross salary, selected earnings, or another approved amount remains a buyer decision.

## 7. Validation errors

Invalid cases produce one stable error code and no payroll result:

| Code | Condition |
|---|---|
| `INVALID_PERIOD` | Missing/invalid ISO date or end date precedes start date |
| `INVALID_MONEY` | Money is not a canonical, non-negative decimal string with at most two fractional digits |
| `INVALID_QUANTITY` | Quantity/rate is invalid, missing, or has more than four fractional digits |
| `INVALID_EARNING` | Earning has both or neither of `amount` and `quantity`/`unit_rate` |
| `INVALID_DEDUCTION` | Deduction has an unsupported tax-treatment label or malformed deduction structure |
| `DUPLICATE_LINE_ID` | Earning or deduction IDs are empty or duplicated within their line collection |
| `DEDUCTIONS_EXCEED_GROSS` | Total deductions exceed gross |
| `INVALID_ALLOCATION` | Allocation IDs/weights are invalid, duplicated, non-positive, or do not sum to 10,000 |

Validation order for deterministic error reporting: period; earnings shape and values; duplicate earning IDs; deduction shape and values; duplicate deduction IDs; deductions-versus-gross; allocation. A missing member of a quantity/rate pair is `INVALID_QUANTITY`; an earning containing both amount and quantity/rate, or neither, is `INVALID_EARNING`. For a line with more than one defect, return the first error under this order.

## 8. Required buyer decisions before baselining

Confirm pay calendars and cut-offs, approved earning and deduction policies, hourly/overtime basis and rounding, arrears/reversal treatment, leave and loan rules, pre-tax treatment, applicable statutory schemes and their effective dates, the definition of the cost-allocation base, allocation precision and tie policy, negative-net handling, and authorized reviewers. Track these in `docs/requirements/open-questions.md`. Do not replace an unresolved decision with an assumed legal or employer rule.

## 9. Test vectors and evidence

`tests/vectors/payroll-calculation-vectors.json` contains synthetic input/expected-output cases and expected validation failures. The accompanying test-only reference oracle checks that the fixture arithmetic and rejection cases satisfy this document. These draft vectors still require independent payroll-reviewer approval before they can be used as contractual payroll acceptance evidence. The oracle is not application code, payroll software, statutory validation, or buyer acceptance evidence.

Run the local fixture checks with:

```text
python -m unittest discover -s tests -v
```

After policy and statutory decisions are approved, add independently prepared expected results and reviewer metadata. A vector is not independent merely because it was copied from the implementation under test.
