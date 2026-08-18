# AIAS 0.5.1 — Sprint S2.03B

## Shared Parameter Library

Este sprint añade la biblioteca corporativa de parámetros compartidos que
conecta el Property Engine con categorías BIM, disciplinas, proyectos e IFC.

### Componentes

- `SharedParameter`
- `ParameterDiscipline`
- `ParameterScope`
- `IfcMapping`
- `ParameterBinding`
- `SharedParameterLibrary`
- `StandardParameterCatalog`

### Capacidades

- identidad persistente mediante GUID;
- versionado de parámetros;
- biblioteca global o de proyecto;
- filtros por disciplina;
- bindings por proyecto, categoría, familia, tipo, instancia o selección;
- integración directa con `PropertyService`;
- persistencia JSON atómica;
- mapeo inicial a IFC Property Sets;
- catálogo estándar multidisciplinario.

### Catálogo inicial

Incluye parámetros de:

- identidad;
- arquitectura;
- estructuras;
- MEP;
- costos.

### Próximo sprint

S2.03C — BIM Property Inspector para consulta, búsqueda, agrupación y edición
visual de propiedades.
