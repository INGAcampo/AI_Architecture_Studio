# Sprint S2.04B.1 — Core Event Framework

## Objetivo

Agregar una columna vertebral de comunicación desacoplada para AI Architecture Studio sin reemplazar el `kernel.event_bus` legado todavía.

## Componentes

- `SystemEvent`: evento tipado e inmutable.
- `EventContext`: cancelación, respuestas y errores por publicación.
- `EventPriority`: orden explícito de consumidores.
- `SubscriptionToken`: cancelación segura de suscripciones.
- `EventDispatcher`: publicación determinista, wildcard, `once`, modo estricto y cola FIFO reentrante.

## Compatibilidad

Este sprint es aditivo. El `src/kernel/event_bus.py` existente permanece intacto para evitar regresiones. La migración gradual se realizará en S2.04B.2.

## Criterios de aceptación

- 13 pruebas nuevas.
- Suite completa esperada: 235 pruebas.
- Ningún cambio visual en la aplicación.
