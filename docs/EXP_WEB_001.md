# EXP-WEB-001 — Sitio oficial y registro veraz

## Resultado

AIAS dispone de una experiencia web oficial compilable que presenta la plataforma, sus disciplinas, el Trust Center y AIAS University sin confundir infraestructura de referencia con cumplimiento normativo o autorización profesional.

## Fuente de verdad pública

`sites/aias-official/public/capabilities.json` separa capacidades verificadas, validaciones pendientes y límites legales. El contenido público debe actualizarse desde evidencia versionada antes de cada despliegue.

## Ejecución local

1. Agregar el runtime Node incluido en el entorno AIAS al `PATH`.
2. Ejecutar `pnpm install` dentro de `sites/aias-official`.
3. Ejecutar `pnpm build` para la validación de producción.
4. Ejecutar `pnpm dev` para revisión local en `http://localhost:3000/`.

Los scripts de compilación autorizados están limitados explícitamente en `pnpm-workspace.yaml`; no se habilitan scripts futuros de forma global.

## Límite vigente

La macroentrega está validada localmente. Publicación, dominio, telemetría, cuentas externas y firma pública permanecen pendientes de autorización explícita.
