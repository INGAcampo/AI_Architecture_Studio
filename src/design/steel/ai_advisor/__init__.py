from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SteelAdvice: kind:str;message:str;data:dict
class SteelAIAdvisor:
 def explain_design(self,r): return SteelAdvice('design',f'El elemento {"cumple" if r.passed else "no cumple"}. Controla {r.governing_check}; unity={r.unity_ratio:.3f}.',{'unity':r.unity_ratio})
 def critical_members(self,results,threshold=.9): return tuple(sorted((r for r in results if r.unity_ratio>=threshold),key=lambda x:x.unity_ratio,reverse=True))
