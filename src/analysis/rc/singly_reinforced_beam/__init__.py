from math import sqrt
class SinglyReinforcedBeamDesigner:
    def required_steel(self,Mu,b,d,fc,fy,phi=.9):
        rn=Mu/max(phi*b*d*d,1e-12); term=max(0,1-2*rn/(.85*fc))
        return .85*fc/fy*(1-sqrt(term))*b*d
