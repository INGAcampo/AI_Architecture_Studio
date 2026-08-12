# ADR S2.08D-001 — Regeneración transaccional

**Decisión:** toda regeneración se ejecuta dentro de una transacción.

**Motivo:** evitar modelos parcialmente actualizados cuando un elemento falla.

**Consecuencia:** los adaptadores deben registrar operaciones reversibles.
