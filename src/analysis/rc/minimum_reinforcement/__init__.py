from math import sqrt
class MinimumReinforcementEngine:
    def area(self,b,d,fc,fy): return max(.25*sqrt(fc)/fy*b*d,1.4/fy*b*d)
