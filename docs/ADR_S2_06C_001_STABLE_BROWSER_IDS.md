# ADR S2.06C-001 — Identificadores estables del árbol

**Decisión:** cada nodo posee `node_id` estable y los objetos además conservan
`object_id`.

**Motivo:** restaurar expansión y selección aunque el árbol se reconstruya por
cambios BIM.

**Consecuencia:** los adaptadores deben evitar identificadores aleatorios para
niveles, categorías y objetos persistentes.
