# Sprint S2.06C — Project Browser BIM

## Objetivo
Crear el primer panel profesional del nuevo Workspace: un navegador jerárquico
para niveles, categorías, objetos y materiales BIM.

## Capacidades
- Modelo de árbol independiente de Qt.
- Construcción desde objetos o diccionarios BIM.
- Niveles, categorías, objetos y materiales.
- Selección sincronizada con el Workspace.
- Búsqueda y filtrado.
- Estado de expansión y selección persistente.
- Widget PySide6 con `QTreeWidget`.
- Menú contextual básico.
- Actualización conservando la selección por `object_id`.

## Integración prevista
El panel se registra en `QtDockingController` con el identificador estable
`project_browser`.
