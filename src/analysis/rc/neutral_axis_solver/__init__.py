class NeutralAxisSolver:
    def solve(self,As,fy,b,fc,beta1=.85):
        a=As*fy/max(.85*fc*b,1e-12); return a/max(beta1,1e-12)
