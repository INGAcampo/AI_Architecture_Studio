# ADR S2.12-001 — Área proyectada y área inclinada

**Decisión:** almacenar el contorno en planta y derivar el área real mediante pendiente.

**Motivo:** mantener una representación geométrica simple y reutilizable.

**Consecuencia:** futuras cubiertas multifaldón podrán sustituir el cálculo global por
cálculos por faldón sin romper la API pública.
