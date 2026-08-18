from design.steel.weld_domain import WeldType,WeldDesignResult
from design.steel.weld_throat import EffectiveThroatEngine
from design.steel.fillet_weld_strength import FilletWeldStrengthEngine
from design.steel.groove_weld import GrooveWeldEngine
class WeldDesignEngine:
    def design(self,s,d,base_strength=450e6):
        g=EffectiveThroatEngine().calculate(s)
        if s.weld_type is WeldType.FILLET: c=FilletWeldStrengthEngine().calculate(s).design_capacity; gov="electrode_shear"
        else: c=GrooveWeldEngine().calculate(s,base_strength).design_capacity; gov="groove_strength"
        q=(d.force_x*d.force_x+d.force_y*d.force_y+d.tension*d.tension)**.5; u=q/max(c,1e-12)
        return WeldDesignResult(s.segment_id,g.effective_throat,g.effective_area,c,q,u,u<=1,gov)
