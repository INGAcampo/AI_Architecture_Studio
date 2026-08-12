from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ContactAdvice: summary:str; warnings:tuple
class ContactAIAdvisor:
    def advise(self,d): return ContactAdvice("El análisis de contacto no lineal es estable." if not d.warnings else "El análisis de contacto requiere revisión.",d.warnings)
