# Sprint S2.03A.1 — Code Integrity

Este micro-sprint corrige una inconsistencia concreta detectada por Pylance:
`main_window.py` importaba dos comandos normativos que no estaban presentes
en el árbol instalado.

## Restaurado

- paquete `commands.core`;
- `StandardsCommand`;
- `StandardsReportCommand`;
- núcleo persistente `core.standards`;
- configuración de normas;
- comprobador estático de imports internos;
- pruebas de recuperación.

## Decisión técnica

No se comentaron ni eliminaron los imports de `main_window.py`, porque la
interfaz ya registra los comandos `STANDARDS` y `STANDARDSREPORT`. Se
restauró la implementación que corresponde a esas referencias.

El comprobador es deliberadamente estático: no ejecuta la GUI ni importa
módulos, por lo que puede detectar rutas internas faltantes sin provocar
efectos secundarios.
