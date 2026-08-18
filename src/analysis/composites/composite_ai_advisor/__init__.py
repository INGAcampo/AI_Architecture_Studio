from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class CompositeAdvice: summary:str; warnings:tuple
class CompositeAIAdvisor:
    def advise(self,d): return CompositeAdvice('El laminado compuesto es estable.' if not d.warnings else 'El laminado compuesto requiere revisión.',d.warnings)
