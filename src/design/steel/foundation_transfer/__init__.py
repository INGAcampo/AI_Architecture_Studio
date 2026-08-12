from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class FoundationTransferResult:
    vertical_load:float
    horizontal_resultant:float
    overturning_moment:float
    transfer_complete:bool

class FoundationTransferEngine:
    def calculate(self,demand,base_plate_result):
        h=(demand.shear_x**2+demand.shear_y**2)**.5
        m=(demand.moment_x**2+demand.moment_y**2)**.5
        return FoundationTransferResult(demand.axial,h,m,base_plate_result.passed)
