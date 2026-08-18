from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class MaterialAdvice:summary:str;warnings:tuple
class MaterialAIAdvisor:
    def advise(self,d):return MaterialAdvice('La respuesta constitutiva es estable.' if not d.warnings else 'La respuesta constitutiva requiere revisión.',d.warnings)
