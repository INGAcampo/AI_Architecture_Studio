from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BraceBatchResult:
    results: tuple
    passed_count: int
    failed_count: int
    maximum_unity: float

class BraceBatchDesignEngine:
    def __init__(self,design_engine): self.design_engine=design_engine
    def design(self,braces,profiles,materials):
        results=tuple(self.design_engine.design(b,profiles.get(b.profile_id),materials.get(b.material_id)) for b in braces)
        passed=sum(1 for r in results if r.passed)
        max_unity=max((r.unity_ratio for r in results),default=0.0)
        return BraceBatchResult(results,passed,len(results)-passed,max_unity)
