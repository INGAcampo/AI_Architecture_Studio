from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Partition: partition_id:int; element_ids:tuple; estimated_cost:float
@dataclass(frozen=True,slots=True)
class SolverRun: iterations:int; residual:float; converged:bool; elapsed_seconds:float
