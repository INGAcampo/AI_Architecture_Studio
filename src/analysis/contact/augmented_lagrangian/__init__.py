class AugmentedLagrangianEngine:
    def update_multiplier(self,old,gap,penalty): return max(0.0,old-penalty*gap)
