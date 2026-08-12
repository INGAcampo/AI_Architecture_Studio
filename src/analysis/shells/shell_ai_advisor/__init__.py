from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ShellAdvice: summary:str; warnings:tuple
class ShellAIAdvisor:
    def advise(self,d): return ShellAdvice('El sistema shell/laminado es estable.' if not d.warnings else 'El sistema shell/laminado requiere revisión.',d.warnings)
