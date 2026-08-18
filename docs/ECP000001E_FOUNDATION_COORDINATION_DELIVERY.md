# ECP-000001E — Foundation Coordination and Delivery Framework

ECP-000001E consumes the complete ECP-000001D technical package and produces a controlled transmittal with completeness evidence, SHA-256 revision manifest, issue register, approval state and versioned release archive.

## Safety and professional responsibility

The default status is `REFERENCE_DELIVERY`. `CONSTRUCTION_APPROVED` is impossible unless verified official-code status and complete professional approval evidence are supplied. Generated material requires qualified human review.

## Commands

```powershell
$env:PYTHONPATH = ".\src"
& ".\.venv\Scripts\python.exe" -m aias_foundation_delivery.cli doctor
& ".\.venv\Scripts\python.exe" -m aias_foundation_delivery.cli validate
& ".\.venv\Scripts\python.exe" -m aias_foundation_delivery.cli release --workspace ecp000001e_outputs
```
