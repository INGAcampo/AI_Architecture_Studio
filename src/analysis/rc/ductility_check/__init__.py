class DuctilityCheckEngine:
    def tension_controlled(self,strain,limit=.005): return strain>=limit
