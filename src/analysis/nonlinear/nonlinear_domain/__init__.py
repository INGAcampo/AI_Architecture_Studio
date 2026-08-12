from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class NonlinearStep: step:int; load_factor:float; displacement:float; residual:float; converged:bool
@dataclass(frozen=True,slots=True)
class NonlinearAnalysisResult: steps:tuple; peak_load_factor:float; target_displacement:float; converged:bool
