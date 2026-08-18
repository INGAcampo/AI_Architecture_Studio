from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class TransientStep:
    time:float; displacement:float; velocity:float; acceleration:float
@dataclass(frozen=True,slots=True)
class TransientResult:
    steps:tuple; converged:bool; method:str
