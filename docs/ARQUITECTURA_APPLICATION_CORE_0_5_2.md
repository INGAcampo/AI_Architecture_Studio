# AIAS 0.5.2 — Application Core

Esta versión introduce un núcleo único de aplicación compatible con la arquitectura existente.

## Servicios registrados

- `application_core`
- `event_bus`
- `object_registry`
- `plugin_manager`
- `project_manager`
- `document_manager`
- `settings_manager`
- `scene_manager`
- `history_manager`
- `layer_manager`
- `ortho_manager`
- `snap_engine`
- `dynamic_input_manager`

`AIASApplication` se conserva como alias de compatibilidad, por lo que `src/main.py` no necesita cambios.

## Integración documental

`ProjectSessionController` sincroniza el documento `.aias` activo con `DocumentManager`.

## Eventos de ciclo de vida

- `application.starting`
- `application.started`
- `application.scene_reset`
- `application.stopping`
- `application.stopped`
- `document.changed`
- `document.dirty_changed`
- `document.closed`
