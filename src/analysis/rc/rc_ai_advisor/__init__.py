from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RCAdvice: summary:str; warnings:tuple
class RCAIAdvisor:
    def advise(self,d): return RCAdvice("La viga de concreto armado cumple." if not d.warnings else "La viga de concreto armado requiere revisión.",d.warnings)
