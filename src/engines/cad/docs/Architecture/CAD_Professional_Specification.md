# AIAS CAD Professional Specification

## 1. Objetivo

Definir el comportamiento profesional del motor CAD de AI Architecture Studio.

Este documento servirá como referencia para desarrollar herramientas como:

- LINE
- PLINE
- RECTANGLE
- CIRCLE
- ARC
- MOVE
- COPY
- ROTATE
- OFFSET
- TRIM
- EXTEND

---

## 2. Principios generales

Todas las herramientas CAD deberán cumplir:

- Uso mediante Ribbon.
- Uso mediante línea de comandos.
- Soporte para ESC.
- Soporte para ENTER.
- Soporte para clic derecho.
- Previsualización dinámica.
- Integración con SceneManager.
- Integración con ObjectRegistry.
- Integración con EventBus.
- Soporte futuro para Undo/Redo.

---

## 3. LINE

### Flujo

1. Activar comando LINE.
2. Seleccionar primer punto.
3. Mostrar línea temporal.
4. Seleccionar segundo punto.
5. Crear objeto CadLine.
6. Registrar en SceneManager.
7. Registrar en ObjectRegistry.
8. Actualizar Canvas.

### Estado actual

Implementado parcialmente.

Incluye:

- Dos clics.
- Línea temporal.
- ESC.
- Registro como CadLine.
- Registro en ObjectRegistry.

---

## 4. PLINE

### Flujo esperado

1. Activar comando PLINE.
2. Seleccionar punto inicial.
3. Mostrar segmento temporal.
4. Cada clic agrega un nuevo segmento.
5. ENTER finaliza.
6. ESC cancela.
7. Clic derecho finaliza.
8. Puede cerrarse automáticamente.

### Requisitos

- Múltiples segmentos.
- Longitud acumulada.
- Previsualización dinámica.
- Registro como CadPolyline.
- Preparado para convertirse en muro, losa o contorno.

---

## 5. RECTANGLE

### Flujo esperado

1. Activar comando RECTANGLE.
2. Seleccionar primera esquina.
3. Mostrar rectángulo temporal.
4. Seleccionar segunda esquina.
5. Crear objeto CadRectangle.

---

## 6. CIRCLE

### Flujo esperado

1. Activar comando CIRCLE.
2. Seleccionar centro.
3. Mover mouse para radio.
4. Mostrar círculo temporal.
5. Segundo clic confirma.

---

## 7. Navegación CAD

El sistema deberá soportar:

- Zoom con rueda.
- Pan con botón central.
- Coordenadas reales.
- Origen CAD.
- Escala configurable.

---

## 8. OSNAP

Modos previstos:

- Endpoint.
- Midpoint.
- Intersection.
- Center.
- Grid.
- Nearest.
- Perpendicular.
- Tangent.

---

## 9. Selección

Funciones previstas:

- Selección simple.
- Selección múltiple.
- Ventana de selección.
- Resaltado.
- Grip points.

---

## 10. Capas

Funciones previstas:

- Crear capas.
- Asignar color.
- Asignar tipo de línea.
- Bloquear capa.
- Ocultar capa.
- Congelar capa.

---

## 11. Undo / Redo

Cada comando deberá ser reversible.

El CommandManager deberá evolucionar hacia un sistema basado en historial de acciones.

---

## 12. Objetivo CAD v0.6 Alpha

AIAS CAD v0.6 Alpha deberá incluir:

- LINE profesional.
- PLINE básica.
- RECTANGLE básico.
- CIRCLE básico.
- PAN.
- ZOOM.
- ESC.
- Scene Graph.
- Object Registry.