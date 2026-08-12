# ADR S2.06B-001 — Qt como adaptador visual

**Decisión:** mantener PySide6 fuera del núcleo del Workspace.

**Motivo:** conservar pruebas rápidas, separación de responsabilidades y capacidad
de reemplazar o automatizar la interfaz sin modificar la lógica de aplicación.

**Consecuencia:** toda interacción con `QDockWidget` se concentra en
`QtDockingController`.
