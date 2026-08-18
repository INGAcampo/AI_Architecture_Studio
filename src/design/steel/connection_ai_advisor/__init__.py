from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConnectionAdvice:
    summary:str; warnings:tuple; recommendations:tuple
class ConnectionAIAdvisor:
    def advise(self,result,optimization=None):
        warnings=()
        if not result.passed:warnings=(f"No cumple: {result.governing_check}.",)
        rec=()
        if optimization and optimization.recommended_option_id:rec=(f"Usar opción {optimization.recommended_option_id}.",)
        return ConnectionAdvice("La conexión cumple." if result.passed else "La conexión requiere revisión.",warnings,rec)
