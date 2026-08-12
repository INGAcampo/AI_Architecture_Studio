# Design Specification — S2.06D

La paleta se divide en cinco capas:

1. `PropertyDescriptor` y `PropertyPaletteModel`.
2. `PropertySchemaRegistry`.
3. `PropertySelectionAdapter`.
4. `PropertyPaletteController`.
5. `PropertyPaletteWidget`.

El modelo no depende de Qt ni de una implementación concreta del motor BIM.
