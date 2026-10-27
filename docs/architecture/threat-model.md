# Payroll Security and Privacy Threat Model

**Status:** Initial checklist, not a completed assessment.

## Assets
Employee identity/contact data; salary, deductions and payslips; bank instructions and exports; credentials/sessions; statutory configuration; approvals; audit records; backups; integration secrets.

## Threats
Unauthorized access or cross-employee exposure; privilege escalation; payroll manipulation or duplicate processing; data leakage through exports/logs/email/backups; compromised credentials; malformed imports; ransomware/deletion; dependency compromise; unauthorized statutory-rule changes; accidental commitment of sensitive data.

## Controls to design and verify
Least-privilege role matrix and maker-checker approval; secure authentication and session policy; MFA as agreed; encryption in transit/at rest; secrets management; validation and safe error handling; protected audit events; retention/deletion; backup and witnessed restore; dependency pinning and vulnerability review; incident response; access review and release approval.

For each control, record threat, design, implementation, test evidence, owner and residual risk. Do not claim certification or completed operational controls without evidence.
