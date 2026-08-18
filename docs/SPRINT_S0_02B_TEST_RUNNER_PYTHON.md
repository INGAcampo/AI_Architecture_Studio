# AIAS 0.5.1 — Sprint S0.02B

## Ejecutor de pruebas multiplataforma

Este micro-sprint elimina la dependencia obligatoria de PowerShell para
ejecutar las pruebas de AIAS.

## Nuevo comando oficial

```powershell
python .\scripts\test.py
```

Para ejecutar únicamente las pruebas de S0.02:

```powershell
python .\scripts\test.py tests/test_s0_02_repository_tools.py
```

Para ejecutar las pruebas del nuevo ejecutor:

```powershell
python .\scripts\test.py tests/test_s0_02b_test_runner.py
```

Para detenerse después del primer fallo:

```powershell
python .\scripts\test.py --fast
```

Para revisar la recopilación sin ejecutar:

```powershell
python .\scripts\test.py --collect-only
```

## Compatibilidad

El ejecutor utiliza Python y funciona en Windows, Linux y macOS. No
requiere modificar la política de ejecución de PowerShell.

## Archivos agregados

- `scripts/test.py`
- `tests/test_s0_02b_test_runner.py`
- `docs/SPRINT_S0_02B_TEST_RUNNER_PYTHON.md`
- `CHANGELOG_S0_02B.md`

## Archivos no modificados

No se reemplaza ningún archivo dentro de `src/`. Tampoco se modifica
`test.ps1`; puede conservarse o eliminarse manualmente, pero deja de ser
necesario.
