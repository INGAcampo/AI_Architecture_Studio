# AIAS 0.5.1 — Sprint S1.01 Structural Recovery

## Objetivo

Restaurar la importación y compatibilidad geométrica básica del Structural Engine sin alterar el CAD, la GUI ni el formato de proyecto.

## Causas corregidas

1. `src/engines/structural` no tenía `__init__.py`.
2. `src/models/structural` no tenía `__init__.py`.
3. `Beam`, `Column` y `Foundation` no aceptaban la API usada por las pruebas existentes.
4. `tests/test_wall_network.py` dejaba módulos simulados dentro de `sys.modules`, contaminando pruebas recopiladas posteriormente y provocando el mensaje falso: `engines is not a package`.

## Compatibilidad agregada

- `Beam(start_point=..., end_point=...)` calcula la longitud automáticamente.
- `Column(width=..., depth=..., height=...)` calcula el volumen.
- `Foundation(width=..., length=..., thickness=...)` calcula área y volumen.
- Los constructores sin argumentos siguen funcionando.
- Propiedades adicionales pueden recibirse mediante argumentos nombrados y quedan almacenadas en `properties`.

## Archivos reemplazados

- `src/models/structural/beam.py`
- `src/models/structural/column.py`
- `src/models/structural/foundation.py`
- `tests/test_wall_network.py`

## Archivos nuevos

- `src/engines/structural/__init__.py`
- `src/models/structural/__init__.py`
- `tests/test_s1_01_structural_recovery.py`

## Validación realizada

Se ejecutaron 15 pruebas relacionadas con Structural Engine y Wall Network:

```text
15 passed
```

La validación completa debe ejecutarse en el equipo del proyecto, donde PySide6 ya está instalado:

```powershell
python .\scripts\test.py
```
