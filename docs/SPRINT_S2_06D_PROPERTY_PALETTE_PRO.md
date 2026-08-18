# Sprint S2.06D — Property Palette Pro

## Objetivo
Crear un inspector profesional de propiedades BIM, desacoplado de Qt y preparado
para edición individual o múltiple.

## Capacidades
- Esquemas de propiedades por tipo de objeto.
- Grupos y categorías.
- Tipos: texto, entero, decimal, booleano, enum y magnitudes.
- Validación de rango y reglas personalizadas.
- Propiedades de solo lectura.
- Valores mixtos para selección múltiple.
- Edición sobre uno o varios objetos.
- Acción reversible para History Engine.
- Eventos de selección, edición y actualización.
- Widget PySide6 con editores especializados.
- Esquema inicial para `Wall`.

## Integración visual
Registrar el widget con el ID estable `property_palette` en el lado derecho del
Workspace.
