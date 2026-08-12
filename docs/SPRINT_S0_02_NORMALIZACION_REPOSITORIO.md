# AIAS 0.5.1 — Sprint S0.02

## Normalización reproducible del repositorio

Este micro-sprint completa la estabilización iniciada en S0.01 sin modificar el motor CAD, la GUI, el formato `.aias` ni `src/main.py`.

### Capacidades añadidas

1. Ruta reproducible de imports para Pytest mediante `tests/conftest.py`.
2. Ejecutor oficial de pruebas para Windows: `.\scripts\test.ps1`.
3. Auditor no destructivo: `python .\scripts\aias_import_audit.py`.
4. Inventario técnico: `python .\scripts\aias_repo_inventory.py`.

### Archivos no modificados

- `src/main.py`
- `src/core/app.py`
- `src/gui/main_window.py`
- `src/core/project_manager.py`
- `src/storage/*`
- motores, modelos y comandos existentes

### Prueba de aceptación

```powershell
python .\scripts\aias_health_check.py
python .\scripts\aias_import_audit.py
python .\scripts\aias_repo_inventory.py
.\scripts\test.ps1 -Path tests/test_s0_02_repository_tools.py
```

Resultado esperado: `2 passed` y `RESULTADO: PRUEBAS CORRECTAS`.
