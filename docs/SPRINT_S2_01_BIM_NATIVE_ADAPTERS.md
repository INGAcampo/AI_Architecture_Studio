# AIAS 0.5.1 — Sprint S2.01

## Adaptadores BIM nativos

S2.01 conecta la arquitectura BIM creada en S2.00 con diez clases
productivas existentes de AIAS:

- Level
- Grid
- Wall
- Door
- Window
- Room
- Slab
- Beam
- Column
- Foundation

## Capacidades

- Conversión tipada hacia `BimElement`.
- Conservación de identidad cuando el objeto posee ID.
- Parámetros específicos por categoría.
- Unidades y grupos de parámetros.
- Registro extensible de adaptadores.
- Relaciones automáticas:
  - muro hospeda puerta;
  - muro hospeda ventana;
  - room contiene slab.
- Rechazo explícito de tipos desconocidos.

## Principio de integración

Los adaptadores no modifican los modelos originales. La geometría, los
comandos, Undo/Redo y el render siguen perteneciendo a sus motores
actuales. BIM agrega identidad interdisciplinaria, datos y relaciones.

## Uso básico

```python
from engines.bim import (
    BimDocument,
    create_default_bim_adapter_registry,
)

document = BimDocument("Proyecto")
registry = create_default_bim_adapter_registry()
bim_wall = registry.add_to_document(document, wall)
```

## Próximo micro-sprint

S2.02 — Sincronización bidireccional de parámetros y servicio BIM
asociado al proyecto activo.
