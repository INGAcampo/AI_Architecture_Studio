# Sprint S2.03C.1 — Launcher & Import Normalization

## Objetivo

Establecer un arranque oficial y reproducible para AI Architecture Studio sin exigir que el usuario configure `PYTHONPATH` manualmente, y eliminar imports duales o mezclados dentro del código de ejecución.

## Comando oficial

Desde la raíz del repositorio:

```powershell
python .\run.py
```

El lanzador agrega `src` al inicio de `sys.path` y delega la ejecución a `src/main.py`.

## Convención de imports

Mientras el proyecto conserve `src` como raíz lógica en tiempo de ejecución, los módulos internos usarán imports canónicos de nivel superior:

```python
from core.app import AIASApplication
from storage.project_io import ProjectIO
from models.project.project_document import ProjectDocument
```

No se permiten alternativas mixtas mediante `try/except ImportError` ni imports `from src...` dentro de los módulos de producción.

## Cambios

- Nuevo `run.py` en la raíz.
- Normalización de imports en almacenamiento, sesión de proyecto y documento.
- Tres pruebas de regresión para bootstrap, idempotencia y convención de imports.
- `src/main.py` permanece como punto de entrada interno para conservar compatibilidad.

## Criterios de aceptación

1. `python .\run.py` inicia AIAS sin definir `PYTHONPATH`.
2. `python .\src\main.py` continúa funcionando.
3. La suite completa mantiene todas las pruebas anteriores.
4. Las nuevas pruebas del sprint pasan.
