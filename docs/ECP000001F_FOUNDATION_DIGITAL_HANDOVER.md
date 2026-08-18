# ECP-000001F — Foundation Digital Handover and Lifecycle Assurance

ECP-000001F consumes the controlled ECP-000001E transmittal and creates an auditable lifecycle dossier. It verifies every checksum independently, records custody, evaluates acceptance gates, measures the constitutional acceleration target and produces findings for continuous improvement.

## Meaning of Level 5

The framework reports Level 5 only when repeatable delivery, traceability, automated quality gates, acceleration evidence and a continuous-improvement loop are all present. A reference-case Level 5 result proves framework capability; it is not an audited organization-wide maturity certification.

## Safety

Lifecycle acceptance does not grant construction approval. Construction acceptance remains false unless the upstream ECP-E package contains verified official-code and professional approval evidence.

```powershell
$env:PYTHONPATH = ".\src"
& ".\.venv\Scripts\python.exe" -m aias_foundation_handover.cli doctor
& ".\.venv\Scripts\python.exe" -m aias_foundation_handover.cli validate
& ".\.venv\Scripts\python.exe" -m aias_foundation_handover.cli release --workspace ecp000001f_outputs
```
