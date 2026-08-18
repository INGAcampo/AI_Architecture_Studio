# L3 Production BIM 004AU

## Persistent AIAS Identity Binding Core

Adds an AIAS-side, document-scoped persistent registry for:

`AIAS ID <-> AutoCAD Handle`

Properties:

- Stable identity rule: `autocad:<document-key>:<HANDLE>`.
- One-to-one uniqueness of AIAS IDs and Handles.
- Fingerprint retained with each binding.
- Atomic JSON persistence using temp-file + `os.replace`.
- Internal payload SHA-256 validation.
- Load-time corruption/tamper rejection.
- Reconciliation against a source binding set.
- Certified-baseline adapter.
- No AutoCAD COM calls.
- No `Save`, `SaveAs`, `SendCommand`, `Dispatch`, or `CreateObject`.

004AU installs only the persistent identity core. It does not materialize or
modify any live AutoCAD entity.
