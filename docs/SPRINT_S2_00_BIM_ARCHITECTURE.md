# AIAS 0.5.1 — Sprint S2.00

## Arquitectura BIM nativa

### Propósito

S2.00 incorpora una base BIM neutral, serializable y desacoplada de la
interfaz gráfica. No reemplaza los muros, puertas, ventanas, rooms,
losas, niveles o elementos estructurales que ya funcionan.

El nuevo núcleo actúa como una capa común para conectar progresivamente:

- CAD
- Arquitectura
- Estructuras
- Topografía
- Instalaciones
- Cómputos
- IFC
- Inteligencia artificial

### Componentes

- `BimCategory`: taxonomía central de categorías.
- `BimParameterSet`: parámetros con unidad, grupo y modo de solo lectura.
- `BimElement`: representación BIM neutral.
- `BimRelationship`: relaciones explícitas entre elementos.
- `BimDocument`: registro, consulta, relaciones y serialización.
- `BIM_SCHEMA_VERSION`: versión independiente del esquema de datos.

### Estrategia de compatibilidad

Los objetos existentes pueden adaptarse mediante:

```python
document.add_aias_object(wall)
```

Este proceso no modifica el objeto original y permite una migración
gradual. Por tanto, S2.00 no rompe los comandos CAD ni los motores
arquitectónicos existentes.

### Regla arquitectónica

A partir de S2.00:

> Los motores especializados conservan sus modelos operativos, mientras
> el BIM Engine mantiene la identidad, clasificación, parámetros y
> relaciones interdisciplinarias.

### Próximo micro-sprint

S2.01 — Adaptadores oficiales para Level, Grid, Wall, Door, Window,
Room, Slab, Beam, Column y Foundation.
