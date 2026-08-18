# AIAS 0.5.1 — Auditoría inicial e integración de pruebas

## Hallazgo principal

El código fuente utiliza una estructura `src/`, pero Pytest se ejecutaba desde la raíz sin agregar `src` a `sys.path`. Por eso el test:

```python
from storage.object_graph import ObjectGraphCodec
```

fallaba con:

```text
ModuleNotFoundError: No module named 'storage'
```

El módulo sí existe en `src/storage/object_graph.py`; el problema era únicamente la configuración del entorno de pruebas.

## Corrección

Se agregó a `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

Esto alinea Pytest con la forma en que AIAS ejecuta sus imports desde `src/main.py`.

## Validación realizada

```text
python -m pytest tests/test_project_gui_contract.py tests/test_object_graph.py -q
2 passed
```

## Estado observado del proyecto

- Punto de entrada real: `src/main.py`.
- Gestor de proyectos legado: `src/core/project_manager.py` todavía crea `.aias.json`.
- Sistema nuevo de documentos: `src/storage/`.
- Integración GUI nueva: `src/gui/project_session.py`.
- Menú Archivo ya contiene Nuevo, Abrir, Guardar y Guardar como.
- El proyecto contiene numerosos backups y módulos conceptuales; no deben formar parte del recorrido principal de ejecución sin revisión previa.

## Próxima acción técnica

Consolidar el gestor de proyectos para que exista una sola ruta oficial de creación, apertura y guardado `.aias`, eliminando la convivencia funcional entre `.aias.json` y `.aias`.
