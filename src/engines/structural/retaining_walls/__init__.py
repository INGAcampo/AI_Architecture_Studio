from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RetainingWallCase:
    case_id: str
    resisting_moment: float
    overturning_moment: float
    resisting_force: float
    driving_force: float

class RetainingWallDesignEngine:
    def overturning_fs(self, case):
        return case.resisting_moment / case.overturning_moment
    def sliding_fs(self, case):
        return case.resisting_force / case.driving_force
