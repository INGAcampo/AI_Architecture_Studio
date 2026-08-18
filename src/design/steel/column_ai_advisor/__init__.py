from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ColumnAdvice:
    kind:str
    message:str
    data:dict

class SteelColumnAIAdvisor:
    def explain(self,result):
        status="cumple" if result.passed else "no cumple"
        return ColumnAdvice(
            "column_design",
            f"La columna {status}. Controla {result.governing_check}; unity={result.unity_ratio:.3f}; eje crítico={result.critical_axis.value}.",
            {"unity":result.unity_ratio,"governing":result.governing_check,"axis":result.critical_axis.value}
        )
    def critical(self,results,threshold=0.9):
        return tuple(sorted((r for r in results if r.unity_ratio>=threshold),key=lambda r:r.unity_ratio,reverse=True))
