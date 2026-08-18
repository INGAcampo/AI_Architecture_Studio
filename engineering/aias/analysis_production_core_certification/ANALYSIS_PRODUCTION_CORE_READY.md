# ANALYSIS_PRODUCTION_CORE_READY

The canonical multi-project factory now produces a deterministic structural analysis package from each isolated Project Graph. The analysis materializes load combinations, governing envelopes, support reactions, equilibrium checks, design checks, and SHA-256 lineage for the graph, analysis model, standards evidence, and result.

## Certified boundary

- Certification projects: `ANALYSIS-CORE-CERT-A` and `ANALYSIS-CORE-CERT-B`.
- Data policy: `SYNTHETIC_TEST_DATA=true` and `NOT_FOR_CONSTRUCTION=true`.
- Real projects remain fail-closed without an authenticated provenance baseline.
- The native DWG edge remains an explicit synthetic test double; this gate certifies analysis, not construction issuance.
- Evidence: `ANALYSIS_PRODUCTION_CORE_MANIFEST.json` plus one analysis evidence file per project.

## Materialized value

The same factory call replaces manual load aggregation, load-combination evaluation, equilibrium reconciliation, governing-envelope selection, evidence hashing, and result packaging. The conservative process model falls from six manual touchpoints to two governed touchpoints, an estimated 66.67% reduction.

## Next technical objective

`STANDARDS_PRODUCTION_CORE_READY`: bind jurisdiction applicability and versioned standards clauses to analysis/design decisions, preserving default-deny behavior when authenticated normative evidence is unavailable.
