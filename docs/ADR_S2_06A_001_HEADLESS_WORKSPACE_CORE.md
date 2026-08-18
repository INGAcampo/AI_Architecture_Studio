# ADR S2.06A-001 — Workspace Core sin dependencia obligatoria de Qt

**Decisión:** modelar el estado y la coordinación del Workspace con Python puro.

**Motivo:** permite pruebas rápidas, evita que la lógica de sesión dependa de widgets y
facilita adaptar posteriormente PySide6, web o automatización.

**Consecuencia:** S2.06B agregará adaptadores visuales; no duplicará el estado.
