# L3 Production BIM 004AX

## Real AIAS-Side Sync Representation & Conflict Policy Integration

Adds a persistent AIAS-side per-entity synchronization representation.

For every document-scoped AutoCAD identity it stores:

- certified baseline fingerprint;
- AIAS-side fingerprint;
- AutoCAD readback fingerprint.

The triadic comparison deterministically classifies:

- `IN_SYNC`
- `AIAS_CHANGED`
- `AUTOCAD_CHANGED`
- `BOTH_CHANGED`
- `MISSING_IN_AIAS`
- `MISSING_IN_AUTOCAD`

Safety policy:

- AIAS-only change -> push remains blocked pending explicit live write gate.
- AutoCAD-only change -> safe pull/read into AIAS.
- Both changed -> manual conflict.
- Missing in AutoCAD -> review delete/recreate; never automatic.
- Missing in AIAS -> create AIAS representation.
- No automatic deletion.
- No vendor APIs or AutoCAD COM calls in this module.
- No Save / SaveAs / SendCommand / Dispatch / CreateObject.

Persistence uses atomic replace plus an internal SHA-256.
