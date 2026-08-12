from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Advice: summary:str;warnings:tuple
class SolidAIAdvisor:
    def advise(self,d):return Advice("El análisis sólido 3D es estable." if not d.warnings else "El análisis sólido 3D requiere revisión.",d.warnings)
