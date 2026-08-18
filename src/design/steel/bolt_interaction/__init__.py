from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BoltInteractionResult:
    shear_ratio:float
    tension_ratio:float
    interaction_ratio:float
    passed:bool

class BoltInteractionEngine:
    def calculate(self,shear,shear_capacity,tension,tension_capacity):
        vr=abs(shear)/max(shear_capacity,1e-12)
        tr=abs(tension)/max(tension_capacity,1e-12)
        interaction=vr*vr+tr*tr
        return BoltInteractionResult(vr,tr,interaction,interaction<=1.0)
