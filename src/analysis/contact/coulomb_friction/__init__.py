class CoulombFrictionEngine:
    def limit(self,p,mu): return abs(p)*max(mu,0)
    def state(self,t,p,mu): return "stick" if abs(t)<=self.limit(p,mu) else "slip"
