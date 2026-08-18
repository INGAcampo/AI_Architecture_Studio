from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AnalysisResult:
    displacements:tuple
    reactions:tuple
    converged:bool
