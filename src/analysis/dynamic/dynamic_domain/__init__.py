from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ModalMode:
    mode_number:int; eigenvalue:float; frequency_hz:float; period_s:float; shape:tuple
@dataclass(frozen=True,slots=True)
class DynamicAnalysisResult:
    modes:tuple; participation_factors:tuple; effective_mass_ratios:tuple; converged:bool
