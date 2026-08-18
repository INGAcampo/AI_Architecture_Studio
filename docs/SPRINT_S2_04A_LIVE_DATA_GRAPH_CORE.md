# Sprint S2.04A — AIAS Live Data Graph Core

## Objetivo

Introducir un núcleo independiente para representar dependencias entre datos CAD,
geométricos, BIM, análisis y renderizado, sin modificar todavía los motores
existentes ni la interfaz.

## Decisiones

- Grafo dirigido: `source -> dependent`.
- Identificadores no sensibles a mayúsculas/minúsculas.
- Propagación determinista en anchura.
- Rechazo preventivo de ciclos.
- Revisiones globales monotónicas.
- Eventos inmutables mediante `GraphChange`.
- Sin dependencia de PySide6.

## Archivos agregados

- `src/engines/live_data_graph/__init__.py`
- `src/engines/live_data_graph/model.py`
- `src/engines/live_data_graph/exceptions.py`
- `src/engines/live_data_graph/graph.py`
- `tests/test_s2_04a_live_data_graph_core.py`

## Alcance excluido

Este sprint no conecta aún `PropertyService`, BIM, Inspector, History ni Renderer.
La integración se realizará en S2.04B mediante un puente explícito y reversible.
