from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class NonlinearAdvice: summary:str; warnings:tuple
class NonlinearAIAdvisor:
 def advise(self,d):return NonlinearAdvice('El análisis no lineal es estable.' if not d.warnings else 'El análisis no lineal requiere revisión.',d.warnings)
