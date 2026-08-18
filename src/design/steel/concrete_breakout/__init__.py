from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class ConcreteBreakoutResult:
    tension_capacity:float
    shear_capacity:float
    tension_ratio:float
    shear_ratio:float
    passed:bool

class ConcreteBreakoutEngine:
    def calculate(self,fc,embedment,edge_distance,tension,shear,phi=.70):
        nt=phi*10*(fc**.5)*(embedment**1.5)*1e3
        vv=phi*8*(fc**.5)*(edge_distance**1.5)*1e3
        tr=tension/max(nt,1e-12)
        vr=shear/max(vv,1e-12)
        return ConcreteBreakoutResult(nt,vv,tr,vr,max(tr,vr)<=1)
