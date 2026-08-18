# AIAS 0.5.1 — Sprint S2.02 BIM Service

## Propósito

S2.02 incorpora el servicio central que mantiene el documento BIM activo y
ofrece una API única a CAD, arquitectura, estructuras y futuros motores.

## Componentes

- `BimService`: registro, consulta, actualización y eliminación.
- `BimEventDispatcher`: eventos locales y puente con `kernel.EventBus`.
- `BimParameterManager`: edición centralizada de parámetros.
- `BimRelationshipManager`: relaciones sin duplicados.
- `BimDocumentRepository`: persistencia JSON atómica.
- `ProjectBimManager`: asociación del servicio con el proyecto activo y el
  `ServiceLocator` existente.

## API básica

```python
service.register(wall)
service.find(wall.id)
service.update(wall)
service.set_parameter(wall.id, "FireRating", "120 min")
service.remove(wall.id)
service.save("model.bim.json")
```

## Garantías

- Registrar dos veces el mismo objeto actualiza sin duplicar.
- Las relaciones inferidas no se duplican.
- La eliminación limpia relaciones huérfanas.
- Los cambios emiten eventos BIM.
- La persistencia se escribe de forma atómica.
- No se modifican comandos, renderer ni modelos existentes.

## Próximo sprint

S2.03 — Sincronización bidireccional CAD ↔ BIM mediante eventos del Scene
Manager y acciones de History.
