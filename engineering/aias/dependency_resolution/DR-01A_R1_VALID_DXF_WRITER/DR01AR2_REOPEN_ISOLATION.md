# DR-01A-R2 — Reopen inspection timeout isolation

## Scope

This evidence reopens `A-101.dwg` through AutoCAD 2027 Core Console in read-only mode. It does not alter the DXF writer, drawing model, DWG, or any PRO program artifact.

## Result

- Backend: `AutoCAD 2027 accoreconsole.exe` (ACADVER `26.0`).
- Sentinel: pass — PID 38488, exit code 0, 2.552 s.
- Inspection: pass — PID 46504, exit code 0, 2.369 s.
- Reopened entities: 13.
- Recovered entity types: `LINE`, `LWPOLYLINE`, `TEXT`.
- Recovered layers: `A-DIMS`, `A-DOOR`, `A-GRID`, `A-TEXT`, `A-WALL`, `S-STRUCT`.
- Recovered handles: `7B`, `7C`, `7D`, `7E`, `7F`, `80`, `87`, `88`, `89`, `8D`, `91`, `92`, `93`.

The former timeout was therefore caused by the previous inspector execution path (external LISP loading / incomplete inspection control), not by DXF validity, DWG opening, or Core Console shutdown. The new inspector uses only read-only AutoLISP expressions, writes an external text file, calls `princ`, and explicitly calls `_.QUIT`.

## Expected mappings and differences

The 13 source CAD entities are retained as 13 DWG entities. The intentionally degraded mappings are: level/bubble/block/dimension as equivalent `TEXT` or `LINE` primitives, and rectangles as `LWPOLYLINE`. They are `EXPECTED_MAPPING`, not loss hidden by the validator. No native `DIMENSION` or `INSERT` entity is claimed.

`AIAS_CAD_ENTITY_ID → AutoCAD handle` is not embedded in the DWG. The R1 sidecar records AIAS IDs and source representations, and R2 records recovered handles, but the current DXF writer does not emit registered XData/APPID metadata. Consequently this run cannot certify persistent per-entity ID/handle recovery.

## Verdict

`BLOCKER_METADATA_MAPPING_NOT_EMBEDDED`.

The reopen-inspection timeout is resolved. The remaining blocker is intentionally isolated: native DWG output and independent read-only reopening are verified, but the persistent AIAS ID ↔ AutoCAD handle contract required for a full `DWG_ROUNDTRIP_PASS` has not yet been implemented. No five-drawing escalation was performed.
