# Payroll Evidence Policy

Each evidence record should include evidence ID, requirement IDs, claim supported, repository and tested SHA, tool/runtime versions, exact command or workflow URL, timestamp/environment, result, raw output/artifact and hash, reviewer/date, limitations and linked defects.

Rules:
- Tie evidence to an exact commit and reproducible command.
- Build success is not functional correctness.
- Generated code remains a candidate until payroll-specific review/tests pass.
- Simulated evidence cannot satisfy a live runtime gate.
- Missing, stale, skipped or ambiguous evidence is not a pass.
- Never store production employee data, bank details, credentials or unredacted payroll outputs in Git.
