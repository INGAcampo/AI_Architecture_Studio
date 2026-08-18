# Sprint L3 Production BIM 004BN v1.1
## AutoCAD 2027 Roundtrip Sync Orchestration Consolidation

### Repair scope
v1.1 is a narrow correction after the first 004BN targeted test run exposed two
contract mismatches. The failed v1 installer rolled back.

1. NEW_IN_AUTOCAD is a discovery state before an AIAS/baseline representation exists.
   AIASSyncRecord's persistent validation intentionally requires baseline_fingerprint,
   so the coordinator now recognizes exactly:
   baseline=None, aias=None, autocad=present
   before delegating persistent records to assess_record().
2. Duplicate AutoCAD Handle validation now runs before duplicate AIAS ID validation,
   because Handle is the primary AutoCAD identity invariant and duplicate Handles can
   naturally cause duplicate derived AIAS IDs.

No changes are made to autocad_persistent_sync_state.py or autocad_sync_orchestrator.py.

### Consolidated states
- IN_SYNC
- AIAS_CHANGED
- AUTOCAD_CHANGED
- BOTH_CHANGED
- MISSING_IN_AIAS
- MISSING_IN_AUTOCAD
- NEW_IN_AUTOCAD

### Safety
Dry-run only. No COM/vendor APIs, no AddLine/Delete/Save/SaveAs/SendCommand and no
automatic AutoCAD write/delete permission. Persistent baseline, bindings and sync state
remain unchanged. Global regression remains deferred until source changes are complete.
