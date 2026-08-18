# ACE-000001 - AIAS Context Engine

ACE converts the active AIAS repository into a versioned continuity source of truth.

## Capabilities

- repository and component inventory
- current-program and roadmap reconciliation
- permanent architectural rules
- decision and capability registry
- AIAS University state
- lightweight knowledge graph
- versioned context snapshots
- SHA-256 integrity validation
- continuity prompt and next-task generation

## Commands

```powershell
cd "C:\AIAS\AI_Architecture_Studio"
$env:PYTHONPATH = ".\src"

& ".\.venv\Scripts\python.exe" -m aias_context_engine.cli doctor
& ".\.venv\Scripts\python.exe" -m aias_context_engine.cli build --project-root "." --output "ACKC"
& ".\.venv\Scripts\python.exe" -m aias_context_engine.cli validate --context ".\ACKC\MASTER_CONTEXT.json"
& ".\.venv\Scripts\python.exe" -m aias_context_engine.cli show --context ".\ACKC\MASTER_CONTEXT.json"
```

`ACKC/MASTER_CONTEXT.json` is generated evidence, not a substitute for repository validation. ACE must be regenerated after every validated macro-delivery.
