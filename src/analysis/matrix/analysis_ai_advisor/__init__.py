from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AnalysisAdvice: summary:str; warnings:tuple
class AnalysisAIAdvisor:
    def advise(self,r,d,drift):
        warnings=list(d.warnings)
        if drift>.02:warnings.append("Drift limit exceeded")
        return AnalysisAdvice("El análisis es estable." if not warnings else "El análisis requiere revisión.",tuple(warnings))
