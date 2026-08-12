from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class AnchorInteractionResult:
    tension_ratio:float
    shear_ratio:float
    interaction_ratio:float
    passed:bool

class AnchorInteractionEngine:
    def calculate(self,tension,tcap,shear,vcap):
        tr=tension/max(tcap,1e-12)
        vr=shear/max(vcap,1e-12)
        u=tr*tr+vr*vr
        return AnchorInteractionResult(tr,vr,u,u<=1)
