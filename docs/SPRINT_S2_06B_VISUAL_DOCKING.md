# Sprint S2.06B — Visual Docking Integration

## Objetivo
Conectar el Workspace Framework de S2.06A con PySide6 mediante `QMainWindow`
y `QDockWidget`.

## Capacidades
- Registro de paneles visuales.
- Docking izquierdo, derecho, superior e inferior.
- Paneles flotantes.
- Sincronización bidireccional con `PanelState`.
- Mostrar, ocultar y eliminar paneles.
- Guardar/restaurar el estado Qt.
- Capturar la geometría de la ventana.
- Ejecución de pruebas con `QT_QPA_PLATFORM=offscreen`.

## Límite deliberado
S2.06B proporciona el adaptador visual reusable. Los paneles profesionales
Project Browser y Property Palette serán incorporados en S2.06C y S2.06D.
