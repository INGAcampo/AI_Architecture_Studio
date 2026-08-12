# SCP-04 — Beam and Column Batch Design

Diseño por lotes que consume demandas trazables del análisis global y genera una comprobación para cada viga y columna. Calcula envolventes absolutas de axial, cortante y momento, compara alternativas del mismo tipo y selecciona la capacidad adecuada de menor peso.

La entrega inicial utiliza capacidades `REFERENCE_ONLY`. `PASS_REFERENCE` significa únicamente que las demandas suministradas no superan las capacidades declaradas en ese paquete; no equivale a cumplimiento de ACI, AISC, normativa sísmica ni aprobación para construcción. Los futuros paquetes legítimos sustituirán el catálogo sin cambiar el contrato del edificio.
