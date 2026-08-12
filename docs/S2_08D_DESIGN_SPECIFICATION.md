# Design Specification — S2.08D

El motor separa invalidación, cola, scheduling, ejecución y transacciones. El scheduler
ordena elementos por dependencias; cada lote se ejecuta dentro de una transacción.
