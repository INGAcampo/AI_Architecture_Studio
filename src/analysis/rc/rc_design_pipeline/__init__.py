from analysis.rc.rc_domain import RCBeamResult
from analysis.rc.singly_reinforced_beam import SinglyReinforcedBeamDesigner
from analysis.rc.flexural_strength import FlexuralStrengthEngine
from analysis.rc.shear_strength import ShearStrengthEngine
class RCDesignPipeline:
    def design(self,b):
        As=SinglyReinforcedBeamDesigner().required_steel(b.factored_moment,b.width,b.effective_depth,b.concrete_strength,b.steel_yield_strength)
        Mn=FlexuralStrengthEngine().nominal_moment(As,b.steel_yield_strength,b.width,b.effective_depth,b.concrete_strength)
        Md=FlexuralStrengthEngine().design_moment(Mn)
        Vd=ShearStrengthEngine().design_capacity(ShearStrengthEngine().concrete_capacity(b.concrete_strength,b.width,b.effective_depth),0)
        u=max(b.factored_moment/max(Md,1e-12),b.factored_shear/max(Vd,1e-12))
        return RCBeamResult(As,Mn,Md,Vd,u,"PASS" if u<=1 else "FAIL")
