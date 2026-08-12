class MomentCurvatureEngine:
    def curvature(self,ecu,c): return ecu/max(c,1e-12)
