# AIAS Fase 5.1A

1. Cierra AIAS y conserva tu respaldo.
2. Copia `src`, `tests` y `docs` en la raíz del proyecto.
3. Acepta **Combinar carpetas**.

Prueba:
```powershell
python -m pytest tests/test_project_storage.py tests/test_checksum_and_version.py -q
```
Resultado esperado: `4 passed`.

Prueba manual:
```powershell
python -c "from src.models.project import ProjectDocument; p=ProjectDocument.create('Prueba AIAS'); r=p.save('projects/Prueba_AIAS.aias'); q=ProjectDocument.load(r); print(q.metadata.name, r)"
```

Esta entrega no modifica `src/main.py` ni la GUI. La conexión de Nuevo/Abrir/Guardar corresponde a 5.1B.
