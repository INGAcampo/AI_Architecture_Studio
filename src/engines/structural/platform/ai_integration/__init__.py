from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class StructuralAIDecision:
    member_id:str
    recommended_section_id:str|None
    confidence:float
    reasons:tuple[str,...]

class StructuralAIIntegration:
    def recommend_section(self,member,demand,candidates):
        feasible=[(capacity-demand,section_id) for section_id,capacity in candidates if capacity>=demand]
        if not feasible:
            return StructuralAIDecision(member.member_id,None,0.0,("no_feasible_section",))
        margin,section_id=min(feasible)
        confidence=max(0.0,min(1.0,1.0-margin/max(demand,1e-9)))
        return StructuralAIDecision(member.member_id,section_id,confidence,(f"capacity_margin={margin:.3f}",))
    def batch_recommend(self,requests):
        return tuple(self.recommend_section(member,demand,candidates) for member,demand,candidates in requests)
