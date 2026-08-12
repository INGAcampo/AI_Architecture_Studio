# ADR S2.11-001 — Contornos poligonales para losas

**Decisión:** cada losa utiliza un contorno 2D cerrado y huecos poligonales internos.

**Motivo:** representar pisos, fundaciones y decks de forma independiente del renderer.

**Consecuencia:** futuras operaciones booleanas y edición por grips se implementarán
como adaptadores sobre este modelo.
