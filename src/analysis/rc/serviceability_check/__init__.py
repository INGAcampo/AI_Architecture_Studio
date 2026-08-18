class ServiceabilityCheckEngine:
    def check(self,deflection,limit,crack,crack_limit): return deflection<=limit and crack<=crack_limit
