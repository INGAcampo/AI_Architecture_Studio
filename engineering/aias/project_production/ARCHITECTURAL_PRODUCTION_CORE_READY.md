# ARCHITECTURAL_PRODUCTION_CORE_READY

This target extends the certified multi-project production factory. It does not replace it and does not create a parallel authoring model.

The canonical parametric Project Graph now carries:

- isolated sites, four boundary grids, ordered levels, contained spaces and complete wall boundaries;
- exterior envelope walls and roof, hosted doors/windows, access and daylight relationships;
- deterministic SI geometry on every architectural/structural node;
- graph and geometry hashes propagated to the Analysis Model, Drawings and Quantities;
- a fail-closed coherence gate before reports, QA/QC and issuance;
- project-scoped selective-regeneration plans stored beside the immutable intake manifest.

Certification policy:

- evidence uses two distinct `PILOT_SYNTHETIC` projects through the existing `ProjectProductionFactory`;
- every certification artifact is marked `SYNTHETIC_TEST_DATA=true` and `NOT_FOR_CONSTRUCTION=true`;
- `REAL_PROJECT` execution without `authenticated_provenance_sha256` raises `AUTHENTICATED_EXTERNAL_INPUT_REQUIRED` before artifacts are created;
- professional review, jurisdictional validation and construction authorization remain outside this synthetic gate.

The authoritative certification record is `engineering/aias/architectural_core_certification/ARCHITECTURAL_PRODUCTION_CORE_MANIFEST.json`.
