# ADR S2.10-001 — Muros dirigidos por tipos compuestos

**Decisión:** cada muro referencia un `WallType` y no almacena directamente sus capas.

**Motivo:** permitir reutilización, cambio masivo de tipo y consistencia BIM.

**Consecuencia:** las capas viven en `CompoundStructure` y las instancias conservan
solo propiedades de colocación y restricciones.
