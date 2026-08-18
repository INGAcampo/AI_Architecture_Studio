class ModeShapeEngine:
    def normalize(self,shape):
        m=max((abs(v) for v in shape),default=1)
        return tuple(v/max(m,1e-12) for v in shape)
