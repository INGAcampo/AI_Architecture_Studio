from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class GPUDevice: device_id:str; name:str; backend:str; memory_bytes:int; compute_units:int
@dataclass(frozen=True,slots=True)
class GPURunResult: backend:str; iterations:int; residual:float; converged:bool; elapsed_seconds:float
