# AIAS Sprint S0.01 - Higiene del repositorio

## Propósito

Esta entrega estabiliza la recolección de pruebas y establece reglas mínimas de higiene sin modificar el motor CAD, la interfaz, los modelos ni el formato `.aias`.

## Cambios

1. `pyproject.toml`
   - Declara `src` como ruta oficial para imports durante Pytest.
   - Limita la recolección a `tests/`.
   - Excluye backups, entornos virtuales, caches, builds y releases.
   - Activa validación estricta de configuración y marcadores.

2. `.gitignore`
   - Excluye caches, logs, entornos, builds y backups locales.
   - Evita que archivos generados contaminen futuros commits.

3. `scripts/clean_workspace.ps1`
   - Elimina solo caches y bytecode generado.
   - No elimina backups, documentos ni código fuente.

4. `scripts/aias_health_check.py`
   - Comprueba la estructura mínima del repositorio.
   - Analiza la sintaxis de los archivos Python fuera de carpetas ignoradas.
   - Es de solo lectura.

## Instalación

Copiar todo el contenido de esta entrega sobre la raíz de `AI_Architecture_Studio` y aceptar reemplazos para `pyproject.toml` y `.gitignore`.

## Verificación

```powershell
python .\scripts\aias_health_check.py
python -m pytest tests/test_project_gui_contract.py tests/test_object_graph.py -q
```

Resultado esperado del segundo comando:

```text
2 passed
```

Luego puede ejecutarse la colección completa:

```powershell
python -m pytest --collect-only -q
```

Pytest debe recolectar únicamente pruebas ubicadas en `tests/`, nunca copias dentro de `backup/` o `backups/`.

## Reversión

Restaurar únicamente los archivos anteriores `pyproject.toml` y `.gitignore`. Los scripts nuevos pueden eliminarse sin afectar AIAS.
