# Design Specification — S2.08C

Las fórmulas se interpretan mediante un subconjunto seguro de Python AST. Cada
dependencia se registra en un DAG. La evaluación sigue orden topológico y escribe
únicamente parámetros calculados mediante `ParameterEngine`.
