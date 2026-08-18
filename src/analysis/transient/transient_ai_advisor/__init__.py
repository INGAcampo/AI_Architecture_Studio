from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Advice: summary:str; warnings:tuple
class TransientAIAdvisor:
    def advise(self,d): return Advice("El análisis transitorio es estable." if not d.warnings else "El análisis transitorio requiere revisión.",d.warnings)
