# ECP-000001D - Foundation Detailing and Documentation

ECP-000001D is the immediate production consumer of the foundation object, calculation and code-check chain.

## Inputs

- ECP-000001A Foundation Object Library
- ECP-000001B Foundation Calculation Engine
- ECP-000001C Foundation Code Check Framework

## Generated artifacts

- foundation plan in SVG
- foundation section in SVG
- reinforcement bar schedule in CSV
- concrete, formwork, excavation and reinforcement quantities
- complete technical package in JSON
- human-readable technical report in Markdown
- QA reference cases
- release archive with SHA-256 checksum

## Commands

```powershell
cd "C:\AIAS\AI_Architecture_Studio"
$env:PYTHONPATH = ".\src"

& ".\.venv\Scripts\python.exe" -m aias_foundation_documentation.cli doctor
& ".\.venv\Scripts\python.exe" -m aias_foundation_documentation.cli validate
& ".\.venv\Scripts\python.exe" -m aias_foundation_documentation.cli release --workspace ".\ecp000001d_outputs"
```

## Regulatory limitation

The bundled generic code pack is `REFERENCE_ONLY`. Generated details are not construction documents until an applicable verified official code pack is used and a qualified professional completes the required review and approval.
