from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Advice: summary:str;warnings:tuple
class HPCAIAdvisor:
    def advise(self,d):return Advice("El solver FEM paralelo es estable." if not d.warnings else "El solver FEM paralelo requiere revisión.",d.warnings)
