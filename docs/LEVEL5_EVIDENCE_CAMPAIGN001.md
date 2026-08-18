# LEVEL5-EVIDENCE-CAMPAIGN-001

Sistema operativo de captura longitudinal para la madurez organizacional AIAS. Registra proyectos, criterios, métricas, revisiones profesionales, recuperaciones, incidentes, mejoras y atestaciones externas en un ledger JSONL autenticado y encadenado.

La clave de firma se suministra externamente mediante `AIAS_LEVEL5_SIGNING_KEY` y debe tener al menos 32 bytes. No se incluye ninguna clave productiva en código, instaladores ni repositorio.

```powershell
$env:AIAS_LEVEL5_SIGNING_KEY = '<clave-externa-de-al-menos-32-bytes>'
python -m aias_level5_assurance.cli --ledger evidence/level5.jsonl record --event PROJECT_STARTED --evidence-id L5E-000001 --observed-at 2026-08-03T12:00:00+00:00 --payload '{"project_id":"PRJ-001","source":"orden firmada"}'
python -m aias_level5_assurance.cli --ledger evidence/level5.jsonl status
```

El sistema rechaza fechas futuras, identificadores duplicados, criterios no normativos, registros sin fuente y auditorías internas o no conformantes. `eligible_for_independent_audit` y `ready_for_formal_level5_assessment` no equivalen a Nivel 5: el ledger nunca establece por sí mismo la madurez organizacional; la decisión corresponde al evaluador formal sobre evidencia y atestación independientes verificadas.
