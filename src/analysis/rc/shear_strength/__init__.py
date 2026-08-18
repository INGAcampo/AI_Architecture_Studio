from math import sqrt
class ShearStrengthEngine:
    def concrete_capacity(self,fc,b,d): return .17*sqrt(fc)*b*d
    def design_capacity(self,Vc,Vs,phi=.75): return phi*(Vc+Vs)
