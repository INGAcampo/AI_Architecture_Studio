# L3-PRODUCTION-BIM-004AQ

Controlled Update/Delete Rollback Contract

This stage installs a backend-agnostic reversible transaction contract for:
- UPDATE_ENTITY
- DELETE_ENTITY

Key invariants:
- exact pre-state snapshot before every mutation;
- undo token for every successful mutation;
- reverse-order rollback;
- automatic rollback on apply failure;
- deterministic in-memory test backend;
- no AutoCAD COM connection;
- no Save / SaveAs / SendCommand surface in the contract.

004AQ does not execute any live AutoCAD mutation.
