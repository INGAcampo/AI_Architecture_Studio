from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DynamicAdvice: summary:str; warnings:tuple
class DynamicAIAdvisor:
    def advise(self,d):
        return DynamicAdvice("El análisis dinámico es estable." if not d.warnings else "El análisis dinámico requiere revisión.",d.warnings)
