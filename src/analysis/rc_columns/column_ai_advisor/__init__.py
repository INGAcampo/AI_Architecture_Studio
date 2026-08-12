from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnAdvice: summary:str; warnings:tuple
class ColumnAIAdvisor:
    def advise(self,d): return ColumnAdvice("La columna de concreto armado cumple." if not d.warnings else "La columna de concreto armado requiere revisión.",d.warnings)
