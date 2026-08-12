"""Human-readable project description for the minimum vertical slice."""
def descriptive_report(brief:dict,source_manifest:dict)->str:
 """Render a concise descriptive report from project and foundation evidence."""
 foundation=source_manifest.get("foundation",{});q=source_manifest.get("quantities",{})
 return f'''# Memoria Descriptiva — Proyecto Faro 001

## Objeto

Demostrar una cadena vertical verificable de AIAS para una edificación de referencia, desde el problema técnico hasta cálculo, plano, cantidades y expediente.

## Alcance actual

{', '.join(brief['scope'])}.

## Cimentación de referencia

- Tipo: {foundation.get('type', foundation.get('name','isolated foundation'))}
- Hormigón: {q.get('concrete_m3','ver expediente')} m³
- Acero: {q.get('reinforcement_kg','ver expediente')} kg

## Limitaciones

Este entregable es `REFERENCE_ONLY`. No representa investigación geotécnica específica, aprobación normativa oficial ni autorización para construcción. Requiere revisión y responsabilidad de profesionales habilitados.
'''
