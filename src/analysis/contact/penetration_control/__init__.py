class PenetrationControlEngine:
    def penalty_update(self,k,p,tol): return k*2 if abs(p)>tol else k
