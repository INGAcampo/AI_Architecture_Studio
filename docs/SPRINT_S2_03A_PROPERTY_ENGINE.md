# AIAS 0.5.1 — Sprint S2.03A

## Property Engine

S2.03A incorpora un motor transversal de propiedades completamente
independiente de PySide6 y de los modelos gráficos.

### Componentes

- `PropertyType`: tipos primitivos, físicos y BIM.
- `PropertyDefinition`: metadatos, grupo, unidad y reglas.
- `PropertyValue`: valor validado enlazado a su definición.
- `PropertyRegistry`: catálogo central de definiciones.
- `PropertyService`: enlace de propiedades con objetos propietarios.
- `UnitRegistry` y `UnitConverter`: conversiones dimensionales.
- Validadores reutilizables.
- Serialización JSON-compatible.
- Excepciones públicas específicas.

### Principios

1. El valor interno utiliza la unidad declarada por la definición.
2. Las conversiones ocurren en la frontera de entrada.
3. Las definiciones son inmutables.
4. Los valores de solo lectura únicamente cambian mediante operaciones
   internas explícitas.
5. El motor no depende de la interfaz gráfica.
6. Las fórmulas quedan preparadas para un sprint posterior; S2.03A no
   ejecuta expresiones arbitrarias.

### Ejemplo

```python
from engines.property import (
    PropertyDefinition,
    PropertyService,
    PropertyType,
    RangeValidator,
)

service = PropertyService()
service.register_definition(
    PropertyDefinition(
        "Thickness",
        PropertyType.LENGTH,
        unit="m",
        validators=(RangeValidator(minimum=0.01),),
    )
)
service.bind("wall-01", "Thickness", 0.20)
service.set_value("wall-01", "Thickness", 250, input_unit="mm")
```

### Próximo micro-sprint

S2.03B — Shared Parameter Library, catálogos de proyecto y definiciones
reutilizables por disciplina.
