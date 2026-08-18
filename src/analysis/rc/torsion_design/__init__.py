class TorsionDesignEngine:
    def required_transverse_ratio(self,Tu,phi,Ao,fy): return Tu/max(phi*2*Ao*fy,1e-12)
