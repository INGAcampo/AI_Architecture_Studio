from math import sqrt
class DevelopmentLengthEngine:
    def tension(self,db,fy,fc,modifier=1): return modifier*.9*fy*db/max(sqrt(fc),1e-12)
