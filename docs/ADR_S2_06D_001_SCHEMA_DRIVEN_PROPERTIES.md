# ADR S2.06D-001 — Propiedades dirigidas por esquemas

**Decisión:** la interfaz se genera desde `PropertyDescriptor`, no mediante
formularios codificados específicamente para cada objeto.

**Motivo:** Door, Window, Slab y futuros objetos BIM podrán añadir propiedades
sin modificar la paleta.

**Consecuencia:** cada tipo BIM debe registrar un esquema estable y validable.
