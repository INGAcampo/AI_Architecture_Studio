# ADR S2.08C-001 — Fórmulas con AST seguro

**Decisión:** no usar `eval`.

**Motivo:** evitar ejecución arbitraria y mantener expresiones auditables.

**Consecuencia:** solo se permiten operadores, nombres y funciones explícitamente
aprobados.
