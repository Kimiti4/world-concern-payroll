# ESAP Boundary and Artifact Handoff

ESAP owns generic generation. This repository owns World Concern payroll requirements, accepted source, payroll tests, configuration, deployment and release evidence.

A handoff may contain generated source and SHA-256 hashes; specification version/hash and requirement IDs; ESAP commit and generator version; backend/compiler versions; dependency lockfiles; exact commands; raw verification outputs; limitations and reviewer disposition.

A generation transcript, generic API test, or statement that code was generated successfully is not sufficient payroll acceptance evidence.

For each handoff: review provenance; verify hashes; inspect diffs for secrets, unsafe defaults, licensing/IP concerns and scope drift; build/test from a clean checkout; run payroll-specific tests and independent statutory vectors; record accepted commit/evidence; quarantine unverified artifacts rather than overwriting accepted source.
