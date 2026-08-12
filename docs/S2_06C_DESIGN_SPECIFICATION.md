# Design Specification — S2.06C

El navegador se divide en cuatro capas:

1. `ProjectBrowserModel`: jerarquía canónica.
2. `ProjectBrowserBuilder`: adaptación desde objetos BIM.
3. `ProjectBrowserController`: selección, filtro y sincronización.
4. `ProjectBrowserWidget`: representación visual PySide6.

La separación permite probar la lógica completa sin crear widgets.
