from analysis.materials.material_state import MaterialState
from analysis.materials.j2_yield import J2YieldEngine
class RadialReturnMapping:
    def integrate(self,trial,G,y,old=0):
        eq=J2YieldEngine().equivalent_stress(trial)
        if eq<=y:return MaterialState(tuple(trial),(0.0,)*6,old,0.0,False)
        dg=(eq-y)/max(3*G,1e-12);scale=max(0,1-3*G*dg/max(eq,1e-12))
        return MaterialState(tuple(v*scale for v in trial),(dg,dg,dg,0,0,0),old+dg,0.0,True)
