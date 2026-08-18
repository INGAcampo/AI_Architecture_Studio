class PenaltyContactEngine:
    def pressure(self,gap,penalty): return penalty*max(-gap,0.0)
