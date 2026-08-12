class ContactConvergenceEngine:
    def check(self,r,p,rt=1e-8,pt=1e-6): return abs(r)<=rt and abs(p)<=pt
