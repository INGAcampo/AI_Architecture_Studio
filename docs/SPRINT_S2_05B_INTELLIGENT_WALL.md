# Sprint S2.05B — Intelligent Wall Core

## Objetivo

Crear el primer objeto BIM especializado de AIAS sobre `BimObject`.

## Entidades

- `Wall`
- `WallPoint`
- `WallLayer`

## Capacidades

- Eje tridimensional.
- Altura, espesor y elevación base validados.
- Dirección y punto medio.
- Área lateral, huella y volumen bruto.
- Capas constructivas con control de espesor total.
- Materiales derivados de capas.
- Clasificación IFC inicial: `IfcWall`.
- Snapshots inmutables.
- Revisión únicamente ante cambios reales.

## Alcance deliberado

Este sprint implementa el núcleo de dominio. La creación visual, los encuentros,
las aberturas y el renderizado se integrarán en sprints posteriores para evitar
acoplamiento prematuro.
