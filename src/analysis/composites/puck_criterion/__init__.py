class PuckCriterionEngine:
    def fiber_failure(self,sigma1,xt,xc): return abs(sigma1)/max(xt if sigma1>=0 else xc,1e-12)
