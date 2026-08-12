# CNS-000001 — AIAS Central Nervous System

The CNS supplies durable circulation between ACE, the Productivity Dashboard, ATO, the Asset Registry, University and PMO. Immutable event envelopes carry stable identity, source, UTC time, correlation, schema version and JSON payload. Events enter an atomic journal before delivery, receive a global sequence and are deduplicated by event identity.

Consumers use monotonic cursors and at-least-once delivery; handlers must therefore be idempotent. Failures enter a dead-letter record without advancing the cursor. The initial company-state projection aggregates completed deliveries, recommendations, risks and issued internal credentials. The trusted core registers handlers in process and never executes handlers supplied by external event payloads.
