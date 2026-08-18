class FlexuralStrengthEngine:
    def nominal_moment(self,As,fy,b,d,fc):
        a=As*fy/max(.85*fc*b,1e-12); return As*fy*(d-a/2)
    def design_moment(self,Mn,phi=.9): return phi*Mn
